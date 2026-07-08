"""Regression tests for SPI3/SPI6 integration in the CID pipeline.

Guards against the two failure modes that broke the initial enable attempt:

1. `filter_data_for_stage` restricts `df_base_period` to the stage months,
   leaving 8-month gaps between years — icclim SPI rejects the gappy input
   with "overlapping depth 5 is larger than your array 4". Fix: pass the
   full multi-year df_group for indices in _ICCLIM_BYPASS_CACHE.

2. `process_row` used to do `df.iloc[[0]]` unconditionally — SPI emits one
   row per month within the requested time_range, so a 4-month stage window
   would drop Feb/Mar/Apr and keep only January. Fix: aggregate multi-row
   SPI output to its mean before the iloc.
"""

import pandas as pd
from unittest import mock

from geocif.cid import indices as indices_mod
from geocif.cid import definitions as di


def test_spi3_and_spi6_are_in_index_dict():
    """SPI3 and SPI6 must be enabled in dict_indices — the whole point
    of enabling drought signal detection. If someone re-comments them
    without also removing this test, the test fails and flags the
    regression before the pipeline silently misses El Niño years."""
    assert "SPI3" in di.dict_indices, (
        "SPI3 disabled in dict_indices — El Niño drought years "
        "(e.g. Brazil 2016 Cerrado) will lack the strongest precip-based "
        "signal in the feature set."
    )
    assert "SPI6" in di.dict_indices, "SPI6 disabled in dict_indices"


def test_spi_indices_are_in_bypass_cache():
    """_ICCLIM_BYPASS_CACHE drives both (a) full-df_group base period in
    process_group and (b) monthly-mean aggregation in process_row. If SPI
    isn't in this set, both fixes are bypassed and the runtime errors
    return."""
    assert "SPI3" in indices_mod._ICCLIM_BYPASS_CACHE
    assert "SPI6" in indices_mod._ICCLIM_BYPASS_CACHE


def _make_stub_group(cls):
    """Build a minimal stub instance of ProcessGroupLike with just the fields
    the code paths under test touch. Avoids the full class init."""
    obj = cls.__new__(cls)
    obj.method = "monthly_r"
    obj.season = 1
    obj.harvest_year = 2016
    obj.crop = "maize"
    obj.file_name = "brazil_maize_s1_2016.csv"
    obj.show_progress = False
    obj.suppress_icclim_logs = True
    obj.stage_mode = "cumulative"

    class _StubLogger:
        def info(self, *a, **k): pass
        def warning(self, *a, **k): pass
        def error(self, *a, **k): pass
    obj.logger = _StubLogger()
    return obj


def test_process_row_aggregates_multi_row_spi_output():
    """SPI emits monthly rows within the time_range window. process_row must
    average them to a single stage-level value instead of iloc[[0]]-ing
    Jan and dropping Feb-Apr."""
    # Find the process_row-bearing class dynamically — it lives on a class
    # in indices_mod but the name varies. Grab the first class defining it.
    cls = None
    for name in dir(indices_mod):
        candidate = getattr(indices_mod, name)
        if isinstance(candidate, type) and "process_row" in vars(candidate):
            cls = candidate
            break
    assert cls is not None, "process_row not found on any class in indices_mod"

    obj = _make_stub_group(cls)

    # Simulate SPI3 icclim output for a 4-month stage window (Jan-Apr 2016):
    # one row per month, values ranging from mild to severe drought.
    df_icclim = pd.DataFrame({
        "lat": [-15.78] * 4,
        "lon": [-47.80] * 4,
        "time": pd.to_datetime(["2016-01-15", "2016-02-15", "2016-03-15", "2016-04-15"]),
        "SPI3": [-0.8, -1.4, -1.5, -0.9],  # mean = -1.15
    })

    df_harvest_year_region = pd.DataFrame({"Area": [42000.0]})

    out = obj.process_row(
        df_icclim.copy(), df_harvest_year_region, [1, 2, 3, 4],
        ("brazil", "distrito_federal"), "SPI3", "Drought", "SPI (3-month)"
    )

    assert len(out) == 1, f"process_row should return exactly 1 row per stage, got {len(out)}"
    stored = float(out["CID"].iloc[0])
    expected = -1.15
    assert abs(stored - expected) < 1e-6, (
        f"SPI3 CID should be the mean of monthly values ({expected}), "
        f"not the first month's value (-0.8). Got {stored}. "
        f"The old iloc[[0]] behavior would return -0.8 and hide Feb-Apr drought."
    )


def test_process_row_single_row_unchanged_for_non_spi():
    """Non-SPI indices (e.g. CDD, PRCPTOT) should still take the first row
    as before — the SPI aggregation must be gated on _ICCLIM_BYPASS_CACHE
    membership, not applied globally."""
    cls = None
    for name in dir(indices_mod):
        candidate = getattr(indices_mod, name)
        if isinstance(candidate, type) and "process_row" in vars(candidate):
            cls = candidate
            break
    obj = _make_stub_group(cls)

    df_icclim = pd.DataFrame({
        "lat": [-15.78], "lon": [-47.80], "PRCPTOT": [340.5],
    })
    df_harvest_year_region = pd.DataFrame({"Area": [42000.0]})

    out = obj.process_row(
        df_icclim.copy(), df_harvest_year_region, [1],
        ("brazil", "distrito_federal"), "PRCPTOT", "Rain", "Total precip"
    )
    assert len(out) == 1
    assert abs(float(out["CID"].iloc[0]) - 340.5) < 1e-6


def test_process_row_handles_multi_row_non_spi_by_taking_first():
    """Non-SPI indices that somehow emit multiple rows must still use the
    original first-row semantics (unchanged behavior). This locks the
    aggregation branch to SPI only."""
    cls = None
    for name in dir(indices_mod):
        candidate = getattr(indices_mod, name)
        if isinstance(candidate, type) and "process_row" in vars(candidate):
            cls = candidate
            break
    obj = _make_stub_group(cls)

    df_icclim = pd.DataFrame({
        "lat": [-15.78, -15.78], "lon": [-47.80, -47.80],
        "CDD": [12.0, 99.0],  # first-row wins → 12.0, not mean 55.5
    })
    df_harvest_year_region = pd.DataFrame({"Area": [42000.0]})

    out = obj.process_row(
        df_icclim.copy(), df_harvest_year_region, [1],
        ("brazil", "distrito_federal"), "CDD", "Drought", "Consecutive dry days"
    )
    assert len(out) == 1
    assert abs(float(out["CID"].iloc[0]) - 12.0) < 1e-6, (
        "Non-SPI indices must retain first-row semantics — the SPI mean-"
        "aggregation branch must not accidentally activate for other indices."
    )
