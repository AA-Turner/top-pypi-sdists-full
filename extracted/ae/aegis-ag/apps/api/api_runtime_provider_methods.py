"""Provider methods for the API runtime app."""


from __future__ import annotations

from dataclasses import asdict, dataclass, is_dataclass, replace
from datetime import UTC, datetime
from pathlib import Path
import json
from typing import Any, Mapping
from uuid import uuid4

from apps.provider_runtime import (
    SurfaceModelProviderCapability,
    provider_selection_from_payload,
)
from packages.auth import AuthProfile, PersistentAuthProfileStore, SecretReference
from packages.context import ContextRuntime
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
from packages.state import PROFILE_MANIFEST_FILENAME, write_profile_manifest
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

from .api_runtime_support import (
    APIAppConfig,
    APIResponse,
    APISessionCreationResult,
    APISessionInspection,
    APIResumeResult,
    APITurnRecord,
    APITurnResult,
    _coerce_str_tuple,
    _json_bytes,
    _jsonable,
    _now,
    _optional_bool,
    _optional_datetime,
    _optional_str,
    _read_json_bytes,
    _split_path,
)


def _profile_dir_for_database(database_path: Path) -> Path:
    state_dir = database_path.parent
    if state_dir.name == "state":
        return state_dir.parent / "profile"
    return state_dir / "profile"


def _read_profile_manifest(profile_dir: Path) -> dict[str, Any]:
    manifest_path = profile_dir / PROFILE_MANIFEST_FILENAME
    try:
        payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, ValueError, json.JSONDecodeError):
        return {}
    return dict(payload) if isinstance(payload, Mapping) else {}


def _persist_default_provider(self, provider_profile: Mapping[str, Any]) -> None:
    profile_dir = _profile_dir_for_database(self.repository.database_path)
    manifest = _read_profile_manifest(profile_dir)
    manifest["model_selection"] = _jsonable(provider_profile)
    write_profile_manifest(profile_dir, manifest)


def list_providers(self) -> dict[str, Any]:
    providers = []
    for record in self.model_provider.runtime_resolver.list_catalog():
        provider = record.as_mapping()
        try:
            discovered_state = asdict(self.model_provider.discovered_provider_state(record.provider_id))
            provider["discovered_state"] = discovered_state
            provider["status"] = discovered_state.get("status")
            provider["source"] = discovered_state.get("source")
        except Exception:
            pass
        providers.append(provider)
    return {
        "active_provider": self.model_provider.describe(),
        "providers": providers,
    }

def setup_provider(self, provider_id: str) -> dict[str, Any]:
    guide = self.model_provider.runtime_resolver.build_setup_guide(provider_id)
    return {
        "active_provider": self.model_provider.describe(),
        "guide": guide.as_mapping(),
    }

def discover_provider_models(self, payload: Mapping[str, Any]) -> dict[str, Any]:
    provider_id = str(payload.get("providerId") or payload.get("provider_id") or "").strip()
    if not provider_id:
        raise ValueError("providerId is required")
    base_url = str(payload.get("baseUrl") or payload.get("base_url") or "").strip() or None
    api_key = str(payload.get("apiKey") or payload.get("api_key") or "").strip() or None
    models = self.model_provider.discover_models(
        provider_id=provider_id,
        base_url=base_url,
        api_key=api_key,
    )
    return {
        "active_provider": self.model_provider.describe(),
        "providerId": provider_id,
        "baseUrl": base_url,
        "models": [asdict(model) for model in models],
    }

def _selection_profiles_from_payload(provider_profile: Mapping[str, Any]) -> tuple[AuthProfile, AuthProfile, str]:
    selection = provider_selection_from_payload(provider_profile)
    strong_profile = selection.strong_profile
    weak_profile = selection.weak_profile
    if strong_profile is None or weak_profile is None:
        raise ValueError("provider_profile must include strong_profile and weak_profile objects")
    return (
        strong_profile,
        weak_profile,
        selection.intent_mode,
    )


def _metadata_context_window_tokens(metadata: Mapping[str, str]) -> int | None:
    raw_value = metadata.get("context_window_tokens")
    if raw_value is None:
        return None
    try:
        parsed = int(str(raw_value).replace(",", ""))
    except (TypeError, ValueError):
        return None
    return parsed if parsed > 0 else None


def _profile_payload_with_metadata(payload: Mapping[str, Any], profile: AuthProfile) -> dict[str, Any]:
    next_payload = dict(payload)
    next_payload["metadata"] = {
        **{str(key): str(value) for key, value in dict(payload.get("metadata", {})).items()},
        **{str(key): str(value) for key, value in dict(profile.metadata).items()},
    }
    return next_payload


