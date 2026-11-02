from __future__ import annotations

import pytest

import textcharts.base as base
from textcharts import BarChart, BarData, ChartOptions, Heatmap
from textcharts.base import ColorMode, TerminalCapabilities
from textcharts.rank_table import from_matrix as rank_from_matrix


def _capabilities(color_mode: ColorMode) -> TerminalCapabilities:
    return TerminalCapabilities(
        width=80,
        height=24,
        color_mode=color_mode,
        unicode_support=True,
        interactive=color_mode != ColorMode.NONE,
    )


def test_get_colors_falls_back_to_extended_when_use_color_true(monkeypatch: pytest.MonkeyPatch):
    """When use_color=True (default) but terminal has no color, fall back to EXTENDED."""
    monkeypatch.setattr(base, "detect_terminal_capabilities", lambda: _capabilities(ColorMode.NONE))
    opts = ChartOptions()

    assert opts.get_colors().color_mode == ColorMode.EXTENDED


def test_get_colors_returns_none_when_use_color_false(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(base, "detect_terminal_capabilities", lambda: _capabilities(ColorMode.NONE))
    opts = ChartOptions(use_color=False)

    assert opts.get_colors().color_mode == ColorMode.NONE


def test_default_render_includes_ansi_when_use_color_true(monkeypatch: pytest.MonkeyPatch):
    """use_color=True (default) produces ANSI even on non-TTY (e.g. MCP stdio)."""
    monkeypatch.setattr(base, "detect_terminal_capabilities", lambda: _capabilities(ColorMode.NONE))
    chart = BarChart([BarData("A", 1), BarData("B", 2)], options=ChartOptions(width=80))

    result = chart.render()

    assert "\033[" in result


def test_render_omits_ansi_when_use_color_false(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(base, "detect_terminal_capabilities", lambda: _capabilities(ColorMode.NONE))
    chart = BarChart([BarData("A", 1), BarData("B", 2)], options=ChartOptions(width=80, use_color=False))

    result = chart.render()

    assert "\033[" not in result


def test_default_render_uses_ansi_when_color_capability_is_detected(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(base, "detect_terminal_capabilities", lambda: _capabilities(ColorMode.TRUECOLOR))
    chart = BarChart([BarData("A", 1), BarData("B", 2)], options=ChartOptions(width=80))

    result = chart.render()

    assert "\033[" in result


def test_heatmap_sequential_scheme_changes_colored_output(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(base, "detect_terminal_capabilities", lambda: _capabilities(ColorMode.TRUECOLOR))
    matrix = [[1.0, 2.0], [3.0, 4.0]]

    sequential = Heatmap(
        matrix=matrix,
        row_labels=["Q1", "Q2"],
        col_labels=["A", "B"],
        color_scheme="sequential",
        options=ChartOptions(width=80),
    ).render()
    diverging = Heatmap(
        matrix=matrix,
        row_labels=["Q1", "Q2"],
        col_labels=["A", "B"],
        color_scheme="diverging",
        options=ChartOptions(width=80),
    ).render()

    assert sequential != diverging
    assert "\033[48;2;27;158;119m" in sequential
    assert "\033[48;2;67;147;195m" in diverging


def test_heatmap_rejects_row_label_count_mismatch():
    with pytest.raises(ValueError, match="row_labels length must match"):
        Heatmap(
            matrix=[[1.0, 2.0], [3.0, 4.0]],
            row_labels=["Q1"],
            col_labels=["A", "B"],
            options=ChartOptions(use_color=False),
        )


def test_heatmap_rejects_ragged_rows():
    with pytest.raises(ValueError, match="matrix row 2 has 1 columns but expected 2"):
        Heatmap(
            matrix=[[1.0, 2.0], [3.0]],
            row_labels=["Q1", "Q2"],
            col_labels=["A", "B"],
            options=ChartOptions(use_color=False),
        )


def test_rank_table_factory_rejects_malformed_matrix():
    with pytest.raises(ValueError, match="matrix row 2 has 1 columns but expected 2"):
        rank_from_matrix(
            matrix=[[10.0, 20.0], [30.0]],
            items=["Q1", "Q2"],
            groups=["DuckDB", "Polars"],
            options=ChartOptions(use_color=False),
        )
