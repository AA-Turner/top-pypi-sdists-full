"""Shared provider runtime wiring for product surfaces.

This module keeps surface-level provider profile parsing, encrypted local
credential lookup, endpoint model discovery, and runtime capability selection
in one place so CLI, API, and gateway do not each keep private copies of the
same rules.
"""

from __future__ import annotations

import base64
from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
from typing import Any
from urllib import error, request
from urllib.parse import quote

from packages.auth import (
    AuthProfile,
    LocalEncryptedSecretCipher,
    PersistentAuthProfileStore,
    ProfileCredentialResolver,
    ProviderAuthState,
    ProviderCatalog,
    ProviderProfileFactory,
    ProviderProfileInput,
    SecretValueResolution,
    SecretReference,
    SecretStore,
    profile_from_input,
)
from packages.capabilities.runtime import CapabilityDescriptor, ModelProviderCapability
from packages.contracts.runtime import (
    ContextBundle,
    ExecutionResult,
    MixtureModelSelection,
    ProfileState,
    SessionState,
    StrongModelProfile,
    WeakModelProfile,
)
from packages.embeddings import (
    AEGIS_EMBED_MODEL_ID,
    AEGIS_EMBED_SOURCE_URL,
    embedding_model_root_path,
    embedding_root_is_healthy,
    sentence_transformers_dependencies_ready,
)
from packages.models import ModelRequest, ProviderRuntimeResolver
from packages.models.model_metadata import resolve_provider_model_metadata
from packages.models.provider_catalog import default_provider_definitions, provider_definition
from packages.models.provider_runtime import provider_auth_headers
from packages.models.providers import build_model_adapter
from packages.storage import RuntimeStorageRepository
from packages.tools import ToolDefinition, ToolRuntime

_MODEL_CONTEXT_KEYS = (
    "context_length",
    "context_window",
    "max_context_length",
    "max_position_embeddings",
    "max_model_len",
    "max_input_tokens",
    "max_sequence_length",
    "max_seq_len",
    "n_ctx",
    "n_ctx_train",
)
_MODEL_OUTPUT_KEYS = (
    "max_completion_tokens",
    "max_output_tokens",
    "max_tokens",
)
DEFAULT_CONTEXT_WINDOW_TOKENS = 128_000


@dataclass(frozen=True, slots=True)
class DiscoveredProviderModel:
    model_id: str
    label: str
    context_window_tokens: int | None = None
    max_output_tokens: int | None = None
    source: str = "endpoint"
    metadata: Mapping[str, str] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class DiscoveredProviderState:
    provider_id: str
    display_name: str
    transport_display_name: str
    auth_type: str
    provider_kind: str
    runtime_enabled: bool
    status: str
    source: str
    profile_id: str | None = None
    base_url: str | None = None
    default_model: str | None = None
    reasoning_efforts: tuple[str, ...] = ()
    metadata: Mapping[str, str] = field(default_factory=dict)


def _normalize_base_url(base_url: str | None) -> str:
    return str(base_url or "").strip().rstrip("/")


def _compose_provider_url(base_url: str, endpoint_path: str) -> str:
    trimmed_base = _normalize_base_url(base_url)
    trimmed_path = endpoint_path.lstrip("/")
    if trimmed_path.startswith("v1/") and trimmed_base.endswith("/v1"):
        trimmed_path = trimmed_path[3:]
    return f"{trimmed_base}/{trimmed_path}"


def _coerce_reasonable_int(value: Any, *, minimum: int = 1024, maximum: int = 10_000_000) -> int | None:
    try:
        if isinstance(value, bool):
            return None
        if isinstance(value, str):
            value = value.strip().replace(",", "")
        parsed = int(value)
    except (TypeError, ValueError):
        return None
    if minimum <= parsed <= maximum:
        return parsed
    return None


def _iter_nested_mappings(value: Any):
    if isinstance(value, Mapping):
        yield value
        for nested in value.values():
            yield from _iter_nested_mappings(nested)
    elif isinstance(value, list):
        for item in value:
            yield from _iter_nested_mappings(item)


def _extract_nested_int(payload: Mapping[str, Any], keys: tuple[str, ...]) -> int | None:
    keyset = {key.casefold() for key in keys}
    for mapping in _iter_nested_mappings(payload):
        for key, value in mapping.items():
            if str(key).casefold() not in keyset:
                continue
            parsed = _coerce_reasonable_int(value)
            if parsed is not None:
                return parsed
    return None


def _context_window_from_payload(payload: Mapping[str, Any]) -> int | None:
    return _extract_nested_int(payload, _MODEL_CONTEXT_KEYS)


def _max_output_tokens_from_payload(payload: Mapping[str, Any]) -> int | None:
    return _extract_nested_int(payload, _MODEL_OUTPUT_KEYS)


def _provider_request_headers(
    *,
    provider_id: str,
    request_family: str,
    api_key: str | None,
    extra_headers: Mapping[str, str] | None = None,
) -> dict[str, str]:
    return {
        "Accept": "application/json",
        **dict(extra_headers or {}),
        **provider_auth_headers(
            provider_id=provider_id,
            request_family=request_family,
            api_key=api_key,
        ),
    }


def _request_json(
    *,
    url: str,
    headers: Mapping[str, str],
    timeout_seconds: float = 10.0,
) -> dict[str, Any]:
    http_request = request.Request(
        url,
        headers=dict(headers),
        method="GET",
    )
    try:
        with request.urlopen(http_request, timeout=timeout_seconds) as response:
            raw_body = response.read().decode("utf-8")
            payload = json.loads(raw_body) if raw_body else {}
    except error.HTTPError as exc:  # pragma: no cover - exercised by integration tests
        detail = exc.read().decode("utf-8", errors="replace").strip()
        suffix = f" {detail[:200]}" if detail else ""
        raise RuntimeError(f"provider metadata request failed with status {exc.code}.{suffix}".strip()) from exc
    except error.URLError as exc:  # pragma: no cover - exercised by integration tests
        raise RuntimeError(f"provider metadata request failed for {url}: {exc.reason}") from exc
    if isinstance(payload, list):
        return {"data": payload}
    if not isinstance(payload, dict):
        raise RuntimeError("provider metadata response must be a JSON object")
    return {str(key): value for key, value in payload.items()}


