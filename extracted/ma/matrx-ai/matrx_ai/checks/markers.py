"""Planted markers: minted per result, substituted where a case writes ``[[marker:NAME]]``.

The variable rule never sees this syntax: markers are replaced in the case's inputs before
anything is sent, so the agent receives plain text.
"""

from __future__ import annotations

import hashlib
import re
from typing import Any

__all__ = ["MARKER_TOKEN", "markers_in", "mint_markers", "substitute_markers"]

MARKER_TOKEN = re.compile(r"\[\[marker:([A-Za-z0-9_\-]+)\]\]")


def mint_markers(names: list[str], *, seed: str) -> dict[str, str]:
    """Deterministic per (seed, name), unique per result when the seed is the result's identity."""
    out: dict[str, str] = {}
    for name in names:
        digest = hashlib.sha256(f"{seed}:{name}".encode()).hexdigest()[:8].upper()
        out[name] = f"{re.sub(r'[^A-Z0-9]', '', name.upper())[:6] or 'MK'}-{digest}"
    return out


def markers_in(value: Any) -> set[str]:
    """Every marker NAME written as ``[[marker:NAME]]`` anywhere inside ``value``."""
    found: set[str] = set()
    if isinstance(value, str):
        found.update(MARKER_TOKEN.findall(value))
    elif isinstance(value, dict):
        for k, v in value.items():
            found |= markers_in(k) | markers_in(v)
    elif isinstance(value, list | tuple):
        for v in value:
            found |= markers_in(v)
    return found


def substitute_markers(value: Any, markers: dict[str, str]) -> Any:
    """Replace every ``[[marker:NAME]]``; an unknown name raises (a case never sends a raw token)."""
    if isinstance(value, str):

        def _sub(m: re.Match[str]) -> str:
            name = m.group(1)
            if name not in markers:
                raise KeyError(f"marker {name!r} is written in the case but was not minted")
            return markers[name]

        return MARKER_TOKEN.sub(_sub, value)
    if isinstance(value, dict):
        return {k: substitute_markers(v, markers) for k, v in value.items()}
    if isinstance(value, list):
        return [substitute_markers(v, markers) for v in value]
    return value
