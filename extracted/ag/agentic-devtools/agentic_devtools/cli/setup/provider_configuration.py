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
        if not parsed.scheme:
            return value
        netloc = f"******@{parsed.netloc.rsplit('@', 1)[1]}" if "@" in parsed.netloc else parsed.netloc
        query = parsed.query
        if query:
            query_pairs = parse_qsl(query, keep_blank_values=True)
            redacted_pairs = [(key, "<redacted>" if _is_secret_key(key) else item) for key, item in query_pairs]
            if redacted_pairs != query_pairs:
                query = urlencode(redacted_pairs, doseq=True)
        fragment = "<redacted>" if parsed.fragment else ""
        if netloc == parsed.netloc and query == parsed.query and not fragment:
            return value
        return parsed._replace(netloc=netloc, query=query, fragment=fragment).geturl()

    def redact(value: Any) -> Any:
        if isinstance(value, dict):
            return {key: "<redacted>" if _is_secret_key(key) else redact(item) for key, item in value.items()}
        if isinstance(value, list):
            return [redact(item) for item in value]
        if isinstance(value, str):
            return redact_url_userinfo(value)
        return value

    return yaml.safe_dump(redact(document), sort_keys=False, default_flow_style=False)


def _is_secret_key(key: Any) -> bool:
    normalized = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", str(key)).lower().replace("-", "_")
    if normalized.endswith(("_env", "_env_var", "_environment_variable")):
        return False
    components = [component for component in re.split(r"[^a-z0-9]+", normalized) if component]
    return (
        "token" in components
        or "secret" in components
        or "password" in components
        or "credential" in components
        or normalized in {"key", "pat", "sig", "signature"}
        or ("api" in components and "key" in components)
        or "authorization" in components
        or ("private" in components and "key" in components)
    )


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
    workflows = document.get("workflows")
    review = workflows.get(PR_REVIEW_WORKFLOW) if isinstance(workflows, Mapping) else None
    if not isinstance(review, Mapping):
        return "workflow_mapping_missing", None, None
    default_provider_id = review.get("default_provider")
    if not isinstance(default_provider_id, str) or not default_provider_id.strip():
        return "default_provider_missing", None, None
    default_provider_id = default_provider_id.strip()
    providers = document.get("providers")
    if not isinstance(providers, Mapping) or not isinstance(providers.get(default_provider_id), Mapping):
        return "provider_missing", default_provider_id, None
    nodes = review.get("nodes")
    node = nodes.get(REVIEW_FILES_NODE) if isinstance(nodes, Mapping) else None
    if not isinstance(node, Mapping):
        return "review_files_mapping_missing", default_provider_id, None
    provider_id = node.get("provider")
    if not isinstance(provider_id, str) or not provider_id.strip():
        return "review_files_mapping_missing", default_provider_id, None
    provider_id = provider_id.strip()
    provider = providers.get(provider_id) if isinstance(providers, Mapping) else None
    if not isinstance(provider, Mapping):
        return "provider_missing", provider_id, None
    return None, provider_id, provider