def _ollama_server_root(base_url: str) -> str:
    server_url = _normalize_base_url(base_url)
    if server_url.endswith("/v1"):
        server_url = server_url[:-3]
    return server_url


def _context_window_from_ollama_show_payload(payload: Mapping[str, Any]) -> int | None:
    parameters = payload.get("parameters")
    if isinstance(parameters, str) and "num_ctx" in parameters:
        for line in parameters.splitlines():
            parts = line.strip().split()
            if len(parts) >= 2 and parts[0] == "num_ctx":
                parsed = _coerce_reasonable_int(parts[-1])
                if parsed is not None:
                    return parsed
    model_info = payload.get("model_info")
    if isinstance(model_info, Mapping):
        for key, value in model_info.items():
            if "context_length" not in str(key).casefold():
                continue
            parsed = _coerce_reasonable_int(value)
            if parsed is not None:
                return parsed
    return _context_window_from_payload(payload)


def _query_ollama_context_window(*, model_id: str, base_url: str, timeout_seconds: float = 5.0) -> int | None:
    server_url = _ollama_server_root(base_url)
    if not server_url:
        return None
    body = json.dumps({"name": model_id}).encode("utf-8")
    http_request = request.Request(
        f"{server_url}/api/show",
        data=body,
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with request.urlopen(http_request, timeout=timeout_seconds) as response:
            raw_body = response.read().decode("utf-8")
            payload = json.loads(raw_body) if raw_body else {}
    except (error.HTTPError, error.URLError, json.JSONDecodeError):  # pragma: no cover - covered by caller fallback
        return None
    if not isinstance(payload, Mapping):
        return None
    return _context_window_from_ollama_show_payload(payload)


def _provider_metadata(provider_id: str) -> Mapping[str, str]:
    definition = provider_definition(provider_id)
    if definition is None:
        return {}
    return {str(key): str(value) for key, value in dict(definition.metadata).items()}


def _provider_model_catalog_path(provider_id: str) -> str:
    configured = _provider_metadata(provider_id).get("model_catalog_path", "").strip()
    return configured or "/v1/models"


def _provider_model_detail_path(provider_id: str, model_id: str) -> str:
    metadata = _provider_metadata(provider_id)
    template = metadata.get("model_detail_path_template", "").strip()
    if template:
        return template.replace("{model_id}", quote(model_id, safe=""))
    catalog_path = _provider_model_catalog_path(provider_id)
    catalog_root = catalog_path.split("?", 1)[0].rstrip("/")
    if catalog_root.endswith("/models"):
        return f"{catalog_root}/{quote(model_id, safe='')}"
    return f"/v1/models/{quote(model_id, safe='')}"


def _provider_model_payload_list_keys(provider_id: str) -> tuple[str, ...]:
    configured = _provider_metadata(provider_id).get("model_payload_list_key", "").strip()
    keys = [configured] if configured else []
    keys.extend(["data", "models"])
    ordered: list[str] = []
    seen: set[str] = set()
    for key in keys:
        normalized = key.strip()
        if not normalized or normalized in seen:
            continue
        seen.add(normalized)
        ordered.append(normalized)
    return tuple(ordered)


def _provider_model_id_keys(provider_id: str) -> tuple[str, ...]:
    configured = _provider_metadata(provider_id).get("model_payload_id_key", "").strip()
    keys = [configured] if configured else []
    keys.extend(["id", "slug"])
    ordered: list[str] = []
    seen: set[str] = set()
    for key in keys:
        normalized = key.strip()
        if not normalized or normalized in seen:
            continue
        seen.add(normalized)
        ordered.append(normalized)
    return tuple(ordered)


def _provider_model_items(provider_id: str, payload: Mapping[str, Any]) -> tuple[Mapping[str, Any], ...]:
    for list_key in _provider_model_payload_list_keys(provider_id):
        items = payload.get(list_key)
        if not isinstance(items, list):
            continue
        return tuple(item for item in items if isinstance(item, Mapping))
    return ()


def _read_json_object(path: Path) -> dict[str, Any] | None:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    if not isinstance(payload, dict):
        return None
    return {str(key): value for key, value in payload.items()}


def _jwt_claims(token: str) -> Mapping[str, Any]:
    parts = str(token or "").split(".")
    if len(parts) < 2:
        return {}
    padded = parts[1] + "=" * (-len(parts[1]) % 4)
    try:
        decoded = base64.urlsafe_b64decode(padded.encode("ascii"))
        payload = json.loads(decoded.decode("utf-8"))
    except (ValueError, UnicodeDecodeError, json.JSONDecodeError):
        return {}
    if not isinstance(payload, dict):
        return {}
    return {str(key): value for key, value in payload.items()}


def _jwt_token_is_expiring(token: str, *, skew_seconds: int = 0) -> bool:
    claims = _jwt_claims(token)
    exp = claims.get("exp")
    if not isinstance(exp, (int, float)):
        return False
    return float(exp) <= (datetime.now(timezone.utc).timestamp() + max(0, int(skew_seconds)))


def _timestamp_string_is_expiring(value: Any, *, skew_seconds: int = 0) -> bool:
    text = str(value or "").strip()
    if not text:
        return False
    if text.endswith("Z"):
        text = f"{text[:-1]}+00:00"
    try:
        expires_at = datetime.fromisoformat(text)
    except ValueError:
        return False
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)
    return expires_at.timestamp() <= (datetime.now(timezone.utc).timestamp() + max(0, int(skew_seconds)))


def _codex_auth_path() -> Path:
    codex_home = os.environ.get("CODEX_HOME", "").strip()
    if not codex_home:
        codex_home = str(Path.home() / ".codex")
    return Path(codex_home).expanduser() / "auth.json"


