"""Configuration loading, resolution, and immutable snapshot."""

from __future__ import annotations

import warnings
from collections.abc import Mapping
from dataclasses import dataclass, field
from pathlib import Path
from types import MappingProxyType
from typing import Any

import yaml

from agentic_devtools.orchestration.llm.config_schema import validate_config
from agentic_devtools.orchestration.llm.types import NodeConfig, ProviderConfig, ProviderType

DEFAULT_CONFIG_PATH = ".agdt/config/llm-providers.yml"


def _coerce_int(value: Any, field_name: str) -> int | None:
    """Coerce a value to int, emitting a warning if coercion is needed."""
    if value is None:
        return None
    if isinstance(value, bool):
        warnings.warn(
            f"LLM config: {field_name!r} has boolean value {value!r}; ignoring",
            stacklevel=4,
        )
        return None
    if isinstance(value, int):
        if value < 0:
            warnings.warn(
                f"LLM config: {field_name!r} has negative value {value!r}; ignoring",
                stacklevel=4,
            )
            return None
        return value
    if isinstance(value, float) and value == int(value):
        coerced = int(value)
        if coerced < 0:
            warnings.warn(
                f"LLM config: {field_name!r} has negative value {value!r}; ignoring",
                stacklevel=4,
            )
            return None
        return coerced
    if isinstance(value, str):
        try:
            coerced = int(value)
            if coerced < 0:
                warnings.warn(
                    f"LLM config: {field_name!r} has negative value {value!r}; ignoring",
                    stacklevel=4,
                )
                return None
            warnings.warn(
                f"LLM config: {field_name!r} should be an integer, got string {value!r}; coercing",
                stacklevel=4,
            )
            return coerced
        except ValueError:
            warnings.warn(
                f"LLM config: {field_name!r} has non-integer value {value!r}; ignoring",
                stacklevel=4,
            )
            return None
    warnings.warn(
        f"LLM config: {field_name!r} has unexpected type {type(value).__name__!r}; ignoring",
        stacklevel=4,
    )
    return None


def _coerce_float(value: Any, field_name: str) -> float | None:
    """Coerce a value to float, emitting a warning if coercion is needed."""
    is_temperature_field = field_name.split(".")[-1] == "temperature"

    def _validate_float_range(coerced: float) -> float | None:
        if is_temperature_field and not (0.0 <= coerced <= 2.0):
            warnings.warn(
                f"LLM config: {field_name!r} has out-of-range value {coerced!r}; expected 0.0-2.0; ignoring",
                stacklevel=4,
            )
            return None
        return coerced

    if value is None:
        return None
    if isinstance(value, bool):
        warnings.warn(
            f"LLM config: {field_name!r} has boolean value {value!r}; ignoring",
            stacklevel=4,
        )
        return None
    if isinstance(value, float):
        return _validate_float_range(value)
    if isinstance(value, int):
        return _validate_float_range(float(value))
    if isinstance(value, str):
        try:
            coerced = float(value)
            if _validate_float_range(coerced) is None:
                return None
            warnings.warn(
                f"LLM config: {field_name!r} should be a float, got string {value!r}; coercing",
                stacklevel=4,
            )
            return coerced
        except ValueError:
            warnings.warn(
                f"LLM config: {field_name!r} has non-numeric value {value!r}; ignoring",
                stacklevel=4,
            )
            return None
    warnings.warn(
        f"LLM config: {field_name!r} has unexpected type {type(value).__name__!r}; ignoring",
        stacklevel=4,
    )
    return None