def validate_provider_configuration(document: Mapping[str, Any]) -> list[str]:
    """Validate the strict provider path required by the PR-review workflow."""
    if not isinstance(document, Mapping):
        return ["invalid_root"]
    errors = validate_config(dict(document))
    if errors:
        return ["invalid_configuration"]
    providers = document.get("providers")
    if not isinstance(providers, Mapping):
        return ["providers_missing"]
    provider = providers.get(COPILOT_PROVIDER_ID)
    if not isinstance(provider, Mapping):
        return ["provider_missing"]
    if provider.get("type") != COPILOT_PROVIDER_TYPE:
        return ["provider_type_invalid"]
    if not isinstance(provider.get("model"), str) or not provider["model"].strip():
        return ["model_missing"]
    if "api_key_env" in provider:
        return ["copilot_api_key_env_forbidden"]
    workflows = document.get("workflows")
    review = workflows.get(PR_REVIEW_WORKFLOW) if isinstance(workflows, Mapping) else None
    if not isinstance(review, Mapping):
        return ["workflow_mapping_missing"]
    if review.get("default_provider") != COPILOT_PROVIDER_ID:
        return ["default_provider_missing"]
    nodes = review.get("nodes")
    node = nodes.get(REVIEW_FILES_NODE) if isinstance(nodes, Mapping) else None
    if not isinstance(node, Mapping) or node.get("provider") != COPILOT_PROVIDER_ID:
        return ["review_files_mapping_missing"]
    return []


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
        mapping_error, selected_provider_id, selected_provider = _resolve_review_provider(existing)
        if selected_provider_id is not None and isinstance(selected_provider, Mapping):
            provider_id = selected_provider_id
            provider_type = selected_provider.get("type") if isinstance(selected_provider.get("type"), str) else None
            model_value = selected_provider.get("model")
            model = model_value.strip() if isinstance(model_value, str) and model_value.strip() else None
        else:
            provider_id, provider_type, model = _provider_fields(existing)
        providers = existing.get("providers")
        try:
            schema_errors = validate_config(dict(existing))
        except DuplicateNodeMappingError:
            schema_errors = ["duplicate_node_mapping"]
        valid = (
            isinstance(providers, Mapping)
            and bool(providers)
            and not schema_errors
            and all(isinstance(value, Mapping) for value in providers.values())
            and mapping_error is None
        )
        readiness_override = readiness if not skip_model_refresh or provider_type == COPILOT_PROVIDER_TYPE else None
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
            credential_status="not_required" if provider_type == COPILOT_PROVIDER_TYPE else "unknown",
            source="custom" if valid else "existing",
            reason=readiness_reason
            if valid and auth_status != "ready"
            else "preserved_custom_config"
            if valid
            else mapping_error or "incomplete_configuration",
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
        custom_mapping = existing_default not in (None, "", COPILOT_PROVIDER_ID) or (
            isinstance(existing_node, Mapping) and existing_node.get("provider") not in (None, "", COPILOT_PROVIDER_ID)
        )
        if custom_mapping:
            validation_error, provider_id, provider = _resolve_review_provider(existing)
            provider_type = provider.get("type") if isinstance(provider, Mapping) else None
            model_value = provider.get("model") if isinstance(provider, Mapping) else None
            model = model_value.strip() if isinstance(model_value, str) and model_value.strip() else None
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
                    credential_status="unknown",
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
                    credential_status="not_required" if resolved_provider_type == COPILOT_PROVIDER_TYPE else "unknown",
                    source="custom",
                    reason="configuration_invalid",
                    dry_run=dry_run,
                    reconfigure=True,
                    template_version=None,
                )
            assert provider is not None
            auth_status, readiness_reason = _run_readiness(
                existing,
                readiness if not skip_model_refresh or provider_type == COPILOT_PROVIDER_TYPE else None,
            )
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
                credential_status="not_required" if provider_type == COPILOT_PROVIDER_TYPE else "unknown",
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
        provider = providers.setdefault(COPILOT_PROVIDER_ID, {})
        if not isinstance(provider, dict):
            raise ValueError("provider_invalid")
        provider.update({"type": COPILOT_PROVIDER_TYPE, "model": model})
        for unsupported in (
            "api_key_env",
            "temperature",
            "max_tokens",
            "top_p",
            "presence_penalty",
            "frequency_penalty",
        ):
            provider.pop(unsupported, None)
        for key in list(provider):
            if _is_secret_key(key):
                provider.pop(key)
        workflows = document.setdefault("workflows", {})
        if not isinstance(workflows, dict):
            raise ValueError("workflow_mapping_invalid")
        review = workflows.setdefault(PR_REVIEW_WORKFLOW, {})
        if not isinstance(review, dict):
            raise ValueError("workflow_mapping_invalid")
        review.setdefault("default_provider", COPILOT_PROVIDER_ID)
        nodes = review.setdefault("nodes", {})
        if not isinstance(nodes, dict):
            raise ValueError("workflow_mapping_invalid")
        node = nodes.setdefault(REVIEW_FILES_NODE, {})
        if not isinstance(node, dict):
            raise ValueError("review_files_mapping_invalid")
        node.setdefault("provider", COPILOT_PROVIDER_ID)
        errors = validate_provider_configuration(document)
        if errors:
            raise ValueError(errors[0])
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
    auth_status, readiness_reason = _run_readiness(document, readiness)
    status = "created" if existing is None else "updated"
    rendered = render_provider_config(document)
    if existing is not None and render_provider_config(existing) == rendered:
        status = "preserved"
        readiness_reason = "no_change"
    if auth_status != "ready":
        status = "skipped" if not reconfigure else "failed"
    return ProviderConfigurationPlan(
        path=path,
        status=status,
        document=document,
        rendered=rendered,
        provider_id=COPILOT_PROVIDER_ID,
        provider_type=COPILOT_PROVIDER_TYPE,
        model=model,
        model_source=model_source,
        mappings=_MAPPINGS,
        auth_status=auth_status,
        credential_status="not_required",
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
    mapping_error, provider_id, provider = _resolve_review_provider(document)
    if mapping_error:
        errors = errors or [mapping_error]
    provider_type = provider.get("type") if isinstance(provider, Mapping) else None
    model = provider.get("model") if isinstance(provider, Mapping) else None
    if not isinstance(provider, Mapping):
        errors = errors or ["provider_missing"]
    elif provider_type not in {"azure_openai", "openai_direct", "local_model", "copilot"}:
        errors = ["provider_type_invalid"]
    elif not isinstance(model, str) or not model.strip():
        errors = ["model_missing"]
    elif provider_type == COPILOT_PROVIDER_TYPE and "api_key_env" in provider:
        errors = ["copilot_api_key_env_forbidden"]
    elif provider_type in {"azure_openai", "openai_direct"}:
        env_name = provider.get("api_key_env")
        if not isinstance(env_name, str) or not env_name.strip():
            errors = errors or ["credential_reference_missing"]
        elif not os.environ.get(env_name):
            errors = errors or ["credential_missing"]
    if provider_type in {"azure_openai", "local_model"}:
        endpoint = provider.get("endpoint") if isinstance(provider, Mapping) else None
        if not isinstance(endpoint, str) or not endpoint.strip():
            errors = errors or ["endpoint_missing"]
        else:
            try:
                parsed_endpoint = urlparse(endpoint)
            except ValueError:
                errors = errors or ["endpoint_invalid"]
            else:
                if parsed_endpoint.scheme.lower() not in {"http", "https"} or not parsed_endpoint.netloc:
                    errors = errors or ["endpoint_invalid"]
    provider_id = provider_id if isinstance(provider_id, str) else None
    provider_type = provider_type if isinstance(provider_type, str) else None
    model = model.strip() if isinstance(model, str) and model.strip() else None
    if errors:
        credential_status = (
            "not_required"
            if provider_type == COPILOT_PROVIDER_TYPE
            else "missing"
            if errors[0] in {"credential_missing", "credential_reference_missing"}
            else "unknown"
        )
        return ProviderConfigurationCheck(
            found=True,
            valid=False,
            reason=errors[0],
            provider_id=provider_id,
            provider_type=provider_type,
            model=model,
            auth_status="not_checked",
            credential_status=credential_status,
            path=path,
        )
    auth_status, reason = _run_readiness(document, readiness)
    return ProviderConfigurationCheck(
        found=True,
        valid=auth_status == "ready",
        reason=reason,
        provider_id=provider_id,
        provider_type=provider_type,
        model=model,
        auth_status=auth_status,
        credential_status="not_required" if provider_type == COPILOT_PROVIDER_TYPE else "unknown",
        path=path,
    )