def _read_codex_cli_resolution() -> SecretValueResolution | None:
    auth_path = _codex_auth_path()
    if not auth_path.is_file():
        return None
    payload = _read_json_object(auth_path)
    if payload is None:
        return None
    tokens = payload.get("tokens")
    if not isinstance(tokens, Mapping):
        return None
    access_token = str(tokens.get("access_token", "") or "").strip()
    refresh_token = str(tokens.get("refresh_token", "") or "").strip()
    if not access_token or not refresh_token or _jwt_token_is_expiring(access_token):
        return None
    return SecretValueResolution(value=access_token, source=f"codex-cli:{auth_path}")


def _qwen_auth_path() -> Path:
    return Path.home() / ".qwen" / "oauth_creds.json"


def _hermes_home_path() -> Path:
    hermes_home = os.environ.get("HERMES_HOME", "").strip()
    if not hermes_home:
        hermes_home = str(Path.home() / ".hermes")
    return Path(hermes_home).expanduser()


def _hermes_auth_path() -> Path:
    return _hermes_home_path() / "auth.json"


def _hermes_google_oauth_path() -> Path:
    return _hermes_home_path() / "auth" / "google_oauth.json"


def _hermes_anthropic_oauth_path() -> Path:
    return _hermes_home_path() / ".anthropic_oauth.json"


def _claude_code_credentials_path() -> Path:
    return Path.home() / ".claude" / ".credentials.json"


def _read_hermes_provider_state(provider_id: str) -> dict[str, Any] | None:
    auth_path = _hermes_auth_path()
    if not auth_path.is_file():
        return None
    payload = _read_json_object(auth_path)
    if payload is None:
        return None
    providers = payload.get("providers")
    if not isinstance(providers, Mapping):
        return None
    state = providers.get(provider_id)
    if not isinstance(state, Mapping):
        return None
    return {str(key): value for key, value in state.items()}


def _read_hermes_credential_pool(provider_id: str) -> tuple[dict[str, Any], ...]:
    auth_path = _hermes_auth_path()
    if not auth_path.is_file():
        return ()
    payload = _read_json_object(auth_path)
    if payload is None:
        return ()
    credential_pool = payload.get("credential_pool")
    if not isinstance(credential_pool, Mapping):
        return ()
    entries = credential_pool.get(provider_id)
    if not isinstance(entries, list):
        return ()
    normalized: list[dict[str, Any]] = []
    for entry in entries:
        if isinstance(entry, Mapping):
            normalized.append({str(key): value for key, value in entry.items()})
    return tuple(normalized)


def _read_token_from_hermes_pool(
    provider_id: str,
    *,
    expiry_keys: tuple[str, ...] = ("expires_at", "access_expires_at", "agent_key_expires_at"),
) -> SecretValueResolution | None:
    auth_path = _hermes_auth_path()
    for entry in _read_hermes_credential_pool(provider_id):
        access_token = str(
            entry.get("runtime_api_key")
            or entry.get("access_token")
            or entry.get("api_key")
            or ""
        ).strip()
        if not access_token:
            continue
        if _jwt_token_is_expiring(access_token):
            continue
        if any(_timestamp_string_is_expiring(entry.get(key)) for key in expiry_keys):
            continue
        return SecretValueResolution(
            value=access_token,
            source=f"hermes-auth-store:{auth_path}:{provider_id}:pool",
        )
    return None


def _read_qwen_oauth_resolution() -> SecretValueResolution | None:
    auth_path = _qwen_auth_path()
    if not auth_path.is_file():
        return None
    payload = _read_json_object(auth_path)
    if payload is None:
        return None
    access_token = str(payload.get("access_token", "") or "").strip()
    if not access_token:
        return None
    try:
        expiry_ms = int(payload.get("expiry_date"))
    except (TypeError, ValueError):
        expiry_ms = 0
    if expiry_ms and expiry_ms <= int(datetime.now(timezone.utc).timestamp() * 1000):
        return None
    return SecretValueResolution(value=access_token, source=f"qwen-cli:{auth_path}")


def _read_hermes_codex_resolution() -> SecretValueResolution | None:
    auth_path = _hermes_auth_path()
    pooled = _read_token_from_hermes_pool("openai-codex")
    if pooled is not None:
        return pooled
    state = _read_hermes_provider_state("openai-codex")
    if state is None:
        return None
    tokens = state.get("tokens")
    if not isinstance(tokens, Mapping):
        return None
    access_token = str(tokens.get("access_token", "") or "").strip()
    if not access_token or _jwt_token_is_expiring(access_token):
        return None
    return SecretValueResolution(value=access_token, source=f"hermes-auth-store:{auth_path}:openai-codex")


def _read_google_gemini_oauth_resolution() -> SecretValueResolution | None:
    auth_path = _hermes_google_oauth_path()
    if not auth_path.is_file():
        return None
    payload = _read_json_object(auth_path)
    if payload is None:
        return None
    access_token = str(payload.get("access", "") or "").strip()
    if not access_token:
        return None
    try:
        expires_ms = int(payload.get("expires") or 0)
    except (TypeError, ValueError):
        expires_ms = 0
    if expires_ms and expires_ms <= int(datetime.now(timezone.utc).timestamp() * 1000):
        return None
    return SecretValueResolution(value=access_token, source=f"hermes-google-oauth:{auth_path}")


def _read_anthropic_token_from_payload(path: Path, payload: Mapping[str, Any], *, source: str) -> SecretValueResolution | None:
    claude_code_oauth = payload.get("claudeAiOauth")
    if isinstance(claude_code_oauth, Mapping):
        payload = {str(key): value for key, value in claude_code_oauth.items()}
    access_token = str(
        payload.get("accessToken")
        or payload.get("access_token")
        or payload.get("token")
        or ""
    ).strip()
    if not access_token:
        return None
    expires_at = payload.get("expiresAt") or payload.get("expires_at")
    if _timestamp_string_is_expiring(expires_at):
        return None
    return SecretValueResolution(value=access_token, source=f"{source}:{path}")


