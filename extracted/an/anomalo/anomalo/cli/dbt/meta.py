from __future__ import annotations

from typing import Any, Dict, Tuple

from ..state.errors import StateMachineError


# Settings live as flat `anomalo_*` keys in a node's `meta`. dbt merges `meta` one key
# deep, so a nested `anomalo:` block set on a model would replace the one set for its
# folder in dbt_project.yml, silently dropping the folder's `enable_data_quality: true`.
# Flat keys merge independently.
META_PREFIX = "anomalo_"
NODE_SETTING_TYPES: Dict[str, Tuple[type, ...]] = {
    "enable_data_quality": (bool,),
    "enable_observability": (bool,),
    "notify": (list,),
    "run_at": (str,),
    "time_column": (str, type(None)),
    "time_column_type": (str,),
    "warehouse": (str,),
}
PRIORITIES = ("high", "low", "normal")
SCOPES = ("full_table", "latest_day")
TEST_SETTING_TYPES: Dict[str, Tuple[type, ...]] = {
    "notify": (list,),
    "priority": (str,),
    "ref": (str,),
    "scope": (str,),
    "table": (str,),
}


class InvalidAnomaloSetting(StateMachineError):
    def __init__(self, node: Dict[str, Any], key: str, details: str) -> None:
        self.location = node.get("original_file_path") or node.get("unique_id", "")
        self.node_name = node.get("name", "")
        self.key = key
        self.details = details

    def __str__(self) -> str:
        return f"{self.location} ({self.node_name}): meta key {self.key} {self.details}"


def node_settings(node: Dict[str, Any]) -> Dict[str, Any]:
    return _settings(node, NODE_SETTING_TYPES)


def dbt_test_settings(node: Dict[str, Any]) -> Dict[str, Any]:
    settings = _settings(node, TEST_SETTING_TYPES)
    if settings.get("priority", "normal") not in PRIORITIES:
        raise InvalidAnomaloSetting(
            node, f"{META_PREFIX}priority", f"must be one of {', '.join(PRIORITIES)}"
        )
    if settings.get("scope", "full_table") not in SCOPES:
        raise InvalidAnomaloSetting(
            node, f"{META_PREFIX}scope", f"must be one of {', '.join(SCOPES)}"
        )
    return settings


def _settings(
    node: Dict[str, Any], types: Dict[str, Tuple[type, ...]]
) -> Dict[str, Any]:
    """The node's `anomalo_*` meta keys with the prefix stripped, after validation."""
    meta = (node.get("config") or {}).get("meta") or {}
    settings: Dict[str, Any] = {}
    for key, value in meta.items():
        if not key.startswith(META_PREFIX):
            continue
        name = key[len(META_PREFIX) :]
        if name not in types:
            known = ", ".join(f"{META_PREFIX}{known_name}" for known_name in types)
            raise InvalidAnomaloSetting(
                node, key, f"is not a setting here; use one of {known}"
            )
        if not isinstance(value, types[name]):
            expected = " or ".join(_type_name(t) for t in types[name])
            raise InvalidAnomaloSetting(node, key, f"must be {expected}")
        if name == "notify" and not all(isinstance(item, str) for item in value):
            raise InvalidAnomaloSetting(node, key, "must be a list of strings")
        settings[name] = value
    return settings


def _type_name(expected: type) -> str:
    return {
        bool: "true or false",
        list: "a list",
        str: "a string",
        type(None): "null",
    }[expected]
