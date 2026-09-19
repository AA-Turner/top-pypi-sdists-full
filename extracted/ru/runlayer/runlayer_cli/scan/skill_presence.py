"""Durable host skill-presence state for removal reconciliation.

Only the complete host project/global scan phases participate. Container and
WSL removal reconciliation require namespace-specific state and are out of
scope. Candidate paths are hashed before serialization and are never persisted.

Standard-library + ``structlog`` only so this remains safe in the frozen
``aiwatch`` import closure.
"""

from __future__ import annotations

import hashlib
import json
import os
import tempfile
import threading
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Any, cast

import structlog

logger = structlog.get_logger(__name__)

SKILL_PRESENCE_FILENAME = "skill-presence.json"
STATE_VERSION = 1

_LOWERCASE_HEX = frozenset("0123456789abcdef")
_SAVE_LOCK = threading.Lock()


@dataclass(frozen=True)
class SkillPresenceParams:
    """Scan inputs that define which host paths a complete crawl covers.

    Only inputs belong here. Discovered project paths are crawl *output*: a
    deleted repository must still yield removals, so it must not reset the
    baseline.
    """

    project_depth: int
    home: str | None

    def to_dict(self) -> dict[str, Any]:
        return {
            "project_depth": self.project_depth,
            "home": self.home,
        }


@dataclass(frozen=True)
class SkillPresenceState:
    """Hashed candidate inventory for one complete host crawl."""

    params: SkillPresenceParams
    project_hashes: tuple[str, ...]
    global_hashes: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "version": STATE_VERSION,
            "params": self.params.to_dict(),
            "phases": {
                "project": list(self.project_hashes),
                "global": list(self.global_hashes),
            },
        }


def default_state_path() -> Path:
    """Return the per-user skill-presence state path."""
    return Path.home() / ".runlayer" / SKILL_PRESENCE_FILENAME


def _resolve_state_path(state_path: Path | None) -> Path:
    return state_path if state_path is not None else default_state_path()


def path_hash(path: str) -> str:
    """Hash one normalized reported path exactly like PostgreSQL ``md5(text)``.

    Crawl and ``os.walk`` paths carry ``surrogateescape`` code points for
    filename bytes that are not UTF-8; a strict encode raised on the first such
    path and aborted presence-state building for the whole scan. Encoding them
    back through ``surrogateescape`` recovers the on-disk bytes, so the hash is
    total and byte-faithful (identical to the strict encode for valid UTF-8).
    """
    return hashlib.md5(
        path.encode("utf-8", "surrogateescape"), usedforsecurity=False
    ).hexdigest()


def _sorted_hashes(paths: Iterable[str]) -> tuple[str, ...]:
    return tuple(sorted({path_hash(path) for path in paths}))


def build_state(
    params: SkillPresenceParams,
    *,
    project_paths: Iterable[str] = (),
    global_paths: Iterable[str] = (),
) -> SkillPresenceState:
    """Build deterministic state without retaining candidate paths."""
    return SkillPresenceState(
        params=params,
        project_hashes=_sorted_hashes(project_paths),
        global_hashes=_sorted_hashes(global_paths),
    )


def _parse_hashes(value: object) -> tuple[str, ...] | None:
    if not isinstance(value, list):
        return None
    hashes: list[str] = []
    for item in value:
        if (
            not isinstance(item, str)
            or len(item) != 32
            or any(character not in _LOWERCASE_HEX for character in item)
        ):
            return None
        hashes.append(item)
    normalized = tuple(sorted(set(hashes)))
    return normalized if tuple(hashes) == normalized else None


def _parse_state(value: object) -> SkillPresenceState | None:
    if not isinstance(value, dict):
        return None
    payload = cast(dict[str, object], value)
    if set(payload) != {"version", "params", "phases"}:
        return None
    version = payload.get("version")
    if type(version) is not int or version != STATE_VERSION:
        return None

    raw_params = payload.get("params")
    raw_phases = payload.get("phases")
    if not isinstance(raw_params, dict) or not isinstance(raw_phases, dict):
        return None
    params = cast(dict[str, object], raw_params)
    phases = cast(dict[str, object], raw_phases)
    if set(params) != {"project_depth", "home"} or set(phases) != {
        "project",
        "global",
    }:
        return None

    project_depth = params.get("project_depth")
    home = params.get("home")
    if (
        not isinstance(project_depth, int)
        or isinstance(project_depth, bool)
        or project_depth <= 0
        or (home is not None and (not isinstance(home, str) or not home))
    ):
        return None

    project_hashes = _parse_hashes(phases.get("project"))
    global_hashes = _parse_hashes(phases.get("global"))
    if project_hashes is None or global_hashes is None:
        return None
    return SkillPresenceState(
        params=SkillPresenceParams(project_depth=project_depth, home=home),
        project_hashes=project_hashes,
        global_hashes=global_hashes,
    )


def load_state(state_path: Path | None = None) -> SkillPresenceState | None:
    """Load valid state; missing, corrupt, or incompatible files are baselines."""
    try:
        payload = json.loads(
            _resolve_state_path(state_path).read_text(encoding="utf-8")
        )
        return _parse_state(payload)
    except Exception:
        return None


def save_state(
    state: SkillPresenceState,
    state_path: Path | None = None,
) -> bool:
    """Atomically persist state; return false on any best-effort write failure."""
    temporary_path: str | None = None
    descriptor: int | None = None
    try:
        path = _resolve_state_path(state_path)
        with _SAVE_LOCK:
            path.parent.mkdir(parents=True, exist_ok=True)
            descriptor, temporary_path = tempfile.mkstemp(
                dir=str(path.parent),
                prefix=f".{path.name}.",
                suffix=".tmp",
            )
            with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
                descriptor = None
                json.dump(
                    state.to_dict(),
                    handle,
                    sort_keys=True,
                    separators=(",", ":"),
                )
                handle.write("\n")
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temporary_path, path)
            temporary_path = None
        return True
    except Exception as exc:
        logger.warning(
            "skill_presence_state_save_failed",
            error_type=type(exc).__name__,
            exc_info=True,
        )
        return False
    finally:
        if descriptor is not None:
            try:
                os.close(descriptor)
            except OSError:
                pass
        if temporary_path is not None:
            try:
                os.unlink(temporary_path)
            except OSError:
                pass


def compute_removals(
    previous: SkillPresenceState | None,
    current: SkillPresenceState,
    *,
    crawl_complete: bool,
) -> list[str]:
    """Return hashes absent from a comparable complete host crawl."""
    if previous is None or not crawl_complete or previous.params != current.params:
        return []
    previous_hashes = set(previous.project_hashes) | set(previous.global_hashes)
    current_hashes = set(current.project_hashes) | set(current.global_hashes)
    return sorted(previous_hashes - current_hashes)