def _read_anthropic_oauth_resolution() -> SecretValueResolution | None:
    path = _hermes_anthropic_oauth_path()
    if path.is_file():
        payload = _read_json_object(path)
        if payload is not None:
            resolution = _read_anthropic_token_from_payload(path, payload, source="hermes-anthropic-oauth")
            if resolution is not None:
                return resolution
    for env_name in ("ANTHROPIC_TOKEN",):
        value = os.environ.get(env_name)
        if value:
            return SecretValueResolution(value=value, source=f"env:{env_name}")
    return None


def _read_claude_code_oauth_resolution() -> SecretValueResolution | None:
    path = _claude_code_credentials_path()
    if path.is_file():
        payload = _read_json_object(path)
        if payload is not None:
            resolution = _read_anthropic_token_from_payload(path, payload, source="claude-code-oauth")
            if resolution is not None:
                return resolution
    value = os.environ.get("CLAUDE_CODE_OAUTH_TOKEN")
    if value:
        return SecretValueResolution(value=value, source="env:CLAUDE_CODE_OAUTH_TOKEN")
    return None


def _read_copilot_resolution() -> SecretValueResolution | None:
    for env_name in ("COPILOT_GITHUB_TOKEN", "GH_TOKEN", "GITHUB_TOKEN"):
        value = str(os.environ.get(env_name) or "").strip()
        if value and not value.startswith("ghp_"):
            return SecretValueResolution(value=value, source=f"env:{env_name}")
    clean_env = {
        key: value
        for key, value in os.environ.items()
        if key not in {"GH_TOKEN", "GITHUB_TOKEN"}
    }
    try:
        completed = subprocess.run(
            ["gh", "auth", "token"],
            check=True,
            capture_output=True,
            text=True,
            timeout=5,
            env=clean_env,
        )
    except (FileNotFoundError, subprocess.SubprocessError):
        return None
    token = completed.stdout.strip()
    if not token or token.startswith("ghp_"):
        return None
    return SecretValueResolution(value=token, source="gh auth token")


def _copilot_acp_status() -> tuple[str, str] | None:
    base_url = os.environ.get("COPILOT_ACP_BASE_URL", "").strip()
    if base_url.startswith("acp+tcp://"):
        return (base_url, "env:COPILOT_ACP_BASE_URL")
    command = (
        os.environ.get("AEGIS_COPILOT_ACP_COMMAND", "").strip()
        or os.environ.get("HERMES_COPILOT_ACP_COMMAND", "").strip()
        or os.environ.get("COPILOT_CLI_PATH", "").strip()
        or "copilot"
    )
    resolved = shutil.which(command) if command else None
    if resolved:
        return ("acp://copilot", f"command:{resolved}")
    return None


def _base_url_aliases(provider_id: str) -> tuple[str, ...]:
    aliases = {
        "openai-codex": ("HERMES_CODEX_BASE_URL",),
        "qwen-oauth": ("HERMES_QWEN_BASE_URL",),
    }
    return aliases.get(provider_id, ())


def _provider_base_url_from_env(provider_id: str, primary_env_var: str | None) -> str | None:
    candidates = []
    if primary_env_var:
        candidates.append(primary_env_var)
    candidates.extend(_base_url_aliases(provider_id))
    for env_name in candidates:
        value = os.environ.get(env_name, "").strip()
        if value:
            return value
    return None


def provider_profile_from_payload(payload: Mapping[str, Any]) -> AuthProfile:
    secret_references = tuple(
        secret_reference_from_payload(item)
        for item in payload.get("secret_references", ())
    )
    profile_input = ProviderProfileInput(
        profile_id=str(payload["profile_id"]),
        provider_id=str(payload["provider_id"]),
        secret_references=secret_references,
        priority=int(payload.get("priority", 0)),
        session_pin=str(payload["session_pin"]) if payload.get("session_pin") is not None else None,
        cooldown_until=None,
        metadata={str(key): str(value) for key, value in dict(payload.get("metadata", {})).items()},
    )
    provider_id = profile_input.provider_id
    base_url = payload.get("base_url")
    default_model = payload.get("default_model")
    transport_id = payload.get("transport_id")
    auth_method = payload.get("auth_method")
    provider_kind = payload.get("provider_kind")
    extra_headers = payload.get("extra_headers")
    catalog = ProviderCatalog.with_defaults()
    provider_defaults = catalog.get(provider_id)
    if provider_id == "openai-compatible" and (base_url is None or default_model is None):
        raise ValueError("openai-compatible provider profiles require base_url and default_model")
    if any(value is not None for value in (base_url, default_model, transport_id, auth_method, provider_kind, extra_headers)):
        default_profile = None
        if provider_defaults is not None:
            default_profile = ProviderProfileFactory(catalog).from_provider_defaults(
                provider_id,
                profile_id=profile_input.profile_id,
                secret_references=profile_input.secret_references,
                priority=profile_input.priority,
                session_pin=profile_input.session_pin,
                cooldown_until=profile_input.cooldown_until,
                metadata=profile_input.metadata,
            )
        return profile_from_input(
            profile_input,
            base_url=(
                str(base_url)
                if base_url is not None
                else (default_profile.base_url if default_profile is not None else "")
            ),
            default_model=(
                str(default_model)
                if default_model is not None
                else (default_profile.default_model if default_profile is not None else "")
            ),
            transport_id=(
                str(transport_id)
                if transport_id is not None
                else (default_profile.transport_id if default_profile is not None else "openai-compatible")
            ),
            auth_method=(
                str(auth_method)
                if auth_method is not None
                else (default_profile.auth_method if default_profile is not None else "api_key")
            ),
            provider_kind=(
                str(provider_kind)
                if provider_kind is not None
                else (default_profile.provider_kind if default_profile is not None else "custom")
            ),
            extra_headers=(
                {
                    **(dict(default_profile.extra_headers) if default_profile is not None else {}),
                    **{str(key): str(value) for key, value in dict(extra_headers or {}).items()},
                }
            ),
        )
    factory = ProviderProfileFactory(catalog)
    return factory.from_provider_defaults(
        provider_id,
        profile_id=profile_input.profile_id,
        secret_references=profile_input.secret_references,
        priority=profile_input.priority,
        session_pin=profile_input.session_pin,
        cooldown_until=profile_input.cooldown_until,
        metadata=profile_input.metadata,
    )


