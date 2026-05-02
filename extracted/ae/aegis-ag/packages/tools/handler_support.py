"""Shared helper utilities for built-in tool handlers."""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from .runtime import ToolInvocation


def tool_summary(
    invocation: ToolInvocation,
    summary: str,
    *,
    side_effects: tuple[str, ...] = ("tool",),
    outcome: str = "success",
) -> Mapping[str, Any]:
    return {
        "execution_id": invocation.invocation_id,
        "summary": summary,
        "outcome": outcome,
        "side_effects": side_effects,
    }


def coerce_bool(value: Any, *, default: bool) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes", "on"}


def coerce_optional_bool(value: Any) -> bool | None:
    if value is None:
        return None
    if isinstance(value, bool):
        return value
    normalized = str(value).strip().lower()
    if normalized in {"true", "1", "yes", "on"}:
        return True
    if normalized in {"false", "0", "no", "off"}:
        return False
    return None


def coerce_int(value: Any, *, default: int) -> int:
    if value is None:
        return default
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def coerce_env(value: Any) -> dict[str, str]:
    if not isinstance(value, Mapping):
        return {}
    return {str(key): str(item) for key, item in value.items()}


def coerce_choices(value: Any) -> tuple[str, ...]:
    if value is None:
        return ()
    if isinstance(value, str):
        return tuple(item.strip() for item in value.split("|") if item.strip())
    if isinstance(value, (list, tuple)):
        return tuple(str(item).strip() for item in value if str(item).strip())
    return ()


def optional_string(value: Any) -> str | None:
    if value is None:
        return None
    resolved = str(value).strip()
    return resolved or None


def truncate(value: str, *, limit: int = 1200) -> str:
    compact = value.strip()
    if len(compact) <= limit:
        return compact
    return compact[: max(0, limit - 1)].rstrip() + "…"


def join_parts(*parts: str) -> str:
    return "\n".join(part.strip() for part in parts if part and part.strip()).strip()


def resolve_workspace_path(
    root: Path,
    raw_path: str | None,
    *,
    must_exist: bool,
    allowed_roots: tuple[Path, ...] = (),
) -> Path:
    base = root.resolve()
    trusted_roots = _trusted_path_roots(base, allowed_roots)
    candidate = base if raw_path is None else Path(raw_path).expanduser()
    if not candidate.is_absolute():
        candidate = base / candidate
    resolved = candidate.resolve()
    if not any(resolved == trusted_root or trusted_root in resolved.parents for trusted_root in trusted_roots):
        allowed_display = ", ".join(str(item) for item in trusted_roots)
        raise ValueError(f"path is outside the allowed roots: {raw_path} (allowed: {allowed_display})")
    if must_exist and not resolved.exists():
        raise ValueError(f"path does not exist: {raw_path}")
    return resolved


def _trusted_path_roots(root: Path, allowed_roots: tuple[Path, ...]) -> tuple[Path, ...]:
    trusted: list[Path] = []
    for candidate in (root, *allowed_roots):
        resolved = candidate.expanduser().resolve()
        if resolved not in trusted:
            trusted.append(resolved)
    return tuple(trusted)


def normalized_url(value: str) -> str | None:
    candidate = value.strip().strip("\"'")
    if not candidate:
        return None
    parsed = urlparse(candidate)
    if not parsed.scheme:
        candidate = f"https://{candidate}"
        parsed = urlparse(candidate)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        return None
    return candidate


__all__ = [
    "coerce_bool",
    "coerce_choices",
    "coerce_env",
    "coerce_int",
    "coerce_optional_bool",
    "join_parts",
    "normalized_url",
    "optional_string",
    "resolve_workspace_path",
    "tool_summary",
    "truncate",
]
