"""JSON schema generation for Plato agent configurations."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from plato.markers import Secret

if TYPE_CHECKING:
    from plato.agents.config import AgentConfig


def get_field_secrets(config_cls: type[AgentConfig]) -> dict[str, Secret]:
    """Get Secret annotations for each field.

    Args:
        config_cls: The AgentConfig subclass to inspect

    Returns:
        Dict mapping field name to Secret annotation
    """
    result: dict[str, Secret] = {}

    for field_name, field_info in config_cls.model_fields.items():
        for meta in field_info.metadata:
            if isinstance(meta, Secret):
                result[field_name] = meta
                break

    return result


def get_agent_config_schema(config_cls: type[AgentConfig]) -> dict[str, Any]:
    """Get JSON schema for an agent config with secrets separated.

    Args:
        config_cls: The AgentConfig subclass to generate schema for

    Returns:
        JSON schema dict with properties, required, and secrets fields
    """
    full_schema = config_cls.model_json_schema()
    full_schema.pop("title", None)

    secrets_map = get_field_secrets(config_cls)
    properties = full_schema.get("properties", {})

    config_properties: dict[str, Any] = {}
    secrets: list[dict[str, Any]] = []

    for field_name, prop_schema in properties.items():
        if field_name in secrets_map:
            secret = secrets_map[field_name]
            secrets.append(
                {
                    "name": field_name,
                    "description": secret.description,
                    "required": secret.required,
                }
            )
        else:
            config_properties[field_name] = prop_schema

    required = [r for r in full_schema.get("required", []) if r not in secrets_map]

    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "properties": config_properties,
        "required": required,
        "secrets": secrets,
    }


def get_agent_schema(agent_cls: type, image: str | None = None) -> dict[str, Any]:
    """Get full schema for an agent including config and secrets schemas.

    Args:
        agent_cls: The BaseAgent subclass to generate schema for
        image: Optional Docker image URL for the agent

    Returns:
        Dict with config_schema, secrets_schema, and image fields
    """
    config_class = agent_cls.get_config_class()
    config_schema = get_agent_config_schema(config_class)

    # Extract secrets into separate schema
    secrets = config_schema.pop("secrets", [])
    secrets_schema = None
    if secrets:
        secrets_schema = {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "type": "object",
            "properties": {s["name"]: {"type": "string", "description": s.get("description")} for s in secrets},
            "required": [s["name"] for s in secrets if s.get("required", False)],
        }

    result = {
        "name": getattr(agent_cls, "_agent_name", agent_cls.__name__),
        "config_schema": config_schema,
        "secrets_schema": secrets_schema,
        "image": image,
    }

    # Include default runtime if the agent declares one
    default_runtime = getattr(agent_cls, "default_runtime", None)
    if default_runtime is not None:
        result["default_runtime"] = default_runtime.model_dump()

    return result
