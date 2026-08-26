"""Regression test: unusable statistics CSVs must not crash the plotting stage.

_load_observed_baselines derives every anomaly-window bound from
``int(df_all["Harvest Year"].max())``. A statistics CSV that exists but carries
no usable rows makes that max() return NaN, and int(NaN) raises
``ValueError: cannot convert float NaN to integer`` — which killed a
yield_outlook run on the cluster at the very first plotting combo (0/8), after
all 88 model executions had already completed.

Two ways in, both reproduced below:
  * every "Yield (tn per ha)" is NaN -> the dropna empties the frame
  * every "Harvest Year" is NaN/non-numeric -> max() of an all-NaN column

The no-files case already returned {} and the caller handles that, so an
unusable file must take the same path rather than aborting the run.
"""
import configparser

import numpy as np
import pandas as pd
import pytest

from geocif import utils
from geocif.yield_outlook import _load_observed_baselines

METHOD = "monthly_r"
PROJECT = "geocif"
COUNTRY = "kenya"
CROP = "maize"


def _parser(dir_output):
    p = configparser.ConfigParser()
    p.add_section("PATHS")
    p.set("PATHS", "dir_output", str(dir_output))
    # DEFAULT is configparser's reserved default section — set, don't add.
    p["DEFAULT"]["project_name"] = PROJECT
    p["DEFAULT"]["method"] = METHOD
    return p


def _write_stats(tmp_path, df):
    """Drop a statistics CSV where _load_observed_baselines will look for it."""
    f = utils.statistics_file_path(tmp_path / PROJECT, METHOD, COUNTRY, CROP)
    f.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(f, index=False)
    return f


def test_all_nan_yields_returns_empty_not_valueerror(tmp_path):
    """CSV exists, but no observed yields -> {} like the no-files case."""
    _write_stats(tmp_path, pd.DataFrame({
        "Region": ["a", "b"],
        "Harvest Year": [2020, 2021],
        "Yield (tn per ha)": [np.nan, np.nan],
    }))
    out = _load_observed_baselines(
        [COUNTRY], CROP, _parser(tmp_path), current_year=2026
    )
    assert out == {}


def test_all_nan_harvest_years_returns_empty_not_valueerror(tmp_path):
    """Yields present but no parseable year -> nothing to window on."""
    _write_stats(tmp_path, pd.DataFrame({
        "Region": ["a", "b"],
        "Harvest Year": [np.nan, np.nan],
        "Yield (tn per ha)": [3.0, 4.0],
    }))
    out = _load_observed_baselines(
        [COUNTRY], CROP, _parser(tmp_path), current_year=2026
    )
    assert out == {}


def test_non_numeric_harvest_years_return_empty(tmp_path):
    """A text year column must coerce, not compare str >= int."""
    _write_stats(tmp_path, pd.DataFrame({
        "Region": ["a", "b"],
        "Harvest Year": ["n/a", "unknown"],
        "Yield (tn per ha)": [3.0, 4.0],
    }))
    out = _load_observed_baselines(
        [COUNTRY], CROP, _parser(tmp_path), current_year=2026
    )
    assert out == {}


def test_partial_nan_years_still_yield_baselines(tmp_path):
    """The guard must drop only the bad rows, never the whole file."""
    _write_stats(tmp_path, pd.DataFrame({
        "Region": ["a"] * 6,
        "Harvest Year": [2021, 2022, 2023, 2024, 2025, np.nan],
        "Yield (tn per ha)": [1.0, 2.0, 3.0, 4.0, 5.0, 99.0],
    }))
    out = _load_observed_baselines(
        [COUNTRY], CROP, _parser(tmp_path), current_year=2026
    )
    assert "2021-2025" in out, f"expected rolling window, got {list(out)}"
    # mean of 1..5 — the NaN-year row (99.0) must not pollute it
    assert out["2021-2025"]["obs_mean"].iloc[0] == pytest.approx(3.0)


def test_healthy_csv_unaffected(tmp_path):
    """Guard must not change behaviour on well-formed input."""
    _write_stats(tmp_path, pd.DataFrame({
        "Region": ["a"] * 5 + ["b"] * 5,
        "Harvest Year": [2013, 2014, 2015, 2016, 2017] * 2,
        "Yield (tn per ha)": [1.0, 2.0, 3.0, 4.0, 5.0] * 2,
    }))
    out = _load_observed_baselines(
        [COUNTRY], CROP, _parser(tmp_path), current_year=2026
    )
    assert "2013-2017" in out
    assert out["2013-2017"]["obs_mean"].tolist() == [3.0, 3.0]


def test_missing_file_still_returns_empty(tmp_path):
    """Pre-existing no-files contract preserved."""
    assert _load_observed_baselines(
        [COUNTRY], CROP, _parser(tmp_path), current_year=2026
    ) == {}
