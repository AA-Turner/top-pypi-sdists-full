"""Package knobs — any ``platform.feature_knob`` value matrx-ai reads, through ONE host-bound reader.

Authority: ``common-docs/policies/limits-are-knobs-agents-set-them.md`` — a limit is a registry row an
admin turns, never a constant. This package must not import aidream, so the host injects a TWO-argument
reader (``(feature, key) -> value``; aidream binds ``knob_raw_sync`` in ``package_integration`` and primes
each feature in ``SYNC_READ_FEATURES``). Every read below goes through it, live.

The per-feature seams that came first (``tools.knobs``, ``catalog.knobs``, ``skills.knobs`` …) keep their
one-argument shape; a NEW matrx-ai knob reads here instead of growing another seam.

Standalone posture: with no host bound, each read answers with the mirror its call site declares beside
a ``KNOB MIRROR`` comment naming the row, announced once per process. A bound host whose row is MISSING
files ``feature_knob_missing`` and uses the mirror (``knob_or_declared_default_sync``); any other read
failure is announced once per key and uses the mirror — never a crashed call.
"""

from __future__ import annotations

import sys
from collections.abc import Callable
from typing import Any

from matrx_utils.knob_fallback import knob_or_declared_default_sync

_reader: Callable[[str, str], Any] | None = None
_announced = False
_failed: set[tuple[str, str]] = set()


def configure_package_knobs(reader: Callable[[str, str], Any] | None) -> None:
    """Bind the host's ``(feature, key) -> value`` reader; ``None`` unbinds (the standalone posture)."""
    global _reader, _announced
    _reader = reader
    _announced = False
    _failed.clear()


def package_knob(feature: str, key: str, mirror: Any) -> Any:
    """The live value of ``<feature>.<key>`` through the host, or the declared mirror (announced)."""
    global _announced
    reader = _reader
    if reader is None:
        if not _announced:
            _announced = True
            print(
                "[matrx_ai] no host knob reader bound for package knobs; using the package's mirrored "
                "defaults (bind one with matrx_ai.knobs.configure_package_knobs())",
                file=sys.stderr,
            )
        return mirror
    try:
        return knob_or_declared_default_sync(
            lambda: reader(feature, key),
            feature=feature,
            key=key,
            declared_default=mirror,
            consequence=f"matrx-ai uses its built-in value {mirror!r} for {feature}.{key}.",
        )
    except Exception as exc:  # noqa: BLE001 — announced, never a crashed call
        if (feature, key) not in _failed:
            _failed.add((feature, key))
            print(
                f"[matrx_ai] host knob reader failed for {feature!r}.{key!r}: {exc!r}; using the mirrored "
                f"default {mirror!r} (aidream: is {feature!r} in SYNC_READ_FEATURES?)",
                file=sys.stderr,
            )
        return mirror


def package_knob_number[N: (int, float)](feature: str, key: str, mirror: N, *, low: N, high: N) -> N:
    """A numeric knob, clamped into ``low..high``; a value that is not a number answers the mirror."""
    raw = package_knob(feature, key, mirror)
    try:
        value = float(str(raw).strip().strip('"'))
    except (TypeError, ValueError):
        return mirror
    value = min(max(value, float(low)), float(high))
    return int(round(value)) if isinstance(mirror, int) else value  # type: ignore[return-value]


__all__ = ["configure_package_knobs", "package_knob", "package_knob_number"]
