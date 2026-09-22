"""Regression test for the empty individual-year panel in the region diagnostic.

NDVI reaches this code as an 8-day composite: ~46 valid days in 366, and the
longest run of consecutive valid days is ONE (measured on Thailand's Northern
Region, maize, every year 2015-2026). ``ax.plot`` cannot draw a line segment
between two points separated by NaN, so panel (C) rendered blank while holding
a full 12-year legend -- the data was present the whole time.

Two things must hold: the panel plots an interpolated series so segments exist,
and it plots only the years actually behind the median.
"""

import inspect

import numpy as np
import pytest
import pandas as pd

from geocif.cropcal import plots, series


def _sparse_year(seed, n_days=366, every=8):
    """One year of 8-day-composite NDVI: valid every 8th day, NaN elsewhere."""
    rng = np.random.default_rng(seed)
    col = np.full(n_days, np.nan)
    idx = np.arange(0, n_days, every)
    col[idx] = 0.3 + 0.3 * rng.random(idx.size)
    return col


def test_sparse_composite_has_no_consecutive_days():
    """The premise: without interpolation there is nothing for a line to join."""
    col = pd.Series(_sparse_year(0), index=range(1, 367))
    valid = col.dropna().index.to_numpy()

    assert np.all(np.diff(valid) > 1), "8-day composites are never adjacent"
    # Interpolation is what makes a drawable segment out of them.
    assert col.interpolate(limit_area="inside").notna().sum() > col.notna().sum()


def test_year_panel_interpolates_and_marks_observations():
    source = inspect.getsource(plots.region_diagnostic)

    # The line must come from the interpolated column ...
    assert 'observed.interpolate(limit_area="inside")' in source
    # ... with the raw observations still visible as points.
    assert 'marker="."' in source
    # ... and no bare plot of the un-interpolated column, which is the bug.
    assert "climatology.ndvi_years[column]" not in source


def test_year_panel_plots_only_the_years_behind_the_median():
    source = inspect.getsource(plots.region_diagnostic)

    assert "series.select_climatology_years(" in source
    assert "for column in climatology.ndvi_years.columns" not in source


def test_panel_uses_a_field_the_plotter_is_actually_given():
    """0.4.1043 shipped `context.num_years`, which RegionContext does not have.

    Only Settings carries num_years and Settings is not passed to the plotter,
    so every diagnostic died in the caught-and-logged path: "diagnostic failed
    for Northern Region Thailand/maize: 'RegionContext' object has no attribute
    'num_years'" -- six regions, zero figures, run reported success.
    """
    from geocif.cropcal.pipeline import RegionContext
    from geocif.cropcal.series import RegionClimatology

    source = inspect.getsource(plots.region_diagnostic)
    assert "context.num_years" not in source

    context_fields = set(RegionContext.__dataclass_fields__)
    climatology_fields = set(RegionClimatology.__dataclass_fields__)
    assert "num_years" not in context_fields
    assert "n_years" in climatology_fields
    assert "climatology.n_years" in source


@pytest.mark.parametrize("n_columns", [1, 2, 3, 5, 6, 12])
def test_reselecting_with_n_years_is_idempotent(n_columns):
    """The panel re-selects with the count the first selection produced.

    That is only safe if selecting twice gives the same columns -- including
    the short-record cases, where drop_last eats one of very few years.
    """
    frame = pd.DataFrame(
        {year: np.full(366, 0.5) for year in range(2015, 2015 + n_columns)},
        index=range(1, 367),
    )

    first = series.select_climatology_years(frame, 5)
    again = series.select_climatology_years(frame, first.shape[1])

    assert list(again.columns) == list(first.columns)


def test_selection_matches_what_the_median_consumes():
    """The panel's years and the median's years must be the same set."""
    frame = pd.DataFrame(
        {year: _sparse_year(year) for year in range(2015, 2027)},
        index=range(1, 367),
    )

    selected = series.select_climatology_years(frame, 5)

    # Newest year dropped as partial, then the last five.
    assert list(selected.columns) == [2021, 2022, 2023, 2024, 2025]
    # And the median is built from exactly those.
    median = series.per_day_median(frame, 5)
    expected = selected.interpolate(axis=0, limit_area="inside").median(axis=1)
    assert np.allclose(median, expected.to_numpy(), equal_nan=True)
