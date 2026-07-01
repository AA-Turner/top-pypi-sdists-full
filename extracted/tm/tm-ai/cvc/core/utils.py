"""
cvc.core.utils — small CVC-native utility helpers (Phase 1A native port).

Common file/env/url helpers used across CVC modules. Type-hinted, fully
covered by tests, and free of any vendored dependency.

Scope (Phase 1A):
    - Atomic file operations (replace / json / yaml round-trip)
    - Defensive JSON loader
    - Env-var coercion helpers
    - Proxy URL normalization
    - Base-URL host matching

Out of scope (Phase 1B+):
    - Tooling-specific utilities (LLM clients, OAuth, prompts, etc.)
"""

from __future__ import annotations

import json
import os
import re
import shutil
import tempfile
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterator, Optional, Union
from urllib.parse import urlparse

import yaml

__all__ = [
    "is_truthy_value",
    "env_var_enabled",
    "atomic_replace",
    "atomic_json_write",
    "atomic_yaml_write",
    "atomic_roundtrip_yaml_update",
    "safe_json_loads",
    "env_int",
    "env_bool",
    "normalize_proxy_url",
    "normalize_proxy_env_vars",
    "base_url_hostname",
    "base_url_host_matches",
]


# ---------------------------------------------------------------------------
# Env-var coercion
# ---------------------------------------------------------------------------

_TRUTHY = frozenset({"1", "true", "yes", "on", "y", "t"})
_FALSY = frozenset({"0", "false", "no", "off", "n", "f", ""})


def is_truthy_value(value: Any, default: bool = False) -> bool:
    """Return ``True``/``False`` for the most common truthy string spellings.

    Accepts booleans as-is. Accepts strings case-insensitively. Anything
    outside the known set returns *default* (defaults to ``False``).
    """
    if isinstance(value, bool):
        return value
    if value is None:
        return default
    s = str(value).strip().lower()
    if s in _TRUTHY:
        return True
    if s in _FALSY:
        return False
    return default


def env_var_enabled(name: str, default: str = "") -> bool:
    """Read an env-var and return whether it is enabled (truthy).

    Falls back to *default* when the variable is unset/empty.
    """
    raw = os.environ.get(name, default)
    if not raw:
        return False
    return is_truthy_value(raw, default=False)


def env_int(key: str, default: int = 0) -> int:
    """Read an env-var and coerce to ``int``. Returns *default* on failure."""
    raw = os.environ.get(key, "").strip()
    if not raw:
        return default
    try:
        return int(raw)
    except ValueError:
        return default


def env_bool(key: str, default: bool = False) -> bool:
    """Read an env-var and coerce to ``bool`` via :func:`is_truthy_value`."""
    raw = os.environ.get(key, "").strip()
    if not raw:
        return default
    return is_truthy_value(raw, default=default)


# ---------------------------------------------------------------------------
# Atomic file operations
# ---------------------------------------------------------------------------

@contextmanager
def _atomic_open(dir_path: Union[str, Path], prefix: str, suffix: str) -> Iterator[tuple[int, str]]:
    """Yield ``(fd, tmp_path)`` for an atomic write; closes and cleans up on error."""
    dir_path = str(dir_path)
    os.makedirs(dir_path, exist_ok=True)
    fd, tmp_path = tempfile.mkstemp(dir=dir_path, prefix=prefix, suffix=suffix)
    try:
        yield fd, tmp_path
    except BaseException:
        try:
            os.close(fd)
        except OSError:
            pass
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise


def atomic_replace(tmp_path: Union[str, Path], target: Union[str, Path]) -> str:
    """Atomically replace *target* with *tmp_path* (rename(2)).

    Creates parent directories of *target* if needed. Returns the final
    absolute path of *target* as a string.
    """
    target = Path(target)
    target.parent.mkdir(parents=True, exist_ok=True)
    os.replace(str(tmp_path), str(target))
    return str(target)


def atomic_json_write(
    target: Union[str, Path],
    data: Any,
    *,
    indent: int = 2,
    sort_keys: bool = True,
    ensure_ascii: bool = False,
) -> str:
    """Atomically write *data* as pretty-printed JSON to *target*."""
    target = Path(target)
    with _atomic_open(target.parent, prefix=f".{target.name}_", suffix=".tmp") as (fd, tmp_path):
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=indent, sort_keys=sort_keys, ensure_ascii=ensure_ascii)
            f.flush()
            os.fsync(f.fileno())
    return atomic_replace(tmp_path, target)


