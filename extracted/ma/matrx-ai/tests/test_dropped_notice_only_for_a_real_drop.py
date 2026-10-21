"""L48 defect 78: a "dropped" notice names a key whose value is NOT on the wire.

Live 2026-10-19/20 (PB-03 Gemini copies): ``include_thoughts=True`` was reported
``dropped`` ("had no effect on this model") while ``thinking_config.include_thoughts: true``
was on the wire. Cause: ``_account_consumed`` re-runs the processor without the key, and
the cell's own ``default_include_thoughts`` produced the same request, so equal-wire was
read as "dropped". A key whose value rides (as itself or via a default that equals it) was
SENT, not dropped.

Guard: over every Gemini thinking mode (legacy + gemini_3) and every subset of the
kitchen sink's competing thinking keys, no ``dropped`` Adjustment may name a key whose
caller value is present at a wire leaf carrying its meaning.
"""

from __future__ import annotations

import copy
import itertools
import json
from typing import Any

import pytest

from matrx_ai.catalog.wire_meaning import leaves, meaning_paths

import test_settings_never_silent_pb03 as pb03

THINKING_KEYS = ("reasoning_effort", "thinking_budget", "thinking_level", "include_thoughts")


def _leaf_values(params: dict[str, Any], key: str) -> list[Any]:
    flat = dict(leaves(params))
    return [flat[p] for p in meaning_paths(params, key) if p in flat]


def _rules(mode: str) -> dict[str, Any]:
    rules = copy.deepcopy(pb03._offerings()["google_gemini_flash_lite_latest"]["rules"])
    rules["reasoning_effort"]["processor_config"]["mode"] = mode
    return rules


def false_drops(mode: str, present: tuple[str, ...]) -> list[str]:
    controls = pb03._controls(_rules(mode))
    saved = dict(pb03.KITCHEN_SINK)
    try:
        for k in THINKING_KEYS:
            if k not in present:
                pb03.KITCHEN_SINK.pop(k, None)
        params, adjustments = pb03.run_kitchen_sink(controls)
        sink = dict(pb03.KITCHEN_SINK)
    finally:
        pb03.KITCHEN_SINK.clear()
        pb03.KITCHEN_SINK.update(saved)
    out: list[str] = []
    for a in adjustments:
        if a.action != "dropped" or a.key not in THINKING_KEYS:
            continue
        if sink.get(a.key) in _leaf_values(params, a.key):
            out.append(f"{mode}/{present}: {a.key}={sink[a.key]!r} reported dropped but its value is on the wire")
    return out


SUBSETS = [
    c for n in range(len(THINKING_KEYS) + 1) for c in itertools.combinations(THINKING_KEYS, n)
]


@pytest.mark.parametrize("mode", ["legacy", "gemini_3"])
def test_no_dropped_notice_for_a_value_that_rides(mode: str) -> None:
    problems = [p for subset in SUBSETS for p in false_drops(mode, subset)]
    assert problems == []
