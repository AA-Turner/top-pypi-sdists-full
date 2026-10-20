"""Skill-reading bounds — host-bound `platform.feature_knob` values (feature ``agents.context``).

Authority: ``common-docs/policies/limits-are-knobs-agents-set-them.md``. This package must not
import aidream, so the host injects a ONE-ARGUMENT reader (``key -> value``) here (aidream binds
``knob_raw_sync("agents.context", key)`` in ``package_integration``) and every read goes through
it, live. With no host bound the package answers with the value the row was seeded with, which
the call site declares as a ``KNOB MIRROR`` naming the row; that is announced once per process.

Rows (feature ``agents.context``): ``skill_outline_min_chars`` (4000), ``skill_preamble_outline_entries``
(24), ``skill_preamble_outline_chars`` (900), ``skill_get_outline_rows`` (200), ``skill_set_max_depth`` (8).
"""

from __future__ import annotations

import sys
from collections.abc import Callable
from typing import Any

FEATURE = "agents.context"

_reader: Callable[[str], Any] | None = None
_announced = False
_failed: set[str] = set()


def configure_skill_knobs(reader: Callable[[str], Any] | None) -> None:
    """Bind the host's reader (``key -> value`` for feature ``agents.context``); ``None`` unbinds."""
    global _reader, _announced
    _reader = reader
    _announced = False
    _failed.clear()


def skill_knob_int(key: str, mirror: int) -> int:
    """The live value of ``agents.context.<key>`` through the host, or the declared mirror."""
    global _announced
    if _reader is None:
        if not _announced:
            _announced = True
            print(
                "[matrx_ai] no host knob reader bound for skill reading ('agents.context'); using "
                "the package's mirrored defaults (bind one with configure_skill_knobs())",
                file=sys.stderr,
            )
        return mirror
    try:
        return int(_reader(key))
    except Exception as exc:  # noqa: BLE001 — announced once per key, never a crashed turn
        if key not in _failed:
            _failed.add(key)
            print(
                f"[matrx_ai] host knob reader failed for {FEATURE!r}.{key!r}: {exc!r}; using the "
                f"mirrored default {mirror!r} until the host primes the feature",
                file=sys.stderr,
            )
        return mirror


def outline_min_chars() -> int:
    return skill_knob_int("skill_outline_min_chars", 4000)  # KNOB MIRROR agents.context.skill_outline_min_chars


def preamble_outline_entries() -> int:
    return skill_knob_int("skill_preamble_outline_entries", 24)  # KNOB MIRROR agents.context.skill_preamble_outline_entries


def preamble_outline_chars() -> int:
    return skill_knob_int("skill_preamble_outline_chars", 900)  # KNOB MIRROR agents.context.skill_preamble_outline_chars


def get_outline_rows() -> int:
    return skill_knob_int("skill_get_outline_rows", 200)  # KNOB MIRROR agents.context.skill_get_outline_rows


def set_max_depth() -> int:
    return skill_knob_int("skill_set_max_depth", 8)  # KNOB MIRROR agents.context.skill_set_max_depth


def skill_bodies_budget() -> int:
    """Whole-body budget for attached skills (the one knob a continuation turn also uses)."""
    return skill_knob_int("skill_bodies_budget_chars", 30000)  # KNOB MIRROR agents.context.skill_bodies_budget_chars