@dataclass(frozen=True)
class LLMConfigSnapshot:
    """Immutable configuration snapshot loaded once at workflow initialization."""

    providers: Mapping[str, ProviderConfig] = field(default_factory=dict)
    workflows: Mapping[str, Any] = field(default_factory=dict)
    defaults: Mapping[str, Any] = field(default_factory=dict)
    raw: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Freeze nested mapping/list structures to prevent in-place mutation."""
        object.__setattr__(self, "providers", _freeze_value(self.providers))
        object.__setattr__(self, "workflows", _freeze_value(self.workflows))
        object.__setattr__(self, "defaults", _freeze_value(self.defaults))
        object.__setattr__(self, "raw", _freeze_value(self.raw))


# Sentinel for distinguishing "key absent" from "key present with value None"
_MISSING = object()


def _freeze_value(value: Any) -> Any:
    """Recursively freeze mappings and lists."""
    if isinstance(value, Mapping):
        return MappingProxyType({key: _freeze_value(item) for key, item in value.items()})
    if isinstance(value, list):
        return tuple(_freeze_value(item) for item in value)
    return value


def load_config(
    config_path: str | Path | None = None,
    *,
    config_dict: dict[str, Any] | None = None,
) -> LLMConfigSnapshot:
    """Load LLM provider configuration from YAML file or dict.

    Args:
        config_path: Path to YAML config file. Defaults to .agdt/config/llm-providers.yml.
        config_dict: Pre-loaded config dict (takes precedence over file).

    Returns:
        Frozen LLMConfigSnapshot.

    Raises:
        DuplicateNodeMappingError: If duplicate (workflow, node_type) mappings found.
    """
    if config_dict is not None:
        raw_loaded: Any = config_dict
    else:
        path = Path(config_path) if config_path else Path(DEFAULT_CONFIG_PATH)
        if not path.exists():
            # Return empty config if no file exists
            return LLMConfigSnapshot()
        with open(path, encoding="utf-8") as f:
            raw_loaded = yaml.safe_load(f) or {}

    if not isinstance(raw_loaded, dict):
        warnings.warn("LLM config validation: root config must be a mapping; using empty config", stacklevel=4)
        raw: dict[str, Any] = {}
    else:
        raw = raw_loaded

    # Validate (may raise DuplicateNodeMappingError)
    errors = validate_config(raw)
    if errors:
        for err in errors:
            warnings.warn(f"LLM config validation: {err}", stacklevel=4)

    providers_raw = raw.get("providers", {})
    workflows_raw = raw.get("workflows", {})
    defaults_raw = raw.get("defaults", {})
    if not isinstance(providers_raw, dict):
        warnings.warn("LLM config validation: 'providers' must be a mapping; using empty providers", stacklevel=4)
        providers_raw = {}
    if not isinstance(workflows_raw, dict):
        warnings.warn("LLM config validation: 'workflows' must be a mapping; using empty workflows", stacklevel=4)
        workflows_raw = {}
    if not isinstance(defaults_raw, dict):
        warnings.warn("LLM config validation: 'defaults' must be a mapping; using empty defaults", stacklevel=4)
        defaults_raw = {}

    # Parse providers
    providers: dict[str, ProviderConfig] = {}
    for provider_id, cfg in providers_raw.items():
        # Provider keys must be non-empty strings; YAML allows unquoted numbers as keys
        if not isinstance(provider_id, str):
            warnings.warn(
                f"LLM config: provider key {provider_id!r} is not a string "
                f"(got {type(provider_id).__name__!r}); skipping",
                stacklevel=4,
            )
            continue
        provider_id = provider_id.strip()
        if not provider_id:
            warnings.warn(
                "LLM config: provider key is empty or whitespace-only; skipping",
                stacklevel=4,
            )
            continue
        if not isinstance(cfg, dict):
            continue
        provider_type_str = cfg.get("type", "")
        try:
            provider_type = ProviderType(provider_type_str)
        except ValueError:
            continue

        model_val = cfg.get("model", "")
        if not isinstance(model_val, str):
            continue
        model_val = model_val.strip()
        if not model_val:
            continue

        # Capture the env var name; the actual key lookup happens later in ProviderFactory
        api_key_env_raw = cfg.get("api_key_env")
        api_key_env = api_key_env_raw if isinstance(api_key_env_raw, str) else None

        endpoint_raw = cfg.get("endpoint")
        endpoint = endpoint_raw if isinstance(endpoint_raw, str) else None

        api_version_raw = cfg.get("api_version")
        api_version = api_version_raw if isinstance(api_version_raw, str) else None

        max_tokens = _coerce_int(cfg.get("max_tokens"), f"providers.{provider_id}.max_tokens")
        temperature = _coerce_float(cfg.get("temperature"), f"providers.{provider_id}.temperature")
        timeout_seconds = _coerce_int(cfg.get("timeout_seconds"), f"providers.{provider_id}.timeout_seconds")

        providers[provider_id] = ProviderConfig(
            provider_id=provider_id,
            provider_type=provider_type,
            model=model_val,
            endpoint=endpoint,
            api_version=api_version,
            api_key_env=api_key_env,
            max_tokens=max_tokens,
            temperature=temperature,
            timeout_seconds=timeout_seconds,
        )

    return LLMConfigSnapshot(
        providers=providers,
        workflows=workflows_raw,
        defaults=defaults_raw,
        raw=raw,
    )


def resolve_node_config(
    snapshot: LLMConfigSnapshot,
    workflow: str,
    node_type: str,
) -> NodeConfig:
    """Resolve configuration for a specific workflow node.

    Resolution hierarchy: global defaults → workflow-level → node-level overrides.

    Args:
        snapshot: The loaded configuration snapshot.
        workflow: Workflow name (e.g., "pr_review", "work_on_issue").
        node_type: Node type identifier (e.g., "planning", "review_analysis").

    Returns:
        Resolved NodeConfig.
    """
    # Start with global defaults
    defaults = snapshot.defaults
    default_provider_raw = defaults.get("provider", "")
    if isinstance(default_provider_raw, str):
        default_provider_id = default_provider_raw.strip()
    else:
        default_provider_id = ""
    default_max_tokens = _coerce_int(defaults.get("max_tokens"), "defaults.max_tokens")
    default_temperature = _coerce_float(defaults.get("temperature"), "defaults.temperature")
    default_timeout_seconds = _coerce_int(defaults.get("timeout_seconds"), "defaults.timeout_seconds")

    # Workflow-level overrides
    workflow_cfg = snapshot.workflows.get(workflow, {})
    if not isinstance(workflow_cfg, Mapping):
        workflow_cfg = {}
    _wf_default_provider = workflow_cfg.get("default_provider")
    if _wf_default_provider is not None and not isinstance(_wf_default_provider, str):
        warnings.warn(
            f"LLM config: workflows.{workflow}.default_provider has non-string value "
            f"{_wf_default_provider!r}; ignoring",
            stacklevel=4,
        )
        _wf_default_provider = ""
    elif isinstance(_wf_default_provider, str):
        _wf_default_provider = _wf_default_provider.strip()
    if _wf_default_provider:
        workflow_provider_id = _wf_default_provider
    else:
        workflow_provider_id = default_provider_id

    # Node-level overrides
    nodes = workflow_cfg.get("nodes", {})
    if not isinstance(nodes, Mapping):
        nodes = {}
    node_cfg = nodes.get(node_type, {})
    if not isinstance(node_cfg, Mapping):
        node_cfg = {}
    _node_provider = node_cfg.get("provider")
    if _node_provider is not None and not isinstance(_node_provider, str):
        warnings.warn(
            f"LLM config: workflows.{workflow}.nodes.{node_type}.provider has non-string value "
            f"{_node_provider!r}; ignoring",
            stacklevel=4,
        )
        _node_provider = ""
    elif isinstance(_node_provider, str):
        _node_provider = _node_provider.strip()
    if _node_provider:
        node_provider_id = _node_provider
    else:
        node_provider_id = workflow_provider_id

    # Resolve the provider
    provider = snapshot.providers.get(node_provider_id)
    if provider is None:
        # PR review must be explicit: selecting the first configured provider
        # can route a Copilot model to an unrelated OpenAI backend.
        if workflow == "pr_review":
            from agentic_devtools.orchestration.llm.errors import ProviderNotConfiguredError

            raise ProviderNotConfiguredError(
                f"No provider configured for workflow={workflow!r}, node={node_type!r}, "
                f"provider={node_provider_id or '<unspecified>'!r}",
                workflow=workflow,
                node_type=node_type,
            )
        if snapshot.providers:
            first_provider = next(iter(snapshot.providers.values()))
            warnings.warn(
                f"LLM config: provider {node_provider_id!r} not found for workflow={workflow!r}, "
                f"node_type={node_type!r}; falling back to first configured provider "
                f"{first_provider.provider_id!r}",
                stacklevel=4,
            )
            provider = first_provider
        else:
            # No providers are configured at all.  Synthesize a minimal OPENAI_DIRECT
            # fallback so that the caller gets a clear authentication error rather than a
            # confusing KeyError.  We intentionally do NOT inherit copilot.model_id here
            # because that is the Copilot CLI model identifier (which may be a Gemini or
            # Claude string) and is unrelated to the LangChain provider model selection.
            from .types import ProviderConfig

            provider = ProviderConfig(
                provider_id="synthesized_fallback",
                provider_type=ProviderType.OPENAI_DIRECT,
                model="gpt-4o",
                api_key_env="OPENAI_API_KEY",
            )
            warnings.warn(
                "LLM config: no providers configured; synthesizing fallback OPENAI_DIRECT "
                "provider with model 'gpt-4o'. Configure llm-providers.yml to select the "
                "correct provider and model.",
                stacklevel=4,
            )

    # Build resolved config with hierarchy: node model, then workflow model.
    model_override = node_cfg.get("model", workflow_cfg.get("model"))
    if model_override is not None and not isinstance(model_override, str):
        warnings.warn(
            f"LLM config: workflows.{workflow}.nodes.{node_type}.model has non-string value "
            f"{model_override!r}; ignoring",
            stacklevel=4,
        )
        model_override = None
    elif isinstance(model_override, str):
        model_override = model_override.strip() or None
    params_override: dict[str, Any] = {}
    _temp_raw = node_cfg.get("temperature") if "temperature" in node_cfg else _MISSING
    if _temp_raw is not _MISSING and _temp_raw is not None:
        coerced_temp = _coerce_float(_temp_raw, f"workflows.{workflow}.nodes.{node_type}.temperature")
        if coerced_temp is not None:
            params_override["temperature"] = coerced_temp
    _max_tokens_raw = node_cfg.get("max_tokens") if "max_tokens" in node_cfg else _MISSING
    if _max_tokens_raw is not _MISSING and _max_tokens_raw is not None:
        coerced_max = _coerce_int(_max_tokens_raw, f"workflows.{workflow}.nodes.{node_type}.max_tokens")
        if coerced_max is not None:
            params_override["max_tokens"] = coerced_max
    _timeout_raw = node_cfg.get("timeout_seconds") if "timeout_seconds" in node_cfg else _MISSING
    if _timeout_raw is not _MISSING and _timeout_raw is not None:
        coerced_timeout = _coerce_int(_timeout_raw, f"workflows.{workflow}.nodes.{node_type}.timeout_seconds")
        if coerced_timeout is not None:
            params_override["timeout_seconds"] = coerced_timeout

    resolved_max_tokens = provider.max_tokens if provider.max_tokens is not None else default_max_tokens
    resolved_temperature = provider.temperature if provider.temperature is not None else default_temperature
    if provider.provider_type == ProviderType.COPILOT:
        ignored_fields: list[str] = []
        if resolved_temperature is not None or "temperature" in params_override:
            ignored_fields.append("temperature")
        if resolved_max_tokens is not None or "max_tokens" in params_override:
            ignored_fields.append("max_tokens")
        if ignored_fields:
            warnings.warn(
                f"LLM config: provider {provider.provider_id!r} uses unsupported Copilot options "
                f"{', '.join(ignored_fields)} for workflow={workflow!r}, node_type={node_type!r}; ignoring",
                stacklevel=4,
            )
        resolved_temperature = None
        resolved_max_tokens = None
        params_override = {k: v for k, v in params_override.items() if k not in {"temperature", "max_tokens"}}

    return NodeConfig(
        provider_id=provider.provider_id,
        provider_type=provider.provider_type,
        model=provider.model,
        endpoint=provider.endpoint,
        api_version=provider.api_version,
        api_key_env=provider.api_key_env,
        max_tokens=resolved_max_tokens,
        temperature=resolved_temperature,
        timeout_seconds=(provider.timeout_seconds if provider.timeout_seconds is not None else default_timeout_seconds),
        model_override=model_override,
        params_override=params_override,
    )
