"""JSON schema generation for Plato world configurations."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from plato.markers import FieldMarker, WorkspaceMarker

if TYPE_CHECKING:
    from plato.worlds.config import RunConfig


def _get_runtime_fields() -> set[str]:
    """Get field names from RunConfig that should be excluded from world schema."""
    from plato.worlds.config import RunConfig

    return set(RunConfig.model_fields.keys())


def get_field_annotations(config_cls: type[RunConfig]) -> dict[str, FieldMarker | WorkspaceMarker | None]:
    """Get FieldMarker annotations for each field.

    Args:
        config_cls: The RunConfig subclass to inspect

    Returns:
        Dict mapping field name to FieldMarker (or None if no marker)
    """
    result: dict[str, FieldMarker | WorkspaceMarker | None] = {}

    for field_name, field_info in config_cls.model_fields.items():
        marker = None

        for meta in field_info.metadata:
            if isinstance(meta, (FieldMarker, WorkspaceMarker)):
                marker = meta
                break

        result[field_name] = marker

    return result


def _collect_nested_agents(model_cls: type, prefix: str = "") -> list[dict[str, Any]]:
    """Recursively find Agent-annotated fields in nested pydantic models.

    Returns agent entries with dotted-path names (e.g. "backend_build.reviewer").
    """
    import typing

    from pydantic import BaseModel

    agents: list[dict[str, Any]] = []
    for field_name, field_info in model_cls.model_fields.items():
        marker = None
        for meta in field_info.metadata:
            if isinstance(meta, FieldMarker) and meta.kind == "agent":
                marker = meta
                break

        path = f"{prefix}.{field_name}" if prefix else field_name
        if marker is not None:
            agents.append(
                {
                    "name": path,
                    "description": marker.description,
                    "required": marker.required,
                }
            )
        else:
            # Recurse into nested BaseModel fields
            annotation = field_info.annotation
            # Unwrap Optional / Union types (handles both typing.Optional and X | None)
            origin = typing.get_origin(annotation)
            if origin is not None:
                args = typing.get_args(annotation)
                non_none = [a for a in args if a is not type(None)]
                if len(non_none) == 1:
                    annotation = non_none[0]
            if isinstance(annotation, type) and issubclass(annotation, BaseModel):
                agents.extend(_collect_nested_agents(annotation, prefix=path))
    return agents


def get_world_config_schema(config_cls: type[RunConfig]) -> dict[str, Any]:
    """Get JSON schema for a world config with agents, secrets, and envs separated.

    Args:
        config_cls: The RunConfig subclass to generate schema for

    Returns:
        JSON schema dict with properties, required, agents, secrets, and envs fields
    """
    full_schema = config_cls.model_json_schema()
    full_schema.pop("title", None)

    annotations = get_field_annotations(config_cls)
    properties = full_schema.get("properties", {})

    world_properties: dict[str, Any] = {}
    agents: list[dict[str, Any]] = []
    secrets: list[dict[str, Any]] = []
    envs: list[dict[str, Any]] = []
    workspaces: list[dict[str, Any]] = []
    env_list_field: dict[str, Any] | None = None

    # Skip runtime fields (derived from RunConfig base class)
    runtime_fields = _get_runtime_fields()

    for field_name, prop_schema in properties.items():
        if field_name in runtime_fields:
            continue

        marker = annotations.get(field_name)

        if marker is None:
            world_properties[field_name] = prop_schema
        elif isinstance(marker, FieldMarker) and marker.kind == "agent":
            agents.append(
                {
                    "name": field_name,
                    "description": marker.description,
                    "required": marker.required,
                }
            )
        elif isinstance(marker, FieldMarker) and marker.kind == "secret":
            secrets.append(
                {
                    "name": field_name,
                    "description": marker.description,
                    "required": marker.required,
                }
            )
        elif isinstance(marker, FieldMarker) and marker.kind == "env":
            # Get default value for this env field
            field_info = config_cls.model_fields.get(field_name)
            default_value = None
            if field_info and field_info.default is not None:
                default_env = field_info.default
                if hasattr(default_env, "model_dump"):
                    default_value = default_env.model_dump()
                elif isinstance(default_env, dict):
                    default_value = default_env

            envs.append(
                {
                    "name": field_name,
                    "description": marker.description,
                    "required": marker.required,
                    "default": default_value,
                }
            )
        elif isinstance(marker, WorkspaceMarker):
            workspaces.append(
                {
                    "name": field_name,
                    "description": marker.description,
                    "tracked": marker.tracked,
                }
            )
        elif isinstance(marker, FieldMarker) and marker.kind == "env_list":
            env_list_field = {
                "name": field_name,
                "description": marker.description,
            }

    # Collect agents from nested models (e.g. backend_build.reviewer)
    nested_agents = _collect_nested_agents(config_cls)
    # Add any nested agents not already found at top level
    top_level_names = {a["name"] for a in agents}
    for agent in nested_agents:
        if agent["name"] not in top_level_names:
            agents.append(agent)

    # Compute required fields (excluding runtime and annotated fields)
    required = [r for r in full_schema.get("required", []) if r not in runtime_fields and annotations.get(r) is None]

    result: dict[str, Any] = {
        "properties": world_properties,
        "required": required,
        "agents": agents,
        "secrets": secrets,
        "envs": envs,
    }

    # Include $defs if present (for nested type references)
    if "$defs" in full_schema:
        result["$defs"] = full_schema["$defs"]

    # Add env_list if present (for worlds with arbitrary environment lists)
    if env_list_field:
        result["env_list"] = env_list_field

    return result


def get_world_schema(world_cls: type, image: str | None = None) -> dict[str, Any]:
    """Get full schema for a world including config and secrets schemas.

    Args:
        world_cls: The BaseWorld subclass to generate schema for
        image: Optional Docker/VM image URL for the world

    Returns:
        Dict with config_schema, secrets_schema, and image fields (same format as agents)
    """
    config_class = world_cls.get_config_class()
    schema = get_world_config_schema(config_class)

    # Build config_schema (same format as agents)
    config_schema: dict[str, Any] = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "properties": schema.get("properties", {}),
        "required": schema.get("required", []),
    }
    if schema.get("$defs"):
        config_schema["$defs"] = schema["$defs"]

    # Convert secrets array to secrets_schema (same format as agents)
    secrets = schema.get("secrets", [])
    secrets_schema = None
    if secrets:
        secrets_schema = {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "type": "object",
            "properties": {s["name"]: {"type": "string", "description": s.get("description")} for s in secrets},
            "required": [s["name"] for s in secrets if s.get("required", False)],
        }

    return {
        "name": getattr(world_cls, "name", world_cls.__name__),
        "config_schema": config_schema,
        "secrets_schema": secrets_schema,
        "image": image,
        # World-specific fields (not in agents)
        "agents": schema.get("agents", []),
        "envs": schema.get("envs", []),
        "env_list": schema.get("env_list"),
    }
