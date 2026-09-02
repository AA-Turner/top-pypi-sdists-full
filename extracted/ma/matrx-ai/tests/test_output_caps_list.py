"""cap_list — the count-side companion to cap_text (the list-shaped size gate).

Regression for the class of `*_list` tools that dumped every row (task_list /
note_list / debug_traces_*): the count must be capped and reported honestly so a
tool can set output_self_capped without lying about what it returned."""

from __future__ import annotations

from matrx_ai.tools.output_caps import TOOL_LIST_DEFAULT_LIMIT, ListCapInfo, cap_list


def test_default_limit_caps_and_reports_true_total() -> None:
    rows = [{"i": i} for i in range(250)]
    out, info = cap_list(rows)
    assert isinstance(info, ListCapInfo)
    assert len(out) == TOOL_LIST_DEFAULT_LIMIT
    assert info.total == 250
    assert info.shown == TOOL_LIST_DEFAULT_LIMIT
    assert info.truncated is True


def test_under_limit_is_not_truncated() -> None:
    rows = [{"i": i} for i in range(5)]
    out, info = cap_list(rows, limit=10)
    assert out == rows
    assert info.total == 5
    assert info.shown == 5
    assert info.truncated is False


def test_explicit_limit_and_order_preserved() -> None:
    rows = [{"i": i} for i in range(20)]
    out, info = cap_list(rows, limit=3)
    assert [r["i"] for r in out] == [0, 1, 2]  # ordering kept
    assert info.truncated is True


def test_negative_limit_is_clamped_to_zero() -> None:
    out, info = cap_list([{"i": 1}], limit=-5)
    assert out == []
    assert info.shown == 0
    assert info.total == 1
    assert info.truncated is True
