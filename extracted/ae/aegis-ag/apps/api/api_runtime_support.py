"""Support contracts and helpers for the API runtime."""


from __future__ import annotations

from dataclasses import asdict, dataclass, is_dataclass, replace
from datetime import UTC, datetime
from pathlib import Path
import json
from typing import Any, Mapping
from uuid import uuid4

from apps.provider_runtime import (
    SurfaceModelProviderCapability,
    provider_profile_from_payload,
)
from packages.auth import AuthProfile, PersistentAuthProfileStore
from packages.context import ContextRuntime
from packages.contracts import ContextBundle, EventEnvelope, ExecutionResult, GoalNode, MemoryRecord, ProfileState, SessionState, ActivityGraph
from packages.kernel import KernelDependencies, KernelOutcome, KernelService, KernelTurnRequest, ObservationPipeline, StateReconciler
from packages.learning import LearningRuntime
from packages.evidence import MemoryRuntime
from packages.growth import ProgressionProjection
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
from .tool_surfaces import APIMemoryManagementSurface

def _now() -> datetime:
    return datetime.now(UTC)

def _jsonable(value: Any) -> Any:
    if is_dataclass(value):
        return _jsonable(asdict(value))
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, Mapping):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, tuple):
        return [_jsonable(item) for item in value]
    if isinstance(value, list):
        return [_jsonable(item) for item in value]
    if isinstance(value, set):
        return [_jsonable(item) for item in sorted(value, key=repr)]
    return value

def _json_bytes(payload: Mapping[str, Any]) -> bytes:
    return json.dumps(_jsonable(payload), separators=(",", ":"), sort_keys=True).encode("utf-8")

def _read_json_bytes(body: bytes | None) -> dict[str, Any]:
    if not body:
        return {}
    data = json.loads(body.decode("utf-8"))
    if not isinstance(data, dict):
        raise ValueError("request body must be a JSON object")
    return data

def _split_path(path: str) -> tuple[str, ...]:
    trimmed = path.strip("/")
    if not trimmed:
        return ()
    parts = tuple(part for part in trimmed.split("/") if part)
    if parts and parts[0] == "v1":
        return parts[1:]
    return parts

def _coerce_str_tuple(value: Any) -> tuple[str, ...]:
    if value is None:
        return ()
    if isinstance(value, str):
        if not value.strip():
            return ()
        return tuple(part.strip() for part in value.split(",") if part.strip())
    if isinstance(value, (list, tuple)):
        return tuple(str(item) for item in value if str(item))
    return (str(value),)

def _optional_str(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None

def _optional_datetime(value: Any) -> datetime | None:
    text = _optional_str(value)
    if text is None:
        return None
    return datetime.fromisoformat(text)

def _optional_bool(value: Any) -> bool | None:
    if value is None:
        return None
    if isinstance(value, bool):
        return value
    text = _optional_str(value)
    if text is None:
        return None
    normalized = text.lower()
    if normalized in {"true", "1", "yes", "on"}:
        return True
    if normalized in {"false", "0", "no", "off"}:
        return False
    raise ValueError(f"invalid boolean value: {value}")

@dataclass(frozen=True, slots=True)
class APIAppConfig:
    database_path: Path
    install_root: Path | None = None
    instruction_refs: tuple[str, ...] = ("apps/api",)
    total_tokens: int = 2048

@dataclass(frozen=True, slots=True)
class APITurnRecord:
    request: dict[str, Any]
    outcome: KernelOutcome
    recorded_at: datetime

    def to_record(self) -> dict[str, Any]:
        return {
            "request": self.request,
            "outcome": self.outcome,
            "recorded_at": self.recorded_at,
        }

@dataclass(frozen=True, slots=True)
class APISessionInspection:
    profile: ProfileState
    session: SessionState
    lineage: tuple[SessionState, ...]
    goals: tuple[GoalNode, ...]
    memories: tuple[MemoryRecord, ...]
    latest_turn: APITurnRecord | None
    memory_count: int
    telemetry_count: int
    goal_graph_revision: str | None = None
    goal_status_counts: dict[str, int] | None = None
    provider_profile: AuthProfile | None = None
    progression: ProgressionProjection | None = None

    def to_record(self) -> dict[str, Any]:
        return {
            "profile": self.profile,
            "session": self.session,
            "lineage": self.lineage,
            "goals": self.goals,
            "memories": self.memories,
            "latest_turn": self.latest_turn,
            "memory_count": self.memory_count,
            "telemetry_count": self.telemetry_count,
            "goal_graph_revision": self.goal_graph_revision,
            "goal_status_counts": self.goal_status_counts,
            "provider_profile": self.provider_profile,
            "progression": self.progression,
        }

@dataclass(frozen=True, slots=True)
class APISessionCreationResult:
    profile: ProfileState
    session: SessionState

    def to_record(self) -> dict[str, Any]:
        return {
            "profile": self.profile,
            "session": self.session,
        }

@dataclass(frozen=True, slots=True)
class APISessionLifecycleResult:
    session: SessionState

    def to_record(self) -> dict[str, Any]:
        return {"session": self.session}

@dataclass(frozen=True, slots=True)
class APIResumeResult:
    parent: SessionState
    session: SessionState
    lineage: tuple[SessionState, ...]

    def to_record(self) -> dict[str, Any]:
        return {
            "parent": self.parent,
            "session": self.session,
            "lineage": self.lineage,
        }

@dataclass(frozen=True, slots=True)
class APITurnResult:
    session: SessionState
    outcome: KernelOutcome
    latest_turn: APITurnRecord
    inspection: APISessionInspection

    def to_record(self) -> dict[str, Any]:
        return {
            "session": self.session,
            "outcome": self.outcome,
            "latest_turn": self.latest_turn,
            "inspection": self.inspection,
        }

@dataclass(frozen=True, slots=True)
class APIResponse:
    status_code: int
    payload: Mapping[str, Any]
    headers: tuple[tuple[str, str], ...] = (("content-type", "application/json; charset=utf-8"),)