def secret_reference_from_payload(payload: Mapping[str, Any]) -> SecretReference:
    return SecretReference(
        reference_id=str(payload["reference_id"]),
        provider_id=str(payload["provider_id"]),
        secret_name=str(payload["secret_name"]),
        secret_key=str(payload["secret_key"]),
        source=str(payload.get("source", "workspace")),
        metadata={str(key): str(value) for key, value in dict(payload.get("metadata", {})).items()},
    )


EMBEDDING_MODEL_ID = AEGIS_EMBED_MODEL_ID
EMBEDDING_MODEL_SOURCE_URL = AEGIS_EMBED_SOURCE_URL
EMBEDDING_MODEL_ROOT = embedding_model_root_path()
EMBEDDING_BOOTSTRAP_STATE_FILE = "embedding-bootstrap.json"
EMBEDDING_BOOTSTRAP_LOG_FILE = "embedding-bootstrap.log"
_ALLOWED_EMBEDDING_BOOTSTRAP_STATUSES = frozenset({"pending", "downloading", "failed", "ready", "skipped"})
_EMBEDDING_BOOTSTRAP_PIP_SPECS = (
    "sentence-transformers>=3,<4",
    "huggingface-hub>=0.30,<1",
)


@dataclass(frozen=True, slots=True)
class PersistedModelSelection:
    strong_profile: AuthProfile | None
    weak_profile: AuthProfile | None
    intent_mode: str = "skip"


@dataclass(frozen=True, slots=True)
class EmbeddingBootstrapState:
    status: str
    summary: str
    intent_mode: str
    updated_at: str
    failure_message: str | None = None
    background_pid: int | None = None
    model_id: str = EMBEDDING_MODEL_ID
    model_root: str = str(EMBEDDING_MODEL_ROOT)
    model_source_url: str = EMBEDDING_MODEL_SOURCE_URL


def _normalize_intent_mode(value: object) -> str:
    normalized = str(value or "skip").strip().lower() or "skip"
    return normalized if normalized in {"embedded", "skip"} else "skip"


def _normalize_embedding_bootstrap_status(value: object) -> str:
    normalized = str(value or "pending").strip().lower() or "pending"
    return normalized if normalized in _ALLOWED_EMBEDDING_BOOTSTRAP_STATUSES else "pending"


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _embedding_bootstrap_pid_from_payload(value: object) -> int | None:
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        return None
    return parsed if parsed > 0 else None


def _embedding_bootstrap_pid_is_active(pid: int | None) -> bool:
    if pid is None:
        return False
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    except OSError:
        return False
    return True


def embedding_bootstrap_state_path(state_dir: Path | None) -> Path | None:
    if state_dir is None:
        return None
    return state_dir / EMBEDDING_BOOTSTRAP_STATE_FILE


def embedding_bootstrap_log_path(state_dir: Path | None) -> Path | None:
    if state_dir is None:
        return None
    return state_dir / EMBEDDING_BOOTSTRAP_LOG_FILE


def _embedding_bootstrap_summary(
    *,
    intent_mode: str,
    status: str,
    failure_message: str | None = None,
) -> str:
    if intent_mode == "skip":
        return "intent_mode=skip keeps the local embedding path off the hot path."
    if status == "ready":
        return f"local embedding root is available at {EMBEDDING_MODEL_ROOT}"
    if status == "pending":
        return (
            "intent_mode=embedded requested the local embedding bootstrap; minimal "
            "sentence-transformers dependencies are being prepared in the background."
        )
    if status == "downloading":
        return (
            "intent_mode=embedded requested the local embedding bootstrap; background "
            f"model acquisition from {EMBEDDING_MODEL_SOURCE_URL} is in progress."
        )
    if status == "failed":
        detail = str(failure_message or "embedding bootstrap request failed").strip() or "embedding bootstrap request failed"
        return f"intent_mode=embedded is staying non-blocking after a bootstrap failure: {detail}"
    return (
        "intent_mode=embedded requested the local embedding bootstrap and is waiting "
        "for the background worker to report state."
    )


def embedding_bootstrap_state_from_payload(payload: Mapping[str, Any]) -> EmbeddingBootstrapState:
    status = _normalize_embedding_bootstrap_status(payload.get("status"))
    intent_mode = _normalize_intent_mode(payload.get("intent_mode"))
    failure_message = str(payload.get("failure_message") or "").strip() or None
    summary = str(payload.get("summary") or "").strip() or _embedding_bootstrap_summary(
        intent_mode=intent_mode,
        status=status,
        failure_message=failure_message,
    )
    updated_at = str(payload.get("updated_at") or "").strip() or _utc_now_iso()
    model_id = str(payload.get("model_id") or EMBEDDING_MODEL_ID).strip() or EMBEDDING_MODEL_ID
    model_root = str(payload.get("model_root") or EMBEDDING_MODEL_ROOT).strip() or str(EMBEDDING_MODEL_ROOT)
    model_source_url = (
        str(payload.get("model_source_url") or EMBEDDING_MODEL_SOURCE_URL).strip()
        or EMBEDDING_MODEL_SOURCE_URL
    )
    background_pid = _embedding_bootstrap_pid_from_payload(payload.get("background_pid"))
    return EmbeddingBootstrapState(
        status=status,
        summary=summary,
        intent_mode=intent_mode,
        updated_at=updated_at,
        failure_message=failure_message,
        background_pid=background_pid,
        model_id=model_id,
        model_root=model_root,
        model_source_url=model_source_url,
    )


