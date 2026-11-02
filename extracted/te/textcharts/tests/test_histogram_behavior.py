from __future__ import annotations

from textcharts import ChartOptions, Histogram, HistogramBar, histogram_from_data


def test_histogram_empty_and_basic_rendering():
    assert "No data" in Histogram(data=[]).render()
    result = Histogram(
        data=[HistogramBar(label="Q1", value=100)],
        title="Test Histogram",
        options=ChartOptions(use_color=False),
    ).render()
    assert "Q1" in result
    assert "Test Histogram" in result


def test_histogram_natural_sort_orders_q1_q2_q10():
    data = [
        HistogramBar(label="Q10", value=100),
        HistogramBar(label="Q2", value=200),
        HistogramBar(label="Q1", value=150),
    ]
    result = Histogram(data=data, sort_by="label", options=ChartOptions(use_color=False)).render()
    label_line = next(line for line in result.splitlines() if "Q1" in line and "Q2" in line and "Q10" in line)
    assert label_line.index("Q1") < label_line.index("Q2") < label_line.index("Q10")


def test_histogram_mean_line_can_be_shown_and_hidden():
    data = [HistogramBar(label="Q1", value=100), HistogramBar(label="Q2", value=200)]
    shown = Histogram(data=data, show_mean_line=True, options=ChartOptions(use_color=False)).render()
    hidden = Histogram(data=data, show_mean_line=False, options=ChartOptions(use_color=False)).render()
    assert "Mean" in shown
    assert "Mean" not in hidden


def test_histogram_splits_large_datasets_by_query_ranges():
    data = [HistogramBar(label=f"Q{i}", value=i * 10) for i in range(1, 41)]
    result = Histogram(data=data, max_per_chart=33, options=ChartOptions(use_color=False)).render()
    assert "Q1-Q33" in result
    assert "Q34-Q40" in result


def test_histogram_multiplatform_mode_renders_legend_and_chunks_by_unique_queries():
    data = []
    for i in range(1, 11):
        data.append(HistogramBar(label=f"Q{i}", value=i * 10, platform="DuckDB"))
        data.append(HistogramBar(label=f"Q{i}", value=i * 15, platform="Polars"))

    result = Histogram(data=data, max_per_chart=5, options=ChartOptions(use_color=False)).render()

    assert "DuckDB" in result
    assert "Polars" in result
    assert "Q1-Q5" in result
    assert "Q6-Q10" in result


def test_histogram_multiplatform_legend_replaces_best_worst_legend():
    data = [
        HistogramBar(label="Q1", value=50, platform="DuckDB", is_best=True),
        HistogramBar(label="Q1", value=60, platform="Polars", is_best=True),
        HistogramBar(label="Q2", value=300, platform="DuckDB", is_worst=True),
        HistogramBar(label="Q2", value=350, platform="Polars", is_worst=True),
    ]
    result = Histogram(data=data, options=ChartOptions(use_color=False)).render()
    assert "DuckDB" in result
    assert "Polars" in result
    assert "Best" not in result
    assert "Worst" not in result


def test_histogram_factory_and_compact_labels_behavior():
    data = [HistogramBar(label=f"Q{i}", value=float(i)) for i in range(10, 20)]
    chart = histogram_from_data(data, title="Factory Test", options=ChartOptions(width=46, use_color=False))
    result = chart.render()
    assert "Factory Test" in result
    assert "10" in result
    assert "11" in result
    assert "19" in result
    assert "Q1 Q1 Q1" not in result


def _extract_label_lines(result: str) -> list[str]:
    """Extract label rows between the last ─ separator and the → axis line."""
    lines = result.splitlines()
    # Find the last horizontal separator (the one below the bars, not the title)
    sep_indices = [i for i, line in enumerate(lines) if "──" in line]
    sep_idx = sep_indices[-1]
    label_lines = []
    for line in lines[sep_idx + 1 :]:
        stripped = line.strip()
        if stripped == "→" or stripped == "" or "Value" in stripped or "Mean" in stripped:
            break
        label_lines.append(line)
    return label_lines


def test_histogram_long_labels_wrap_to_two_rows():
    """Long labels should wrap onto a second label row."""
    data = [
        HistogramBar(label="summary_box", value=100),
        HistogramBar(label="scatter_plot", value=120),
        HistogramBar(label="histogram", value=200),
        HistogramBar(label="line_chart", value=180),
        HistogramBar(label="box_plot", value=90),
        HistogramBar(label="heatmap", value=150),
        HistogramBar(label="sparkline", value=160),
        HistogramBar(label="Q1", value=140),
    ]
    result = Histogram(data=data, options=ChartOptions(use_color=False, width=80)).render()
    label_lines = _extract_label_lines(result)
    # With 8 bars at width=80, bar_width is small enough to force wrapping
    assert len(label_lines) == 2
    # First row has first parts, second row has wrapped second parts
    assert "box" in label_lines[0]  # "box_plot" first part
    assert "plot" in label_lines[1]  # "box_plot" second part


def test_histogram_short_labels_no_extra_row():
    """Short labels (e.g. Q1-Q6) should render on a single line with no second row."""
    data = [HistogramBar(label=f"Q{i}", value=i * 10) for i in range(1, 7)]
    result = Histogram(data=data, options=ChartOptions(use_color=False, width=80)).render()
    label_lines = _extract_label_lines(result)
    assert len(label_lines) == 1
    assert "Q1" in label_lines[0]
    assert "Q6" in label_lines[0]


def test_histogram_q_prefix_preserved_at_standard_width():
    """At standard terminal width, 2-digit query labels must retain their Q prefix."""
    data = [HistogramBar(label=f"Q{i}", value=float(i)) for i in range(10, 20)]
    # 132-char width: bar_area=120, 120//10=12, bar_width=11 — no compaction needed
    result = histogram_from_data(data, options=ChartOptions(width=132, use_color=False)).render()
    assert "Q10" in result
    assert "Q19" in result


def test_histogram_variant_labels_are_distinct_after_compaction():
    """Q14a and Q14b must produce distinct labels even after compaction."""
    data = [
        HistogramBar(label="Q14a", value=100.0),
        HistogramBar(label="Q14b", value=110.0),
    ]
    # width=46, 2 bars: bar_area=36, 36//2=18, bar_width=17 — labels fit in full
    result = Histogram(data=data, options=ChartOptions(width=46, use_color=False)).render()
    assert "Q14a" in result
    assert "Q14b" in result

    # width=40 → bar_width narrows but variants must still be distinct
    result_narrow = Histogram(data=data, options=ChartOptions(width=40, use_color=False)).render()
    label_lines = _extract_label_lines(result_narrow)
    all_labels = " ".join(label_lines)
    # Extract the two label tokens; they must differ
    tokens = [t for t in all_labels.split() if t]
    assert len(tokens) >= 2, "Expected two label tokens"
    assert tokens[0] != tokens[1], f"Labels collapsed: both rendered as {tokens[0]!r}"
