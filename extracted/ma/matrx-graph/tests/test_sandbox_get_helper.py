"""get(value, 'a.b.0', default): read a field that may be missing, without the guard.

Design: common-docs/systems/workflows/projects/generic-only/PRIMITIVES-LIST-EXPRESSIONS.md § get.
Replaces `x['k'] if 'k' in x and x['k'] else d` — found 140 times in 62 live workflows (2026-10-27).
"""

from __future__ import annotations

import pytest

from matrx_graph.errors import ExecutionError
from matrx_graph.nodes._sandbox import safe_eval, validate_expression

DATA = {"p": {"title": "T", "empty": "", "none": None, "zero": 0, "off": False, "pages": [{"url": "u0"}, {"url": "u1"}]}}


@pytest.mark.parametrize(
    ("expr", "expected"),
    [
        ("get(inputs['p'], 'title', '')", "T"),
        ("get(inputs['p'], 'missing', 'd')", "d"),
        ("get(inputs['p'], 'none', 'd')", "d"),
        ("get(inputs['p'], 'missing')", None),
        ("get(inputs['p'], 'empty', 'd')", ""),
        ("get(inputs['p'], 'zero', 5)", 0),
        ("get(inputs['p'], 'off', True)", False),
        ("get(inputs, 'p.pages.1.url')", "u1"),
        ("get(inputs, 'p.pages.9.url', 'none')", "none"),
        ("get(inputs, 'p.title.x', 'd')", "d"),
        ("get(None, 'a', 'd')", "d"),
        ("[get(x, 'url') for x in inputs['p']['pages']]", ["u0", "u1"]),
    ],
)
def test_get_reads_or_falls_back(expr: str, expected: object) -> None:
    assert safe_eval(expr, DATA) == expected


def test_get_needs_a_text_path() -> None:
    with pytest.raises(ExecutionError, match="get\\(\\)"):
        safe_eval("get(inputs, 3)", DATA)


def test_get_validates_as_a_helper() -> None:
    validate_expression("get(inputs, 'a.b', '')")


@pytest.mark.parametrize("path", ["p.pages.²", "p.pages.-1", "p..title", "p.pages.0.url.x"])
def test_odd_paths_fall_back_never_crash(path: str) -> None:
    assert safe_eval(f"get(inputs, '{path}', 'd')", DATA) == "d"


def test_get_reads_tuples() -> None:
    assert safe_eval("get(inputs['t'], '1')", {"t": ("a", "b")}) == "b"
