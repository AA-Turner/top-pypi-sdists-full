"""Lightweight, shared profile-archive exclusion policy.

This module deliberately has no checkpoint-engine dependencies so the browser
worker can apply the same policy without importing the zstandard/crypto stack.
"""

from __future__ import annotations

from typing import Final

ARCHIVE_EXCLUDE_PREFIXES: Final[tuple[str, ...]] = (
    "Crashpad/",
    "GrShaderCache/",
    "ShaderCache/",
    "GPUCache/",
    "Code Cache/",
    "Default/Code Cache/",
    "Default/GPUCache/",
    "Default/Service Worker/CacheStorage/",
    "Default/Service Worker/ScriptCache/",
    "component_crx_cache/",
    "Default/optimization_guide",
    "Default/Cache/",
)
ARCHIVE_EXCLUDE_NAMES: Final[frozenset[str]] = frozenset(
    {"SingletonLock", "SingletonCookie", "SingletonSocket"}
)
ARCHIVE_EXCLUDE_SUFFIXES: Final[tuple[str, ...]] = (".lock",)


def is_profile_archive_path_excluded(rel_path: str) -> bool:
    """Return whether an archive-root-relative path is regenerable content."""
    name = rel_path.rsplit("/", 1)[-1]
    if name in ARCHIVE_EXCLUDE_NAMES:
        return True
    if any(name.endswith(suffix) for suffix in ARCHIVE_EXCLUDE_SUFFIXES):
        return True
    padded = f"/{rel_path}"
    for prefix in ARCHIVE_EXCLUDE_PREFIXES:
        segment = prefix.rstrip("/")
        if (
            rel_path.startswith(prefix)
            or f"/{segment}/" in f"{padded}/"
            or padded.startswith(f"/{segment}/")
        ):
            return True
    return False
