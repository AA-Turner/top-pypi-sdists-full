"""Context assembly, memory retrieval, and preview capabilities for the CLI runtime."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field, replace
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import quote
from uuid import uuid4

from .snapshot_io import load_snapshot_payload
from packages.capabilities.runtime import CapabilityDescriptor
from packages.context import (
    ContextAssemblyResult,
    ContextProjectionCompactionResult,
    ContextRuntime,
    ProviderProjectionSummaryHook,
    SessionProjectionCompactor,
    estimate_projection_tokens,
    projection_result_with_estimated_tokens,
)
from packages.contracts.runtime import (
    ContextBundle,
    EvidenceRetrievalRequest,
    ExecutionResult,
    GoalNode,
    IntentDecision,
    MemoryRecord,
    MixtureModelSelection,
    PlanDraft,
    ProfileState,
    RelationshipMemoryRecord,
    SessionContinuityState,
    SessionState,
    StrongModelProfile,
    WeakModelProfile,
    ActivityGraph,
    PromptEnvelope,
)
from packages.evidence import MemoryRuntime
from packages.operator import library_procedure_overlays
from packages.planning.runtime import PlanningDecision
from packages.skills import (
    SkillCatalogEntry,
    SkillHub,
    SkillRuntime,
    builtin_prompt_skill_catalog_entries,
)
from packages.state import (
    LoadedProfile,
    PromptMode,
    build_prompt_contract,
    load_persisted_canonical_state,
    overlay_canonical_profile_state,
)
from packages.storage import RuntimeStorageRepository
from packages.tools import ToolRuntime, build_tool_fallback_prompt

from .runtime_snapshot import (
    SessionContextEpoch,
    restore_snapshot_session_context_epoch,
    write_snapshot_session_context_epoch,
)
from .runtime_support import _restore_datetime, _utc_now


def _goal_ids_for_memory_search(goal_graph: ActivityGraph | None) -> tuple[str, ...]:
    if goal_graph is None:
        return ()
    goal_ids: list[str] = []
    if goal_graph.active_goal_id is not None:
        goal_ids.append(goal_graph.active_goal_id)
    active_goal = goal_graph.active_goal()
    if active_goal is not None and active_goal.parent_goal_id is not None:
        goal_ids.append(active_goal.parent_goal_id)
    for goal in goal_graph.goals:
        if goal.status in {"active", "blocked", "queued", "proposed"}:
            goal_ids.append(goal.goal_id)
        if len(goal_ids) >= 5:
            break
    return tuple(dict.fromkeys(goal_ids))


def _memory_query_seed(goal_graph: ActivityGraph | None) -> str:
    if goal_graph is None or not goal_graph.goals:
        return "resume continuity next step"
    titles: list[str] = []
    active_goal = goal_graph.active_goal()
    if active_goal is not None:
        titles.append(active_goal.title)
    for goal in goal_graph.goals:
        if goal.goal_id == goal_graph.active_goal_id:
            continue
        if goal.status in {"active", "blocked", "queued", "proposed"}:
            titles.append(goal.title)
        if len(titles) >= 3:
            break
    title_seed = " | ".join(title for title in titles if title)
    if not title_seed:
        return "resume continuity next step"
    return f"resume continuity next step {title_seed}"


def _memory_query_with_relationship(
    goal_graph: ActivityGraph | None,
    *,
    relationship: RelationshipMemoryRecord | None,
) -> str:
    base = _memory_query_seed(goal_graph)
    if relationship is None or not relationship.continuity_notes:
        return base
    note_seed = " | ".join(note for note in relationship.continuity_notes[:2] if note)
    if not note_seed:
        return base
    return f"{base} | relationship continuity {note_seed}"


def _memory_scope_session_ids(
    repository: RuntimeStorageRepository,
    session: SessionState,
) -> tuple[str, ...]:
    lineage = repository.lineage(session.session_id)
    if not lineage:
        return (session.session_id,)
    return tuple(dict.fromkeys(state.session_id for state in lineage))


def _memory_scope_reason(
    *,
    session: SessionState,
    goal_graph: ActivityGraph | None,
    relationship: RelationshipMemoryRecord | None,
    scope_session_ids: tuple[str, ...],
) -> str:
    reasons: list[str] = []
    if len(scope_session_ids) > 1:
        reasons.append("resume recovery spans the current session lineage")
    else:
        reasons.append("no parent lineage was available, so recovery stays in the active session")
    if goal_graph is not None and goal_graph.active_goal_id is not None:
        reasons.append(f"active goal {goal_graph.active_goal_id} stays ahead of generic recall")
    if relationship is not None and relationship.continuity_notes:
        reasons.append("relationship continuity notes add continuity-sensitive recall cues")
    if session.interruption_state:
        reasons.append(f"session interruption state is {session.interruption_state}")
    return "; ".join(reasons)


def _list_scope_memories(
    repository: RuntimeStorageRepository,
    *,
    scope_session_ids: tuple[str, ...],
) -> tuple[MemoryRecord, ...]:
    scope_set = set(scope_session_ids)
    if not scope_set:
        return ()
    records = [
        record
        for record in repository.list_memory_records(session_id=None)
        if record.session_id in scope_set
    ]
    records.sort(
        key=lambda record: (
            record.created_at if record.created_at is not None else datetime.min.replace(tzinfo=timezone.utc),
            record.memory_id,
        )
    )
    return tuple(records)


def _load_snapshot_record(snapshot_path: Path | None) -> dict[str, Any] | None:
    if snapshot_path is None or not snapshot_path.exists():
        return None
    return load_snapshot_payload(snapshot_path)


def _recent_hot_turns(snapshot_path: Path | None, *, session_id: str) -> tuple[str, ...]:
    snapshot = _load_snapshot_record(snapshot_path)
    if not snapshot:
        return ()
    session = snapshot.get("session")
    if not isinstance(session, Mapping) or str(session.get("session_id") or "") != session_id:
        return ()

    turns: list[str] = []
    event = snapshot.get("event")
    include_turn = _snapshot_event_is_user_turn(event)
    if include_turn and isinstance(event, Mapping):
        payload = event.get("payload")
        if isinstance(payload, Mapping):
            message = str(payload.get("message") or payload.get("content") or payload.get("summary") or "").strip()
            if message:
                turns.append(f"user: {message}")

    execution = snapshot.get("execution")
    if include_turn and isinstance(execution, Mapping):
        summary = str(execution.get("summary") or "").strip()
        if summary:
            turns.append(f"aegis: {summary}")

    delivery = snapshot.get("delivery")
    if include_turn and isinstance(delivery, Mapping):
        summary = str(delivery.get("summary") or "").strip()
        if summary:
            turns.append(f"delivery: {summary}")

    return tuple(turns[:4])


def _snapshot_event_is_user_turn(event: object) -> bool:
    if not isinstance(event, Mapping):
        return False
    source = str(event.get("source") or "").strip()
    if source == "cli.startup":
        return False
    event_type = str(event.get("event_type") or "").strip().lower()
    if not event_type:
        return True
    return event_type == "turn.received"


def _render_session_history_block(history_lines: tuple[str, ...], *, compacted_summary: str = "") -> str:
    if not history_lines and not compacted_summary.strip():
        return ""
    sections: list[str] = []
    if compacted_summary.strip():
        sections.append(compacted_summary.strip())
    if history_lines:
        bullet_lines = "\n".join(f"- {line}" for line in history_lines)
        sections.append(
            "## SessionHistoryRecentTail\n"
            "protected recent completed turns from this session; preserve ordering and do not treat earlier summarized requests as active.\n"
            f"{bullet_lines}"
        )
    body = "\n\n".join(sections)
    return (
        "## SessionHistory\n"
        "prompt projection of completed turns from this session; durable records remain the source of truth.\n"
        f"{body}"
    )


@dataclass(frozen=True, slots=True)
class _DurableMemoryCapability:
    memory_runtime: MemoryRuntime
    repository: RuntimeStorageRepository
    descriptor: CapabilityDescriptor = CapabilityDescriptor(
        capability_id="cli.memory.runtime",
        kind="memory",
        version="1.0.0",
        metadata={"description": "Repo-backed memory adapter for CLI kernel flows."},
    )

    def record(self, memory: MemoryRecord) -> None:
        self.memory_runtime.store.upsert(memory)

    def search(
        self,
        session_id: str,
        query: str,
        *,
        goal_ids: tuple[str, ...] = (),
        scope_session_ids: tuple[str, ...] = (),
        scope_reason: str = "",
    ) -> tuple[MemoryRecord, ...]:
        session = self.repository.load_session(session_id)
        goal_graph = self.repository.load_activity_graph(session_id)
        resolved_goal_ids = goal_ids or _goal_ids_for_memory_search(goal_graph)
        resolved_query = query.strip() or _memory_query_seed(goal_graph)
        request = EvidenceRetrievalRequest(
            session_id=session_id,
            profile_id=session.profile_id if session is not None else "profile:unknown",
            workspace_id=session.workspace_id if session is not None else None,
            lineage_session_ids=scope_session_ids or ((session_id,) if session is None else _memory_scope_session_ids(self.repository, session)),
            work_item_ids=resolved_goal_ids,
            query=resolved_query,
            scopes=("session", "lineage", "workspace") if session is not None and session.workspace_id else ("session", "lineage"),
            latency_mode="fast",
            limit=5,
            scope_reason=scope_reason,
        )
        result = self.memory_runtime.retrieve_evidence(request)
        return tuple(candidate.memory for candidate in result.candidates)


@dataclass(frozen=True, slots=True)
class _PreviewMemoryCapability:
    session: SessionState
    snapshot_path: Path
    descriptor: Any = None

    def search(
        self,
        session_id: str,
        query: str,
        *,
        goal_ids: tuple[str, ...] = (),
        scope_session_ids: tuple[str, ...] = (),
        scope_reason: str = "",
    ) -> tuple[MemoryRecord, ...]:
        snapshot = self._load_snapshot()
        if snapshot is not None:
            memories = snapshot.get("memories", ())
            if memories:
                return tuple(MemoryRecord(**self._restore_memory(memory)) for memory in memories)
        now = _utc_now()
        return (
            MemoryRecord(
                memory_id=f"memory:{session_id}:profile",
                session_id=session_id,
                kind="semantic",
                content=f"Profile continuity is bound to {self.session.profile_id}.",
                goal_refs=goal_ids,
                tags=("profile", "continuity"),
                created_at=now,
            ),
            MemoryRecord(
                memory_id=f"memory:{session_id}:query",
                session_id=session_id,
                kind="episodic",
                content=f"Most recent query: {query}",
                source_event_id=None,
                goal_refs=goal_ids,
                tags=("query", "scope-aware") if scope_session_ids or scope_reason else ("query",),
                created_at=now,
            ),
        )

    def _load_snapshot(self) -> dict[str, Any] | None:
        return load_snapshot_payload(self.snapshot_path)

    def _restore_memory(self, memory: Mapping[str, Any]) -> dict[str, Any]:
        payload = dict(memory)
        created_at = payload.get("created_at")
        if created_at is not None:
            payload["created_at"] = _restore_datetime(str(created_at))
        for field_name in ("goal_refs", "tags"):
            value = payload.get(field_name)
            if value is not None:
                payload[field_name] = tuple(value)
        return payload


@dataclass(frozen=True, slots=True)
class _CliContextCapability:
    profile_loader: ProfileLoader
    repository: RuntimeStorageRepository
    prompt_mode: PromptMode = "full"
    snapshot_path: Path | None = None
    total_tokens: int = 4096
    tool_runtime: ToolRuntime | None = None
    skill_runtime: SkillRuntime | None = None
    skill_hub: SkillHub | None = None
    workspace_dir: Path | None = None
    summary_model_provider: Any | None = None
    last_projection_compaction: ContextProjectionCompactionResult | None = field(default=None, init=False, repr=False, compare=False)
    descriptor: CapabilityDescriptor = CapabilityDescriptor(
        capability_id="cli.context.runtime",
        kind="context_assembler",
        version="1.0.0",
        metadata={"description": "CLI context runtime with Aegis identity and durable profile instructions."},
    )

    def _load_profile(self, profile_id: str) -> LoadedProfile:
        loaded = self.profile_loader.load(profile_id=profile_id)
        persisted = load_persisted_canonical_state(self.repository, profile_id)
        return overlay_canonical_profile_state(
            loaded,
            identity_record=persisted.clone_identity,
            user_card=persisted.user_card,
            relationship_record=persisted.relationship_memory,
        )

    def assemble(
        self,
        session: SessionState,
        goals: tuple[GoalNode, ...],
        memories: tuple[MemoryRecord, ...],
        *,
        intent: IntentDecision | None = None,
    ) -> ContextBundle:
        return self.assemble_detailed(session, goals, memories, intent=intent).bundle

    def assemble_detailed(
        self,
        session: SessionState,
        goals: tuple[GoalNode, ...],
        memories: tuple[MemoryRecord, ...],
        *,
        intent: IntentDecision | None = None,
        decision: PlanningDecision | None = None,
        plan: PlanDraft | None = None,
        continuity: SessionContinuityState | None = None,
        bundle_id: str | None = None,
    ) -> ContextAssemblyResult:
        loaded = self._load_profile(session.profile_id)
        return self._assemble_result(
            session=session,
            goals=goals,
            memories=memories,
            loaded=loaded,
            intent=intent,
            artifacts=self._capability_artifacts(
                session,
                loaded,
                goals=goals,
                memories=memories,
                decision=decision,
                plan=plan,
                continuity=continuity,
            ),
            tool_prompt=self._tool_prompt_artifacts(),
            procedure_overlays=self._capability_procedure_overlays(session, loaded),
            bundle_id=bundle_id,
        )

    def augment_for_generation(
        self,
        *,
        session: SessionState,
        goals: tuple[GoalNode, ...],
        memories: tuple[MemoryRecord, ...],
        context: ContextBundle,
        intent: IntentDecision | None,
        decision: PlanningDecision | None,
        plan: PlanDraft | None,
        continuity: SessionContinuityState,
    ) -> ContextBundle:
        return self.assemble_detailed(
            session,
            goals,
            memories,
            intent=intent,
            decision=decision,
            plan=plan,
            continuity=continuity,
            bundle_id=context.bundle_id,
        ).bundle

    def _assemble_result(
        self,
        *,
        session: SessionState,
        goals: tuple[GoalNode, ...],
        memories: tuple[MemoryRecord, ...],
        loaded: LoadedProfile,
        intent: IntentDecision | None,
        artifacts: tuple[str, ...],
        tool_prompt: str,
        procedure_overlays: tuple[str, ...],
        bundle_id: str | None = None,
    ) -> ContextAssemblyResult:
        prompt_contract = build_prompt_contract(loaded, prompt_mode=self.prompt_mode)
        stable_prefix_lines = tuple(prompt_contract.stable_prefix_refs or prompt_contract.instruction_refs)
        capability_prefix_lines = self._capability_stable_prefix_lines(loaded)
        runtime = ContextRuntime(
            instruction_refs=stable_prefix_lines + capability_prefix_lines,
            total_tokens=max(1024, self.total_tokens),
        )
        hot_turns = _recent_hot_turns(self.snapshot_path, session_id=session.session_id)
        assembled = runtime.assemble_detailed(
            session,
            goals,
            memories,
            hot_turns=hot_turns,
            intent=intent,
            profile_snapshot_refs=prompt_contract.profile_snapshot_refs,
            procedure_overlays=procedure_overlays,
            artifacts=artifacts,
        )
        bundle_envelope = assembled.bundle.prompt_envelope
        bundle = replace(
            assembled.bundle,
            bundle_id=bundle_id or f"bundle:{session.session_id}:{len(goals)}:{len(memories)}",
            instruction_refs=prompt_contract.instruction_refs + capability_prefix_lines,
            prompt_envelope=replace(bundle_envelope, tool_schema=""),
        )
        frozen_epoch = restore_snapshot_session_context_epoch(
            _load_snapshot_record(self.snapshot_path),
            session_id=session.session_id,
        )
        object.__setattr__(self, "last_projection_compaction", None)
        if frozen_epoch is not None and frozen_epoch.frozen:
            frozen_epoch, projection_result = self._compact_frozen_epoch_if_needed(frozen_epoch)
            object.__setattr__(self, "last_projection_compaction", projection_result)
            history_block = _render_session_history_block(
                frozen_epoch.history_lines,
                compacted_summary=frozen_epoch.compacted_history_summary,
            )
            frozen_turn_injections = frozen_epoch.base_turn_injections.strip()
            combined_turn_injections = "\n\n".join(
                part for part in (frozen_turn_injections, history_block) if part.strip()
            )
            bundle = replace(
                bundle,
                prompt_envelope=PromptEnvelope(
                    frozen_prefix=frozen_epoch.frozen_prefix,
                    session_snapshot=frozen_epoch.session_snapshot,
                    turn_injections=combined_turn_injections,
                    tool_schema="",
                ),
            )
        return replace(assembled, bundle=bundle)

    def compact_session_projection(
        self,
        *,
        session_id: str | None = None,
        reason: str = "preflight",
        force: bool = False,
    ) -> ContextProjectionCompactionResult | None:
        frozen_epoch = restore_snapshot_session_context_epoch(
            _load_snapshot_record(self.snapshot_path),
            session_id=session_id,
        )
        if frozen_epoch is None or not frozen_epoch.frozen:
            return None
        _updated_epoch, result = self._compact_frozen_epoch_if_needed(frozen_epoch, force=force, reason=reason)
        object.__setattr__(self, "last_projection_compaction", result)
        return result

    def force_projection_compaction(
        self,
        *,
        reason: str = "provider-overflow",
        session_id: str | None = None,
    ) -> ContextProjectionCompactionResult | None:
        return self.compact_session_projection(session_id=session_id, reason=reason, force=True)

    def flush_projection_memory(self) -> None:
        object.__setattr__(self, "last_projection_compaction", None)

    def _compact_frozen_epoch_if_needed(
        self,
        frozen_epoch: SessionContextEpoch,
        *,
        force: bool = False,
        reason: str = "preflight",
    ) -> tuple[SessionContextEpoch, ContextProjectionCompactionResult]:
        total_tokens = max(1024, self.total_tokens)
        before_prompt_tokens = self._estimate_epoch_prompt_tokens(
            frozen_epoch,
            history_lines=frozen_epoch.history_lines,
            compacted_summary=frozen_epoch.compacted_history_summary,
        )
        projection = SessionProjectionCompactor(summary_hook=self._projection_summary_hook(frozen_epoch)).compact(
            history_lines=frozen_epoch.history_lines,
            thread_focus=frozen_epoch.thread_focus,
            previous_summary=frozen_epoch.compacted_history_summary,
            total_tokens=total_tokens,
            reason=reason,
            force=force,
        )
        after_prompt_tokens = self._estimate_epoch_prompt_tokens(
            frozen_epoch,
            history_lines=projection.history_lines,
            compacted_summary=projection.summary,
        )
        result = projection_result_with_estimated_tokens(
            projection.result,
            before_tokens=before_prompt_tokens,
            after_tokens=after_prompt_tokens,
        )
        updated_epoch = replace(
            frozen_epoch,
            compacted_history_summary=projection.summary,
            compaction_count=frozen_epoch.compaction_count + (1 if result.compacted else 0),
            compacted_history_count=frozen_epoch.compacted_history_count + result.compacted_line_count,
            context_projection_tokens=after_prompt_tokens,
            context_projection_limit=total_tokens,
            history_lines=projection.history_lines,
        )
        if updated_epoch != frozen_epoch:
            self._write_compacted_epoch(updated_epoch)
        return updated_epoch, result

    def _estimate_epoch_prompt_tokens(
        self,
        epoch: SessionContextEpoch,
        *,
        history_lines: tuple[str, ...],
        compacted_summary: str,
    ) -> int:
        return estimate_projection_tokens(
            "\n\n".join(
                part
                for part in (
                    epoch.frozen_prefix,
                    epoch.session_snapshot,
                    epoch.base_turn_injections,
                    _render_session_history_block(history_lines, compacted_summary=compacted_summary),
                    epoch.tool_schema,
                )
                if part.strip()
            )
        )

    def _write_compacted_epoch(self, epoch: SessionContextEpoch) -> None:
        if self.snapshot_path is None:
            return
        runtime_proxy = type("_SnapshotRuntimeProxy", (), {"snapshot_path": self.snapshot_path})()
        write_snapshot_session_context_epoch(runtime_proxy, epoch)

    def _projection_summary_hook(self, frozen_epoch: SessionContextEpoch):
        if self.summary_model_provider is None:
            return None
        try:
            session = self.repository.load_session(frozen_epoch.session_id)
            if session is None:
                return None
            profile = self._load_profile(session.profile_id).state
        except Exception:
            return None
        return ProviderProjectionSummaryHook(
            provider=self.summary_model_provider,
            profile=profile,
            session=session,
        )

    def _capability_stable_prefix_lines(self, loaded: LoadedProfile) -> tuple[str, ...]:
        skill_overrides = _skill_prompt_index_overrides(loaded.manifest)
        builtin_entries = self._builtin_skill_packages(limit=10_000, enabled_overrides=skill_overrides)
        if not builtin_entries:
            return ()
        categories: dict[str, list[SkillCatalogEntry]] = {}
        for entry in builtin_entries:
            category = str(entry.metadata.get("category") or "general").strip() or "general"
            categories.setdefault(category, []).append(entry)
        lines = [
            "### Capability Disclosure",
            "Skill index is discovery-only: entries expose names and ids only, not full procedures.",
            (
                "For execution, coding, research, setup, review, or workflow tasks, scan the index; "
                "if a listed skill is relevant, call `tool.skill.view` with its `skill_id` before relying on the procedure."
            ),
            "Do not load skills for casual conversation or simple continuity replies unless the request needs a procedure.",
            "After viewing a skill, treat the returned full skill body as the procedural source of truth.",
            f"Skill index ({len(builtin_entries)} built-in entries):",
        ]
        for category in sorted(categories):
            entries = sorted(categories[category], key=lambda item: (item.display_name.casefold(), item.skill_id))
            listing = ", ".join(f"{entry.display_name} ({entry.skill_id})" for entry in entries)
            lines.append(f"- {category} - {listing}")
        return tuple(lines)

    def _capability_procedure_overlays(self, session: SessionState, loaded: LoadedProfile) -> tuple[str, ...]:
        overlays: list[str] = []
        goal_graph = self.repository.load_activity_graph(session.session_id)
        library = self.repository.load_procedure_library(loaded.state.profile_id)
        overlays.extend(
            library_procedure_overlays(
                goals=goal_graph.goals if goal_graph is not None else (),
                procedures=library.procedures if library is not None else (),
            )
        )
        return tuple(overlays)

    def _capability_artifacts(
        self,
        session: SessionState,
        loaded: LoadedProfile,
        *,
        goals: tuple[GoalNode, ...] = (),
        memories: tuple[MemoryRecord, ...] = (),
        decision: PlanningDecision | None = None,
        plan: PlanDraft | None = None,
        continuity: SessionContinuityState | None = None,
    ) -> tuple[str, ...]:
        artifacts = list(
            self._generation_artifacts(
                goals=goals,
                memories=memories,
                decision=decision,
                plan=plan,
                continuity=continuity,
            )
        )
        workspace = self._default_workspace_attachment(session)
        if workspace:
            artifacts.append(workspace)
        active_run = self.repository.load_latest_open_agent_run(session.session_id)
        if active_run is not None:
            artifacts.append(
                "active-agent-run: there is unfinished long-horizon work in flight; "
                f"run={active_run.run_id}; status={active_run.status}; "
                f"objective={_compact_runtime_text(active_run.prompt, limit=180)}; "
                f"checkpoint={_compact_runtime_text(active_run.last_summary or active_run.waiting_reason or '<empty>', limit=220)}"
            )
            recent_steps = self.repository.list_agent_run_steps(active_run.run_id, limit=4)
            if recent_steps:
                step_lines = "; ".join(
                    f"{step.kind} {step.title}: {_compact_runtime_text(step.content, limit=120)}"
                    for step in recent_steps
                )
                artifacts.append(f"active-agent-run-steps: {step_lines}")
        return tuple(artifacts)

    def _default_workspace_attachment(self, session: SessionState) -> str | None:
        if self.workspace_dir is None:
            return None
        root = self.workspace_dir.expanduser()
        workspace_id = str(session.workspace_id or "").strip()
        current = root / quote(workspace_id, safe="") if workspace_id else root
        return (
            "default-workspace: "
            f"root={root}; current={current}; "
            "when the user asks to write a file, clone a repository, download an asset, or create generated artifacts without an explicit path, use the current workspace path."
        )

    def _builtin_skill_packages(
        self,
        *,
        limit: int | None = 8,
        enabled_overrides: Mapping[str, bool] | None = None,
    ) -> tuple[SkillCatalogEntry, ...]:
        return builtin_prompt_skill_catalog_entries(enabled_overrides, limit=limit)

    def _generation_artifacts(
        self,
        *,
        goals: tuple[GoalNode, ...],
        memories: tuple[MemoryRecord, ...],
        decision: PlanningDecision | None,
        plan: PlanDraft | None,
        continuity: SessionContinuityState | None,
    ) -> tuple[str, ...]:
        active_goal = _goal_for_generation(goals, decision)
        artifacts = [
            artifact
            for artifact in (
                _decision_artifact(decision),
                _active_goal_artifact(active_goal, continuity=continuity),
                _memory_summary_artifact(memories),
            )
            if artifact.strip()
        ]
        if plan is not None and plan.steps:
            step = plan.steps[0]
            artifacts.append(
                "runtime-plan-step: "
                f"{step.title}; rationale={_compact_runtime_text(step.rationale, limit=160)}"
                )
        return tuple(artifacts)

    def _tool_prompt_artifacts(self) -> str:
        if self.tool_runtime is None:
            return ""
        enabled_tools = self.tool_runtime.list_tools(
            audience="model",
            enabled_only=True,
            available_only=True,
        )
        return build_tool_fallback_prompt(enabled_tools)


def _goal_for_generation(
    goals: tuple[GoalNode, ...],
    decision: PlanningDecision | None,
) -> GoalNode | None:
    preferred_goal_ids = (
        decision.rationale.planned_active_goal_id if decision is not None else None,
        decision.selected_move.goal_id if decision is not None else None,
    )
    for goal_id in preferred_goal_ids:
        if not goal_id:
            continue
        for goal in goals:
            if goal.goal_id == goal_id:
                return goal
    for goal in goals:
        if goal.status == "active":
            return goal
    return goals[0] if goals else None


def _decision_artifact(decision: PlanningDecision | None) -> str:
    if decision is None:
        return ""
    return (
        "runtime-planning-decision: "
        f"kind={decision.selected_move.kind}; "
        f"goal={decision.selected_move.goal_id or '<none>'}; "
        f"planned-active-goal={decision.rationale.planned_active_goal_id or '<none>'}; "
        f"rationale={_compact_runtime_text(decision.rationale.summary, limit=180)}"
    )


def _active_goal_artifact(
    goal: GoalNode | None,
    *,
    continuity: SessionContinuityState | None,
) -> str:
    continuity_hint = ""
    if continuity is not None and continuity.requires_recovery:
        continuity_hint = f"; continuity={_compact_runtime_text(continuity.summary, limit=120)}"
    if goal is None:
        if continuity_hint:
            return f"runtime-continuity:{continuity_hint.removeprefix(';')}"
        return ""
    return (
        "runtime-active-goal: "
        f"{goal.goal_id} -> {goal.title} [{goal.status}/{goal.priority}]"
        f"{continuity_hint}"
    )


def _memory_summary_artifact(memories: tuple[MemoryRecord, ...], *, limit: int = 3) -> str:
    if not memories:
        return ""
    preview = memories[:limit]
    entries = "; ".join(
        (
            f"{memory.memory_id}[{memory.kind}; "
            f"goals={','.join(memory.goal_refs) or 'none'}; "
            f"tags={','.join(memory.tags) or 'none'}]"
        )
        for memory in preview
    )
    remainder = len(memories) - len(preview)
    suffix = f"; +{remainder} more" if remainder > 0 else ""
    return f"recovered-memory-summary: {len(memories)} retrieved for this turn; {entries}{suffix}"


def _compact_runtime_text(value: str, *, limit: int) -> str:
    compact = " ".join(value.split())
    if len(compact) <= limit:
        return compact
    return compact[: max(0, limit - 1)].rstrip() + "…"


def _skill_prompt_index_overrides(manifest: Mapping[str, object]) -> dict[str, bool]:
    raw = manifest.get("skill_overrides", {})
    if not isinstance(raw, Mapping):
        return {}
    overrides: dict[str, bool] = {}
    for skill_id, record in raw.items():
        if isinstance(record, Mapping) and "enabled" in record:
            overrides[str(skill_id)] = bool(record["enabled"])
    return overrides


@dataclass(frozen=True, slots=True)
class _PreviewModelProviderCapability:
    descriptor: Any = None

    def selection_state(self) -> MixtureModelSelection:
        return MixtureModelSelection(
            strong_model=StrongModelProfile(
                profile_id="preview:strong",
                provider_id="preview",
                model_id="preview-strong",
            ),
            weak_model=WeakModelProfile(
                profile_id="preview:weak",
                provider_id="preview",
                model_id="preview-weak",
            ),
            intent_mode="skip",
        )

    def generate(
        self,
        *,
        profile: ProfileState,
        session: SessionState,
        context: ContextBundle,
        prompt: str,
        model_role: str = "strong",
    ) -> ExecutionResult:
        summary = (
            f"Next step for {profile.display_name} in {session.session_id}: "
            f"continue from {len(context.goal_ids)} goal(s) and {len(context.memory_ids)} memory item(s) "
            f"with the {model_role} model path."
        )
        return ExecutionResult(
            execution_id=f"exec:{session.session_id}:{uuid4().hex[:8]}",
            session_id=session.session_id,
            outcome="ok",
            summary=summary,
            prompt_tokens=len(prompt.split()),
            completion_tokens=len(summary.split()),
            total_tokens=len(prompt.split()) + len(summary.split()),
            side_effects=(f"model_role={model_role}",),
        )

class _PreviewToolCapability:
    descriptor: Any = None

    def invoke(
        self,
        tool_name: str,
        arguments: Mapping[str, Any],
        *,
        session_id: str,
    ) -> ExecutionResult:
        summary = f"invoked {tool_name} with {dict(arguments)}"
        return ExecutionResult(
            execution_id=f"tool:{session_id}:{tool_name}",
            session_id=session_id,
            outcome="ok",
            summary=summary,
            side_effects=(tool_name,),
        )


@dataclass(frozen=True, slots=True)
class _PreviewDeliveryCapability:
    descriptor: Any = None

    def deliver(
        self,
        session_id: str,
        payload: Mapping[str, Any],
    ) -> ExecutionResult:
        return ExecutionResult(
            execution_id=f"delivery:{session_id}:{uuid4().hex[:8]}",
            session_id=session_id,
            outcome="ok",
            summary=f"delivered {payload.get('event_id', 'event')}",
        )
