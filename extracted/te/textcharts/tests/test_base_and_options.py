from __future__ import annotations

import io

import pytest

import textcharts.base as base
from textcharts import (
    BoxPlot,
    BoxPlotSeries,
    CDFChart,
    CDFSeriesData,
    ComparisonBar,
    ComparisonBarData,
    Histogram,
    HistogramBar,
    LineChart,
    LinePoint,
    ScatterPlot,
    ScatterPoint,
    StackedBar,
    StackedBarData,
    StackedBarSegment,
)
from textcharts.base import (
    DARK_PALETTE,
    LIGHT_PALETTE,
    ChartBase,
    ChartOptions,
    ColorMode,
    TerminalCapabilities,
    TerminalColors,
    compute_percentile_linear,
    detect_terminal_capabilities,
    outlier_severity_markers,
    robust_p95,
)


class _DummyChart(ChartBase):
    def render(self) -> str:
        return ""


def test_detect_capabilities_returns_valid_object(monkeypatch: pytest.MonkeyPatch):
    stdout = io.StringIO()
    stdin = io.StringIO()
    monkeypatch.setattr(base.sys, "stdout", stdout)
    monkeypatch.setattr(base.sys, "stdin", stdin)
    monkeypatch.setattr(stdout, "isatty", lambda: False)
    monkeypatch.setattr(stdin, "isatty", lambda: False)

    caps = detect_terminal_capabilities()

    assert caps.width >= 40
    assert caps.height >= 10
    assert isinstance(caps.color_mode, ColorMode)
    assert isinstance(caps.unicode_support, bool)


def test_detect_capabilities_honors_truecolor_and_no_color(monkeypatch: pytest.MonkeyPatch):
    stdout = io.StringIO()
    stdin = io.StringIO()
    monkeypatch.setattr(base.sys, "stdout", stdout)
    monkeypatch.setattr(base.sys, "stdin", stdin)
    monkeypatch.setattr(stdout, "isatty", lambda: True)
    monkeypatch.setattr(stdin, "isatty", lambda: True)
    monkeypatch.setenv("COLORTERM", "truecolor")
    monkeypatch.setenv("NO_COLOR", "1")

    caps = detect_terminal_capabilities()

    assert caps.color_mode == ColorMode.NONE
    assert caps.interactive is True


def test_terminal_colors_modes_and_colorize():
    none = TerminalColors(color_mode=ColorMode.NONE)
    assert none.fg("#ff0000") == ""
    assert none.bg("#ff0000") == ""
    assert none.colorize("x", fg_color="#ff0000") == "x"

    basic = TerminalColors(color_mode=ColorMode.BASIC)
    assert "\033[" in basic.fg(2)
    assert "\033[" in basic.bg(2)

    extended = TerminalColors(color_mode=ColorMode.EXTENDED)
    assert "\033[38;5;" in extended.fg("#1b9e77")
    assert "\033[48;5;" in extended.bg("#1b9e77")
    assert extended.colorize("test", fg_color="#ff0000", bg_color="#000000").endswith(extended.RESET)

    truecolor = TerminalColors(color_mode=ColorMode.TRUECOLOR)
    assert "\033[38;2;255;0;0m" == truecolor.fg("#ff0000")
    assert "\033[48;2;255;0;0m" == truecolor.bg("#ff0000")


def test_chart_options_width_and_character_selection():
    opts = ChartOptions(width=200)
    assert opts.get_effective_width() == 140

    opts = ChartOptions(width=20)
    assert opts.get_effective_width() == 40

    opts = ChartOptions(use_unicode=False, use_color=False)
    assert "#" in opts.get_horizontal_block_chars()
    assert "#" in opts.get_vertical_block_chars()
    assert opts.get_box_chars()["h"] == "-"
    assert opts.get_intensity_chars() == " .-=#"
    assert opts.get_series_fill(1) == "="
    assert opts.get_series_marker(1) == "*"


def test_chart_options_auto_width_uses_cached_capabilities():
    opts = ChartOptions()
    opts._capabilities = TerminalCapabilities(width=100, height=24, color_mode=ColorMode.BASIC)

    assert opts.get_effective_width() == 98
    assert opts.get_colors().color_mode == ColorMode.BASIC


