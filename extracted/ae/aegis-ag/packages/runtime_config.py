"""Global Aegis runtime configuration stored as a small YAML document."""

from __future__ import annotations

from collections.abc import Mapping
from copy import deepcopy
from pathlib import Path
import json
from typing import Any


GLOBAL_CONFIG_FILENAME = "config.yaml"


def global_config_path_for_database(database_path: str | Path) -> Path:
    state_dir = Path(database_path).parent
    if state_dir.name == "state":
        return state_dir.parent / GLOBAL_CONFIG_FILENAME
    return state_dir / GLOBAL_CONFIG_FILENAME


def default_global_config(*, state_dir: str | Path, profile_dir: str | Path) -> dict[str, Any]:
    return {
        "runtime": {
            "state_dir": str(state_dir),
            "profile_dir": str(profile_dir),
            "default_profile_id": "default",
        },
        "models": {
            "default_provider_source": "profile",
            "intent_mode": "balanced",
        },
        "sessions": {
            "persist_system_prompts": True,
            "persist_assistant_responses": True,
            "max_history_rows": 200,
        },
        "skills": {
            "enable_profile_overrides": True,
        },
        "tools": {
            "require_approval_for_risky": True,
        },
        "gateway": {
            "enabled": False,
            "state_dir": str(Path(state_dir) / "gateway"),
        },
        "dashboard": {
            "host": "127.0.0.1",
            "port": 4174,
        },
    }


def global_config_schema() -> list[dict[str, Any]]:
    return [
        {"path": "runtime.state_dir", "type": "string", "label": "State directory", "section": "Runtime"},
        {"path": "runtime.profile_dir", "type": "string", "label": "Profile directory", "section": "Runtime"},
        {"path": "runtime.default_profile_id", "type": "string", "label": "Default profile", "section": "Runtime"},
        {"path": "models.default_provider_source", "type": "string", "label": "Provider source", "section": "Models"},
        {"path": "models.intent_mode", "type": "string", "label": "Intent mode", "section": "Models"},
        {"path": "sessions.persist_system_prompts", "type": "boolean", "label": "Persist system prompts", "section": "Sessions"},
        {"path": "sessions.persist_assistant_responses", "type": "boolean", "label": "Persist assistant responses", "section": "Sessions"},
        {"path": "sessions.max_history_rows", "type": "number", "label": "Max history rows", "section": "Sessions"},
        {"path": "skills.enable_profile_overrides", "type": "boolean", "label": "Skill profile overrides", "section": "Skills"},
        {"path": "tools.require_approval_for_risky", "type": "boolean", "label": "Approval for risky tools", "section": "Tools"},
        {"path": "gateway.enabled", "type": "boolean", "label": "Gateway enabled", "section": "Gateway"},
        {"path": "gateway.state_dir", "type": "string", "label": "Gateway state directory", "section": "Gateway"},
        {"path": "dashboard.host", "type": "string", "label": "Dashboard host", "section": "Dashboard"},
        {"path": "dashboard.port", "type": "number", "label": "Dashboard port", "section": "Dashboard"},
    ]


def load_global_config(
    path: str | Path,
    *,
    state_dir: str | Path,
    profile_dir: str | Path,
) -> dict[str, Any]:
    defaults = default_global_config(state_dir=state_dir, profile_dir=profile_dir)
    config_path = Path(path)
    try:
        raw = config_path.read_text(encoding="utf-8")
    except OSError:
        return defaults
    loaded = parse_global_config_text(raw)
    if not isinstance(loaded, Mapping):
        return defaults
    return _deep_merge(defaults, loaded)


def read_global_config_text(path: str | Path, *, fallback: Mapping[str, Any]) -> str:
    config_path = Path(path)
    try:
        return config_path.read_text(encoding="utf-8")
    except OSError:
        return serialize_global_config(fallback)


def write_global_config(path: str | Path, config: Mapping[str, Any]) -> None:
    config_path = Path(path)
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(serialize_global_config(config), encoding="utf-8")


def parse_global_config_text(text: str) -> dict[str, Any]:
    stripped = text.strip()
    if not stripped:
        return {}
    if stripped.startswith("{"):
        parsed = json.loads(stripped)
        if not isinstance(parsed, dict):
            raise ValueError("config JSON must be an object")
        return parsed
    return _parse_simple_yaml(stripped)


def serialize_global_config(config: Mapping[str, Any]) -> str:
    lines: list[str] = []
    _write_yaml_mapping(lines, config, indent=0)
    return "\n".join(lines).rstrip() + "\n"


def _deep_merge(base: Mapping[str, Any], overlay: Mapping[str, Any]) -> dict[str, Any]:
    merged: dict[str, Any] = deepcopy(dict(base))
    for key, value in overlay.items():
        if isinstance(value, Mapping) and isinstance(merged.get(key), Mapping):
            merged[key] = _deep_merge(merged[key], value)
        else:
            merged[key] = deepcopy(value)
    return merged


def _parse_simple_yaml(text: str) -> dict[str, Any]:
    root: dict[str, Any] = {}
    stack: list[tuple[int, dict[str, Any]]] = [(-1, root)]
    for raw_line in text.splitlines():
        line_without_comment = raw_line.split("#", 1)[0].rstrip()
        if not line_without_comment.strip():
            continue
        indent = len(line_without_comment) - len(line_without_comment.lstrip(" "))
        if ":" not in line_without_comment:
            raise ValueError(f"invalid YAML line: {raw_line}")
        key, raw_value = line_without_comment.lstrip(" ").split(":", 1)
        key = key.strip()
        if not key:
            raise ValueError(f"invalid YAML key: {raw_line}")
        while stack and indent <= stack[-1][0]:
            stack.pop()
        if not stack:
            raise ValueError(f"invalid YAML indentation: {raw_line}")
        parent = stack[-1][1]
        value_text = raw_value.strip()
        if value_text == "":
            child: dict[str, Any] = {}
            parent[key] = child
            stack.append((indent, child))
        else:
            parent[key] = _parse_scalar(value_text)
    return root


def _parse_scalar(value: str) -> Any:
    if value in {"true", "True"}:
        return True
    if value in {"false", "False"}:
        return False
    if value in {"null", "None", "~"}:
        return None
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        return value[1:-1]
    if value.startswith(("{", "[")):
        return json.loads(value)
    try:
        return int(value)
    except ValueError:
        return value


def _write_yaml_mapping(lines: list[str], mapping: Mapping[str, Any], *, indent: int) -> None:
    prefix = " " * indent
    for key, value in mapping.items():
        if isinstance(value, Mapping):
            lines.append(f"{prefix}{key}:")
            _write_yaml_mapping(lines, value, indent=indent + 2)
        elif isinstance(value, list):
            lines.append(f"{prefix}{key}: {json.dumps(value, ensure_ascii=False)}")
        else:
            lines.append(f"{prefix}{key}: {_format_scalar(value)}")


def _format_scalar(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if value is None:
        return "null"
    if isinstance(value, (int, float)):
        return str(value)
    text = str(value)
    if not text or any(character in text for character in (":", "#", "{", "}", "[", "]", "\n")):
        return json.dumps(text, ensure_ascii=False)
    return text

