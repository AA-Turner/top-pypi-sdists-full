"""Plan and validate the LangChain provider configuration used by setup.

The setup planner is intentionally separate from the repository mutation
callback.  It reads configuration, resolves a non-secret model choice, and
validates the exact provider/workflow path used by the review runner before
``apply_provider_configuration`` writes anything.
"""

from __future__ import annotations

import asyncio
import copy
import inspect
import os
import re
from collections.abc import Awaitable, Callable, Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any, cast
from urllib.parse import parse_qsl, urlencode, urlparse

import yaml

from agentic_devtools.orchestration.llm.config import load_config
from agentic_devtools.orchestration.llm.config_schema import validate_config
from agentic_devtools.orchestration.llm.errors import DuplicateNodeMappingError
from agentic_devtools.orchestration.llm.factory import ProviderFactory

PROVIDER_CONFIG_RELATIVE_PATH = Path(".agdt/config/llm-providers.yml")
COPILOT_PROVIDER_ID = "copilot_pr_review"
COPILOT_PROVIDER_TYPE = "copilot"
PR_REVIEW_WORKFLOW = "pr_review"
REVIEW_FILES_NODE = "review_files"
TEMPLATE_VERSION = "1"
_TEMPLATE_NAME = "llm-providers.copilot.yml"

ProviderReadiness = Callable[
    [dict[str, Any]],
    tuple[str, str] | str | None | Awaitable[tuple[str, str] | str | None],
]


@dataclass(frozen=True)
class ProviderConfigurationPlan:
    """A side-effect-free provider configuration decision."""

    path: Path
    status: str
    document: dict[str, Any] | None
    rendered: str | None
    provider_id: str | None
    provider_type: str | None
    model: str | None
    model_source: str | None
    mappings: tuple[str, ...]
    auth_status: str
    credential_status: str
    source: str
    reason: str
    dry_run: bool
    reconfigure: bool
    template_version: str | None = TEMPLATE_VERSION

    def report_details(self) -> dict[str, Any]:
        """Return the stable, sanitized setup-report representation."""
        return {
            "status": self.status,
            "path": str(self.path),
            "provider_id": self.provider_id,
            "provider_type": self.provider_type,
            "model": self.model,
            "model_source": self.model_source,
            "mappings": list(self.mappings),
            "auth_status": self.auth_status,
            "credential_status": self.credential_status,
            "source": self.source,
            "reason": self.reason,
            "dry_run": self.dry_run,
            "reconfigure": self.reconfigure,
            "template_version": self.template_version,
        }


@dataclass(frozen=True)
class ProviderConfigurationCheck:
    """Sanitized readiness result for ``agdt-setup-check``."""

    found: bool
    valid: bool
    reason: str
    provider_id: str | None
    provider_type: str | None
    model: str | None
    auth_status: str
    credential_status: str
    path: Path

    def report_details(self) -> dict[str, Any]:
        """Return check details without configuration contents or credentials."""
        return {
            "status": "preserved" if self.valid else "failed",
            "path": str(self.path),
            "provider_id": self.provider_id,
            "provider_type": self.provider_type,
            "model": self.model,
            "model_source": None,
            "mappings": list(_MAPPINGS),
            "auth_status": self.auth_status,
            "credential_status": self.credential_status,
            "source": "existing" if self.found else "none",
            "reason": self.reason,
            "dry_run": False,
            "reconfigure": False,
            "template_version": None,
        }


_MAPPINGS = (
    "pr_review.default_provider",
    "pr_review.nodes.review_files",
)
_SAFE_ENV_REFERENCE_KEYS = frozenset(
    {
        "api_key_env",
        "api_key_env_var",
        "api_key_environment_variable",
        "token_env",
        "token_env_var",
        "token_environment_variable",
    }
)
_SECRET_KEY_ALIASES = {
    "accesskey": "access_key",
    "accesstoken": "access_token",
    "accountkey": "account_key",
    "apikey": "api_key",
    "apisecret": "api_secret",
    "bearertoken": "bearer_token",
    "clientsecret": "client_secret",
    "idtoken": "id_token",
    "pass_phrase": "password",
    "passphrase": "password",
    "passwd": "password",
    "privatekey": "private_key",
    "pwd": "password",
    "refreshtoken": "refresh_token",
    "secretkey": "secret_key",
    "sessionkey": "session_key",
    "signingkey": "signing_key",
    "subscriptionkey": "subscription_key",
}
_COMPACT_ENV_SUFFIXES = (
    ("environmentvariable", "environment_variable"),
    ("envvar", "env_var"),
    ("env", "env"),
)
_COMPACT_SECRET_SUFFIXES = (
    "credentials",
    "credential",
    "connectionstring",
    "signature",
    "password",
    "passphrase",
    "passwd",
    "secret",
    "token",
    "pat",
    "pwd",
    "sig",
)
_COMPACT_KEY_SUFFIXES = ("keys", "key")
_SECRET_COMPONENTS = {
    "auth",
    "cookie",
    "cookies",
    "token",
    "secret",
    "password",
    "credential",
    "credentials",
    "pat",
    "sig",
    "signature",
    "key",
    "keys",
}


def _is_secret_container_key(key: Any) -> bool:
    normalized = _normalize_secret_key(key)
    components = [component for component in re.split(r"[^a-z0-9]+", normalized) if component]
    compact = "".join(components)
    has_header_component = "header" in components or "headers" in components
    has_header_suffix = compact.endswith("header") or compact.endswith("headers")
    return has_header_component or has_header_suffix


def resolve_template_path() -> Path | None:
    """Resolve the checked-out template, then the installed-package resource."""
    module_path = Path(__file__).resolve()
    checkout = module_path.parents[3] / "agentic_devtools" / "resources" / "setup-templates" / _TEMPLATE_NAME
    if checkout.exists():
        return checkout
    packaged = module_path.parents[2] / "resources" / "setup-templates" / _TEMPLATE_NAME
    if packaged.exists():
        return packaged
    return None