def test_percentile_and_outlier_helpers_cover_edge_cases():
    assert compute_percentile_linear([], 95) == 0.0
    assert compute_percentile_linear([42], 95) == 42
    assert compute_percentile_linear([1, 2, 3, 4], 50) == 2.5
    assert robust_p95([0, 0, 0, 10, 20]) == 10
    assert robust_p95([0, 0, 0]) == 0
    assert outlier_severity_markers(21, 2) == "▸▸▸▸"
    assert outlier_severity_markers(3, 2) == "▸"


def test_base_render_helpers_and_subtitle_formatting():
    chart = _DummyChart(
        options=ChartOptions(use_color=False, use_unicode=True),
        subtitle="TPC-H | SF=1 | v1 | tuned",
    )

    rendered = chart._render_subtitle(80)

    assert rendered is not None
    assert "TPC-H" in rendered
    assert "SF=1" in rendered
    assert "v1" in rendered
    assert "tuned" in rendered
    assert "Injected" == chart._truncate_label("\033[31mInjected\033[0m", 20)
    assert chart._format_value(1500) == "1.5K"
    assert chart._format_value(0.001) == "1.00e-03"
    assert "Latency" in chart._render_axis_label("Latency", 40, axis="y")


def test_base_legend_wraps_and_respects_show_legend():
    chart = _DummyChart(options=ChartOptions(width=40, use_color=False))
    lines = chart._render_legend(
        [("DuckDB", "#1b9e77"), ("SQLite", "#d95f02"), ("Polars", "#7570b3"), ("Pandas", "#666666")],
        chart.options.get_colors(),
    )
    assert len(lines) >= 2

    no_legend = _DummyChart(options=ChartOptions(width=40, use_color=False, show_legend=False))
    assert no_legend._render_legend([("DuckDB", "#1b9e77")], no_legend.options.get_colors()) == []


# -- _wrap_label tests --------------------------------------------------------


def test_wrap_label_short_label_returns_single_line():
    assert ChartBase._wrap_label("Q1", 4) == ["Q1"]
    assert ChartBase._wrap_label("foo", 10) == ["foo"]


def test_wrap_label_splits_at_underscore():
    assert ChartBase._wrap_label("summary_box", 7) == ["summary", "box"]
    assert ChartBase._wrap_label("line_chart", 7) == ["line", "chart"]


def test_wrap_label_splits_at_camel_case():
    assert ChartBase._wrap_label("camelCase", 5) == ["camel", "Case"]


def test_wrap_label_splits_alpha_digit_boundary():
    result = ChartBase._wrap_label("Q10", 2)
    assert result == ["Q", "10"]


def test_wrap_label_hard_splits_when_no_boundary():
    result = ChartBase._wrap_label("abcdef", 3)
    assert result == ["abc", "def"]


def test_wrap_label_truncates_line2_with_dots():
    result = ChartBase._wrap_label("a_longersecondpart", 6)
    assert len(result) == 2
    assert len(result[1]) <= 6
    # Line 2 should be truncated with ".." if it exceeds max_width
    assert result[0] == "a"
    assert result[1] == "long.."


def test_wrap_label_strips_ansi():
    result = ChartBase._wrap_label("\033[31mhello_world\033[0m", 6)
    assert result == ["hello", "world"]


@pytest.mark.parametrize(
    ("label", "width", "expected"),
    [
        ("_all", 3, ["_al", "l"]),
        ("-foo", 3, ["-fo", "o"]),
        (" foo", 3, [" fo", "o"]),
        ("__x", 2, ["__", "x"]),
    ],
)
def test_wrap_label_avoids_blank_first_line_for_leading_delimiters(
    label: str, width: int, expected: list[str]
):
    assert ChartBase._wrap_label(label, width) == expected


def test_wrap_label_leading_delim_with_later_valid_split():
    """Leading delimiter is skipped but a later boundary is still found."""
    assert ChartBase._wrap_label("_hello_world", 7) == ["_hello", "world"]
    assert ChartBase._wrap_label(" foo_bar", 5) == [" foo", "bar"]


def test_wrap_label_all_delimiter_preserves_content():
    """All-delimiter labels are hard-split without silently dropping content."""
    assert ChartBase._wrap_label("___", 2) == ["__", "_"]
    assert ChartBase._wrap_label("---", 1) == ["-", "-"]
    # Trailing delimiter after hard split is preserved
    assert ChartBase._wrap_label("foo_", 3) == ["foo", "_"]


# -- _build_wrapped_label_rows tests ------------------------------------------


