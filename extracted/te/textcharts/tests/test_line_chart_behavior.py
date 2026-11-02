from __future__ import annotations

import re

from textcharts import ChartOptions, LineChart, LinePoint


def _opts(**kw):
    return ChartOptions(use_color=False, width=80, **kw)


def _extract_x_label_lines(result: str) -> list[str]:
    lines = result.splitlines()
    axis_idx = next(i for i, line in enumerate(lines) if "└" in line)
    label_lines: list[str] = []
    for line in lines[axis_idx + 1 :]:
        if not line.strip():
            break
        label_lines.append(line)
    return label_lines


def test_empty_data():
    assert "No data" in LineChart(points=[]).render()


def test_trend_line_renders_dots():
    # Simple ascending series — trend line should produce "." characters
    points = [LinePoint("S", i, float(i * 10)) for i in range(1, 8)]
    result = LineChart(
        points=points, show_trend=True, options=_opts()
    ).render()
    assert "." in result  # trend dots appear in grid


def test_trend_not_shown_when_disabled():
    points = [LinePoint("S", i, float(i * 10)) for i in range(1, 8)]
    no_trend = LineChart(points=points, show_trend=False, options=_opts()).render()
    with_trend = LineChart(points=points, show_trend=True, options=_opts()).render()
    # Trend version should have more dots
    assert with_trend.count(".") >= no_trend.count(".")


def test_compute_trend_linear():
    chart = LineChart(points=[LinePoint("S", 1, 1.0)], options=_opts())
    # Perfect linear: 0, 10, 20 → trend should be exactly [0, 10, 20]
    trend = chart._compute_trend([0.0, 10.0, 20.0])
    assert len(trend) == 3
    assert abs(trend[0] - 0.0) < 0.01
    assert abs(trend[1] - 10.0) < 0.01
    assert abs(trend[2] - 20.0) < 0.01


def test_compute_trend_single_value():
    chart = LineChart(points=[LinePoint("S", 1, 1.0)], options=_opts())
    assert chart._compute_trend([42.0]) == [42.0]


def test_compute_trend_constant():
    chart = LineChart(points=[LinePoint("S", 1, 1.0)], options=_opts())
    # All same values: denom == 0, returns original
    trend = chart._compute_trend([5.0, 5.0, 5.0])
    assert trend == [5.0, 5.0, 5.0]


def test_multi_series_renders_legend():
    points = [
        LinePoint("Alpha", 1, 10.0),
        LinePoint("Alpha", 2, 20.0),
        LinePoint("Beta", 1, 15.0),
        LinePoint("Beta", 2, 25.0),
    ]
    result = LineChart(points=points, options=_opts()).render()
    assert "Legend" in result
    assert "Alpha" in result
    assert "Beta" in result


def test_categorical_x_axis():
    points = [
        LinePoint("S", "Mon", 10.0),
        LinePoint("S", "Tue", 20.0),
        LinePoint("S", "Wed", 15.0),
    ]
    result = LineChart(points=points, options=_opts()).render()
    assert "Mon" in result
    assert "Tue" in result
    assert "Wed" in result


def test_categorical_x_axis_data_points_align_with_labels():
    """Data point markers should appear above their label slot centers."""
    points = [
        LinePoint("S", "A", 10.0),
        LinePoint("S", "B", 20.0),
        LinePoint("S", "C", 15.0),
        LinePoint("S", "D", 18.0),
    ]
    result = LineChart(points=points, options=ChartOptions(use_color=False, width=80)).render()
    chart_lines = result.splitlines()

    # Find x-axis line and label line
    axis_idx = next(i for i, line in enumerate(chart_lines) if "└" in line)
    label_line = chart_lines[axis_idx + 1]

    # Find the column of each label (center of the character)
    y_axis_width = 8  # known constant
    prefix_len = y_axis_width + 1  # spaces + axis corner

    label_centers = {}
    for lbl in ["A", "B", "C", "D"]:
        pos = label_line.find(lbl, prefix_len)
        assert pos >= 0, f"Label '{lbl}' not found in label line"
        label_centers[lbl] = pos - prefix_len  # column within plot area

    # Find a grid row where the '*' marker for each point appears.
    # Collect all marker positions within the grid area.
    marker_cols: dict[str, int] = {}
    for line in chart_lines[:axis_idx]:
        content = line[y_axis_width:]  # strip y-axis label area
        if len(content) > 1:
            plot_content = content[1:]  # strip axis char (│/┐/┘)
            for col, ch in enumerate(plot_content):
                if ch == "*":
                    # Map this column to the nearest label center
                    nearest = min(label_centers, key=lambda lbl: abs(label_centers[lbl] - col))
                    marker_cols[nearest] = col

    # Each marker should be within 1 column of its label center
    for lbl in ["A", "B", "C", "D"]:
        if lbl in marker_cols:
            assert abs(marker_cols[lbl] - label_centers[lbl]) <= 1, (
                f"Marker for '{lbl}' at col {marker_cols[lbl]} "
                f"misaligned with label center at col {label_centers[lbl]}"
            )


def test_categorical_x_axis_wrapped_labels_keep_gutters():
    points = [
        LinePoint("S", "summary_box", 10.0),
        LinePoint("S", "scatter_plot", 20.0),
        LinePoint("S", "histogram", 15.0),
        LinePoint("S", "line_chart", 18.0),
    ]
    result = LineChart(points=points, options=ChartOptions(use_color=False, width=56)).render()
    label_lines = _extract_x_label_lines(result)

    assert len(label_lines) == 2
    assert re.search(r"summary\s+scatter", label_lines[0])
    assert re.search(r"box\s+plot", label_lines[1])
    assert "summaryscatter" not in label_lines[0]


def test_categorical_x_axis_boundary_label_wraps_for_gutter():
    """A label exactly label_width chars wraps because wrap_width is label_width-1."""
    # With width=60: plot_width = 60-8-2 = 50, label_width = 50//2 = 25,
    # wrap_width = 24.  A 25-char label must wrap.
    long_label = "a" * 25
    points = [
        LinePoint("S", long_label, 10.0),
        LinePoint("S", "short", 20.0),
    ]
    result = LineChart(points=points, options=ChartOptions(use_color=False, width=60)).render()
    label_lines = _extract_x_label_lines(result)
    # Label was too long for wrap_width so it should have produced 2 label rows
    assert len(label_lines) == 2
    # The full 25-char string should NOT appear intact on one line
    assert long_label not in label_lines[0]


def test_axis_labels_rendered():
    points = [LinePoint("S", 1, 10.0), LinePoint("S", 2, 20.0)]
    result = LineChart(
        points=points, x_label="Time", y_label="Value", options=_opts()
    ).render()
    assert "Time" in result
    assert "Value" in result


def test_y_axis_capping_with_outlier():
    # One extreme outlier should trigger y-axis capping
    points = [LinePoint("S", i, 10.0) for i in range(1, 10)]
    points.append(LinePoint("S", 10, 10000.0))  # extreme outlier
    result = LineChart(points=points, options=_opts()).render()
    # Truncation marker should appear
    assert "capped" in result.lower() or "\u25b8" in result