def atomic_yaml_write(target: Union[str, Path], data: Any) -> str:
    """Atomically write *data* as YAML to *target*.

    Uses ``default_flow_style=False`` and ``sort_keys=True`` for stable
    diffs across runs.
    """
    target = Path(target)
    with _atomic_open(target.parent, prefix=f".{target.name}_", suffix=".tmp") as (fd, tmp_path):
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            yaml.safe_dump(
                data,
                f,
                default_flow_style=False,
                sort_keys=True,
                allow_unicode=True,
            )
            f.flush()
            os.fsync(f.fileno())
    return atomic_replace(tmp_path, target)


def atomic_roundtrip_yaml_update(
    target: Union[str, Path],
    mutator,
    *,
    default: Any = None,
) -> Any:
    """Read-modify-write a YAML file atomically.

    *mutator* receives the current parsed YAML value (or *default* if the
    file is missing/unreadable) and returns the new value. The new value
    is written back atomically and returned.
    """
    target = Path(target)
    if target.exists():
        try:
            with open(target, encoding="utf-8") as f:
                current = yaml.safe_load(f)
        except (OSError, yaml.YAMLError):
            current = default
    else:
        current = default
    new_value = mutator(current)
    atomic_yaml_write(target, new_value)
    return new_value


# ---------------------------------------------------------------------------
# Defensive JSON
# ---------------------------------------------------------------------------

def safe_json_loads(text: str, default: Any = None) -> Any:
    """Parse *text* as JSON, returning *default* on any failure.

    Treats ``""`` and ``"null"`` as ``default`` (which defaults to ``None``).
    """
    if text is None:
        return default
    if not isinstance(text, str):
        return default
    stripped = text.strip()
    if not stripped or stripped == "null":
        return default
    try:
        return json.loads(stripped)
    except (ValueError, TypeError):
        return default


# ---------------------------------------------------------------------------
# Proxy / URL helpers
# ---------------------------------------------------------------------------

def normalize_proxy_url(proxy_url: Optional[str]) -> Optional[str]:
    """Return a normalized proxy URL with scheme://host:port shape.

    Pass-through for ``None`` and empty strings. Strips whitespace and
    trailing slashes.
    """
    if not proxy_url:
        return None
    cleaned = proxy_url.strip().rstrip("/")
    if not cleaned:
        return None
    # Add scheme if missing — assume http
    if "://" not in cleaned:
        cleaned = f"http://{cleaned}"
    return cleaned


def normalize_proxy_env_vars() -> None:
    """Normalize ``HTTP_PROXY``/``HTTPS_PROXY``/``NO_PROXY`` env vars in place.

    Lowercases the variable names (httpx respects lowercase) and strips
    trailing whitespace/slashes.
    """
    for name in ("HTTP_PROXY", "HTTPS_PROXY", "NO_PROXY"):
        val = os.environ.get(name)
        if val is None:
            continue
        cleaned = val.strip()
        if name != "NO_PROXY":
            cleaned = normalize_proxy_url(cleaned) or ""
        os.environ[name] = cleaned
        # Mirror to lowercase (httpx and most libs prefer lowercase)
        os.environ[name.lower()] = cleaned
        # Drop uppercase mirror if it was different from the env-var name
        if name == name.lower():
            continue


def base_url_hostname(base_url: str) -> str:
    """Return the hostname (lowercased, no port) of *base_url*.

    Returns ``""`` for empty/invalid input.
    """
    if not base_url:
        return ""
    cleaned = base_url.strip()
    if "://" not in cleaned:
        cleaned = f"http://{cleaned}"
    try:
        return (urlparse(cleaned).hostname or "").lower()
    except (ValueError, TypeError):
        return ""


def base_url_host_matches(base_url: str, domain: str) -> bool:
    """Return ``True`` if *base_url*'s hostname is *domain* or a subdomain of it.

    Comparison is case-insensitive. Empty *base_url* or *domain* returns
    ``False``.
    """
    host = base_url_hostname(base_url)
    if not host or not domain:
        return False
    domain = domain.lower().lstrip(".")
    return host == domain or host.endswith(f".{domain}")
