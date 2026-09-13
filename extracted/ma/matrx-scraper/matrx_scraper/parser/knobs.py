"""Parser thresholds — host-bound `platform.feature_knob` values (feature ``knowledge.scraper``).

Authority: ``common-docs/policies/limits-are-knobs-agents-set-them.md`` (Arman,
2026-08-20) and USD-5 (2026-09-10): a behavioural value is a registry row an
admin turns, never a constant nobody can see. This package must not import
aidream, so the host injects a ONE-ARGUMENT reader (``key -> value``) here —
aidream binds ``knob_*_sync("knowledge.scraper", key)`` in ``package_integration`` —
and every read below goes through it, live, so turning the row takes effect
within the host's knob cache TTL and no deploy.

Standalone posture: with no host bound, each read answers with the package's
own default, which the call site declares beside a ``KNOB MIRROR`` comment
naming the registry row. That mirror is the standalone contract, not a silent
fallback: it is the value the row was seeded with, and it is announced once
per process so a host that forgot to bind is never mistaken for one that did.
"""

from __future__ import annotations

import sys
from collections.abc import Callable
from typing import Any

FEATURE = "knowledge.scraper"

_reader: Callable[[str], Any] | None = None
_announced = False
_failed: set[str] = set()


def configure_parser_knobs(reader: Callable[[str], Any] | None) -> None:
    """Bind the host's reader (``key -> value`` for feature ``knowledge.scraper``).
    ``None`` unbinds it, restoring the standalone posture."""
    global _reader, _announced
    _reader = reader
    _announced = False
    _failed.clear()


def parser_knob(key: str, mirror: Any) -> Any:
    """The live value of ``knowledge.scraper.<key>`` through the host, or the declared
    mirror when no host is bound (announced once)."""
    global _announced
    if _reader is None:
        if not _announced:
            _announced = True
            print(
                "[matrx_scraper] no host knob reader bound for 'knowledge.scraper'; using the "
                "package's mirrored defaults (bind one with configure_parser_knobs())",
                file=sys.stderr,
            )
        return mirror
    try:
        return _reader(key)
    except Exception as exc:  # noqa: BLE001 — announced, never a crashed parse
        # The host is bound but cannot answer (typically a process that never
        # primed its knob snapshot). Say so once per key, with the remedy, and
        # keep the declared mirror rather than failing the caller's work.
        if key not in _failed:
            _failed.add(key)
            print(
                f"[matrx_scraper] host knob reader failed for {FEATURE!r}.{key!r}: {exc!r}; "
                f"using the mirrored default {mirror!r} until the host primes the "
                f"feature (aidream: prime_knob_features(*SYNC_READ_FEATURES))",
                file=sys.stderr,
            )
        return mirror


__all__ = ["FEATURE", "configure_parser_knobs", "parser_knob"]