def provider_selection_from_payload(payload: Mapping[str, Any]) -> PersistedModelSelection:
    strong_payload = payload.get("strong_profile")
    weak_payload = payload.get("weak_profile")
    if not isinstance(strong_payload, Mapping) or not isinstance(weak_payload, Mapping):
        raise ValueError("provider_profile must include strong_profile and weak_profile objects")
    raw_intent_mode = payload.get("intent_mode")
    if raw_intent_mode is None or not str(raw_intent_mode).strip():
        intent_mode = "skip"
    else:
        intent_mode = str(raw_intent_mode).strip().lower()
        if intent_mode not in {"embedded", "skip"}:
            raise ValueError("provider_profile intent_mode must be 'embedded' or 'skip'")
    return PersistedModelSelection(
        strong_profile=provider_profile_from_payload(strong_payload),
        weak_profile=provider_profile_from_payload(weak_payload),
        intent_mode=intent_mode,
    )


def load_provider_selection(profile_dir: Path) -> PersistedModelSelection:
    manifest_path = profile_dir / "profile.json"
    if not manifest_path.exists():
        return PersistedModelSelection(None, None)
    with manifest_path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise ValueError("profile.json must contain a JSON object")
    selection_payload = payload.get("model_selection")
    if not isinstance(selection_payload, dict):
        return PersistedModelSelection(None, None)
    return provider_selection_from_payload(selection_payload)


def load_provider_profile(profile_dir: Path) -> AuthProfile | None:
    return load_provider_selection(profile_dir).strong_profile


def load_embedding_bootstrap_state(state_dir: Path | None) -> EmbeddingBootstrapState | None:
    path = embedding_bootstrap_state_path(state_dir)
    if path is None or not path.exists():
        return None
    payload = _read_json_object(path)
    if payload is None:
        return None
    return embedding_bootstrap_state_from_payload(payload)


def persist_embedding_bootstrap_state(
    state_dir: Path | None,
    state: EmbeddingBootstrapState,
) -> EmbeddingBootstrapState:
    path = embedding_bootstrap_state_path(state_dir)
    if path is None:
        return state
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "status": state.status,
        "summary": state.summary,
        "intent_mode": state.intent_mode,
        "updated_at": state.updated_at,
        "failure_message": state.failure_message,
        "background_pid": state.background_pid,
        "model_id": state.model_id,
        "model_root": state.model_root,
        "model_source_url": state.model_source_url,
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return state


def _embedding_bootstrap_worker_command(state_dir: Path) -> tuple[str, ...]:
    return (
        sys.executable,
        "-c",
        (
            "import sys; "
            "from apps.provider_runtime_support import run_embedding_bootstrap_worker as _worker; "
            "raise SystemExit(_worker(sys.argv[1]))"
        ),
        str(state_dir),
    )


def _spawn_embedding_bootstrap_worker(
    state_dir: Path,
    state: EmbeddingBootstrapState,
) -> EmbeddingBootstrapState:
    log_path = embedding_bootstrap_log_path(state_dir)
    if log_path is None:
        return state
    log_path.parent.mkdir(parents=True, exist_ok=True)
    command = _embedding_bootstrap_worker_command(state_dir)
    with log_path.open("ab") as log_stream:
        process = subprocess.Popen(
            list(command),
            stdin=subprocess.DEVNULL,
            stdout=log_stream,
            stderr=subprocess.STDOUT,
            start_new_session=True,
        )
    return EmbeddingBootstrapState(
        status=state.status,
        summary=state.summary,
        intent_mode=state.intent_mode,
        updated_at=_utc_now_iso(),
        failure_message=state.failure_message,
        background_pid=process.pid,
        model_id=state.model_id,
        model_root=state.model_root,
        model_source_url=state.model_source_url,
    )


def _embedding_bootstrap_state_for_runtime(
    *,
    status: str,
    failure_message: str | None = None,
    updated_at: str | None = None,
    background_pid: int | None = None,
) -> EmbeddingBootstrapState:
    return EmbeddingBootstrapState(
        status=status,
        summary=_embedding_bootstrap_summary(
            intent_mode="embedded",
            status=status,
            failure_message=failure_message,
        ),
        intent_mode="embedded",
        updated_at=updated_at or _utc_now_iso(),
        failure_message=failure_message,
        background_pid=background_pid,
    )


def resolve_embedding_bootstrap_state(
    state_dir: Path | None,
    *,
    intent_mode: str,
) -> EmbeddingBootstrapState:
    normalized_intent_mode = _normalize_intent_mode(intent_mode)
    stored = load_embedding_bootstrap_state(state_dir)
    if normalized_intent_mode == "skip":
        updated_at = (
            stored.updated_at
            if stored is not None and stored.intent_mode == "skip"
            else _utc_now_iso()
        )
        return EmbeddingBootstrapState(
            status="skipped",
            summary=_embedding_bootstrap_summary(intent_mode="skip", status="skipped"),
            intent_mode="skip",
            updated_at=updated_at,
            background_pid=None,
        )
    if embedding_root_is_healthy(str(EMBEDDING_MODEL_ROOT)):
        updated_at = (
            stored.updated_at
            if stored is not None and stored.intent_mode == "embedded" and stored.status == "ready"
            else _utc_now_iso()
        )
        return _embedding_bootstrap_state_for_runtime(status="ready", updated_at=updated_at)
    if stored is not None and stored.intent_mode == "embedded" and stored.status == "failed":
        return stored
    active_pid = None
    if stored is not None and stored.intent_mode == "embedded":
        active_pid = stored.background_pid if _embedding_bootstrap_pid_is_active(stored.background_pid) else None
        if stored.status in {"pending", "downloading"} and active_pid is not None:
            return _embedding_bootstrap_state_for_runtime(
                status=stored.status,
                updated_at=stored.updated_at,
                background_pid=active_pid,
            )
    status = "downloading" if sentence_transformers_dependencies_ready() else "pending"
    return _embedding_bootstrap_state_for_runtime(status=status, background_pid=active_pid)


