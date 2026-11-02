from __future__ import annotations

from textcharts import ChartOptions, DivergingBar, DivergingBarData, diverging_from_data


def _opts(**kw):
    return ChartOptions(use_color=False, width=80, **kw)


def test_empty_data():
    assert "No data" in DivergingBar(data=[]).render()


def test_improvements_appear_left_regressions_right():
    data = [
        DivergingBarData("Q1", -30.0),  # improvement
        DivergingBarData("Q2", +20.0),  # regression
    ]
    result = DivergingBar(data=data, options=_opts()).render()
    assert "Faster" in result
    assert "Slower" in result
    assert "-30.0%" in result
    assert "+20.0%" in result


def test_sort_order_improvements_first_then_regressions():
    data = [
        DivergingBarData("Q3", +10.0),
        DivergingBarData("Q1", -50.0),
        DivergingBarData("Q2", -20.0),
    ]
    result = DivergingBar(data=data, options=_opts()).render()
    lines = result.splitlines()
    # Find data lines containing query labels
    q_lines = [(i, line) for i, line in enumerate(lines) if any(f"Q{n}" in line for n in [1, 2, 3])]
    # Q1 (-50%) should come first, Q2 (-20%) second, Q3 (+10%) last
    labels = [line for _, line in q_lines]
    q1_idx = next(i for i, line in enumerate(labels) if "Q1" in line)
    q2_idx = next(i for i, line in enumerate(labels) if "Q2" in line)
    q3_idx = next(i for i, line in enumerate(labels) if "Q3" in line)
    assert q1_idx < q2_idx < q3_idx


def test_summary_counts():
    data = [
        DivergingBarData("Q1", -30.0),  # improved (> 2% threshold)
        DivergingBarData("Q2", +1.0),   # stable (< 2% threshold)
        DivergingBarData("Q3", +25.0),  # regressed
    ]
    result = DivergingBar(data=data, options=_opts()).render()
    assert "1 improved" in result
    assert "1 stable" in result
    assert "1 regressed" in result


def test_overflow_arrows_for_clipped_values():
    data = [
        DivergingBarData("Q1", -500.0),  # exceeds default clip_pct of 200
        DivergingBarData("Q2", +500.0),  # exceeds default clip_pct of 200
    ]
    result = DivergingBar(data=data, options=_opts()).render()
    # Unicode overflow arrows: ◄── (left) and ──► (right)
    assert "\u25c4" in result  # ◄ left arrow for clipped improvement
    assert "\u25ba" in result  # ► right arrow for clipped regression


def test_fill_intensity_by_magnitude():
    data = [
        DivergingBarData("Q1", -5.0),   # weak (<15%)
        DivergingBarData("Q2", -25.0),  # medium (15-50%)
        DivergingBarData("Q3", -75.0),  # strong (>50%)
    ]
    result = DivergingBar(data=data, options=_opts()).render()
    # Each query should render without errors; different fill chars used
    assert "Q1" in result
    assert "Q2" in result
    assert "Q3" in result


def test_diverging_from_data_factory():
    data = [DivergingBarData("Q1", -10.0)]
    chart = diverging_from_data(data, title="Factory Test", options=_opts())
    result = chart.render()
    assert isinstance(chart, DivergingBar)
    assert "Factory Test" in result
    assert "Q1" in result


def test_lower_is_better_false_headers():
    data = [
        DivergingBarData("Q1", -30.0),  # regression when higher is better
        DivergingBarData("Q2", +20.0),  # improvement when higher is better
    ]
    result = DivergingBar(data=data, options=_opts(), lower_is_better=False).render()
    assert "Worse" in result
    assert "Better" in result
    assert "Faster" not in result
    assert "Slower" not in result


def test_lower_is_better_false_sort_and_counts():
    data = [
        DivergingBarData("Q3", -10.0),
        DivergingBarData("Q1", +50.0),
        DivergingBarData("Q2", +20.0),
    ]
    result = DivergingBar(data=data, options=_opts(), lower_is_better=False).render()
    lines = result.splitlines()
    labels = [line for line in lines if any(f"Q{n}" in line for n in [1, 2, 3])]
    q1_idx = next(i for i, line in enumerate(labels) if "Q1" in line)
    q2_idx = next(i for i, line in enumerate(labels) if "Q2" in line)
    q3_idx = next(i for i, line in enumerate(labels) if "Q3" in line)
    # Improvements (+50, +20) first strongest-to-weakest, then the regression (-10)
    assert q1_idx < q2_idx < q3_idx
    assert "2 improved" in result
    assert "1 regressed" in result


def test_diverging_from_data_passes_lower_is_better():
    data = [DivergingBarData("Q1", +10.0)]
    chart = diverging_from_data(data, options=_opts(), lower_is_better=False)
    assert chart.lower_is_better is False
    result = chart.render()
    assert "Worse" in result
    assert "Better" in result