def load_provider_template() -> dict[str, Any]:
    """Load and validate the packaged Copilot setup template."""
    path = resolve_template_path()
    if path is None:
        raise FileNotFoundError("provider template is not installed")
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("provider template root must be a mapping")
    errors = validate_config(raw)
    if errors:
        raise ValueError("provider template validation failed")
    return raw


def render_provider_config(document: Mapping[str, Any]) -> str:
    """Render a provider document deterministically."""
    return yaml.safe_dump(dict(document), sort_keys=False, default_flow_style=False)


def redact_provider_config_rendering(rendered: str) -> str:
    """Redact secret-like keys before provider configuration is displayed."""
    document = yaml.safe_load(rendered)

    def redact_url_userinfo(value: str) -> str:
        try:
            parsed = urlparse(value)
        except ValueError:
            return "<redacted>"
        if not parsed.netloc and "@" in value:
            try:
                malformed_userinfo = urlparse(f"//{value}")
            except ValueError:
                return "<redacted>"
            if malformed_userinfo.netloc and "@" in malformed_userinfo.netloc:
                return "<redacted>"
        query = parsed.query
        if query:
            query_pairs = parse_qsl(query, keep_blank_values=True)
            redacted_pairs = []
            for key, item in query_pairs:
                normalized = _normalize_secret_key(key)
                if normalized in _SAFE_ENV_REFERENCE_KEYS:
                    redacted_pairs.append((key, "<redacted>"))
                    continue
                redacted_pairs.append((key, "<redacted>" if _is_secret_key(key) else item))
            if redacted_pairs != query_pairs:
                query = urlencode(redacted_pairs, doseq=True)
        fragment = "<redacted>" if parsed.fragment else ""
        netloc = f"******@{parsed.netloc.rsplit('@', 1)[1]}" if "@" in parsed.netloc else parsed.netloc
        if netloc == parsed.netloc and query == parsed.query and not fragment:
            return value
        return parsed._replace(netloc=netloc, query=query, fragment=fragment).geturl()

    def redact(value: Any, *, force_redaction: bool = False) -> Any:
        if isinstance(value, dict):
            redacted: dict[Any, Any] = {}
            for key, item in value.items():
                if force_redaction:
                    redacted[key] = redact(item, force_redaction=True)
                    continue
                normalized = _normalize_secret_key(key)
                if normalized in _SAFE_ENV_REFERENCE_KEYS:
                    redacted[key] = "<redacted>"
                    continue
                if _is_secret_key(key):
                    redacted[key] = "<redacted>"
                    continue
                if _is_secret_container_key(key):
                    redacted[key] = redact(item, force_redaction=True)
                    continue
                redacted[key] = redact(item)
            return redacted
        if isinstance(value, list):
            return [redact(item, force_redaction=force_redaction) for item in value]
        if force_redaction:
            return "<redacted>"
        if isinstance(value, str):
            return redact_url_userinfo(value)
        return value

    return yaml.safe_dump(redact(document), sort_keys=False, default_flow_style=False)


def _normalize_secret_key(key: Any) -> str:
    raw_key = str(key)
    normalized = raw_key.replace("-", "_")
    normalized = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", normalized)
    normalized = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", normalized)
    normalized = normalized.lower()
    normalized = _SECRET_KEY_ALIASES.get(normalized, normalized)
    for compact_suffix, canonical_suffix in _COMPACT_ENV_SUFFIXES:
        if normalized.endswith(f"_{canonical_suffix}") or not normalized.endswith(compact_suffix):
            continue
        stem = normalized[: -len(compact_suffix)].rstrip("_")
        if not stem:
            continue
        stem = _SECRET_KEY_ALIASES.get(stem, stem)
        if "_" in stem or stem in {"authorization", "password"} or stem in _SECRET_COMPONENTS:
            return f"{stem}_{canonical_suffix}"
        for secret_suffix in (*_COMPACT_SECRET_SUFFIXES, *_COMPACT_KEY_SUFFIXES):
            if stem == secret_suffix:
                return f"{stem}_{canonical_suffix}"
            if stem.endswith(secret_suffix):
                return f"{stem[: -len(secret_suffix)]}_{secret_suffix}_{canonical_suffix}"
    return normalized


def _is_secret_key(key: Any) -> bool:
    raw_key = str(key)
    normalized = _normalize_secret_key(raw_key)
    if normalized in _SAFE_ENV_REFERENCE_KEYS:
        return False
    components = [component for component in re.split(r"[^a-z0-9]+", normalized) if component]
    compact = "".join(components)
    compact_key_compound = any(compact.endswith(suffix) and compact != suffix for suffix in _COMPACT_KEY_SUFFIXES)
    return (
        any(component in _SECRET_COMPONENTS for component in components)
        or any(compact.endswith(suffix) for suffix in _COMPACT_SECRET_SUFFIXES)
        or compact_key_compound
        or normalized in _SECRET_COMPONENTS
        or ("api" in components and any(key_component in components for key_component in {"key", "keys"}))
        or "authorization" in components
        or ("private" in components and any(key_component in components for key_component in {"key", "keys"}))
    )


def _credential_status_for_reason(provider_type: str | None, reason: str | None, *, default: str) -> str:
    if provider_type == COPILOT_PROVIDER_TYPE:
        return "not_required"
    if reason in {"credential_missing", "credential_reference_missing"}:
        return "missing"
    return default


def _parse_document(path: Path) -> tuple[dict[str, Any] | None, str | None]:
    try:
        if not path.exists():
            return None, None
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, yaml.YAMLError):
        return None, "invalid_yaml"
    if not isinstance(raw, dict):
        return None, "invalid_root"
    return raw, None