def run_embedding_bootstrap_worker(state_dir_arg: str) -> int:
    state_dir = Path(state_dir_arg).expanduser()
    current_pid = os.getpid()
    try:
        if embedding_root_is_healthy(str(EMBEDDING_MODEL_ROOT)):
            persist_embedding_bootstrap_state(
                state_dir,
                _embedding_bootstrap_state_for_runtime(status="ready", background_pid=None),
            )
            return 0
        if not sentence_transformers_dependencies_ready():
            persist_embedding_bootstrap_state(
                state_dir,
                _embedding_bootstrap_state_for_runtime(status="pending", background_pid=current_pid),
            )
            subprocess.check_call(
                [
                    sys.executable,
                    "-m",
                    "pip",
                    "install",
                    "--disable-pip-version-check",
                    *(_EMBEDDING_BOOTSTRAP_PIP_SPECS),
                ]
            )
        persist_embedding_bootstrap_state(
            state_dir,
            _embedding_bootstrap_state_for_runtime(status="downloading", background_pid=current_pid),
        )
        from huggingface_hub import snapshot_download

        EMBEDDING_MODEL_ROOT.parent.mkdir(parents=True, exist_ok=True)
        snapshot_download(
            repo_id=EMBEDDING_MODEL_ID,
            local_dir=str(EMBEDDING_MODEL_ROOT),
        )
        if not embedding_root_is_healthy(str(EMBEDDING_MODEL_ROOT)):
            raise RuntimeError(f"downloaded embedding root at {EMBEDDING_MODEL_ROOT} is missing sentence-transformers markers")
        persist_embedding_bootstrap_state(
            state_dir,
            _embedding_bootstrap_state_for_runtime(status="ready", background_pid=None),
        )
        return 0
    except Exception as error:
        failure_message = str(error).strip() or error.__class__.__name__
        persist_embedding_bootstrap_state(
            state_dir,
            _embedding_bootstrap_state_for_runtime(
                status="failed",
                failure_message=failure_message,
                background_pid=None,
            ),
        )
        return 1


def trigger_embedding_bootstrap(
    state_dir: Path | None,
    *,
    intent_mode: str,
) -> EmbeddingBootstrapState:
    state = resolve_embedding_bootstrap_state(state_dir, intent_mode=intent_mode)
    if state_dir is None:
        return state
    resolved_state_dir = Path(state_dir)
    if state.status in {"skipped", "ready", "failed"}:
        return persist_embedding_bootstrap_state(resolved_state_dir, state)
    if _embedding_bootstrap_pid_is_active(state.background_pid):
        return persist_embedding_bootstrap_state(resolved_state_dir, state)
    try:
        started = _spawn_embedding_bootstrap_worker(resolved_state_dir, state)
    except OSError as error:
        failure_message = str(error).strip() or error.__class__.__name__
        started = _embedding_bootstrap_state_for_runtime(
            status="failed",
            failure_message=failure_message,
            background_pid=None,
        )
    return persist_embedding_bootstrap_state(resolved_state_dir, started)


RUNTIME_LOCAL_SECRET_ENV_FILE = "runtime-local-secrets.json"


def runtime_local_secret_env_path(state_dir: Path) -> Path:
    return state_dir / RUNTIME_LOCAL_SECRET_ENV_FILE


def load_runtime_local_secret_env(state_dir: Path | None) -> dict[str, str]:
    if state_dir is None:
        return {}
    path = runtime_local_secret_env_path(state_dir)
    if not path.exists():
        return {}
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, Mapping):
        raise ValueError(f"{path} must contain a JSON object")
    resolved: dict[str, str] = {}
    for key, value in payload.items():
        text = str(value).strip()
        if text:
            resolved[str(key)] = text
    return resolved


def persist_runtime_local_secret_env(
    state_dir: Path | None,
    updates: Mapping[str, str],
) -> Path | None:
    if state_dir is None:
        return None
    filtered = {str(key): str(value).strip() for key, value in updates.items() if str(value).strip()}
    if not filtered:
        return None
    state_dir.mkdir(parents=True, exist_ok=True)
    path = runtime_local_secret_env_path(state_dir)
    payload = load_runtime_local_secret_env(state_dir)
    payload.update(filtered)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    try:
        os.chmod(path, 0o600)
    except OSError:
        pass
    return path


def capture_runtime_secret_env(
    state_dir: Path | None,
    profile: AuthProfile | None,
    *,
    environ: Mapping[str, str] | None = None,
) -> Path | None:
    if profile is None:
        return None
    source = os.environ if environ is None else environ
    updates: dict[str, str] = {}
    for reference in profile.secret_references:
        for env_var in reference.env_var_candidates():
            value = str(source.get(env_var) or "").strip()
            if value:
                updates[env_var] = value
    return persist_runtime_local_secret_env(state_dir, updates)


def build_runtime_secret_environ(
    state_dir: Path | None,
    *,
    environ: Mapping[str, str] | None = None,
) -> dict[str, str]:
    resolved = load_runtime_local_secret_env(state_dir)
    source = os.environ if environ is None else environ
    resolved.update({str(key): str(value) for key, value in source.items()})
    return resolved


def strong_model_profile_from_auth_profile(profile: AuthProfile) -> StrongModelProfile:
    if not str(profile.default_model or "").strip():
        raise ValueError(f"auth profile '{profile.profile_id}' is missing a strong model id")
    return StrongModelProfile(
        profile_id=profile.profile_id,
        provider_id=profile.provider_id,
        model_id=str(profile.default_model),
        base_url=profile.base_url,
        transport_id=profile.transport_id,
        reasoning_effort=str(profile.metadata.get("reasoning_effort", "")).strip() or None,
        metadata=dict(profile.metadata),
    )


def weak_model_profile_from_auth_profile(profile: AuthProfile) -> WeakModelProfile:
    if not str(profile.default_model or "").strip():
        raise ValueError(f"auth profile '{profile.profile_id}' is missing a weak model id")
    return WeakModelProfile(
        profile_id=profile.profile_id,
        provider_id=profile.provider_id,
        model_id=str(profile.default_model),
        base_url=profile.base_url,
        transport_id=profile.transport_id,
        reasoning_effort=str(profile.metadata.get("reasoning_effort", "")).strip() or None,
        metadata=dict(profile.metadata),
    )


