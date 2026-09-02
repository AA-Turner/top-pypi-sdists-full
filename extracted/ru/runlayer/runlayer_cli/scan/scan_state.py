"""Persisted per-user scan rotation state.

A host can hold more artifacts or artifact content than one scan may retain.
To avoid permanently skipping the overflow, the scan persists path-keyed
artifact-window cursors and integer content offsets in
``~/.runlayer/scan-state.json``. Successive runs resume after those positions,
providing full coverage at the 15-minute scan cadence.

The state is a pure optimization: corrupt or missing state cold-starts from
the beginning of the sorted candidate list, and every write is best-effort —
a state failure must never fail a scan.

Standard-library + ``structlog`` only, so it stays importable inside the
frozen ``aiwatch`` bundle (guarded by ``tests/test_aiwatch_imports.py``).
"""

from __future__ import annotations

import json
import os
import tempfile
import threading
from bisect import bisect_right
from collections.abc import Sequence
from pathlib import Path

import structlog

from runlayer_cli.paths import get_runlayer_dir

logger = structlog.get_logger(__name__)

SCAN_STATE_FILENAME = "scan-state.json"

_STATE_VERSION = 1
# In-process only: overlapping scan processes may last-write-win and repeat a
# window. State is best-effort, so that is preferable to cross-process locking
# becoming another way for inventory scans to fail.
_SAVE_LOCK = threading.Lock()


def _resolve_state_path(state_path: Path | None) -> Path:
    if state_path is not None:
        return state_path
    return get_runlayer_dir() / SCAN_STATE_FILENAME


def _load_state(path: Path) -> dict:
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    if not isinstance(raw, dict) or raw.get("version") != _STATE_VERSION:
        return {}
    return raw


def load_cursor(category: str, state_path: Path | None = None) -> str | None:
    """Return the persisted rotation cursor for *category*, or ``None``."""
    state = _load_state(_resolve_state_path(state_path))
    cursors = state.get("cursors")
    if not isinstance(cursors, dict):
        return None
    cursor = cursors.get(category)
    return cursor if isinstance(cursor, str) else None


def load_content_offset(category: str, state_path: Path | None = None) -> int:
    """Return a non-negative content offset for *category*, defaulting to zero."""
    state = _load_state(_resolve_state_path(state_path))
    offsets = state.get("content_offsets")
    if not isinstance(offsets, dict):
        return 0
    offset = offsets.get(category)
    if not isinstance(offset, int) or isinstance(offset, bool) or offset < 0:
        return 0
    return offset


def _save_value(
    section: str,
    category: str,
    value: str | int | None,
    state_path: Path | None,
) -> None:
    """Atomically update one state value; best-effort, never raises."""
    try:
        path = _resolve_state_path(state_path)
        with _SAVE_LOCK:
            state = _load_state(path)
            values = state.get(section)
            if not isinstance(values, dict):
                values = {}
            else:
                values = dict(values)
            if value is None:
                values.pop(category, None)
            else:
                values[category] = value
            payload = dict(state)
            payload["version"] = _STATE_VERSION
            payload[section] = values

            path.parent.mkdir(parents=True, exist_ok=True)
            fd, tmp_name = tempfile.mkstemp(
                dir=str(path.parent), prefix=path.name, suffix=".tmp"
            )
            try:
                with os.fdopen(fd, "w", encoding="utf-8") as handle:
                    json.dump(payload, handle)
                os.replace(tmp_name, path)
            except OSError:
                try:
                    os.unlink(tmp_name)
                except OSError:
                    pass
                raise
    except Exception:
        logger.warning(
            "scan_state_save_failed",
            section=section,
            category=category,
            exc_info=True,
        )


def save_cursor(
    category: str, cursor: str | None, state_path: Path | None = None
) -> None:
    """Persist *cursor* for *category*; ``None`` clears it."""
    _save_value("cursors", category, cursor, state_path)


def save_content_offset(
    category: str, offset: int, state_path: Path | None = None
) -> None:
    """Persist a non-negative content offset for *category*."""
    _save_value("content_offsets", category, max(0, offset), state_path)


def rotation_window(
    keys: Sequence[str], cursor: str | None, limit: int
) -> tuple[list[str], str | None]:
    """Pick this run's window of *limit* keys, resuming after *cursor*.

    *keys* must be sorted. The window wraps to the start of the list when the
    cursor is near the end. Returns ``(window, new_cursor)``; ``new_cursor``
    is ``None`` when the window covered every key (nothing left to catch up).
    """
    keys = list(keys)
    if limit >= len(keys):
        return keys, None
    start = bisect_right(keys, cursor) if cursor is not None else 0
    window = keys[start : start + limit]
    if len(window) < limit:
        window += keys[: limit - len(window)]
    return window, window[-1]