def _provider_fields(document: Mapping[str, Any]) -> tuple[str | None, str | None, str | None]:
    providers = document.get("providers")
    if not isinstance(providers, Mapping):
        return None, None, None
    provider = providers.get(COPILOT_PROVIDER_ID)
    if not isinstance(provider, Mapping):
        provider_id = next((key for key in providers if isinstance(key, str)), None)
        provider = providers.get(provider_id) if provider_id else None
        if not isinstance(provider, Mapping):
            return None, None, None
        provider_type = provider.get("type")
        model = provider.get("model")
        return (
            provider_id,
            provider_type if isinstance(provider_type, str) else None,
            model.strip() if isinstance(model, str) and model.strip() else None,
        )
    provider_type = provider.get("type")
    model = provider.get("model")
    return (
        COPILOT_PROVIDER_ID,
        provider_type if isinstance(provider_type, str) else None,
        model.strip() if isinstance(model, str) and model.strip() else None,
    )


def _resolve_review_provider(document: Mapping[str, Any]) -> tuple[str | None, str | None, Mapping[str, Any] | None]:
    error, default_provider_id, _default_provider, review_provider_id, review_provider = _resolve_review_providers(
        document
    )
    if review_provider_id is None and review_provider is None:
        return error, default_provider_id, None
    return error, review_provider_id, review_provider


def _resolve_review_providers(
    document: Mapping[str, Any],
) -> tuple[str | None, str | None, Mapping[str, Any] | None, str | None, Mapping[str, Any] | None]:
    workflows = document.get("workflows")
    review = workflows.get(PR_REVIEW_WORKFLOW) if isinstance(workflows, Mapping) else None
    if not isinstance(review, Mapping):
        return "workflow_mapping_missing", None, None, None, None
    default_provider_id = review.get("default_provider")
    if not isinstance(default_provider_id, str) or not default_provider_id.strip():
        return "default_provider_missing", None, None, None, None
    default_provider_id = default_provider_id.strip()
    providers = document.get("providers")
    default_provider = providers.get(default_provider_id) if isinstance(providers, Mapping) else None
    if not isinstance(default_provider, Mapping):
        return "provider_missing", default_provider_id, None, None, None
    nodes = review.get("nodes")
    node = nodes.get(REVIEW_FILES_NODE) if isinstance(nodes, Mapping) else None
    if not isinstance(node, Mapping):
        return "review_files_mapping_missing", default_provider_id, default_provider, None, None
    provider_id = node.get("provider")
    if not isinstance(provider_id, str) or not provider_id.strip():
        return "review_files_mapping_missing", default_provider_id, default_provider, None, None
    provider_id = provider_id.strip()
    provider = providers.get(provider_id) if isinstance(providers, Mapping) else None
    if not isinstance(provider, Mapping):
        return "provider_missing", default_provider_id, default_provider, provider_id, None
    return None, default_provider_id, default_provider, provider_id, provider


def _provider_details(
    provider_id: str | None, provider: Mapping[str, Any] | None
) -> tuple[str | None, str | None, str | None]:
    provider_type = provider.get("type") if isinstance(provider, Mapping) else None
    model = provider.get("model") if isinstance(provider, Mapping) else None
    return (
        provider_id if isinstance(provider_id, str) else None,
        provider_type if isinstance(provider_type, str) else None,
        model.strip() if isinstance(model, str) and model.strip() else None,
    )


def _validate_provider_mapping(provider: Mapping[str, Any] | None) -> str | None:
    provider_type = provider.get("type") if isinstance(provider, Mapping) else None
    model = provider.get("model") if isinstance(provider, Mapping) else None
    if not isinstance(provider, Mapping):
        return "provider_missing"
    if provider_type not in {"azure_openai", "openai_direct", "local_model", "copilot"}:
        return "provider_type_invalid"
    if not isinstance(model, str) or not model.strip():
        return "model_missing"
    if provider_type == COPILOT_PROVIDER_TYPE and "api_key_env" in provider:
        return "copilot_api_key_env_forbidden"
    if provider_type in {"azure_openai", "openai_direct"}:
        env_name = provider.get("api_key_env")
        if not isinstance(env_name, str) or not env_name.strip():
            return "credential_reference_missing"
        if not os.environ.get(env_name):
            return "credential_missing"
    if provider_type == "azure_openai":
        endpoint = provider.get("endpoint")
        if not isinstance(endpoint, str) or not endpoint.strip():
            return "endpoint_missing"
    elif provider_type == "local_model":
        endpoint = provider.get("endpoint")
        if endpoint is None:
            return None
        if not isinstance(endpoint, str) or not endpoint.strip():
            return "endpoint_invalid"
    else:
        endpoint = None
    if isinstance(endpoint, str):
        try:
            parsed_endpoint = urlparse(endpoint)
        except ValueError:
            return "endpoint_invalid"
        if parsed_endpoint.scheme.lower() not in {"http", "https"} or not parsed_endpoint.netloc:
            return "endpoint_invalid"
        if any(character.isspace() for character in parsed_endpoint.netloc):
            return "endpoint_invalid"
        if "@" in parsed_endpoint.netloc:
            return "endpoint_invalid"
        if not parsed_endpoint.hostname:
            return "endpoint_invalid"
        if any(character.isspace() for character in parsed_endpoint.hostname):
            return "endpoint_invalid"
        try:
            parsed_endpoint.port
        except ValueError:
            return "endpoint_invalid"
    return None


def _readiness_override_for_providers(
    readiness: ProviderReadiness | None,
    *,
    skip_model_refresh: bool,
    provider_types: tuple[str | None, ...],
) -> ProviderReadiness | None:
    if readiness is None:
        return None
    if not skip_model_refresh or any(provider_type == COPILOT_PROVIDER_TYPE for provider_type in provider_types):
        return readiness
    return None


