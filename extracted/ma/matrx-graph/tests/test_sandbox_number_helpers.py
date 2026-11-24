"""Guard (2026-11-10): the expression sandbox's number helpers ``log10`` and ``power``.

Research's video ranking (``research/video_ranking.py::score_video``) scores reach and channel on a log10 scale
and freshness as a half-life; its workflow twin (the triage offer's ``video_rank_score``) needs both in an
expression. ``**`` stays refused (a whole-number power can allocate without bound); ``power`` is a decimal power
with a bounded exponent.
"""

from __future__ import annotations

import math

import pytest

from matrx_graph.errors import ExecutionError
from matrx_graph.nodes._sandbox import safe_eval


def test_log10_matches_the_math_library_and_keeps_none():
    assert safe_eval("log10(inputs['v'] + 1)", {"v": 999_999}) == math.log10(1_000_000)
    assert safe_eval("log10(inputs['v'])", {"v": None}) is None


def test_power_is_a_decimal_power_like_the_half_life_the_code_uses():
    assert safe_eval("power(0.5, inputs['years'] / 3)", {"years": 1.5}) == 0.5**0.5
    assert safe_eval("power(inputs['b'], 2)", {"b": None}) is None


@pytest.mark.parametrize(
    "expr, inputs",
    [
        ("log10(0)", {}),
        ("log10(-1)", {}),
        ("log10('x')", {}),
        ("power(10, 5000)", {}),
        ("power(1e300, 2)", {}),
        ("power(-8, 0.5)", {}),
        ("power(True, 2)", {}),
    ],
)
def test_a_number_helper_given_what_has_no_answer_says_so(expr, inputs):
    with pytest.raises(ExecutionError):
        safe_eval(expr, inputs)


def test_double_star_is_still_refused():
    with pytest.raises(ExecutionError):
        safe_eval("2 ** 10", {})


def test_an_enormous_whole_number_is_a_named_error_never_a_raw_overflow() -> None:
    """Review 2026-11-10 finding 8: ``float(10**400)`` raised a raw OverflowError out of power/log10."""
    huge = 10**400
    with pytest.raises(ExecutionError, match="power"):
        safe_eval("power(inputs['x'], 2)", {"x": huge})
    with pytest.raises(ExecutionError, match="power"):
        safe_eval("power(2, inputs['x'])", {"x": huge})
    assert safe_eval("log10(inputs['x'])", {"x": huge}) == pytest.approx(400.0)
