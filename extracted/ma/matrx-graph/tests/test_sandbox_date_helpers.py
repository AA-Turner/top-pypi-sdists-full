"""Date arithmetic in expressions: ``seconds_between`` and ``add_seconds``.

The class: a step needs "how long between two times" or "this time plus an offset" — a recording's
length from its row, each transcript segment's start (recording start + offset), elapsed [mm:ss] in a
meeting, a deadline from a setting. No expression or ``datetime.*`` step could do either per item.
"""

from __future__ import annotations

import pytest

from matrx_graph.nodes._sandbox import safe_eval
from matrx_graph.errors import ExecutionError


def test_seconds_between_two_times() -> None:
    assert safe_eval("seconds_between(inputs['a'], inputs['b'])",
                     {"a": "2026-10-28T08:00:00Z", "b": "2026-10-28T08:01:30.500Z"}) == 90.5
    assert safe_eval("seconds_between(inputs['b'], inputs['a'])",
                     {"a": "2026-10-28T08:00:00+00:00", "b": "2026-10-28T09:00:00+01:00"}) == 0.0
    assert safe_eval("seconds_between(inputs['a'], inputs['b'])", {"a": None, "b": "2026-10-28T08:00:00Z"}) is None


def test_add_seconds_per_item_in_one_expression() -> None:
    out = safe_eval(
        "[add_seconds(inputs['origin'], s['start']) for s in inputs['segments']]",
        {"origin": "2026-10-28T08:00:00+00:00", "segments": [{"start": 0}, {"start": 61.25}, {"start": -1}]},
    )
    assert out == ["2026-10-28T08:00:00+00:00", "2026-10-28T08:01:01.250000+00:00", "2026-10-28T07:59:59+00:00"]
    assert safe_eval("add_seconds(inputs['t'], 5)", {"t": None}) is None


def test_bad_values_fail_loudly_never_guess() -> None:
    with pytest.raises(ExecutionError):
        safe_eval("add_seconds(inputs['t'], 'five')", {"t": "2026-10-28T08:00:00Z"})
    with pytest.raises(ExecutionError):
        safe_eval("seconds_between(inputs['a'], inputs['b'])", {"a": "not a date", "b": "2026-10-28T08:00:00Z"})
    with pytest.raises(ExecutionError):  # one with a timezone, one without: no silent guess
        safe_eval("seconds_between(inputs['a'], inputs['b'])", {"a": "2026-10-28T08:00:00", "b": "2026-10-28T08:00:00Z"})
