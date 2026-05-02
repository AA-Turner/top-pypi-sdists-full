"""Programmatic API runtime implementation assembled from smaller method modules."""


from __future__ import annotations

from dataclasses import asdict, dataclass, is_dataclass, replace
from datetime import UTC, datetime
from pathlib import Path
import json
from typing import Any, Mapping
from uuid import uuid4

from apps.provider_runtime import (
    SurfaceModelProviderCapability,
    load_provider_selection,
    provider_profile_from_payload,
)
from packages.auth import AuthProfile, PersistentAuthProfileStore
from packages.context import ContextRuntime
from packages.cron import CronRuntime
from packages.contracts import ContextBundle, EventEnvelope, ExecutionResult, GoalNode, MemoryRecord, ProfileState, SessionState, ActivityGraph
from packages.kernel import KernelDependencies, KernelOutcome, KernelService, KernelTurnRequest, ObservationPipeline, StateReconciler
from packages.learning import LearningRuntime
from packages.evidence import MemoryRuntime
from packages.operator import (
    MemoryOperatorDetail,
    MemorySearchHit,
    ProcedureOperatorDetail,
    build_audit_surface,
    build_memory_operator_surface,
    build_procedure_operator_surface,
    build_profile_operator_surface,
    build_activity_operator_surface,
    library_procedure_overlays,
)
from packages.planning import PlanningService
from packages.session import SessionLineageService, SessionResumeResult
from packages.storage import RuntimeStorageRepository
from packages.tools import BuiltinToolDependencies, build_tool_runtime
from packages.tools.adapters import DeliveryMessageSurfaceAdapter, StructuredClarifySurface
from packages.tools.browser_backend import create_playwright_browser_backend

from .capabilities import (
    APIContextCapability,
    APIDeliveryCapability,
    APIMemoryCapability,
    APIModelProvider,
    APIPlanningCapability,
    APITelemetrySink,
    APIToolExecution,
)
from .state_runtime import APIContinuityInspection, APIStateService
from .tool_surfaces import APIMemoryManagementSurface, APIRecallSearchSurface

from .api_runtime_support import (
    APIAppConfig,
    APIResponse,
    APISessionCreationResult,
    APISessionInspection,
    APISessionLifecycleResult,
    APIResumeResult,
    APITurnRecord,
    APITurnResult,
)
from . import api_runtime_provider_methods as _provider_methods
from . import api_runtime_surface_methods as _surface_methods
from . import api_runtime_goal_methods as _goal_methods
from . import api_runtime_http_methods as _http_methods
from . import api_runtime_console as _console_methods


def _profile_dir_for_database(database_path: Path) -> Path:
    state_dir = database_path.parent
    if state_dir.name == "state":
        return state_dir.parent / "profile"
    return state_dir / "profile"


def _enabled_overrides(profile_dir: Path, section: str) -> dict[str, bool]:
    try:
        manifest = json.loads((profile_dir / "profile.json").read_text(encoding="utf-8"))
    except (OSError, ValueError, json.JSONDecodeError):
        return {}
    payload = manifest.get(section) if isinstance(manifest, Mapping) else None
    if not isinstance(payload, Mapping):
        return {}
    overrides: dict[str, bool] = {}
    for item_id, record in payload.items():
        if isinstance(record, Mapping) and isinstance(record.get("enabled"), bool):
            overrides[str(item_id)] = bool(record["enabled"])
    return overrides