def test_wrapped_label_rows_single_row_when_all_fit():
    rows = ChartBase._build_wrapped_label_rows(["Q1", "Q2", "Q3"], 4)
    assert len(rows) == 1
    assert "Q1" in rows[0]
    assert "Q2" in rows[0]
    assert "Q3" in rows[0]


def test_wrapped_label_rows_two_rows_when_any_wraps():
    rows = ChartBase._build_wrapped_label_rows(
        ["summary_box", "Q1", "histogram"],
        7,
        prefix="  ",
        separator=" ",
    )
    assert len(rows) == 2
    assert "summary" in rows[0]
    assert "box" in rows[1]
    # Q1 has no second line so row 2 should have blank space in that slot
    assert "Q1" in rows[0]


def test_wrapped_label_rows_respects_prefix_and_separator():
    rows = ChartBase._build_wrapped_label_rows(["AB", "CD"], 4, prefix=">>", separator="|")
    assert rows[0].startswith(">>")
    assert "|" in rows[0]


def test_wrapped_label_rows_wrap_width_limits_content_but_preserves_slot():
    """wrap_width shrinks label text while col_width controls centering/slot size."""
    # "abcdefghij" is 10 chars — fits in col_width=10 but exceeds wrap_width=9
    rows = ChartBase._build_wrapped_label_rows(
        ["abcdefghij", "Q1"],
        col_width=10,
        wrap_width=9,
    )
    assert len(rows) == 2
    # Line 1 should NOT contain the full 10-char label (it was wrapped)
    assert "abcdefghij" not in rows[0]
    # But each slot is still 10 chars wide (centered)
    assert "Q1" in rows[0]


def _truecolor_caps() -> TerminalCapabilities:
    return TerminalCapabilities(
        width=80, height=24, color_mode=ColorMode.TRUECOLOR,
        unicode_support=True, interactive=False,
    )


def _hex_to_truecolor_esc(hex_color: str) -> str:
    hex_color = hex_color.lstrip("#")
    r, g, b = (int(hex_color[i : i + 2], 16) for i in (0, 2, 4))
    return f"\033[38;2;{r};{g};{b}m"


def _themed_chart_factory(theme: str):
    """Build one chart per palette-consuming type bound to *theme*."""
    opts = ChartOptions(theme=theme, width=80)
    return {
        "box": BoxPlot(series=[BoxPlotSeries(name="S", values=[1, 2, 3, 4, 5])], options=opts),
        "histogram": Histogram(
            data=[HistogramBar(label="A", value=10), HistogramBar(label="B", value=20)],
            options=opts,
        ),
        "cdf": CDFChart(data=[CDFSeriesData(name="S", values=[1, 2, 3])], options=opts),
        "stacked": StackedBar(
            data=[StackedBarData(label="A", segments=[StackedBarSegment("p", 10.0)])],
            options=opts,
        ),
        "comparison": ComparisonBar(
            data=[ComparisonBarData(label="Q", baseline_value=100, comparison_value=120)],
            options=opts,
        ),
        "scatter": ScatterPlot(
            points=[ScatterPoint(name="A", x=10, y=20), ScatterPoint(name="B", x=30, y=40)],
            options=opts,
        ),
        "line": LineChart(
            points=[LinePoint(series="S", x=0, y=1), LinePoint(series="S", x=1, y=2)],
            options=opts,
        ),
    }


def test_dark_theme_renders_dark_palette(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(base, "detect_terminal_capabilities", _truecolor_caps)
    charts = _themed_chart_factory("dark")
    assert len(charts) == 7
    dark_esc = _hex_to_truecolor_esc(DARK_PALETTE[0])
    light_esc = _hex_to_truecolor_esc(LIGHT_PALETTE[0])
    for name, chart in charts.items():
        result = chart.render()
        assert dark_esc in result, f"{name} missing DARK_PALETTE color with theme='dark'"
        assert light_esc not in result, f"{name} leaked LIGHT_PALETTE color with theme='dark'"


def test_light_theme_renders_light_palette(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(base, "detect_terminal_capabilities", _truecolor_caps)
    charts = _themed_chart_factory("light")
    assert len(charts) == 7
    dark_esc = _hex_to_truecolor_esc(DARK_PALETTE[0])
    light_esc = _hex_to_truecolor_esc(LIGHT_PALETTE[0])
    for name, chart in charts.items():
        result = chart.render()
        assert light_esc in result, f"{name} missing LIGHT_PALETTE color with theme='light'"
        assert dark_esc not in result, f"{name} leaked DARK_PALETTE color with theme='light'"
