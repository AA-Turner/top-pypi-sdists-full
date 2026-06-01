"""Local deploy YAML key check used before env substitution."""

from typing import Any

import yaml

DEPLOY_YAML_SCHEMA: dict[str, object] = {
    "id": None,
    "name": None,
    "runtime": None,
    "build": {
        "dockerfile": None,
        "context": None,
        "platform": None,
        "args": None,
        "target": None,
    },
    "image": None,
    "service": {
        "port": None,
        "path": None,
        "expose": None,
    },
    "infrastructure": {
        "cpu": None,
        "memory": None,
        "platform": None,
        "enable_db": None,
    },
    "env": None,
}


def validate_deploy_yaml_keys(yaml_content: str) -> None:
    """Reject runlayer.yaml keys that the backend deploy schema will not use."""
    try:
        data = yaml.safe_load(yaml_content)
    except yaml.YAMLError as e:
        raise ValueError(f"Invalid YAML syntax: {e}")

    if not data:
        raise ValueError("Configuration file is empty")
    if not isinstance(data, dict):
        raise ValueError("Configuration file root must be a mapping")

    _validate_keys(data, DEPLOY_YAML_SCHEMA, ())


def _validate_keys(
    data: dict[Any, Any],
    schema: dict[Any, Any],
    path: tuple[str, ...],
) -> None:
    for key, value in data.items():
        key_name = str(key)
        child_schema = schema.get(key_name)

        if key_name not in schema:
            key_path = ".".join((*path, key_name))
            allowed_keys = ", ".join(schema)
            raise ValueError(
                f"Unsupported runlayer.yaml key: {key_path}\n"
                f"Allowed keys here: {allowed_keys}"
            )

        if isinstance(child_schema, dict) and isinstance(value, dict):
            _validate_keys(value, child_schema, (*path, key_name))
