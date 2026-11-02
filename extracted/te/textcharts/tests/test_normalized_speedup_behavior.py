from __future__ import annotations

from textcharts import (
    ChartOptions,
    NormalizedSpeedup,
    SpeedupData,
    speedup_from_ratios,
)


def test_normalized_speedup_renders_faster_and_slower_sides():
    data = [
        SpeedupData("SQLite", 1.0, True),
        SpeedupData("DuckDB", 8.2, False),
        SpeedupData("Pandas", 0.4, False),
    ]
    result = NormalizedSpeedup(data=data, options=ChartOptions(use_color=False)).render()
    assert "SQLite" in result
    assert "DuckDB" in result
    assert "Pandas" in result
    assert "Slower" in result
    assert "Faster" in result
    assert "8.20x" in result
    assert "0.40x" in result


def test_normalized_speedup_handles_empty_and_invalid_ratios():
    assert "No data" in NormalizedSpeedup(data=[]).render()
    assert NormalizedSpeedup._format_ratio(0.0) == "N/A"
    assert NormalizedSpeedup._format_ratio(float("inf")) == "N/A"
    assert NormalizedSpeedup._format_ratio(150.0) == "150x"
    assert NormalizedSpeedup._format_ratio(15.0) == "15.0x"


def test_speedup_from_ratios_selects_requested_baseline_modes():
    slowest = speedup_from_ratios(
        [("A", 100), ("B", 500), ("C", 200)],
        baseline="slowest",
        options=ChartOptions(use_color=False),
    ).render()
    fastest = speedup_from_ratios(
        [("A", 100), ("B", 500), ("C", 200)],
        baseline="fastest",
        options=ChartOptions(use_color=False),
    ).render()
    assert "1.00x" in slowest
    assert "1.00x" in fastest


def test_speedup_from_ratios_handles_empty_and_zero_baseline_inputs():
    empty = speedup_from_ratios([], options=ChartOptions(use_color=False)).render()
    zeroish = speedup_from_ratios(
        [("A", 0.0), ("B", 10.0)],
        baseline="A",
        options=ChartOptions(use_color=False),
    ).render()
    assert "No data" in empty
    assert "N/A" in zeroish
