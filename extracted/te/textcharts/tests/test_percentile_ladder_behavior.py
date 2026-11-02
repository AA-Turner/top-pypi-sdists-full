from __future__ import annotations

from textcharts import ChartOptions, PercentileData, PercentileLadder
from textcharts.percentile_ladder import compute_percentile, from_series


def _opts(**kw):
    return ChartOptions(use_color=False, width=80, **kw)


def test_empty_data():
    assert "No data" in PercentileLadder(data=[]).render()


def test_percentile_bands_appear_in_output():
    data = [PercentileData("Platform1", p50=10, p90=50, p95=80, p99=120)]
    result = PercentileLadder(data=data, options=_opts()).render()
    assert "Platform1" in result
    assert "P50" in result
    assert "P90" in result
    assert "P95" in result
    assert "P99" in result


def test_annotation_values_shown():
    data = [PercentileData("A", p50=10.0, p90=50.0, p95=80.0, p99=120.0)]
    result = PercentileLadder(data=data, options=_opts()).render()
    assert "10.0" in result
    assert "50.0" in result
    assert "80.0" in result
    assert "120.0" in result


def test_multiple_platforms_rendered():
    data = [
        PercentileData("Fast", p50=5, p90=20, p95=30, p99=50),
        PercentileData("Slow", p50=50, p90=200, p95=300, p99=500),
    ]
    result = PercentileLadder(data=data, options=_opts()).render()
    assert "Fast" in result
    assert "Slow" in result


def test_non_finite_annotation_shows_na():
    data = [PercentileData("X", p50=float("inf"), p90=10.0, p95=20.0, p99=30.0)]
    result = PercentileLadder(data=data, options=_opts()).render()
    assert "N/A" in result


def test_compute_percentile_edge_cases():
    assert compute_percentile([], 50) == 0.0
    assert compute_percentile([42.0], 50) == 42.0
    assert compute_percentile([10.0, 20.0], 50) == 15.0
    assert compute_percentile([1.0, 2.0, 3.0, 4.0, 5.0], 0) == 1.0
    assert compute_percentile([1.0, 2.0, 3.0, 4.0, 5.0], 100) == 5.0


def test_from_series_factory():
    platform_queries = [
        ("DuckDB", [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]),
        ("SQLite", [50, 100, 150, 200, 250, 300, 350, 400, 450, 500]),
    ]
    chart = from_series(platform_queries, title="Factory Test", options=_opts())
    result = chart.render()
    assert isinstance(chart, PercentileLadder)
    assert "Factory Test" in result
    assert "DuckDB" in result
    assert "SQLite" in result


def test_from_series_empty_values():
    platform_queries = [("Empty", [])]
    chart = from_series(platform_queries, options=_opts())
    result = chart.render()
    # Empty values should produce zeros
    assert "0.0" in result


def test_unicode_vs_ascii_fill_chars():
    data = [PercentileData("A", p50=10, p90=50, p95=80, p99=120)]
    unicode_result = PercentileLadder(data=data, options=_opts(use_unicode=True)).render()
    ascii_result = PercentileLadder(data=data, options=_opts(use_unicode=False)).render()
    # Unicode uses ░▒▓█, ASCII uses .=#@
    assert any(c in unicode_result for c in "░▒▓█")
    assert any(c in ascii_result for c in ".=#@")
