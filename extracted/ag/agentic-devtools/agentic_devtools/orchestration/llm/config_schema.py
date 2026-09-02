"""YAML configuration schema definition and validation."""

from __future__ import annotations

from typing import Any

from agentic_devtools.orchestration.llm.errors import DuplicateNodeMappingError

CONFIG_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "providers": {
            "type": "object",
            "additionalProperties": {
                "type": "object",
                "properties": {
                    "type": {
                        "type": "string",
                        "enum": ["azure_openai", "openai_direct", "local_model", "copilot"],
                    },
                    "model": {"type": "string"},
                    "endpoint": {"type": "string"},
                    "api_version": {"type": "string"},
                    "api_key_env": {"type": "string"},
                    "max_tokens": {"type": "integer", "minimum": 0},
                    "temperature": {"type": "number", "minimum": 0, "maximum": 2},
                    "timeout_seconds": {"type": "integer", "minimum": 0},
                },
                "required": ["type", "model"],
            },
        },
        "workflows": {
            "type": "object",
            "additionalProperties": {
                "type": "object",
                "properties": {
                    "default_provider": {"type": "string"},
                    "model": {"type": "string"},
                    "nodes": {
                        "type": "object",
                        "additionalProperties": {
                            "type": "object",
                            "properties": {
                                "provider": {"type": "string"},
                                "model": {"type": "string"},
                                "temperature": {"type": "number", "minimum": 0, "maximum": 2},
                                "max_tokens": {"type": "integer", "minimum": 0},
                                "timeout_seconds": {"type": "integer", "minimum": 0},
                            },
                        },
                    },
                },
            },
        },
        "defaults": {
            "type": "object",
            "properties": {
                "provider": {"type": "string"},
                "temperature": {"type": "number", "minimum": 0, "maximum": 2},
                "max_tokens": {"type": "integer", "minimum": 0},
                "timeout_seconds": {"type": "integer", "minimum": 0},
            },
        },
    },
}


def validate_config(config: dict[str, Any]) -> list[str]:
    """Validate configuration dict for required fields and business rules.

    Returns a list of validation error messages. Empty list means valid.
    Checks provider required fields ('type', 'model'), valid provider type
    values, and duplicate (workflow, node_type) → provider mappings.
    Note: does not enforce the type and range constraints defined in
    CONFIG_SCHEMA. Numeric coercion and temperature range validation are
    applied separately by load_config() but not here.

    Raises:
        DuplicateNodeMappingError: If two entries in the same workflow map the
            same node_type to different providers (conflicting provider
            assignments for the same (workflow, node_type) key).
    """
    errors: list[str] = []

    if not isinstance(config, dict):
        errors.append("Configuration must be a dictionary")
        return errors

    providers = config.get("providers", {})
    if not isinstance(providers, dict):
        errors.append("'providers' must be a dictionary")
        return errors

    for provider_id, provider_cfg in providers.items():
        if not isinstance(provider_cfg, dict):
            errors.append(f"Provider '{provider_id}' must be a dictionary")
            continue
        if "type" not in provider_cfg:
            errors.append(f"Provider '{provider_id}' missing required field 'type'")
        elif provider_cfg["type"] not in ("azure_openai", "openai_direct", "local_model", "copilot"):
            errors.append(f"Provider '{provider_id}' has invalid type: {provider_cfg['type']}")
        if "model" not in provider_cfg:
            errors.append(f"Provider '{provider_id}' missing required field 'model'")
        elif not isinstance(provider_cfg["model"], str) or not provider_cfg["model"].strip():
            errors.append(f"Provider '{provider_id}' field 'model' must be a non-empty string")
        if provider_cfg.get("type") == "copilot":
            if "api_key_env" in provider_cfg:
                errors.append(f"Provider '{provider_id}' of type 'copilot' must not define 'api_key_env'")
            for unsupported in ("temperature", "max_tokens"):
                if unsupported in provider_cfg:
                    errors.append(
                        f"Provider '{provider_id}' of type 'copilot' does not support '{unsupported}'; "
                        "remove it from the provider configuration"
                    )

    # Check for duplicate node mappings
    workflows = config.get("workflows", {})
    if isinstance(workflows, dict):
        seen_mappings: dict[tuple[str, str], str] = {}
        for workflow_name, workflow_cfg in workflows.items():
            if not isinstance(workflow_cfg, dict):
                continue
            # Validate default_provider type directly so misconfigured workflows
            # without any nodes are still caught early.
            default_provider = workflow_cfg.get("default_provider")
            if default_provider is not None and not isinstance(default_provider, str):
                errors.append(
                    f"Workflow '{workflow_name}' has non-string 'default_provider' value "
                    f"(got {type(default_provider).__name__!r})"
                )
            nodes = workflow_cfg.get("nodes", {})
            if not isinstance(nodes, dict):
                continue
            for node_type, node_cfg in nodes.items():
                if not isinstance(node_cfg, dict):
                    continue
                raw_provider = node_cfg.get("provider")
                # Empty string is the explicit "use workflow default" sentinel.
                # Other falsy non-string values (for example 0/False) must remain
                # visible to the validation branch below instead of falling back.
                if raw_provider is None or raw_provider == "":
                    raw_provider = workflow_cfg.get("default_provider")
                if raw_provider is not None and not isinstance(raw_provider, str):
                    errors.append(
                        f"Node '{node_type}' in workflow '{workflow_name}' has non-string"
                        f" provider value (got {type(raw_provider).__name__!r}); skipping mapping"
                    )
                    continue
                provider = raw_provider or ""
                key = (workflow_name, node_type)
                if key in seen_mappings and seen_mappings[key] != provider:
                    raise DuplicateNodeMappingError(
                        f"Duplicate mapping for ({workflow_name}, {node_type})",
                        workflow=workflow_name,
                        node_type=node_type,
                    )
                seen_mappings[key] = provider

    return errors