def _document_for_provider_preflight(
    document: Mapping[str, Any], provider_id: str, *, drop_node_model: bool = False
) -> dict[str, Any]:
    preflight_document = copy.deepcopy(dict(document))
    workflows = preflight_document.setdefault("workflows", {})
    if not isinstance(workflows, dict):
        raise ValueError("workflow_mapping_invalid")
    review = workflows.setdefault(PR_REVIEW_WORKFLOW, {})
    if not isinstance(review, dict):
        raise ValueError("workflow_mapping_invalid")
    review["default_provider"] = provider_id
    nodes = review.setdefault("nodes", {})
    if not isinstance(nodes, dict):
        raise ValueError("workflow_mapping_invalid")
    node = nodes.setdefault(REVIEW_FILES_NODE, {})
    if not isinstance(node, dict):
        raise ValueError("review_files_mapping_invalid")
    node["provider"] = provider_id
    if drop_node_model:
        node.pop("model", None)
    return preflight_document


def _run_review_provider_readiness(
    document: Mapping[str, Any],
    *,
    default_provider_id: str,
    review_provider_id: str,
    readiness: ProviderReadiness | None,
    skip_model_refresh: bool = False,
    default_provider_type: str | None = None,
    review_provider_type: str | None = None,
) -> tuple[str, str, str, str | None]:
    def _effective_preflight_model(
        candidate: Mapping[str, Any], provider_id: str, *, include_node_model: bool = True
    ) -> str | None:
        providers = candidate.get("providers")
        provider = providers.get(provider_id) if isinstance(providers, Mapping) else None
        provider_model = provider.get("model") if isinstance(provider, Mapping) else None
        workflows = candidate.get("workflows")
        review = workflows.get(PR_REVIEW_WORKFLOW) if isinstance(workflows, Mapping) else None
        workflow_model = review.get("model") if isinstance(review, Mapping) else None
        nodes = review.get("nodes") if isinstance(review, Mapping) else None
        node = nodes.get(REVIEW_FILES_NODE) if isinstance(nodes, Mapping) else None
        node_model = node.get("model") if isinstance(node, Mapping) else None
        normalized_node_model = node_model.strip() if isinstance(node_model, str) and node_model.strip() else None
        normalized_workflow_model = (
            workflow_model.strip() if isinstance(workflow_model, str) and workflow_model.strip() else None
        )
        if include_node_model and normalized_node_model is not None:
            return normalized_node_model
        if normalized_workflow_model is not None:
            return normalized_workflow_model
        return provider_model.strip() if isinstance(provider_model, str) and provider_model.strip() else None

    same_provider_distinct_model = False
    if review_provider_id == default_provider_id:
        default_effective_model = _effective_preflight_model(document, default_provider_id, include_node_model=False)
        review_effective_model = _effective_preflight_model(document, review_provider_id)
        same_provider_distinct_model = bool(
            default_effective_model and review_effective_model and default_effective_model != review_effective_model
        )
    needs_review_preflight = review_provider_id != default_provider_id or same_provider_distinct_model
    default_readiness = _readiness_override_for_providers(
        readiness,
        skip_model_refresh=skip_model_refresh,
        provider_types=(default_provider_type,),
    )
    default_document = _document_for_provider_preflight(
        document,
        default_provider_id,
        drop_node_model=needs_review_preflight,
    )
    auth_status, reason = _run_readiness(default_document, default_readiness)
    default_model = _effective_preflight_model(default_document, default_provider_id)
    if auth_status != "ready":
        return auth_status, reason, default_provider_id, default_model
    if not needs_review_preflight:
        return auth_status, reason, review_provider_id, default_model
    review_readiness = _readiness_override_for_providers(
        readiness,
        skip_model_refresh=skip_model_refresh,
        provider_types=(review_provider_type,),
    )
    review_document = _document_for_provider_preflight(document, review_provider_id)
    auth_status, reason = _run_readiness(review_document, review_readiness)
    return auth_status, reason, review_provider_id, _effective_preflight_model(review_document, review_provider_id)


def _run_readiness(document: dict[str, Any], readiness: ProviderReadiness | None) -> tuple[str, str]:
    if readiness is not None:
        result = readiness(document)
        if inspect.isawaitable(result):
            result = asyncio.run(cast(Any, result))
        if isinstance(result, tuple):
            return result
        return ("ready", result or "ready")
    try:
        factory = ProviderFactory(config=load_config(config_dict=document))
        preflight = factory.preflight(REVIEW_FILES_NODE, PR_REVIEW_WORKFLOW)
        if inspect.isawaitable(preflight):
            asyncio.run(preflight)
        return "ready", "ready"
    except Exception as exc:  # noqa: BLE001
        name = type(exc).__name__
        if name in {"AuthenticationError", "CopilotAuthenticationError"}:
            return "unavailable", "authentication_unavailable"
        if name == "ModelNotAvailableError":
            return "unavailable", "model_unavailable"
        return "unknown", "provider_unavailable"


def _select_model(
    *,
    explicit_model: str | None,
    existing_model: str | None,
    available_models: list[str] | None,
    defaults: bool,
    interactive: bool,
) -> tuple[str | None, str | None, str]:
    inventory = [m.strip() for m in (available_models or []) if isinstance(m, str) and m.strip()]
    candidates: list[tuple[str | None, str]] = [
        (explicit_model.strip() if isinstance(explicit_model, str) and explicit_model.strip() else None, "explicit"),
        (
            existing_model.strip() if isinstance(existing_model, str) and existing_model.strip() else None,
            "default_copilot_model",
        ),
    ]
    candidates.append((inventory[0] if inventory else None, "availableModels"))
    for candidate, source in candidates:
        if candidate and (not inventory or candidate in inventory):
            return candidate, source, "ready"
    return None, None, "model_unavailable_without_refresh" if not inventory else "model_unavailable"