def _provider_profile_payload_with_profiles(
    provider_profile: Mapping[str, Any],
    *,
    strong_profile: AuthProfile,
    weak_profile: AuthProfile,
    intent_mode: str,
) -> dict[str, Any]:
    strong_payload = provider_profile.get("strong_profile")
    weak_payload = provider_profile.get("weak_profile")
    return {
        **dict(provider_profile),
        "intent_mode": intent_mode,
        "strong_profile": _profile_payload_with_metadata(
            strong_payload if isinstance(strong_payload, Mapping) else {},
            strong_profile,
        ),
        "weak_profile": _profile_payload_with_metadata(
            weak_payload if isinstance(weak_payload, Mapping) else {},
            weak_profile,
        ),
    }


def _provider_profile_with_auto_context(self, profile: AuthProfile) -> AuthProfile:
    metadata = {str(key): str(value) for key, value in dict(profile.metadata).items()}
    context_window_mode = str(metadata.get("context_window_mode") or "auto").strip().lower() or "auto"
    metadata["context_window_mode"] = context_window_mode
    if context_window_mode == "manual" or _metadata_context_window_tokens(metadata) is not None:
        return replace(profile, metadata=metadata)
    model_id = str(profile.default_model or "").strip()
    if not model_id:
        return replace(profile, metadata=metadata)
    try:
        detected = self.model_provider.detect_context_window(
            provider_id=profile.provider_id,
            base_url=profile.base_url,
            model_id=model_id,
        )
    except Exception:
        detected = None
    if detected is not None:
        metadata["context_window_tokens"] = str(detected)
    return replace(profile, metadata=metadata)


def set_default_provider(self, provider_profile: Mapping[str, Any]) -> dict[str, Any]:
    strong_profile, weak_profile, intent_mode = _selection_profiles_from_payload(provider_profile)
    strong_profile = _provider_profile_with_auto_context(self, strong_profile)
    weak_profile = _provider_profile_with_auto_context(self, weak_profile)
    enriched_provider_profile = _provider_profile_payload_with_profiles(
        provider_profile,
        strong_profile=strong_profile,
        weak_profile=weak_profile,
        intent_mode=intent_mode,
    )
    _persist_default_provider(self, enriched_provider_profile)
    self.auth_store.register(strong_profile)
    self.auth_store.register(weak_profile)
    self.model_provider.set_active_profiles(
        strong_provider_profile_id=strong_profile.profile_id,
        weak_provider_profile_id=weak_profile.profile_id,
        provider_id=strong_profile.provider_id,
        intent_mode=intent_mode,
    )
    return {
        "provider_profiles": {
            "strong": strong_profile,
            "weak": weak_profile,
            "intent_mode": intent_mode,
        },
        "active_provider": self.model_provider.describe(),
    }

def _provider_probe(
    self,
    *,
    prompt: str,
) -> ExecutionResult:
    active_profile = self.model_provider.active_profile()
    profile = ProfileState(
        profile_id=f"provider-test:{active_profile.provider_id if active_profile is not None else 'preview'}",
        display_name=active_profile.provider_id if active_profile is not None else "Provider Test",
        mode="default",
    )
    session = SessionState(
        session_id=f"session:provider-test:{uuid4().hex[:8]}",
        profile_id=profile.profile_id,
        workspace_id="provider-test",
        status="active",
        started_at=_now(),
        updated_at=_now(),
    )
    context = ContextBundle(
        bundle_id=f"bundle:provider-test:{uuid4().hex[:8]}",
        session_id=session.session_id,
        instruction_refs=("apps/api",),
        goal_ids=(),
        memory_ids=(),
        artifact_ids=(),
        token_budget=512,
        rendered_prompt="provider test",
    )
    return self.model_provider.generate(
        profile=profile,
        session=session,
        context=context,
        prompt=prompt,
    )

def test_provider(self, *, prompt: str = "Summarize the current provider configuration.") -> dict[str, Any]:
    active_provider = self.model_provider.describe()
    try:
        result = self._provider_probe(prompt=prompt)
    except Exception as error:  # pragma: no cover - defensive surface guard
        return {
            "active_provider": active_provider,
            "status": "not-ready",
            "error": str(error),
        }
    return {
        "active_provider": active_provider,
        "status": "ok",
        "result": result,
    }

def doctor_provider(self) -> dict[str, Any]:
    active_provider = self.model_provider.describe()
    bootstrap_check = {
        "check": "embedding_bootstrap",
        "status": str(active_provider.get("embedding_bootstrap_status") or "unknown"),
        "summary": str(active_provider.get("embedding_bootstrap_summary") or ""),
    }
    if active_provider["source"] != "configured":
        return {
            "status": "preview",
            "active_provider": active_provider,
            "checks": (
                {"check": "provider_profile", "status": "missing"},
                {"check": "credentials", "status": "preview"},
                bootstrap_check,
            ),
            "probe_summary": "",
        }
    try:
        probe = self._provider_probe(prompt="Doctor check")
    except Exception as error:  # pragma: no cover - defensive surface guard
        return {
            "status": "not-ready",
            "active_provider": active_provider,
            "checks": (
                {"check": "provider_profile", "status": "configured"},
                {"check": "credentials", "status": "missing", "summary": str(error)},
                bootstrap_check,
            ),
            "probe_summary": "",
        }
    return {
        "status": "ready",
        "active_provider": active_provider,
        "checks": (
            {"check": "provider_profile", "status": "configured"},
            {"check": "credentials", "status": "available"},
            bootstrap_check,
            {"check": "runtime", "status": "ok", "summary": probe.summary},
        ),
        "probe_summary": probe.summary,
    }


