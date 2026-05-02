"""Tool, cron, skill, and extension management methods for the CLI runtime."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import replace
from pathlib import Path
import shutil
from typing import Any

from packages.embeddings import embedding_runtime_is_loaded, embedding_runtime_state
from packages.contracts.runtime import ExperienceRecord, ExecutionResult, SessionState
from packages.cron import CronJob, CronJobExecution
from packages.growth import (
    GrowthUpdate,
    ProgressionProjection,
    ProgressionProjectionBuilder,
    ProgressionTransition,
)
from packages.skills import (
    PublicSkillSourceDescriptor,
    SkillDefinition,
    SkillHubEntry,
    SkillManifestLoadRecord,
    SkillPackageLoader,
    SkillSearchEntry,
    build_installed_skill_provenance,
    build_public_skill_source_descriptor,
    install_bucket_for_source_descriptor,
    load_skill_package_definition,
    materialize_skill_package,
    public_skill_source_descriptor_from_metadata,
)
from packages.skills.authoring import write_skill_package
from packages.state import PromptContract, PromptMode, build_prompt_contract, personality_presets, write_profile_manifest
from packages.tools import BuiltinToolDependencies, ToolAudience, ToolDefinition, ToolManifestLoadRecord
from packages.tools.adapters import StructuredClarifySurface

from .runtime_extensions import (
    CliExtensionManifest,
    build_skill_runtime,
    build_tool_runtime,
    load_extension_manifest,
    sanitize_extension_manifest_payload,
    serialize_manifest_path,
)
from .runtime_extensions_skill_sources import (
    install_record_detail as _install_record_detail,
    installed_skill_record as _installed_skill_record,
    matching_install_record as _matching_install_record,
    normalized_install_requester as _normalized_install_requester,
    remote_skill_definition as _remote_skill_definition,
    source_descriptor_for_hub_entry as _source_descriptor_for_hub_entry,
    source_descriptor_for_path as _source_descriptor_for_path,
)
from .runtime_cron_sub_agents import compose_cron_prompt
from .runtime_sub_agents import CliRuntimeSubAgentsMixin
from .runtime_support import _path_is_within, _utc_now

_PROGRESSION_BUILDER = ProgressionProjectionBuilder()


class CliRuntimeExtensionsMixin(CliRuntimeSubAgentsMixin):
    def personality_presets(self):
        return personality_presets()

    def prompt_contract(
        self,
        *,
        profile_id: str | None = None,
        prompt_mode: PromptMode = "full",
    ) -> PromptContract:
        loaded = self._load_profile(profile_id or self.current_profile().state.profile_id)
        return build_prompt_contract(loaded, prompt_mode=prompt_mode)

    def prepare_session_surface(self, session_id: str, *, warm_embeddings: bool = True) -> SessionState:
        session = self._load_session(session_id)
        self._refresh_extensions(profile_id=session.profile_id)
        if warm_embeddings:
            self._warm_embedding_runtime()
        return session

    def _warm_embedding_runtime(self) -> None:
        evidence_retriever = getattr(self.memory_runtime.retriever, "evidence_retriever", None)
        embedding_service = getattr(evidence_retriever, "embedding_service", None)
        warm_async = getattr(embedding_service, "warm_async", None)
        if not callable(warm_async):
            return
        try:
            warm_async()
        except Exception:
            # Surface preparation should stay cheap and non-blocking even when the
            # local embedding runtime is missing or mid-bootstrap.
            return

    def intent_runtime_status(self) -> Mapping[str, object]:
        evidence_retriever = getattr(self.memory_runtime.retriever, "evidence_retriever", None)
        embedding_service = getattr(evidence_retriever, "embedding_service", None)
        if embedding_service is None:
            return {
                "intent_mode": str(self.provider_summary().get("intent_mode") or "skip"),
                "health_status": "missing",
                "runtime_state": "cold",
                "intent_ready": False,
                "summary": "no embedding runtime is attached to the active CLI memory retriever",
            }
        try:
            health = embedding_service.health()
        except Exception as error:
            return {
                "intent_mode": str(self.provider_summary().get("intent_mode") or "skip"),
                "health_status": "failed",
                "runtime_state": "cold",
                "intent_ready": False,
                "summary": str(error).strip() or error.__class__.__name__,
            }
        runtime_state = embedding_runtime_state(health)
        intent_mode = str(self.provider_summary().get("intent_mode") or "skip")
        intent_ready = intent_mode == "embedded" and embedding_runtime_is_loaded(health)
        return {
            "intent_mode": intent_mode,
            "health_status": health.status,
            "runtime_state": runtime_state,
            "intent_ready": intent_ready,
            "summary": health.summary,
        }

    def tool_catalog(self, *, session_id: str | None = None, audience: ToolAudience | None = None) -> tuple[ToolDefinition, ...]:
        if session_id is not None:
            self.prepare_session_surface(session_id, warm_embeddings=False)
        return self.tool_runtime.list_tools(audience=audience)

    def inspect_tool(self, tool_id: str, *, session_id: str | None = None) -> ToolDefinition:
        if session_id is not None:
            self.prepare_session_surface(session_id, warm_embeddings=False)
        tool = self.tool_runtime.describe(tool_id)
        if tool is None:
            raise KeyError(tool_id)
        return tool

    def set_tool_enabled(
        self,
        tool_id: str,
        enabled: bool,
        *,
        session_id: str | None = None,
        profile_id: str | None = None,
    ) -> ToolDefinition:
        resolved_profile_id = self._resolve_extension_profile_id(session_id=session_id, profile_id=profile_id)
        self._refresh_extensions(profile_id=resolved_profile_id)
        updated = self.tool_runtime.set_enabled(tool_id, enabled)
        self._write_extension_override(
            "tool_overrides",
            tool_id,
            enabled,
            profile_id=resolved_profile_id,
        )
        return updated

    def install_tool_manifest(
        self,
        manifest_path: str | Path,
        *,
        session_id: str | None = None,
        profile_id: str | None = None,
    ) -> ToolManifestLoadRecord:
        resolved_profile_id = self._resolve_extension_profile_id(session_id=session_id, profile_id=profile_id)
        target_profile = self._load_profile(resolved_profile_id)
        resolved_path = Path(manifest_path).expanduser().resolve()
        if not resolved_path.exists():
            raise FileNotFoundError(resolved_path)
        profile_dir = Path(target_profile.profile_dir)
        manifest = dict(target_profile.manifest)
        existing_paths = list(load_extension_manifest(manifest, profile_dir=profile_dir).tool_manifest_paths)
        if resolved_path not in existing_paths:
            existing_paths.append(resolved_path)
        manifest["tool_manifests"] = [
            serialize_manifest_path(path, profile_dir=profile_dir)
            for path in existing_paths
        ]
        write_profile_manifest(profile_dir, manifest)
        self._refresh_extensions(profile_id=resolved_profile_id)
        return self._tool_manifest_load_record(resolved_path)

    def run_tool(
        self,
        tool_id: str,
        arguments: Mapping[str, Any],
        *,
        session_id: str,
    ) -> ExecutionResult:
        self.prepare_session_surface(session_id)
        return self.tool_runtime.invoke(tool_id, arguments, session_id=session_id, requester="operator")

    def set_clarify_surface(self, surface: Any) -> None:
        object.__setattr__(self, "clarify_surface", surface)
        self._refresh_extensions(profile_id=self.current_profile().state.profile_id)

    def cron_jobs(self, *, session_id: str) -> tuple[CronJob, ...]:
        profile_id, clone_id = self._cron_scope(session_id)
        return self.cron_runtime.list_jobs(
            profile_id=profile_id,
            clone_id=clone_id,
        )

    def inspect_cron_job(self, job_id: str) -> CronJob:
        return self.cron_runtime.inspect_job(job_id)

    def create_cron_job(
        self,
        *,
        session_id: str,
        name: str,
        schedule: str,
        action_kind: str,
        payload: Mapping[str, Any],
        skills: tuple[str, ...] = (),
    ) -> CronJob:
        self._authorize_write(
            operation="cli.cron.create",
            session_id=session_id,
            description=f"{name} @ {schedule}",
            metadata={"action_kind": action_kind},
        )
        profile_id, clone_id = self._cron_scope(session_id)
        stored_payload = dict(payload)
        if skills:
            stored_payload["skills"] = list(dict.fromkeys(skill.strip() for skill in skills if skill.strip()))
        return self.cron_runtime.create_job(
            name=name,
            schedule_text=schedule,
            action_kind=action_kind,
            payload=stored_payload,
            profile_id=profile_id,
            clone_id=clone_id,
        )

    def pause_cron_job(self, job_id: str) -> CronJob:
        job = self.cron_runtime.inspect_job(job_id)
        scoped_session = self.latest_session_for_clone(job.clone_id or "") if job.clone_id else None
        self._authorize_write(
            operation="cli.cron.pause",
            session_id=scoped_session.session_id if scoped_session is not None else None,
            description=job.name,
            metadata={"job_id": job_id},
        )
        return self.cron_runtime.pause_job(job_id)

    def resume_cron_job(self, job_id: str) -> CronJob:
        job = self.cron_runtime.inspect_job(job_id)
        scoped_session = self.latest_session_for_clone(job.clone_id or "") if job.clone_id else None
        self._authorize_write(
            operation="cli.cron.resume",
            session_id=scoped_session.session_id if scoped_session is not None else None,
            description=job.name,
            metadata={"job_id": job_id},
        )
        return self.cron_runtime.resume_job(job_id)

    def remove_cron_job(self, job_id: str) -> CronJob:
        job = self.cron_runtime.inspect_job(job_id)
        scoped_session = self.latest_session_for_clone(job.clone_id or "") if job.clone_id else None
        self._authorize_write(
            operation="cli.cron.remove",
            session_id=scoped_session.session_id if scoped_session is not None else None,
            description=job.name,
            is_destructive=True,
            metadata={"job_id": job_id},
        )
        return self.cron_runtime.remove_job(job_id)

    def run_due_cron_jobs(self, *, session_id: str) -> tuple[CronJobExecution, ...]:
        session = self._load_session(session_id)
        loaded = self._load_profile(session.profile_id)
        display_name = loaded.state.display_name or self.clone_id_for_session(session)

        def executor(job: CronJob) -> tuple[str, str]:
            return self._execute_cron_job(job, session_id=session_id, display_name=display_name)

        return self.cron_runtime.run_due(
            executor,
            profile_id=loaded.state.profile_id,
            clone_id=self.clone_id_for_session(session),
        )

    def run_due_cron_jobs_for_scheduler(self) -> tuple[CronJobExecution, ...]:
        def executor(job: CronJob) -> tuple[str, str]:
            session = self._cron_session_for_job(job)
            if session is None:
                return ("failed", f"{job.name} skipped because no matching session is available.")
            loaded = self._load_profile(session.profile_id)
            display_name = loaded.state.display_name or self.clone_id_for_session(session)
            return self._execute_cron_job(
                job,
                session_id=session.session_id,
                display_name=display_name,
            )

        return self.cron_runtime.run_due(executor)

    def _execute_cron_job(
        self,
        job: CronJob,
        *,
        session_id: str,
        display_name: str,
    ) -> tuple[str, str]:
        try:
            if job.action_kind == "greeting":
                message = str(job.payload.get("message") or "").strip()
                summary = message or f"{display_name} is checking in and keeping the thread warm."
                return ("success", summary)
            if job.action_kind == "web_search":
                query = str(job.payload.get("query") or "").strip()
                if not query:
                    return ("success", f"{job.name} skipped because no query was stored.")
                result = self.run_tool(
                    "tool.web.search",
                    {"query": query},
                    session_id=session_id,
                )
                return ("success", result.summary)
            if job.action_kind == "prompt":
                prompt = str(job.payload.get("prompt") or "").strip()
                if not prompt:
                    return ("success", f"{job.name} skipped because no prompt was stored.")
                result = self.explain_next_step(
                    session_id=session_id,
                    prompt=compose_cron_prompt(self, job, user_prompt=prompt, session_id=session_id),
                    event_payload={
                        "message": f"cron job: {job.name}",
                        "summary": f"scheduled prompt job: {job.name}",
                        "content": prompt,
                        "intent_mode_override": "skip",
                    },
                )
                return ("success", result.execution.summary)
            return ("success", f"{job.name} is scheduled but uses an unknown action kind: {job.action_kind}")
        except Exception as error:
            return ("failed", f"{job.name} failed: {error}")

    def _cron_session_for_job(self, job: CronJob) -> SessionState | None:
        if job.clone_id:
            return self.latest_session_for_clone(job.clone_id)
        if job.profile_id:
            for session in self._list_sessions():
                if session.profile_id == job.profile_id:
                    return session
            return self.start(profile_id=job.profile_id)
        latest = self.latest_session()
        if latest is not None:
            return latest
        return self.start(profile_id=self.current_profile().state.profile_id)

    def has_due_cron_jobs(self, *, session_id: str) -> bool:
        session = self._load_session(session_id)
        loaded = self._load_profile(session.profile_id)
        return bool(
            self.cron_runtime.due_jobs(
                profile_id=loaded.state.profile_id,
                clone_id=self.clone_id_for_session(session),
            )
        )

    def skill_catalog(self, *, session_id: str | None = None) -> tuple[SkillDefinition, ...]:
        if session_id is not None:
            self.prepare_session_surface(session_id, warm_embeddings=False)
        return self.skill_runtime.catalog.list()

    def list_skill_hub(self, *, limit: int | None = None) -> tuple[SkillHubEntry, ...]:
        entries = self.skill_hub.list(self._current_skill_enabled_overrides())
        if limit is None or limit <= 0:
            return entries
        return entries[:limit]

    def search_skill_hub(self, query: str, *, limit: int = 12) -> tuple[SkillHubEntry, ...]:
        return self.skill_hub.search(query, limit=limit, enabled_overrides=self._current_skill_enabled_overrides())

    def search_skill_sources(
        self,
        query: str,
        *,
        source: str | None = None,
        limit: int = 12,
    ) -> tuple[SkillSearchEntry, ...]:
        return self.skill_search_hub.search(query, source=source, limit=limit)

    def inspect_experiences(
        self,
        *,
        session_id: str | None = None,
        profile_id: str | None = None,
        statuses: tuple[str, ...] = (),
        limit: int | None = None,
    ) -> tuple[ExperienceRecord, ...]:
        return self.repository.list_experiences(
            session_id=session_id,
            profile_id=profile_id,
            statuses=statuses,
            limit=limit,
        )

    def inspect_growth(
        self,
        *,
        session_id: str | None = None,
        profile_id: str | None = None,
    ) -> ProgressionProjection:
        resolved_profile_id = profile_id
        active_goal = None
        continuity_mode = "foreground"
        wake_action = ""
        resolved_session = None
        if resolved_profile_id is None:
            if session_id is None:
                raise ValueError("inspect_growth requires session_id or profile_id")
            resolved_session = self.inspect_session(session_id)
            resolved_profile_id = resolved_session.profile_id
        if session_id is not None:
            continuity = self.inspect_continuity(session_id=session_id)
            resolved_session = resolved_session or self.inspect_session(session_id)
            continuity_mode = "background" if resolved_session.parent_session_id is not None else "foreground"
            wake_action = continuity.wake_action
            graph = self._load_activity_graph_or_none(session_id)
            if graph is not None and graph.active_goal_id is not None:
                active_goal = graph.goal(graph.active_goal_id)
        state = self.repository.load_profile_growth(resolved_profile_id)
        experiences = self.repository.list_experiences(profile_id=resolved_profile_id)
        procedure_library = self.repository.load_procedure_library(resolved_profile_id)
        return _PROGRESSION_BUILDER.build(
            profile_id=resolved_profile_id,
            state=state,
            experiences=experiences,
            procedures=procedure_library.procedures if procedure_library is not None else (),
            active_goal=active_goal,
            continuity_mode=continuity_mode,
            wake_action=wake_action,
        )

    def consume_growth_update(self, *, session_id: str) -> GrowthUpdate | None:
        return self.growth_updates.pop(session_id, None)

    def inspect_growth_transition(self, update: GrowthUpdate, *, session_id: str) -> ProgressionTransition:
        session = self.inspect_session(session_id)
        continuity = self.inspect_continuity(session_id=session_id)
        graph = self._load_activity_graph_or_none(session_id)
        active_goal = graph.goal(graph.active_goal_id) if graph is not None and graph.active_goal_id is not None else None
        experiences = self.repository.list_experiences(profile_id=session.profile_id)
        procedure_library = self.repository.load_procedure_library(session.profile_id)
        return _PROGRESSION_BUILDER.transition(
            update,
            profile_id=session.profile_id,
            experiences=experiences,
            procedures=procedure_library.procedures if procedure_library is not None else (),
            active_goal=active_goal,
            continuity_mode="background" if session.parent_session_id is not None else "foreground",
            wake_action=continuity.wake_action,
        )

    def inspect_skill_hub_entry(self, reference: str) -> SkillHubEntry:
        entry = self.skill_hub.resolve(reference)
        if entry is None:
            raise KeyError(reference)
        return entry

    def inspect_skill(self, skill_id: str, *, session_id: str | None = None) -> SkillDefinition:
        if session_id is not None:
            self.prepare_session_surface(session_id)
        skill = self.skill_runtime.catalog.get(skill_id)
        if skill is None:
            entry = self.skill_hub.resolve(skill_id)
            if entry is not None:
                definition = load_skill_package_definition(Path(entry.entry_path))
                metadata = dict(definition.metadata)
                metadata.update(entry.metadata)
                source_descriptor = _source_descriptor_for_hub_entry(entry)
                if source_descriptor is not None:
                    metadata.update(source_descriptor.to_metadata())
                metadata.update(
                    {
                        "installed": False,
                        "hub_reference": entry.reference,
                    }
                )
                return replace(definition, enabled=False, metadata=metadata)
            raise KeyError(skill_id)
        metadata = dict(skill.metadata)
        metadata.setdefault("installed", True)
        metadata.setdefault("hub_reference", f"aegis-installed:{skill.skill_id}")
        return replace(skill, metadata=metadata)

    def inspect_skill_source(self, skill_id: str, *, session_id: str | None = None) -> SkillDefinition:
        if session_id is not None: self.prepare_session_surface(session_id)
        try:
            return self.inspect_skill(skill_id)
        except KeyError:
            fetched = self.skill_search_hub.fetch(skill_id)
            if fetched is None:
                raise KeyError(skill_id) from None
            return _remote_skill_definition(fetched)

    def set_skill_enabled(
        self,
        skill_id: str,
        enabled: bool,
        *,
        session_id: str | None = None,
        profile_id: str | None = None,
    ) -> SkillDefinition:
        resolved_profile_id = self._resolve_extension_profile_id(session_id=session_id, profile_id=profile_id)
        self._refresh_extensions(profile_id=resolved_profile_id)
        updated = self.skill_runtime.set_enabled(skill_id, enabled)
        self._write_extension_override(
            "skill_overrides",
            skill_id,
            enabled,
            profile_id=resolved_profile_id,
        )
        return updated

    def _current_skill_enabled_overrides(self) -> Mapping[str, bool]:
        loaded = self.current_profile()
        return load_extension_manifest(
            loaded.manifest,
            profile_dir=Path(loaded.profile_dir),
        ).skill_overrides

    def install_skill_manifest(
        self,
        manifest_path: str | Path,
        *,
        session_id: str | None = None,
        profile_id: str | None = None,
    ) -> SkillManifestLoadRecord:
        resolved_profile_id = self._resolve_extension_profile_id(session_id=session_id, profile_id=profile_id)
        target_profile = self._load_profile(resolved_profile_id)
        resolved_path = Path(manifest_path).expanduser().resolve()
        if not resolved_path.exists():
            raise FileNotFoundError(resolved_path)
        profile_dir = Path(target_profile.profile_dir)
        manifest = dict(target_profile.manifest)
        extension_manifest = load_extension_manifest(manifest, profile_dir=profile_dir)
        existing_paths = list(extension_manifest.skill_manifest_paths)
        if resolved_path not in existing_paths:
            existing_paths.append(resolved_path)
        manifest["skill_manifests"] = [
            serialize_manifest_path(path, profile_dir=profile_dir)
            for path in existing_paths
        ]
        write_profile_manifest(profile_dir, manifest)
        self._refresh_extensions(profile_id=resolved_profile_id)
        return self._skill_manifest_load_record(resolved_path)

    def install_skill_source(
        self,
        reference: str | Path,
        *,
        session_id: str | None = None,
        profile_id: str | None = None,
        requester: str | None = "operator",
    ) -> SkillManifestLoadRecord:
        raw = str(reference).strip()
        if not raw:
            raise ValueError("skill install requires a hub id, skill path, or manifest path")
        resolved_requester = _normalized_install_requester(requester)
        self._authorize_write(
            operation="cli.skill.install",
            session_id=session_id,
            description=raw,
            metadata={
                "reference": raw,
                "requester": resolved_requester,
            },
        )
        path_candidate = Path(raw).expanduser()
        if path_candidate.exists():
            resolved_path = path_candidate.resolve()
            if resolved_path.is_dir() or resolved_path.name == "SKILL.md":
                return self._install_skill_package_path(
                    resolved_path,
                    session_id=session_id,
                    profile_id=profile_id,
                    source_bucket="path",
                    source_descriptor=_source_descriptor_for_path(resolved_path),
                    requester=resolved_requester,
                )
            return self.install_skill_manifest(
                resolved_path,
                session_id=session_id,
                profile_id=profile_id,
            )
        entry = self.skill_hub.resolve(raw)
        if entry is not None:
            return self._install_skill_package_path(
                Path(entry.entry_path),
                session_id=session_id,
                profile_id=profile_id,
                source_bucket=entry.source_id,
                source_descriptor=_source_descriptor_for_hub_entry(entry),
                requester=resolved_requester,
            )
        fetched = self.skill_search_hub.fetch(raw)
        if fetched is None:
            raise KeyError(f"skill source was not found: {raw}")
        return self._install_skill_package_path(
            Path(fetched.package_path),
            session_id=session_id,
            profile_id=profile_id,
            source_bucket=fetched.source_id,
            source_descriptor=build_public_skill_source_descriptor(
                source_id=fetched.source_id,
                source_label=fetched.source_label,
                source_reference=fetched.reference,
                install_reference=fetched.install_reference,
                trust_level=fetched.trust_level,
                metadata=fetched.metadata,
            ),
            requester=resolved_requester,
        )

    def create_authored_skill(
        self,
        *,
        skill_id: str,
        display_name: str,
        summary: str,
        instruction_text: str,
        category: str | None = None,
        install: bool = True,
        overwrite: bool = False,
        session_id: str | None = None,
        profile_id: str | None = None,
    ) -> SkillManifestLoadRecord:
        package_path = write_skill_package(
            self.paths.authored_skills_dir,
            skill_id=skill_id,
            display_name=display_name,
            summary=summary,
            instruction_text=instruction_text,
            category=category,
            overwrite=overwrite,
            source_kind="aegis-authored",
        )
        if install:
            return self._install_skill_package_path(
                package_path,
                session_id=session_id,
                profile_id=profile_id,
                source_bucket="authored",
            )
        manifest = SkillPackageLoader().load(package_path)
        return SkillManifestLoadRecord(
            source_path=manifest.source_path,
            skill_ids=tuple(skill.skill_id for skill in manifest.skills),
            loaded_at=_utc_now(),
            status="written",
            detail="shared Aegis authored skill package",
        )

    def update_authored_skill(
        self,
        skill_id: str,
        *,
        display_name: str | None = None,
        summary: str | None = None,
        instruction_text: str | None = None,
        category: str | None = None,
        session_id: str | None = None,
        profile_id: str | None = None,
    ) -> SkillManifestLoadRecord:
        skill = self.inspect_skill(skill_id, session_id=session_id)
        entry_path = Path(skill.entry_path).expanduser().resolve()
        authored_root = self.paths.authored_skills_dir.expanduser().resolve()
        if not _path_is_within(entry_path, authored_root):
            raise ValueError(f"only authored skills can be updated through tool.skill.manage: {skill_id}")
        current = load_skill_package_definition(entry_path)
        resolved_category = category
        if resolved_category is None:
            try:
                relative = entry_path.parent.relative_to(authored_root)
            except ValueError:
                relative = Path()
            parents = relative.parts[:-1]
            resolved_category = parents[0] if parents else None
        return self.create_authored_skill(
            skill_id=current.skill_id,
            display_name=display_name or current.display_name,
            summary=summary or current.summary,
            instruction_text=instruction_text or current.instruction_text,
            category=resolved_category,
            install=True,
            overwrite=True,
            session_id=session_id,
            profile_id=profile_id,
        )

    def delete_skill_source(
        self,
        skill_id: str,
        *,
        session_id: str | None = None,
        profile_id: str | None = None,
    ) -> tuple[str, str]:
        resolved_profile_id = self._resolve_extension_profile_id(session_id=session_id, profile_id=profile_id)
        skill = self.inspect_skill(skill_id, session_id=session_id)
        entry_path = Path(skill.entry_path).expanduser().resolve()
        installed_root = self.paths.installed_skills_dir.expanduser().resolve()
        authored_root = self.paths.authored_skills_dir.expanduser().resolve()
        if not (_path_is_within(entry_path, installed_root) or _path_is_within(entry_path, authored_root)):
            raise ValueError(f"only installed or authored skills can be deleted from this surface: {skill_id}")
        target_profile = self._load_profile(resolved_profile_id)
        profile_dir = Path(target_profile.profile_dir)
        manifest = dict(target_profile.manifest)
        extension_manifest = load_extension_manifest(manifest, profile_dir=profile_dir)
        removed_path = entry_path
        manifest["skill_packages"] = [
            serialize_manifest_path(path, profile_dir=profile_dir)
            for path in extension_manifest.skill_package_paths
            if path.resolve() != removed_path
        ]
        existing_overrides = manifest.get("skill_overrides", {})
        overrides = dict(existing_overrides) if isinstance(existing_overrides, Mapping) else {}
        overrides.pop(skill.skill_id, None)
        if overrides:
            manifest["skill_overrides"] = overrides
        else:
            manifest.pop("skill_overrides", None)
        write_profile_manifest(profile_dir, manifest)
        skill_dir = removed_path.parent
        if skill_dir.exists():
            shutil.rmtree(skill_dir)
        self._refresh_extensions(profile_id=resolved_profile_id)
        return skill.skill_id, str(removed_path)

    def create_experience_skill(
        self,
        *,
        skill_id: str,
        display_name: str,
        summary: str,
        instruction_text: str,
        category: str | None = None,
        install: bool = True,
        overwrite: bool = False,
        session_id: str | None = None,
        profile_id: str | None = None,
    ) -> SkillManifestLoadRecord:
        package_path = write_skill_package(
            self.paths.authored_skills_dir,
            skill_id=skill_id,
            display_name=display_name,
            summary=summary,
            instruction_text=instruction_text,
            category=category or "experience",
            overwrite=overwrite,
        )
        if install:
            return self._install_skill_package_path(
                package_path,
                session_id=session_id,
                profile_id=profile_id,
            )
        manifest = SkillPackageLoader().load(package_path)
        return SkillManifestLoadRecord(
            source_path=manifest.source_path,
            skill_ids=tuple(skill.skill_id for skill in manifest.skills),
            loaded_at=_utc_now(),
            status="written",
            detail="shared Aegis experience skill package",
        )

    def _resolve_extension_profile_id(
        self,
        *,
        session_id: str | None = None,
        profile_id: str | None = None,
    ) -> str:
        if session_id is not None:
            return self._load_session(session_id).profile_id
        if profile_id is not None:
            return profile_id
        return self.current_profile().state.profile_id

    def _install_skill_package_path(
        self,
        package_path: Path,
        *,
        session_id: str | None = None,
        profile_id: str | None = None,
        source_bucket: str | None = None,
        source_descriptor: PublicSkillSourceDescriptor | None = None,
        requester: str | None = "operator",
    ) -> SkillManifestLoadRecord:
        resolved_profile_id = self._resolve_extension_profile_id(session_id=session_id, profile_id=profile_id)
        target_profile = self._load_profile(resolved_profile_id)
        resolved_path = package_path.expanduser().resolve()
        if resolved_path.is_dir():
            resolved_path = resolved_path / "SKILL.md"
        if not resolved_path.exists():
            raise FileNotFoundError(resolved_path)
        installed_root = self.paths.installed_skills_dir
        authored_root = self.paths.authored_skills_dir
        definition = load_skill_package_definition(resolved_path)
        source_descriptor = source_descriptor or public_skill_source_descriptor_from_metadata(definition.metadata)
        if (
            source_descriptor is None
            and not _path_is_within(resolved_path, installed_root)
            and not _path_is_within(resolved_path, authored_root)
        ):
            source_descriptor = _source_descriptor_for_path(resolved_path, source_bucket=source_bucket)
        profile_dir = Path(target_profile.profile_dir)
        manifest = dict(target_profile.manifest)
        extension_manifest = load_extension_manifest(manifest, profile_dir=profile_dir)
        existing_paths = list(extension_manifest.skill_package_paths)
        existing_records = [
            record
            for path in existing_paths
            if (record := _installed_skill_record(path)) is not None and record["skill_id"] == definition.skill_id
        ]
        matching_record = _matching_install_record(
            existing_records,
            source_descriptor=source_descriptor,
            fallback_path=resolved_path,
        )
        install_action = "install"
        previous_install_reference: str | None = None
        if existing_records:
            install_action = "refresh" if matching_record is not None else "migrate"
            if install_action == "migrate":
                previous_install_reference = _record_install_reference(existing_records[0])
        installed_at = _utc_now().isoformat()
        install_provenance = None
        if source_descriptor is not None:
            install_provenance = build_installed_skill_provenance(
                source=source_descriptor,
                install_action=install_action,
                installed_at=installed_at,
                install_requester=_normalized_install_requester(requester),
                previous_install_reference=previous_install_reference,
            )
        if _path_is_within(resolved_path, installed_root) or _path_is_within(resolved_path, authored_root):
            materialized_path = resolved_path
        else:
            materialized_dir = materialize_skill_package(
                installed_root,
                resolved_path,
                source_bucket=(
                    install_bucket_for_source_descriptor(source_descriptor)
                    if source_descriptor is not None
                    else source_bucket or "imported"
                ),
                install_provenance=install_provenance,
            )
            materialized_path = (materialized_dir / "SKILL.md").resolve()
        stale_paths = {
            Path(record["path"]).expanduser().resolve()
            for record in existing_records
            if Path(record["path"]).expanduser().resolve() != materialized_path
        }
        retained_paths: list[Path] = []
        retained_resolved: set[Path] = set()
        for path in existing_paths:
            resolved_existing = path.expanduser().resolve()
            if resolved_existing in stale_paths:
                continue
            if resolved_existing in retained_resolved:
                continue
            retained_paths.append(resolved_existing)
            retained_resolved.add(resolved_existing)
        if materialized_path not in retained_resolved:
            retained_paths.append(materialized_path)
        manifest["skill_packages"] = [
            serialize_manifest_path(path, profile_dir=profile_dir)
            for path in retained_paths
        ]
        write_profile_manifest(profile_dir, manifest)
        for stale_path in stale_paths:
            if not _path_is_within(stale_path, installed_root):
                continue
            stale_dir = stale_path.parent if stale_path.name == "SKILL.md" else stale_path
            if stale_dir.exists():
                shutil.rmtree(stale_dir, ignore_errors=True)
        self._refresh_extensions(profile_id=resolved_profile_id)
        record = self._skill_manifest_load_record(materialized_path)
        record_metadata = dict(record.metadata)
        if install_provenance is not None:
            record_metadata.update(install_provenance.to_metadata())
        return replace(
            record,
            detail=_install_record_detail(
                source_descriptor=source_descriptor,
                install_action=install_action,
                previous_install_reference=previous_install_reference,
            ),
            metadata=record_metadata,
        )

    def _cron_scope(self, session_id: str) -> tuple[str, str]:
        session = self._load_session(session_id)
        return session.profile_id, self.clone_id_for_session(session)

    def _refresh_extensions(self, *, profile_id: str | None = None) -> None:
        if profile_id is None:
            loaded = self.current_profile()
        else:
            loaded = self._load_profile(profile_id)
        manifest_payload, removed_legacy_keys = sanitize_extension_manifest_payload(dict(loaded.manifest))
        if removed_legacy_keys:
            write_profile_manifest(Path(loaded.profile_dir), manifest_payload)
        self._apply_extension_manifest(
            load_extension_manifest(manifest_payload, profile_dir=Path(loaded.profile_dir))
        )

    def _apply_extension_manifest(self, manifest: CliExtensionManifest) -> None:
        def _workspace_root_for_session(session_id: str | None) -> Path:
            session = self.repository.load_session(session_id) if session_id else None
            if session is not None and session.workspace_id:
                workspace = self.paths.workspace_path_for_clone(session.workspace_id)
                workspace.mkdir(parents=True, exist_ok=True)
                return workspace
            return Path.cwd()
        object.__setattr__(
            self,
            "tool_runtime",
            build_tool_runtime(
                manifest,
                dependencies=BuiltinToolDependencies(
                    cwd=Path.cwd(),
                    workspace_resolver=_workspace_root_for_session,
                    cron_runtime=self.cron_runtime,
                    profile_management=self,
                    activity_management=self,
                    memory_management=self,
                    recall_search=self,
                    procedure_management=self,
                    skill_management=self,
                    sub_agents_surface=self,
                    todo_store=self.todo_store,
                    browser_backend=self.browser_backend,
                    clarify_surface=self.clarify_surface or StructuredClarifySurface(surface_label="cli"),
                ),
                snapshot_path=self.snapshot_path,
                security_policy=self.security_policy,
            ),
        )
        self.model_provider.tool_runtime = self.tool_runtime
        object.__setattr__(
            self,
            "skill_runtime",
            build_skill_runtime(
                manifest,
                repository=self.repository,
                profile_loader=self.profile_loader,
            ),
        )

    def _tool_manifest_load_record(self, manifest_path: Path) -> ToolManifestLoadRecord:
        for record in reversed(self.tool_runtime.list_manifest_loads()):
            if Path(record.source_path) == manifest_path:
                return record
        raise LookupError(f"tool manifest was not loaded: {manifest_path}")

    def _skill_manifest_load_record(self, manifest_path: Path) -> SkillManifestLoadRecord:
        for record in reversed(self.skill_runtime.list_manifest_loads()):
            if Path(record.source_path) == manifest_path:
                return record
        raise LookupError(f"skill manifest was not loaded: {manifest_path}")

    def _write_extension_override(
        self,
        section: str,
        item_id: str,
        enabled: bool,
        *,
        profile_id: str | None = None,
    ) -> None:
        loaded = self.current_profile() if profile_id is None else self._load_profile(profile_id)
        profile_dir = Path(loaded.profile_dir)
        manifest = dict(loaded.manifest)
        existing = manifest.get(section, {})
        overrides = dict(existing) if isinstance(existing, Mapping) else {}
        overrides[item_id] = {"enabled": enabled}
        manifest[section] = overrides
        write_profile_manifest(profile_dir, manifest)