def mixture_model_selection_from_auth_profiles(
    *,
    strong_profile: AuthProfile,
    weak_profile: AuthProfile,
    intent_mode: str,
) -> MixtureModelSelection:
    return MixtureModelSelection(
        strong_model=strong_model_profile_from_auth_profile(strong_profile),
        weak_model=weak_model_profile_from_auth_profile(weak_profile),
        intent_mode=intent_mode,
    )


def provider_profile_summary(profile: AuthProfile) -> dict[str, Any]:
    context_window_tokens = _coerce_reasonable_int(profile.metadata.get("context_window_tokens"))
    return {
        "profile_id": profile.profile_id,
        "provider_id": profile.provider_id,
        "transport_id": profile.transport_id,
        "base_url": profile.base_url,
        "default_model": profile.default_model,
        "auth_method": profile.auth_method,
        "provider_kind": profile.provider_kind,
        "extra_headers": dict(profile.extra_headers),
        "secret_reference_ids": tuple(reference.reference_id for reference in profile.secret_references),
        "context_window_tokens": context_window_tokens,
        "context_window_mode": str(profile.metadata.get("context_window_mode", "auto")),
        "reasoning_effort": str(profile.metadata.get("reasoning_effort", "")).strip() or None,
        "source": "configured",
    }


def provider_fallback_summary() -> dict[str, Any]:
    return {
        "profile_id": "",
        "provider_id": "preview",
        "transport_id": "preview",
        "base_url": None,
        "default_model": None,
        "auth_method": "preview",
        "provider_kind": "preview",
        "extra_headers": {},
        "secret_reference_ids": (),
        "context_window_tokens": None,
        "context_window_mode": "unset",
        "reasoning_effort": None,
        "source": "preview-fallback",
    }


def _normalize_env_name(candidate: str) -> str:
    return candidate.strip().replace("-", "_").replace(".", "_").upper()


class EnvironmentSecretStore(SecretStore):
    def __init__(self, environ: Mapping[str, str] | None = None) -> None:
        self.environ = environ

    def resolve(self, reference: SecretReference) -> SecretValueResolution:
        env = self.environ or os.environ
        candidates: list[str] = list(reference.env_var_candidates())
        seen = set(candidates)
        for candidate in (reference.secret_name, reference.secret_key, reference.reference_id):
            normalized = _normalize_env_name(candidate)
            if normalized and normalized not in seen:
                seen.add(normalized)
                candidates.append(normalized)
        for candidate in candidates:
            value = env.get(candidate)
            if value is not None:
                return SecretValueResolution(value=value, source=f"env:{candidate}")
        raise LookupError(f"missing environment secret for reference: {reference.reference_id}")

    def read(self, reference: SecretReference) -> str:
        return self.resolve(reference).value


class EncryptedRepositorySecretStore(SecretStore):
    def __init__(
        self,
        repository: RuntimeStorageRepository,
        *,
        cipher: LocalEncryptedSecretCipher,
    ) -> None:
        self.repository = repository
        self.cipher = cipher

    def resolve(self, reference: SecretReference) -> SecretValueResolution:
        stored = self.repository.load_auth_secret_value(reference.reference_id)
        if stored is not None:
            return SecretValueResolution(
                value=self.cipher.decrypt(stored),
                source="encrypted-local-store",
            )
        for env_name in reference.env_var_candidates():
            value = os.environ.get(env_name)
            if value is not None:
                if reference.provider_id.strip().lower() == "copilot" and value.strip().startswith("ghp_"):
                    continue
                return SecretValueResolution(value=value, source=f"env:{env_name}")
        external = self._external_resolution(reference)
        if external is not None:
            return external
        raise LookupError(f"missing stored secret for reference: {reference.reference_id}")

    def read(self, reference: SecretReference) -> str:
        return self.resolve(reference).value

    def _external_resolution(self, reference: SecretReference) -> SecretValueResolution | None:
        provider_id = reference.provider_id.strip().lower()
        if provider_id == "anthropic":
            return _read_anthropic_oauth_resolution()
        if provider_id == "claude-code":
            return _read_claude_code_oauth_resolution()
        if provider_id == "openai-codex":
            return _read_codex_cli_resolution() or _read_hermes_codex_resolution()
        if provider_id == "google-gemini-cli":
            return _read_google_gemini_oauth_resolution()
        if provider_id == "qwen-oauth":
            return _read_qwen_oauth_resolution()
        if provider_id == "copilot":
            return _read_copilot_resolution()
        return None



def register_provider_profile(
    repository: RuntimeStorageRepository,
    payload: Mapping[str, Any],
) -> AuthProfile:
    profile = provider_profile_from_payload(payload)
    PersistentAuthProfileStore(repository).register(profile)
    return profile


def _heuristic_context_window(model_id: str) -> int | None:
    normalized = model_id.casefold()
    heuristics = (
        ("gpt-5.4-nano", 400_000),
        ("gpt-5.4-mini", 400_000),
        ("gpt-5.4", 1_050_000),
        ("gpt-5.3-codex-spark", 128_000),
        ("gpt-5.1-chat", 128_000),
        ("gpt-5", 400_000),
        ("gpt-4.1", 1_047_576),
        ("gpt-4o", 128_000),
        ("claude", 200_000),
        ("gemini", 1_048_576),
        ("minimax", 204_800),
        ("mimo-v2-pro", 1_000_000),
        ("mimo-v2-omni", 256_000),
        ("mimo-v2-flash", 256_000),
        ("xiaomi", 256_000),
        ("qwen3-coder-plus", 1_000_000),
        ("qwen3-coder", 262_144),
        ("llama", 131_072),
        ("qwen", 131_072),
        ("deepseek", 128_000),
        ("kimi", 262_144),
    )
    for prefix, size in sorted(heuristics, key=lambda item: len(item[0]), reverse=True):
        if prefix in normalized:
            return size
    return DEFAULT_CONTEXT_WINDOW_TOKENS


__all__ = [name for name in globals() if not name.startswith("__")]
