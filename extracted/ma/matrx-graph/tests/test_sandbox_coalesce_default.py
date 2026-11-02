"""``coalesce`` gives back the caller's default when every value is empty.

Break caught (2026-10-28): ``coalesce(x, '')`` was None when ``x`` was empty, so
``len(coalesce(x, ''))`` / ``coalesce(x, []) + [...]`` crashed a run — Smart Add unit 9's
facts step died on a name-only brand, and the CONVERSION-PLAYBOOK recorded the trap five times.
A single-argument ``coalesce(x)`` keeps None for an empty ``x``: live workflows use
``coalesce(x) is not None`` as "x has a value" (21 published calls, checked 2026-10-28).
"""

from __future__ import annotations

import pytest

from matrx_graph.nodes._sandbox import safe_eval


@pytest.mark.parametrize(
    ("expr", "inputs", "expected"),
    [
        ("coalesce(inputs['x'], '')", {"x": None}, ""),
        ("coalesce(inputs['x'], '')", {"x": "   "}, ""),
        ("coalesce(inputs['x'], [])", {"x": []}, []),
        ("coalesce(inputs['x'], {})", {"x": None}, {}),
        ("coalesce(inputs['a'], inputs['b'], [])", {"a": "", "b": None}, []),
    ],
)
def test_all_empty_gives_back_the_last_argument(expr, inputs, expected):
    assert safe_eval(expr, inputs) == expected


def test_the_default_keeps_a_name_only_run_alive():
    # Unit 9's facts step on a brand with only a name: no description, no pages.
    expr = "len(coalesce(inputs['description'], '')) + len(coalesce(inputs['pages'], []) + ['name'])"
    assert safe_eval(expr, {"description": None, "pages": []}) == 1


def test_whitespace_still_counts_as_empty():
    assert safe_eval("coalesce(inputs['t'], inputs['n'], '')", {"t": " \n", "n": "Marigold Bakery"}) == "Marigold Bakery"


def test_first_value_still_wins_and_zero_is_a_value():
    assert safe_eval("coalesce(inputs['a'], '')", {"a": 0}) == 0
    assert safe_eval("coalesce(inputs['a'], 'z')", {"a": "Riverbend"}) == "Riverbend"


@pytest.mark.parametrize("empty", [None, "", "  ", [], {}])
def test_one_argument_is_still_none_when_empty(empty):
    assert safe_eval("coalesce(inputs['x']) is not None", {"x": empty}) is False
