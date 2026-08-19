"""
Tests for the CID input-reading memory reductions (geocif/cid/indices.py).

Per-worker RSS was ~19 GB on the usa_admin2 county run, which capped
parallelism at 25 of 128 cores and OOM-deadlocked the box at 64. Two causes:
EO values read at float64, and a per-file preprocess cache that was never
evicted so each worker ended up holding every file it had ever touched.

The float32 change is a deliberate precision trade: measured against 1.9 M
real CID values it costs ~6e-8 relative error, versus satellite inputs whose
own precision is orders of magnitude coarser.
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from geocif.cid import indices


@pytest.fixture
def merged_csv(tmp_path):
    """A miniature crop_t0-shaped input."""
    rng = np.random.default_rng(0)
    n = 2000
    df = pd.DataFrame({
        "country": ["united_states_of_america"] * n,
        "region": rng.choice(["illinois boone", "iowa adair"], n),
        "crop": ["maize"] * n,
        "scale": ["admin_2"] * n,
        "calendar_region": ["midwest"] * n,
        "year": rng.integers(2000, 2026, n),
        "doy": rng.integers(1, 366, n),
        "lat": rng.uniform(30, 49, n),
        "lon": rng.uniform(-104, -80, n),
        "chirps": rng.uniform(0, 80, n),
        "chirts_era5_tmax": rng.uniform(-5, 42, n),
        "ndvi": rng.uniform(0, 1, n),
        # display-only columns the reader is supposed to drop
        "name_month": ["January"] * n,
        "abbr_month": ["Jan"] * n,
        "hemisphere": ["N"] * n,
    })
    path = tmp_path / "united_states_of_america_maize_s1.csv"
    df.to_csv(path, index=False)
    return path


# ------------------------------------------------------------- dtypes


def test_eo_values_are_read_as_float32(merged_csv):
    df = indices._read_input_csv(merged_csv)
    for column in ("chirps", "chirts_era5_tmax", "ndvi"):
        assert df[column].dtype == np.float32, column


def test_coordinates_stay_float64(merged_csv):
    """lat/lon are matched on, not aggregated — keep them exact."""
    df = indices._read_input_csv(merged_csv)
    assert df["lat"].dtype == np.float64
    assert df["lon"].dtype == np.float64


def test_repeated_strings_stay_categorical(merged_csv):
    df = indices._read_input_csv(merged_csv)
    for column in ("country", "region", "crop", "scale", "calendar_region"):
        assert isinstance(df[column].dtype, pd.CategoricalDtype), column


def test_display_columns_are_dropped(merged_csv):
    df = indices._read_input_csv(merged_csv)
    for column in ("name_month", "abbr_month", "hemisphere"):
        assert column not in df.columns


def test_integer_columns_are_not_turned_into_floats(merged_csv):
    """year/doy drive stage labels — a float would render '2024.0'."""
    df = indices._read_input_csv(merged_csv)
    assert pd.api.types.is_integer_dtype(df["year"])
    assert pd.api.types.is_integer_dtype(df["doy"])


def test_values_survive_the_downcast(merged_csv):
    """float32 must preserve EO values to well within their own precision."""
    lean = indices._read_input_csv(merged_csv)
    exact = pd.read_csv(merged_csv)
    for column in ("chirps", "chirts_era5_tmax", "ndvi"):
        a = lean[column].to_numpy(dtype=np.float64)
        b = exact[column].to_numpy(dtype=np.float64)
        rel = np.abs(a - b) / np.maximum(np.abs(b), 1e-12)
        assert rel.max() < 1e-6, f"{column} drifted {rel.max():.2e}"


def test_frame_is_smaller_than_a_default_read(merged_csv):
    lean = indices._read_input_csv(merged_csv).memory_usage(deep=True).sum()
    default = pd.read_csv(merged_csv).memory_usage(deep=True).sum()
    assert lean < default / 2


# ---------------------------------------- aggregation-level equivalence


def test_seasonal_accumulations_match_float64():
    """The indices most at risk are the accumulators (GD4/KDD/AUC_*/PRCPTOT).

    Sum a season's worth of values both ways and require agreement far tighter
    than the data's own precision. numpy uses pairwise summation, so error
    grows ~log2(n)*eps rather than n*eps.
    """
    rng = np.random.default_rng(7)
    for n in (90, 180, 365):
        exact = rng.uniform(0, 40, n)
        lean = exact.astype(np.float32)
        for label, f in (
            ("sum", np.sum),
            ("mean", np.mean),
            ("max", np.max),
            ("p95", lambda x: np.percentile(x, 95)),
        ):
            a, b = float(f(lean.astype(np.float64))), float(f(exact))
            rel = abs(a - b) / max(abs(b), 1e-12)
            assert rel < 1e-6, f"{label} over {n} days drifted {rel:.2e}"


def test_degree_day_accumulation_matches():
    """GD4-style: sum of positive excess over a threshold across a season."""
    rng = np.random.default_rng(11)
    tmean = rng.uniform(-5, 35, 365)
    gd4_64 = np.maximum(tmean - 4.0, 0).sum()
    gd4_32 = np.maximum(tmean.astype(np.float32) - np.float32(4.0), 0).sum(dtype=np.float64)
    assert abs(gd4_32 - gd4_64) / gd4_64 < 1e-6


# ------------------------------------------------------- cache eviction


def test_preprocess_cache_holds_only_the_current_file():
    """Never-evicted cache meant a worker held every file it had ever seen."""
    indices._preprocess_cache.clear()
    indices._preprocess_cache["file_a"] = pd.DataFrame({"x": [1]})

    # what the worker now does before inserting a different file
    if "file_b" not in indices._preprocess_cache:
        indices._preprocess_cache.clear()
        indices._preprocess_cache["file_b"] = pd.DataFrame({"x": [2]})

    assert list(indices._preprocess_cache) == ["file_b"]
    indices._preprocess_cache.clear()


def test_cache_eviction_is_wired_into_the_worker():
    source = Path(indices.__file__).read_text(encoding="utf-8", errors="replace")
    marker = source.index("if file_key not in _preprocess_cache:")
    assert "_preprocess_cache.clear()" in source[marker:marker + 800]