def list_provider_keys(self) -> dict[str, Any]:
    with self.repository.connection() as connection:
        rows = connection.execute(
            """
            SELECT r.reference_id, r.profile_id, r.provider_id, r.secret_name,
                   r.secret_key, r.source, r.metadata_json, r.created_at,
                   CASE WHEN v.reference_id IS NULL THEN 0 ELSE 1 END AS has_value,
                   v.updated_at AS value_updated_at
            FROM auth_secret_references AS r
            LEFT JOIN auth_secret_values AS v ON v.reference_id = r.reference_id
            ORDER BY r.provider_id ASC, r.profile_id ASC, r.reference_order ASC
            """
        ).fetchall()
    keys: list[dict[str, Any]] = []
    for row in rows:
        metadata = {}
        try:
            metadata = json.loads(str(row["metadata_json"] or "{}"))
        except (TypeError, ValueError, json.JSONDecodeError):
            metadata = {}
        keys.append(
            {
                "referenceId": row["reference_id"],
                "profileId": row["profile_id"],
                "providerId": row["provider_id"],
                "secretName": row["secret_name"],
                "secretKey": row["secret_key"],
                "source": row["source"],
                "metadata": metadata,
                "createdAt": row["created_at"],
                "hasValue": bool(row["has_value"]),
                "valueUpdatedAt": row["value_updated_at"],
                "redactedValue": "***" if row["has_value"] else "",
            }
        )
    return {"keys": keys}


def upsert_provider_key(self, reference_id: str, payload: Mapping[str, Any]) -> dict[str, Any]:
    value = str(payload.get("value") or "")
    if not value.strip():
        raise ValueError("value is required")
    reference = _load_secret_reference(self, reference_id)
    self.model_provider.store_secret_value(reference, value)
    return {"status": "ok", "referenceId": reference_id, "hasValue": True}


def create_provider_key(self, payload: Mapping[str, Any]) -> dict[str, Any]:
    profile_id = str(payload.get("profileId") or payload.get("profile_id") or "").strip()
    provider_id = str(payload.get("providerId") or payload.get("provider_id") or "").strip()
    secret_key = str(payload.get("secretKey") or payload.get("secret_key") or "api_key").strip()
    secret_name = str(payload.get("secretName") or payload.get("secret_name") or "api_token").strip()
    reference_id = str(payload.get("referenceId") or payload.get("reference_id") or f"secret:{profile_id}:{secret_key}").strip()
    if not profile_id or not provider_id or not reference_id:
        raise ValueError("profileId, providerId, and referenceId are required")
    profile = self.repository.load_auth_profile(profile_id)
    if profile is None:
        raise KeyError(profile_id)
    metadata = payload.get("metadata") if isinstance(payload.get("metadata"), Mapping) else {}
    reference = SecretReference(
        reference_id=reference_id,
        provider_id=provider_id,
        secret_name=secret_name,
        secret_key=secret_key,
        metadata={str(key): str(value) for key, value in dict(metadata).items()},
    )
    next_refs = tuple(ref for ref in profile.secret_references if ref.reference_id != reference_id) + (reference,)
    self.repository.upsert_auth_profile(replace(profile, secret_references=next_refs))
    raw_value = payload.get("value")
    if isinstance(raw_value, str) and raw_value.strip():
        self.model_provider.store_secret_value(reference, raw_value)
    return {"status": "ok", "referenceId": reference_id, "hasValue": bool(raw_value)}


def delete_provider_key(self, reference_id: str) -> dict[str, Any]:
    self.repository.delete_auth_secret_value(reference_id)
    return {"status": "ok", "referenceId": reference_id, "hasValue": False}


def _load_secret_reference(self, reference_id: str) -> SecretReference:
    with self.repository.connection() as connection:
        row = connection.execute(
            """
            SELECT reference_id, provider_id, secret_name, secret_key, source, metadata_json
            FROM auth_secret_references
            WHERE reference_id = ?
            """,
            (reference_id,),
        ).fetchone()
    if row is None:
        raise KeyError(reference_id)
    try:
        metadata = json.loads(str(row["metadata_json"] or "{}"))
    except (TypeError, ValueError, json.JSONDecodeError):
        metadata = {}
    return SecretReference(
        reference_id=str(row["reference_id"]),
        provider_id=str(row["provider_id"]),
        secret_name=str(row["secret_name"]),
        secret_key=str(row["secret_key"]),
        source=str(row["source"] or "workspace"),
        metadata={str(key): str(value) for key, value in metadata.items()},
    )