class AegisAPIApp:
    def __init__(self, config: APIAppConfig) -> None:
        self.config = config
        self.repository = RuntimeStorageRepository(config.database_path)
        self.repository.bootstrap()
        persisted_selection = load_provider_selection(_profile_dir_for_database(config.database_path))
        active_provider_profile = persisted_selection.strong_profile
        weak_provider_profile = persisted_selection.weak_profile
        strong_provider_profile_id = None
        weak_provider_profile_id = None
        active_provider_id = None
        if active_provider_profile is not None:
            self.repository.upsert_auth_profile(active_provider_profile)
            strong_provider_profile_id = active_provider_profile.profile_id
            active_provider_id = active_provider_profile.provider_id
        if weak_provider_profile is not None:
            self.repository.upsert_auth_profile(weak_provider_profile)
            weak_provider_profile_id = weak_provider_profile.profile_id
        elif active_provider_profile is not None:
            weak_provider_profile_id = active_provider_profile.profile_id
        self.auth_store = PersistentAuthProfileStore(self.repository)
        self.session_lineage = SessionLineageService(self.repository)
        self.memory_runtime = MemoryRuntime.from_repository(self.repository)
        self.cron_runtime = CronRuntime(self.repository.database_path.parent / "cron-jobs.json")
        self.context_runtime = ContextRuntime(instruction_refs=config.instruction_refs, total_tokens=config.total_tokens)
        self.planning_service = PlanningService()
        self.personal_state = APIStateService(
            repository=self.repository,
            session_lineage=self.session_lineage,
            memory_runtime=self.memory_runtime,
            planning_service=self.planning_service,
        )
        self.telemetry = APITelemetrySink()
        self.preview_model_provider = APIModelProvider()
        self.delivery = APIDeliveryCapability()
        self.memory = APIMemoryCapability(self.memory_runtime)
        self.context = APIContextCapability(self.context_runtime)
        self.planning = APIPlanningCapability(self.planning_service)
        browser_backend, _ = create_playwright_browser_backend()
        self.tool_runtime = build_tool_runtime(
            enabled_overrides=_enabled_overrides(_profile_dir_for_database(config.database_path), "tool_overrides"),
            dependencies=BuiltinToolDependencies(
                cwd=Path.cwd(),
                cron_runtime=self.cron_runtime,
                profile_management=self,
                activity_management=self,
                memory_management=APIMemoryManagementSurface(self),
                recall_search=APIRecallSearchSurface(self),
                procedure_management=self,
                browser_backend=browser_backend,
                message_delivery=DeliveryMessageSurfaceAdapter(
                    self.delivery,
                    surface_label="api",
                    default_target="api",
                ),
                clarify_surface=StructuredClarifySurface(
                    surface_label="api",
                    extra_metadata={"transport": "http"},
                ),
            ),
        )
        self.tools = APIToolExecution(self.tool_runtime)
        self.model_provider = SurfaceModelProviderCapability(
            repository=self.repository,
            fallback=self.preview_model_provider,
            secret_key_path=self.repository.database_path.parent / "provider-secrets.key",
            tool_runtime=self.tool_runtime,
            capability_id="api.model.runtime",
            surface_label="api",
            strong_provider_profile_id=strong_provider_profile_id,
            weak_provider_profile_id=weak_provider_profile_id,
            active_provider_id=active_provider_id,
            intent_mode=persisted_selection.intent_mode,
            bootstrap_state_dir=self.repository.database_path.parent,
        )
        self.kernel = KernelService(
            dependencies=KernelDependencies(
                storage=self.repository,
                context=self.context,
                planning=self.planning,
                memory=self.memory,
                model_provider=self.model_provider,
                telemetry=self.telemetry,
                tools=self.tools,
                delivery=self.delivery,
                embedding_service=self.memory_runtime.retriever.evidence_retriever.embedding_service,
            )
        )
        self._turns: dict[str, list[APITurnRecord]] = {}