def _managed_copilot_provider(
    existing_provider: Mapping[str, Any] | None,
    *,
    model: str,
) -> dict[str, Any]:
    """Return the normalized managed Copilot provider block."""
    if not isinstance(existing_provider, Mapping):
        return {
            "type": COPILOT_PROVIDER_TYPE,
            "model": model,
        }
    provider: dict[str, Any] = {}
    for key in existing_provider:
        if key == "type":
            provider[key] = COPILOT_PROVIDER_TYPE
        elif key == "model":
            provider[key] = model
        elif key == "timeout_seconds":
            timeout_seconds = existing_provider.get(key)
            if isinstance(timeout_seconds, int) and not isinstance(timeout_seconds, bool) and timeout_seconds >= 0:
                provider[key] = timeout_seconds
    provider.setdefault("type", COPILOT_PROVIDER_TYPE)
    provider.setdefault("model", model)
    return provider


def plan_provider_configuration(
    git_root: Path | None,
    *,
    explicit_model: str | None = None,
    available_models: list[str] | None = None,
    existing_model: str | None = None,
    defaults: bool = False,
    reconfigure: bool = False,
    dry_run: bool = False,
    interactive: bool = False,
    readiness: ProviderReadiness | None = None,
    skip_model_refresh: bool = False,
    skip_reason: str = "no_git_root",
) -> ProviderConfigurationPlan:
    """Plan provider setup without writing repository files."""
    path = (git_root / PROVIDER_CONFIG_RELATIVE_PATH) if git_root else PROVIDER_CONFIG_RELATIVE_PATH
    default_provider_custom = False
    review_provider_custom = False
    if git_root is None:
        return ProviderConfigurationPlan(
            path=path,
            status="skipped",
            document=None,
            rendered=None,
            provider_id=None,
            provider_type=None,
            model=None,
            model_source=None,
            mappings=_MAPPINGS,
            auth_status="not_checked",
            credential_status="not_checked",
            source="none",
            reason=skip_reason,
            dry_run=dry_run,
            reconfigure=reconfigure,
            template_version=None,
        )
    existing, parse_reason = _parse_document(path)
    if parse_reason:
        return ProviderConfigurationPlan(
            path=path,
            status="failed" if reconfigure else "skipped",
            document=None,
            rendered=None,
            provider_id=None,
            provider_type=None,
            model=None,
            model_source=None,
            mappings=_MAPPINGS,
            auth_status="not_checked",
            credential_status="not_checked",
            source="existing",
            reason=parse_reason,
            dry_run=dry_run,
            reconfigure=reconfigure,
            template_version=None,
        )
    if existing is not None and not reconfigure:
        provider_id: str | None
        provider_type: str | None
        model: str | None
        mapping_error, default_provider_id, default_provider, selected_provider_id, selected_provider = (
            _resolve_review_providers(existing)
        )
        if selected_provider_id is not None and isinstance(selected_provider, Mapping):
            provider_id, provider_type, model = _provider_details(selected_provider_id, selected_provider)
        else:
            provider_id, provider_type, model = _provider_fields(existing)
        providers = existing.get("providers")
        try:
            schema_errors = validate_config(dict(existing))
        except DuplicateNodeMappingError:
            schema_errors = ["duplicate_node_mapping"]
        default_error = _validate_provider_mapping(default_provider) if mapping_error is None else None
        selected_error = _validate_provider_mapping(selected_provider) if mapping_error is None else None
        validation_reason = default_error or selected_error
        if validation_reason is None and schema_errors:
            validation_reason = "incomplete_configuration"
        valid = (
            isinstance(providers, Mapping)
            and bool(providers)
            and validation_reason is None
            and all(isinstance(value, Mapping) for value in providers.values())
            and mapping_error is None
        )
        if default_error and default_provider_id:
            provider_id, provider_type, model = _provider_details(default_provider_id, default_provider)
        elif selected_error and selected_provider_id:
            provider_id, provider_type, model = _provider_details(selected_provider_id, selected_provider)
        readiness_provider_id = provider_id
        default_provider_type = _provider_details(default_provider_id, default_provider)[1]
        readiness_override = _readiness_override_for_providers(
            readiness,
            skip_model_refresh=skip_model_refresh,
            provider_types=(provider_type,),
        )
        if valid and default_provider_id and selected_provider_id:
            auth_status, readiness_reason, readiness_provider_id, readiness_model = _run_review_provider_readiness(
                existing,
                default_provider_id=default_provider_id,
                review_provider_id=selected_provider_id,
                readiness=readiness,
                skip_model_refresh=skip_model_refresh,
                default_provider_type=default_provider_type,
                review_provider_type=provider_type,
            )
            if auth_status != "ready" and readiness_provider_id != provider_id:
                provider_id, provider_type, model = _provider_details(readiness_provider_id, default_provider)
            if auth_status != "ready" and readiness_model is not None:
                model = readiness_model
        else:
            auth_status, readiness_reason = _run_readiness(existing, readiness_override)
        return ProviderConfigurationPlan(
            path=path,
            status="preserved" if valid else "skipped",
            document=existing,
            rendered=None,
            provider_id=provider_id,
            provider_type=provider_type,
            model=model,
            model_source="existing" if model else None,
            mappings=_MAPPINGS,
            auth_status=auth_status if valid else "not_checked",
            credential_status=_credential_status_for_reason(
                provider_type,
                validation_reason if not valid else None,
                default="unknown",
            ),
            source="custom" if valid else "existing",
            reason=readiness_reason
            if valid and auth_status != "ready"
            else "preserved_custom_config"
            if valid
            else validation_reason or mapping_error or "incomplete_configuration",
            dry_run=dry_run,
            reconfigure=False,
            template_version=None,
        )
    if existing is not None and reconfigure:
        review = existing.get("workflows", {})
        review = review.get(PR_REVIEW_WORKFLOW) if isinstance(review, Mapping) else None
        nodes = review.get("nodes", {}) if isinstance(review, Mapping) else {}
        existing_default = review.get("default_provider") if isinstance(review, Mapping) else None
        existing_node = nodes.get(REVIEW_FILES_NODE) if isinstance(nodes, Mapping) else None
        default_provider_custom = (
            isinstance(existing_default, str)
            and bool(existing_default.strip())
            and existing_default.strip() != COPILOT_PROVIDER_ID
        )
        review_provider_id = existing_node.get("provider") if isinstance(existing_node, Mapping) else None
        review_provider_custom = (
            isinstance(review_provider_id, str)
            and bool(review_provider_id.strip())
            and review_provider_id.strip() != COPILOT_PROVIDER_ID
        )
        if default_provider_custom and review_provider_custom:
            validation_error, default_provider_id, default_provider, provider_id, provider = _resolve_review_providers(
                existing
            )
            provider_id, provider_type, model = _provider_details(provider_id, provider)
            if validation_error:
                fallback_provider_id, provider_type, model = _provider_fields(existing)
                return ProviderConfigurationPlan(
                    path=path,
                    status="failed",
                    document=existing,
                    rendered=None,
                    provider_id=provider_id or fallback_provider_id,
                    provider_type=provider_type,
                    model=model,
                    model_source="existing" if model else None,
                    mappings=_MAPPINGS,
                    auth_status="not_checked",
                    credential_status=_credential_status_for_reason(
                        provider_type,
                        validation_error,
                        default="unknown",
                    ),
                    source="custom",
                    reason=validation_error,
                    dry_run=dry_run,
                    reconfigure=True,
                    template_version=None,
                )
            try:
                validation_errors = validate_config(dict(existing))
            except DuplicateNodeMappingError:
                validation_errors = ["duplicate_node_mapping"]
            if validation_errors:
                fallback_provider_id, fallback_provider_type, fallback_model = _provider_fields(existing)
                resolved_provider_type = provider_type if isinstance(provider_type, str) else fallback_provider_type
                resolved_model = model or fallback_model
                return ProviderConfigurationPlan(
                    path=path,
                    status="failed",
                    document=existing,
                    rendered=None,
                    provider_id=provider_id or fallback_provider_id,
                    provider_type=resolved_provider_type,
                    model=resolved_model,
                    model_source="existing" if resolved_model else None,
                    mappings=_MAPPINGS,
                    auth_status="not_checked",
                    credential_status=_credential_status_for_reason(
                        resolved_provider_type,
                        "configuration_invalid",
                        default="unknown",
                    ),
                    source="custom",
                    reason="configuration_invalid",
                    dry_run=dry_run,
                    reconfigure=True,
                    template_version=None,
                )
            default_error = _validate_provider_mapping(default_provider)
            if default_error:
                provider_id, provider_type, model = _provider_details(default_provider_id, default_provider)
                return ProviderConfigurationPlan(
                    path=path,
                    status="failed",
                    document=existing,
                    rendered=None,
                    provider_id=provider_id,
                    provider_type=provider_type,
                    model=model,
                    model_source="existing" if model else None,
                    mappings=_MAPPINGS,
                    auth_status="not_checked",
                    credential_status=_credential_status_for_reason(
                        provider_type,
                        default_error,
                        default="unknown",
                    ),
                    source="custom",
                    reason=default_error,
                    dry_run=dry_run,
                    reconfigure=True,
                    template_version=None,
                )
            provider_error = _validate_provider_mapping(provider)
            if provider_error:
                return ProviderConfigurationPlan(
                    path=path,
                    status="failed",
                    document=existing,
                    rendered=None,
                    provider_id=provider_id,
                    provider_type=provider_type,
                    model=model,
                    model_source="existing" if model else None,
                    mappings=_MAPPINGS,
                    auth_status="not_checked",
                    credential_status=_credential_status_for_reason(
                        provider_type,
                        provider_error,
                        default="unknown",
                    ),
                    source="custom",
                    reason=provider_error,
                    dry_run=dry_run,
                    reconfigure=True,
                    template_version=None,
                )
            assert provider is not None
            default_provider_type = _provider_details(default_provider_id, default_provider)[1]
            readiness_override = _readiness_override_for_providers(
                readiness,
                skip_model_refresh=skip_model_refresh,
                provider_types=(provider_type,),
            )
            auth_status, readiness_reason, readiness_provider_id, readiness_model = _run_review_provider_readiness(
                existing,
                default_provider_id=default_provider_id or provider_id or COPILOT_PROVIDER_ID,
                review_provider_id=provider_id or default_provider_id or COPILOT_PROVIDER_ID,
                readiness=readiness,
                skip_model_refresh=skip_model_refresh,
                default_provider_type=default_provider_type,
                review_provider_type=provider_type,
            )
            if auth_status != "ready" and readiness_provider_id == default_provider_id:
                provider_id, provider_type, model = _provider_details(default_provider_id, default_provider)
            if auth_status != "ready" and readiness_model is not None:
                model = readiness_model
            return ProviderConfigurationPlan(
                path=path,
                status="preserved" if auth_status == "ready" else "failed",
                document=existing,
                rendered=None,
                provider_id=provider_id,
                provider_type=provider_type,
                model=model,
                model_source="existing" if model else None,
                mappings=_MAPPINGS,
                auth_status=auth_status,
                credential_status=_credential_status_for_reason(
                    provider_type,
                    readiness_reason if auth_status != "ready" else None,
                    default="unknown",
                ),
                source="custom",
                reason="preserved_custom_mapping" if auth_status == "ready" else readiness_reason,
                dry_run=dry_run,
                reconfigure=True,
                template_version=None,
            )
    model, model_source, model_reason = _select_model(
        explicit_model=explicit_model,
        existing_model=existing_model,
        available_models=available_models,
        defaults=defaults,
        interactive=interactive,
    )
    if model is None:
        return ProviderConfigurationPlan(
            path=path,
            status="skipped" if not reconfigure else "failed",
            document=existing,
            rendered=None,
            provider_id=COPILOT_PROVIDER_ID,
            provider_type=COPILOT_PROVIDER_TYPE,
            model=None,
            model_source=None,
            mappings=_MAPPINGS,
            auth_status="not_checked",
            credential_status="not_required",
            source="template" if existing is None else "existing",
            reason=model_reason,
            dry_run=dry_run,
            reconfigure=reconfigure,
            template_version=TEMPLATE_VERSION if existing is None else None,
        )
    try:
        document = load_provider_template() if existing is None else copy.deepcopy(existing)
        providers = document.setdefault("providers", {})
        if not isinstance(providers, dict):
            raise ValueError("providers_missing")
        if existing is None:
            provider = providers.setdefault(COPILOT_PROVIDER_ID, {})
            if not isinstance(provider, dict):
                raise ValueError("provider_invalid")
            provider["type"] = COPILOT_PROVIDER_TYPE
            provider["model"] = model
        else:
            existing_provider = providers.get(COPILOT_PROVIDER_ID)
            if existing_provider is not None and not isinstance(existing_provider, Mapping):
                raise ValueError("provider_invalid")
            providers[COPILOT_PROVIDER_ID] = _managed_copilot_provider(existing_provider, model=model)
        workflows = document.setdefault("workflows", {})
        if not isinstance(workflows, dict):
            raise ValueError("workflow_mapping_invalid")
        review = workflows.setdefault(PR_REVIEW_WORKFLOW, {})
        if not isinstance(review, dict):
            raise ValueError("workflow_mapping_invalid")
        if not default_provider_custom:
            review["default_provider"] = COPILOT_PROVIDER_ID
        nodes = review.setdefault("nodes", {})
        if not isinstance(nodes, dict):
            raise ValueError("workflow_mapping_invalid")
        node = nodes.setdefault(REVIEW_FILES_NODE, {})
        if not isinstance(node, dict):
            raise ValueError("review_files_mapping_invalid")
        if not review_provider_custom:
            node["provider"] = COPILOT_PROVIDER_ID
        try:
            errors = validate_config(dict(document))
        except DuplicateNodeMappingError:
            errors = ["duplicate_node_mapping"]
        if errors:
            raise ValueError(errors[0])
        mapping_error, _default_provider_id, default_provider, _selected_provider_id, selected_provider = (
            _resolve_review_providers(document)
        )
        if mapping_error:
            raise ValueError(mapping_error)
        default_error = _validate_provider_mapping(default_provider)
        if default_error:
            provider_id, provider_type, resolved_model = _provider_details(
                review.get("default_provider") if isinstance(review.get("default_provider"), str) else None,
                default_provider,
            )
            return ProviderConfigurationPlan(
                path=path,
                status="failed",
                document=document if existing is not None else None,
                rendered=None,
                provider_id=provider_id,
                provider_type=provider_type,
                model=resolved_model,
                model_source="existing" if resolved_model and existing is not None else model_source,
                mappings=_MAPPINGS,
                auth_status="not_checked",
                credential_status=_credential_status_for_reason(
                    provider_type,
                    default_error,
                    default="unknown",
                ),
                source="existing" if existing is not None else "template",
                reason=default_error,
                dry_run=dry_run,
                reconfigure=reconfigure,
                template_version=TEMPLATE_VERSION if existing is None else None,
            )
        selected_error = _validate_provider_mapping(selected_provider)
        if selected_error:
            provider_id, provider_type, resolved_model = _provider_details(
                node.get("provider") if isinstance(node.get("provider"), str) else None,
                selected_provider,
            )
            return ProviderConfigurationPlan(
                path=path,
                status="failed",
                document=document if existing is not None else None,
                rendered=None,
                provider_id=provider_id,
                provider_type=provider_type,
                model=resolved_model,
                model_source="existing" if resolved_model and existing is not None else model_source,
                mappings=_MAPPINGS,
                auth_status="not_checked",
                credential_status=_credential_status_for_reason(
                    provider_type,
                    selected_error,
                    default="unknown",
                ),
                source="existing" if existing is not None else "template",
                reason=selected_error,
                dry_run=dry_run,
                reconfigure=reconfigure,
                template_version=TEMPLATE_VERSION if existing is None else None,
            )
    except (OSError, ValueError, yaml.YAMLError):
        return ProviderConfigurationPlan(
            path=path,
            status="failed",
            document=None,
            rendered=None,
            provider_id=COPILOT_PROVIDER_ID,
            provider_type=COPILOT_PROVIDER_TYPE,
            model=model,
            model_source=model_source,
            mappings=_MAPPINGS,
            auth_status="not_checked",
            credential_status="not_required",
            source="template",
            reason="configuration_invalid",
            dry_run=dry_run,
            reconfigure=reconfigure,
            template_version=TEMPLATE_VERSION,
        )
    provider_id = COPILOT_PROVIDER_ID
    provider_type = COPILOT_PROVIDER_TYPE
    resolved_model = model
    if existing is not None and (default_provider_custom or review_provider_custom):
        (
            _mapping_error,
            default_provider_id,
            default_provider,
            selected_provider_id,
            selected_provider,
        ) = _resolve_review_providers(document)
        default_provider_type = _provider_details(default_provider_id, default_provider)[1]
        selected_provider_type = _provider_details(selected_provider_id, selected_provider)[1]
        auth_status, readiness_reason, readiness_provider_id, readiness_model = _run_review_provider_readiness(
            document,
            default_provider_id=default_provider_id or COPILOT_PROVIDER_ID,
            review_provider_id=selected_provider_id or COPILOT_PROVIDER_ID,
            readiness=readiness,
            skip_model_refresh=skip_model_refresh,
            default_provider_type=default_provider_type,
            review_provider_type=selected_provider_type,
        )
        provider_id, provider_type, resolved_model = {
            default_provider_id: _provider_details(default_provider_id, default_provider),
            selected_provider_id: _provider_details(selected_provider_id, selected_provider),
        }.get(
            readiness_provider_id,
            (provider_id, provider_type, resolved_model),
        )
        if auth_status != "ready" and readiness_model is not None:
            resolved_model = readiness_model
    else:
        auth_status, readiness_reason = _run_readiness(document, readiness)
    status = "created" if existing is None else "updated"
    rendered = render_provider_config(document)
    if existing is not None and render_provider_config(existing) == rendered:
        status = "preserved"
        if auth_status == "ready":
            readiness_reason = "no_change"
    if auth_status != "ready":
        status = "skipped" if not reconfigure else "failed"
    provider_model_source = "existing" if resolved_model and provider_id != COPILOT_PROVIDER_ID else model_source
    credential_status = _credential_status_for_reason(
        provider_type,
        readiness_reason if auth_status != "ready" else None,
        default="unknown",
    )
    return ProviderConfigurationPlan(
        path=path,
        status=status,
        document=document,
        rendered=rendered,
        provider_id=provider_id,
        provider_type=provider_type,
        model=resolved_model,
        model_source=provider_model_source,
        mappings=_MAPPINGS,
        auth_status=auth_status,
        credential_status=credential_status,
        source="template" if existing is None else "existing",
        reason=readiness_reason,
        dry_run=dry_run,
        reconfigure=reconfigure,
        template_version=TEMPLATE_VERSION,
    )


