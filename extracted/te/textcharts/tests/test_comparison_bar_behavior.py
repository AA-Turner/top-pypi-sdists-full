from __future__ import annotations

from textcharts import ChartOptions, ComparisonBar, ComparisonBarData, comparison_from_data


def _opts(**kw):
    return ChartOptions(use_color=False, width=80, **kw)


def test_empty_and_no_finite_data():
    assert "No data" in ComparisonBar(data=[]).render()
    data = [ComparisonBarData("Q1", float("inf"), float("nan"))]
    assert "No finite" in ComparisonBar(data=data, options=_opts()).render()


def test_percentage_change_annotation():
    data = [ComparisonBarData("Q1", 100.0, 75.0, "Run1", "Run2")]
    result = ComparisonBar(data=data, options=_opts()).render()
    # 75 vs 100 = -25% improvement — should show negative annotation with arrow
    assert "-25.0%" in result
    assert "v" in result  # down arrow (ASCII mode, improvement)


def test_regression_annotation():
    data = [ComparisonBarData("Q1", 100.0, 200.0, "Run1", "Run2")]
    result = ComparisonBar(data=data, options=_opts()).render()
    assert "+100.0%" in result
    assert "\u2191" in result  # up arrow (Unicode mode, regression)


def test_stable_change_produces_no_annotation():
    data = [ComparisonBarData("Q1", 100.0, 101.0)]
    result = ComparisonBar(data=data, options=_opts()).render()
    # 1% change is below STABLE_THRESHOLD_PCT (2.0)
    lines = result.splitlines()
    comparison_line = [line for line in lines if "Comparison" in line or "101" in line]
    for line in comparison_line:
        assert "%" not in line


def test_outlier_truncation_shows_severity_markers():
    # sorted_vals = [5000, 13, 12, 11, 11, 10, 10, 10], median ~11
    # top/median = 454 > 5 => truncate_threshold = sorted_vals[1]*2 = 26
    # 5000 > 26 => bar is truncated => severity markers appended
    data = [
        ComparisonBarData("Q1", 10.0, 10.0),
        ComparisonBarData("Q2", 12.0, 11.0),
        ComparisonBarData("Q3", 11.0, 13.0),
        ComparisonBarData("Q4", 5000.0, 10.0),  # extreme outlier on baseline
    ]
    result = ComparisonBar(data=data, options=_opts()).render()
    # outlier_severity_markers(5000, 26) should produce markers
    assert "\u25b8" in result  # ▸ severity marker for truncated outlier


def test_run_names_appear_in_output():
    data = [ComparisonBarData("Q1", 50.0, 60.0, "Alpha", "Beta")]
    result = ComparisonBar(data=data, options=_opts()).render()
    assert "Alpha" in result
    assert "Beta" in result


def test_comparison_from_data_factory():
    data = [ComparisonBarData("Q1", 100.0, 80.0)]
    chart = comparison_from_data(data, title="Factory Test", options=_opts())
    result = chart.render()
    assert isinstance(chart, ComparisonBar)
    assert "Factory Test" in result
    assert "Q1" in result


def test_scale_note_and_legend():
    data = [ComparisonBarData("Q1", 100.0, 200.0, "Run1", "Run2")]
    result = ComparisonBar(data=data, options=_opts()).render()
    assert "each" in result  # scale note
    assert "\u2248" in result  # approx symbol (≈, Unicode mode)
    assert "improvement" in result
    assert "regression" in result
