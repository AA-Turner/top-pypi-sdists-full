"""Basic tests for Altex library."""

import altair as alt
import pandas as pd
import pytest

import altex


def test_imports():
    """Test that all main functions can be imported."""
    assert hasattr(altex, "line_chart")
    assert hasattr(altex, "bar_chart")
    assert hasattr(altex, "scatter_chart")
    assert hasattr(altex, "area_chart")
    assert hasattr(altex, "hist_chart")
    assert hasattr(altex, "sparkline_chart")
    assert hasattr(altex, "get_stocks_data")
    assert hasattr(altex, "get_weather_data")


def test_data_functions():
    """Test that data loading functions work."""
    # Test get_random_data (doesn't require network)
    random_data = altex.get_random_data()
    assert isinstance(random_data, pd.DataFrame)
    assert len(random_data) == 20
    assert len(random_data.columns) == 8  # 7 data columns + index


def test_chart_creation():
    """Test that the underlying chart function works."""
    # Create sample data
    data = pd.DataFrame(
        {
            "x": range(5),
            "y": [i**2 for i in range(5)],
            "category": ["A", "B", "A", "B", "A"],
        }
    )

    # Test using the internal _chart function that returns Altair objects
    from altex.charts import _chart

    # Test line chart
    chart = _chart("line", data=data, x="x", y="y")
    assert isinstance(chart, alt.Chart)

    # Test bar chart
    chart = _chart("bar", data=data, x="x", y="y")
    assert isinstance(chart, alt.Chart)

    # Test point chart (scatter)
    chart = _chart("point", data=data, x="x", y="y", color="category")
    assert isinstance(chart, alt.Chart)


def test_chart_with_options():
    """Test charts with various options."""
    data = pd.DataFrame({"x": range(5), "y": [i**2 for i in range(5)]})

    from altex.charts import _chart

    # Test with title and dimensions
    chart = _chart(
        "line", data=data, x="x", y="y", title="Test Chart", width=400, height=300
    )
    assert isinstance(chart, alt.Chart)

    # Test sparkline
    chart = _chart("line", data=data, x="x", y="y", spark=True)
    assert isinstance(chart, alt.Chart)


def test_version():
    """Test that version is available."""
    assert hasattr(altex, "__version__")
    assert isinstance(altex.__version__, str)


if __name__ == "__main__":
    pytest.main([__file__])
