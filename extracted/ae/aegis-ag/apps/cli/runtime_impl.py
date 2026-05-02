"""Core CLI runtime implementation composed from smaller mixin surfaces."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
import os
from pathlib import Path
from typing import Any

from apps.provider_runtime import (
    SurfaceModelProviderCapability,
    capture_runtime_secret_env,
    load_provider_selection,
)
from packages.contracts.runtime import (
    ContextBundle,
    EventEnvelope,
    ExecutionResult,
    ExperienceRecord,
    GoalNode,
    IntentDecision,
    MemoryRecord,
    PlanDraft,
    ProfileGrowthState,
    ProfileState,
    SessionState,
)
from packages.cron import CronRuntime
from packages.evidence import MemoryRuntime
from packages.growth import GrowthUpdate
from packages.kernel import KernelDependencies, KernelOutcome
from packages.runtime_layout import (
    default_authored_skills_dir,
    default_builtin_skills_dir,
    default_cron_dir,
    default_installed_skills_dir,
    default_pairing_dir,
    default_skill_search_cache_dir,
    default_workspace_dir,
    infer_install_root_from_runtime_paths,
)
from packages.security import SecurityPolicy
from packages.session import SessionLineageService, SessionResumeResult
from packages.skills import SkillHub, SkillSearchHub, SkillRuntime, sync_builtin_skill_shelf
from packages.state import PROFILE_MANIFEST_FILENAME, ProfileLoader, ensure_profile_aegis_file, write_profile_manifest
from packages.storage import RuntimeStorageRepository
from packages.tools import BuiltinToolDependencies, InMemorySessionTodoStore, ToolRuntime
from packages.tools.adapters import StructuredClarifySurface
from packages.tools.browser_backend import create_playwright_browser_backend
from packages.tools.surfaces import BrowserToolBackend, ClarifySurface

from .runtime_cognition import (
    _CliContextCapability,
    _DurableMemoryCapability,
    _PreviewDeliveryCapability,
    _PreviewModelProviderCapability,
)
from .runtime_extensions import (
    _PreviewTelemetrySink,
    build_skill_runtime,
    build_tool_runtime,
    load_extension_manifest,
    load_json_file,
    sanitize_extension_manifest_payload,
)
from .runtime_extensions_surface import CliRuntimeExtensionsMixin
from .runtime_profile import CliRuntimeProfileMixin
from .runtime_provider import CliRuntimeProviderMixin
from .runtime_records import CliRuntimeRecordsMixin
from .runtime_snapshot import (
    append_outcome_experience as _append_runtime_outcome_experience,
    append_outcome_growth as _append_runtime_outcome_growth,
    append_outcome_memory as _append_runtime_outcome_memory,
    load_snapshot as _load_runtime_snapshot,
    write_snapshot as _write_runtime_snapshot,
)
from .runtime_support import *  # noqa: F401,F403
from .runtime_support import _seed_clone_text
from .runtime_turns import (
    build_kernel_dependencies as _build_runtime_kernel_dependencies,
    create_clone_session as _create_runtime_clone_session,
    explain_next_step as _explain_runtime_next_step,
    generate_opening_reply as _generate_runtime_opening_reply,
    resume_session as _resume_runtime_session,
    run_turn as _run_runtime_turn,
    start_session as _start_runtime_session,
    wake as _wake_runtime,
)

@dataclass(frozen=True, slots=True)
class CliRuntime(CliRuntimeProfileMixin, CliRuntimeProviderMixin, CliRuntimeExtensionsMixin, CliRuntimeRecordsMixin):
    paths: CliPaths
    repository: RuntimeStorageRepository
    session_service: SessionLineageService
    profile_loader: ProfileLoader
    snapshot_path: Path
    memory_runtime: MemoryRuntime
    cron_runtime: CronRuntime
    model_provider: SurfaceModelProviderCapability
    tool_runtime: ToolRuntime
    skill_runtime: SkillRuntime
    skill_hub: SkillHub
    skill_search_hub: SkillSearchHub
    security_policy: SecurityPolicy
    todo_store: InMemorySessionTodoStore = field(default_factory=InMemorySessionTodoStore)
    browser_backend: BrowserToolBackend | None = None
    clarify_surface: ClarifySurface | None = None
    sub_agent_active: bool = field(default=False, repr=False, compare=False)
    strong_provider_profile_id: str | None = None
    weak_provider_profile_id: str | None = None
    active_provider_id: str | None = None
    growth_updates: dict[str, GrowthUpdate] = field(default_factory=dict, repr=False, compare=False)
    kernel_event_observer: Any = field(default=None, repr=False, compare=False)

    @classmethod
    def create(
        cls,
        *,
        state_dir: Path,
        profile_dir: Path,
    ) -> "CliRuntime":
        home_dir = infer_install_root_from_runtime_paths(state_dir=state_dir, profile_dir=profile_dir)
        skills_dir = home_dir / "skills"
        paths = CliPaths(
            home_dir=home_dir,
            state_dir=state_dir,
            profile_dir=profile_dir,
            skills_dir=skills_dir,
            builtin_skills_dir=default_builtin_skills_dir(install_root=home_dir),
            installed_skills_dir=default_installed_skills_dir(install_root=home_dir),
            authored_skills_dir=default_authored_skills_dir(install_root=home_dir),
            skill_search_cache_dir=default_skill_search_cache_dir(install_root=home_dir),
            cron_dir=default_cron_dir(install_root=home_dir),
            workspace_dir=default_workspace_dir(install_root=home_dir),
            pairing_dir=default_pairing_dir(install_root=home_dir),
        )
        repository = RuntimeStorageRepository(paths.database_path)
        repository.bootstrap()
        sync_builtin_skill_shelf(destination_root=paths.builtin_skills_dir)
        ensure_profile_aegis_file(profile_dir)
        profile_loader = ProfileLoader(profile_dir)
        persisted_selection = load_provider_selection(profile_dir)
        active_provider_profile = persisted_selection.strong_profile
        weak_provider_profile = persisted_selection.weak_profile
        strong_provider_profile_id = None
        weak_provider_profile_id = None
        active_provider_id = None
        intent_mode = persisted_selection.intent_mode
        if active_provider_profile is not None:
            repository.upsert_auth_profile(active_provider_profile)
            strong_provider_profile_id = active_provider_profile.profile_id
            active_provider_id = active_provider_profile.provider_id
            capture_runtime_secret_env(paths.state_dir, active_provider_profile)
        if weak_provider_profile is not None:
            repository.upsert_auth_profile(weak_provider_profile)
            weak_provider_profile_id = weak_provider_profile.profile_id
            capture_runtime_secret_env(paths.state_dir, weak_provider_profile)
        elif active_provider_profile is not None:
            weak_provider_profile_id = active_provider_profile.profile_id
        raw_manifest, removed_legacy_keys = sanitize_extension_manifest_payload(
            load_json_file(profile_dir / PROFILE_MANIFEST_FILENAME)
        )
        if removed_legacy_keys:
            write_profile_manifest(profile_dir, raw_manifest)
        extension_manifest = load_extension_manifest(raw_manifest, profile_dir=profile_dir)
        cron_runtime = CronRuntime(paths.cron_jobs_path, output_dir=paths.cron_output_dir, lock_path=paths.cron_lock_path)
        skill_hub = SkillHub()
        skill_search_hub = SkillSearchHub(cache_root=paths.skill_search_cache_dir)
        security_policy = SecurityPolicy.default()
        todo_store = InMemorySessionTodoStore()
        browser_backend, _browser_reason = create_playwright_browser_backend()
        clarify_surface = StructuredClarifySurface(surface_label="cli")
        def _workspace_root_for_session(session_id: str | None) -> Path:
            if session_id:
                session = repository.load_session(session_id)
                if session is not None and session.workspace_id:
                    workspace = paths.workspace_path_for_clone(session.workspace_id)
                    workspace.mkdir(parents=True, exist_ok=True)
                    return workspace
            return Path.cwd()

        tool_runtime = build_tool_runtime(
            extension_manifest,
            dependencies=BuiltinToolDependencies(
                cwd=Path.cwd(),
                workspace_resolver=_workspace_root_for_session,
                cron_runtime=cron_runtime,
                todo_store=todo_store,
                browser_backend=browser_backend,
                clarify_surface=clarify_surface,
            ),
            snapshot_path=paths.snapshot_path,
            security_policy=security_policy,
        )
        skill_runtime = build_skill_runtime(
            extension_manifest,
            repository=repository,
            profile_loader=profile_loader,
        )
        runtime = cls(
            paths=paths,
            repository=repository,
            session_service=SessionLineageService(repository),
            profile_loader=profile_loader,
            snapshot_path=paths.snapshot_path,
            memory_runtime=MemoryRuntime.from_repository(repository),
            cron_runtime=cron_runtime,
            model_provider=SurfaceModelProviderCapability(
                repository=repository,
                fallback=_PreviewModelProviderCapability(),
                secret_key_path=paths.secret_key_path,
                tool_runtime=tool_runtime,
                capability_id="cli.model.runtime",
                surface_label="cli",
                strong_provider_profile_id=strong_provider_profile_id,
                weak_provider_profile_id=weak_provider_profile_id,
                active_provider_id=active_provider_id,
                intent_mode=intent_mode,
                bootstrap_state_dir=paths.state_dir,
            ),
            tool_runtime=tool_runtime,
            skill_runtime=skill_runtime,
            skill_hub=skill_hub,
            skill_search_hub=skill_search_hub,
            security_policy=security_policy,
            todo_store=todo_store,
            browser_backend=browser_backend,
            clarify_surface=clarify_surface,
            sub_agent_active=os.environ.get("AEGIS_SUB_AGENT_CHILD") == "1",
            strong_provider_profile_id=strong_provider_profile_id,
            weak_provider_profile_id=weak_provider_profile_id,
            active_provider_id=active_provider_id,
        )
        runtime._apply_extension_manifest(extension_manifest)
        return runtime

    def start(
        self,
        *,
        profile_id: str | None = None,
        display_name: str | None = None,
        mode: str | None = None,
        session_id: str | None = None,
        initial_goal: str | None = None,
    ) -> SessionState:
        return _start_runtime_session(
            self,
            profile_id=profile_id,
            display_name=display_name,
            mode=mode,
            session_id=session_id,
            initial_goal=initial_goal,
        )

    def create_clone(
        self,
        *,
        clone_id: str,
        profile_id: str | None = None,
        display_name: str | None = None,
        mode: str | None = None,
        session_id: str | None = None,
        initial_goal: str | None = None,
    ) -> SessionState:
        return _create_runtime_clone_session(
            self,
            clone_id=clone_id,
            profile_id=profile_id,
            display_name=display_name,
            mode=mode,
            session_id=session_id,
            initial_goal=initial_goal,
            seed_clone_text=_seed_clone_text,
        )

    def seed_initial_goal(self, session_id: str, initial_goal: str) -> GoalNode | None:
        normalized = initial_goal.strip()
        if not normalized:
            return None
        existing = self.inspect_goals(session_id)
        if existing:
            return existing[0]
        return self.create_goal(
            session_id,
            title=normalized,
            priority="high",
            owner="shared",
            reason="initial goal seeded during onboarding",
            activate=True,
        )

    def resume(self, session_id: str, *, resumed_session_id: str | None = None) -> SessionResumeResult:
        return _resume_runtime_session(
            self,
            session_id,
            resumed_session_id=resumed_session_id,
        )

    def explain_next_step(
        self,
        *,
        session_id: str,
        prompt: str,
        goal_query: str | None = None,
        tool_name: str | None = None,
        tool_arguments: Mapping[str, Any] | None = None,
        delivery_payload: Mapping[str, Any] | None = None,
        event_payload: Mapping[str, str] | None = None,
    ) -> KernelOutcome:
        return _explain_runtime_next_step(
            self,
            session_id=session_id,
            prompt=prompt,
            goal_query=goal_query,
            tool_name=tool_name,
            tool_arguments=tool_arguments,
            delivery_payload=delivery_payload,
            event_payload=event_payload,
        )

    def compact_session_context(
        self,
        session_id: str,
        *,
        reason: str = "gateway-hygiene",
        force: bool = False,
    ):
        session = self._load_session(session_id)
        capability = _CliContextCapability(
            profile_loader=self.profile_loader,
            repository=self.repository,
            prompt_mode="full",
            snapshot_path=self.snapshot_path,
            total_tokens=self.active_provider_context_window(),
            tool_runtime=self.tool_runtime,
            skill_runtime=self.skill_runtime,
            workspace_dir=self.paths.workspace_dir,
            summary_model_provider=self.model_provider,
        )
        return capability.compact_session_projection(
            session_id=session.session_id,
            reason=reason,
            force=force,
        )

    def generate_opening_reply(
        self,
        *,
        session_id: str,
        prompt: str,
        opening_label: str,
    ) -> KernelOutcome | None:
        return _generate_runtime_opening_reply(
            self,
            session_id=session_id,
            prompt=prompt,
            opening_label=opening_label,
        )

    def _run_turn(
        self,
        *,
        session_id: str,
        prompt: str,
        goal_query: str | None = None,
        tool_name: str | None = None,
        tool_arguments: Mapping[str, Any] | None = None,
        delivery_payload: Mapping[str, Any] | None = None,
        event_type: str = "turn.received",
        source: str = "cli",
        event_payload: Mapping[str, str] | None = None,
        record_input_event: bool = True,
        record_outcome_memory: bool = True,
        capture_experience: bool = True,
        apply_growth: bool = True,
    ) -> KernelOutcome:
        return _run_runtime_turn(
            self,
            session_id=session_id,
            prompt=prompt,
            goal_query=goal_query,
            tool_name=tool_name,
            tool_arguments=tool_arguments,
            delivery_payload=delivery_payload,
            event_type=event_type,
            source=source,
            event_payload=event_payload,
            record_input_event=record_input_event,
            record_outcome_memory=record_outcome_memory,
            capture_experience=capture_experience,
            apply_growth=apply_growth,
        )

    def wake(self, session_id: str, *, inspect_only: bool = False) -> WakeProgressionResult:
        return _wake_runtime(
            self,
            session_id,
            inspect_only=inspect_only,
            result_cls=WakeProgressionResult,
        )

    def _build_kernel_dependencies(self, session: SessionState, profile: ProfileState) -> KernelDependencies:
        return _build_runtime_kernel_dependencies(
            self,
            session,
            profile,
            memory_capability_cls=_DurableMemoryCapability,
            context_capability_cls=_CliContextCapability,
            telemetry_cls=_PreviewTelemetrySink,
            delivery_capability_cls=_PreviewDeliveryCapability,
        )

    def set_kernel_event_observer(self, observer) -> None:
        object.__setattr__(self, "kernel_event_observer", observer)

    def _load_snapshot(self) -> dict[str, Any] | None:
        return _load_runtime_snapshot(self)

    def _append_outcome_memory(self, outcome: KernelOutcome) -> None:
        _append_runtime_outcome_memory(self, outcome)

    def _append_outcome_experience(self, outcome: KernelOutcome) -> ExperienceRecord | None:
        return _append_runtime_outcome_experience(self, outcome)

    def _append_outcome_growth(
        self,
        outcome: KernelOutcome,
        *,
        experience: ExperienceRecord | None,
    ) -> ProfileGrowthState:
        return _append_runtime_outcome_growth(
            self,
            outcome,
            experience=experience,
        )

    def _restore_goal(self, goal: Mapping[str, Any]) -> dict[str, Any]:
        payload = dict(goal)
        for field_name in ("dependencies", "evidence_refs"):
            value = payload.get(field_name)
            if value is not None:
                payload[field_name] = tuple(value)
        return payload

    def _write_snapshot(
        self,
        *,
        profile: ProfileState,
        session: SessionState,
        goals: tuple[GoalNode, ...],
        memories: tuple[MemoryRecord, ...],
        plan: PlanDraft | None,
        execution: ExecutionResult | None,
        delivery: ExecutionResult | None,
        stages: tuple[Any, ...],
        event: EventEnvelope | None,
        clone_text: str | None,
        intent: IntentDecision | None,
        context: ContextBundle | None = None,
    ) -> None:
        _write_runtime_snapshot(
            self,
            profile=profile,
            session=session,
            goals=goals,
            memories=memories,
            plan=plan,
            execution=execution,
            delivery=delivery,
            stages=stages,
            event=event,
            clone_text=clone_text,
            intent=intent,
            context=context,
        )