AegisAPIApp.list_providers = _provider_methods.list_providers
AegisAPIApp.setup_provider = _provider_methods.setup_provider
AegisAPIApp.discover_provider_models = _provider_methods.discover_provider_models
AegisAPIApp.set_default_provider = _provider_methods.set_default_provider
AegisAPIApp._provider_probe = _provider_methods._provider_probe
AegisAPIApp.test_provider = _provider_methods.test_provider
AegisAPIApp.doctor_provider = _provider_methods.doctor_provider
AegisAPIApp.list_provider_keys = _provider_methods.list_provider_keys
AegisAPIApp.create_provider_key = _provider_methods.create_provider_key
AegisAPIApp.upsert_provider_key = _provider_methods.upsert_provider_key
AegisAPIApp.delete_provider_key = _provider_methods.delete_provider_key
AegisAPIApp.create_session = _surface_methods.create_session
AegisAPIApp.interrupt_session = _surface_methods.interrupt_session
AegisAPIApp.resume_session = _surface_methods.resume_session
AegisAPIApp._load_activity_graph = _surface_methods._load_activity_graph
AegisAPIApp.list_goals = _surface_methods.list_goals
AegisAPIApp.list_memories = _surface_methods.list_memories
AegisAPIApp.inspect_identity = _surface_methods.inspect_identity
AegisAPIApp.update_identity_state = _surface_methods.update_identity_state
AegisAPIApp.inspect_user = _surface_methods.inspect_user
AegisAPIApp.update_user_state = _surface_methods.update_user_state
AegisAPIApp.inspect_relationship = _surface_methods.inspect_relationship
AegisAPIApp.update_relationship_state = _surface_methods.update_relationship_state
AegisAPIApp.inspect_continuity = _surface_methods.inspect_continuity
AegisAPIApp.inspect_context_frame = _surface_methods.inspect_context_frame
AegisAPIApp.inspect_profile_surface = _surface_methods.inspect_profile_surface
AegisAPIApp.patch_profile_surface = _surface_methods.patch_profile_surface
AegisAPIApp.inspect_activity_surface = _surface_methods.inspect_activity_surface
AegisAPIApp.inspect_memory_surface = _surface_methods.inspect_memory_surface
AegisAPIApp.search_memory_surface = _surface_methods.search_memory_surface
AegisAPIApp.inspect_procedure_surface = _surface_methods.inspect_procedure_surface
AegisAPIApp.inspect_procedure_detail = _surface_methods.inspect_procedure_detail
AegisAPIApp.patch_procedure_surface = _surface_methods.patch_procedure_surface
AegisAPIApp.retire_procedure_surface = _surface_methods.retire_procedure_surface
AegisAPIApp.inspect_audit_surface = _surface_methods.inspect_audit_surface
AegisAPIApp.inspect_session = _surface_methods.inspect_session
AegisAPIApp.inspect_dashboard_surface = _surface_methods.inspect_dashboard_surface
AegisAPIApp.inspect_operator_console = _console_methods.inspect_operator_console
AegisAPIApp.patch_operator_settings = _console_methods.patch_operator_settings
AegisAPIApp.patch_operator_global_config = _console_methods.patch_operator_global_config
AegisAPIApp.set_console_item_enabled = _console_methods.set_console_item_enabled
AegisAPIApp.gateway_action = _console_methods.gateway_action
AegisAPIApp.inspect_goal = _goal_methods.inspect_goal
AegisAPIApp.create_goal = _goal_methods.create_goal
AegisAPIApp.inspect_memory = _goal_methods.inspect_memory
AegisAPIApp.update_goal = _goal_methods.update_goal
AegisAPIApp.delete_goal = _goal_methods.delete_goal
AegisAPIApp.correct_memory = _goal_methods.correct_memory
AegisAPIApp.delete_memory = _goal_methods.delete_memory
AegisAPIApp.pin_memory = _goal_methods.pin_memory
AegisAPIApp.run_turn = _http_methods.run_turn
AegisAPIApp.dispatch = _http_methods.dispatch
AegisAPIApp._dispatch_providers = _http_methods._dispatch_providers
AegisAPIApp._dispatch_operator = _http_methods._dispatch_operator
AegisAPIApp.__call__ = _http_methods.__call__

def create_app(
    *,
    database_path: str | Path,
    install_root: str | Path | None = None,
    instruction_refs: tuple[str, ...] = ("apps/api",),
    total_tokens: int = 2048,
) -> AegisAPIApp:
    return AegisAPIApp(
        APIAppConfig(
            database_path=Path(database_path),
            install_root=Path(install_root) if install_root is not None else None,
            instruction_refs=instruction_refs,
            total_tokens=total_tokens,
        )
    )

__all__ = [
    "APIAppConfig",
    "APIResponse",
    "APISessionCreationResult",
    "APISessionInspection",
    "APISessionLifecycleResult",
    "APIResumeResult",
    "APITurnRecord",
    "APITurnResult",
    "AegisAPIApp",
    "create_app",
]