def apply_provider_configuration(plan: ProviderConfigurationPlan) -> bool:
    """Atomically apply a planned generated/reconfigured document."""
    if plan.dry_run or plan.status not in {"created", "updated"} or not plan.rendered:
        return False
    from .script_generators.atomic_write import atomic_write

    atomic_write(plan.path, plan.rendered)
    return True


def check_provider_configuration(
    git_root: Path | None,
    *,
    readiness: ProviderReadiness | None = None,
) -> ProviderConfigurationCheck:
    """Validate an existing provider file and its explicit review mapping."""
    path = (git_root / PROVIDER_CONFIG_RELATIVE_PATH) if git_root else PROVIDER_CONFIG_RELATIVE_PATH
    try:
        found = path.exists()
    except OSError:
        found = False
    if git_root is None or not found:
        return ProviderConfigurationCheck(
            found=False,
            valid=False,
            reason="missing_file",
            provider_id=None,
            provider_type=None,
            model=None,
            auth_status="not_checked",
            credential_status="not_checked",
            path=path,
        )
    document, parse_reason = _parse_document(path)
    if parse_reason or document is None:
        return ProviderConfigurationCheck(
            found=True,
            valid=False,
            reason=parse_reason or "invalid_configuration",
            provider_id=None,
            provider_type=None,
            model=None,
            auth_status="not_checked",
            credential_status="not_checked",
            path=path,
        )
    try:
        errors = validate_config(document)
    except DuplicateNodeMappingError:
        errors = ["duplicate_node_mapping"]
    mapping_error, default_provider_id, default_provider, provider_id, provider = _resolve_review_providers(document)
    if mapping_error:
        errors = [mapping_error]
    provider_id, provider_type, model = _provider_details(provider_id, provider)
    default_error: str | None = None
    provider_error: str | None = None
    if mapping_error is None:
        if default_provider_id:
            default_error = _validate_provider_mapping(default_provider)
            if default_error:
                provider_id, provider_type, model = _provider_details(default_provider_id, default_provider)
                errors = [default_error]
        provider_error = _validate_provider_mapping(provider)
        if provider_error and default_error is None:
            errors = [provider_error]
    if errors:
        return ProviderConfigurationCheck(
            found=True,
            valid=False,
            reason=errors[0],
            provider_id=provider_id,
            provider_type=provider_type,
            model=model,
            auth_status="not_checked",
            credential_status=_credential_status_for_reason(provider_type, errors[0], default="unknown"),
            path=path,
        )
    if default_provider_id is None or provider_id is None:
        return ProviderConfigurationCheck(
            found=True,
            valid=False,
            reason="provider_missing",
            provider_id=provider_id,
            provider_type=provider_type,
            model=model,
            auth_status="not_checked",
            credential_status="unknown",
            path=path,
        )
    auth_status, reason, readiness_provider_id, readiness_model = _run_review_provider_readiness(
        document,
        default_provider_id=default_provider_id,
        review_provider_id=provider_id,
        readiness=readiness,
    )
    if auth_status != "ready" and readiness_provider_id == default_provider_id:
        provider_id, provider_type, model = _provider_details(default_provider_id, default_provider)
    if auth_status != "ready" and readiness_model is not None:
        model = readiness_model
    return ProviderConfigurationCheck(
        found=True,
        valid=auth_status == "ready",
        reason=reason,
        provider_id=provider_id,
        provider_type=provider_type,
        model=model,
        auth_status=auth_status,
        credential_status=_credential_status_for_reason(
            provider_type,
            reason if auth_status != "ready" else None,
            default="unknown",
        ),
        path=path,
    )
