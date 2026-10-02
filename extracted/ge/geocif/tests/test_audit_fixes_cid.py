"""CID-extraction fixes from the 2026-09-30 audit.

- A0  percentile / spell indices were blanked on every leap-year window
      spanning Feb 29 (Feb 29 was removed from the icclim input, so the
      season window had a missing day and ``missing="any"`` returned NaN,
      which the ML layer then zero-filled).
- A0e ENSO scalars were emitted once per (region, year) under whichever
      stage window came first, so the forecast year's column never lined
      up with the hindcast years', and ONI_curr_MAM was attached to stages
      ending before May.
- B   dekad numbering did not match ``utils.compute_time_periods``.
- B   pre-season / current-month decisions read the UTC month.
"""
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

pytest.importorskip("icclim")
from geocif.cid import indices as ix  # noqa: E402


# --------------------------------------------------------------------------
# ENSO
# --------------------------------------------------------------------------
@pytest.mark.parametrize("iname, end, hy, expected", [
    ("ONI_prev_JJA", "2023-11-30", 2024, True),
    ("ONI_prev_NDJ", "2023-12-31", 2024, False),  # NDJ ends in January of the harvest year
    ("ONI_prev_NDJ", "2024-01-31", 2024, True),
    ("ONI_curr_DJF", "2024-02-29", 2024, True),
    ("ONI_curr_MAM", "2024-02-29", 2024, False),
    ("ONI_curr_MAM", "2024-05-31", 2024, True),
    ("MEI_curr_MA", "2024-03-31", 2024, False),
    ("MEI_curr_MA", "2024-04-30", 2024, True),
    ("MEI_prev_ND", "2023-11-30", 2024, False),
    ("NOT_AN_ENSO_INDEX", "2024-01-01", 2024, True),
])
def test_enso_availability_follows_the_season_end(iname, end, hy, expected):
    assert ix.enso_available(iname, pd.Timestamp(end), hy) is expected


def test_enso_availability_without_a_window_end_is_permissive():
    assert ix.enso_available("ONI_curr_MAM", None, 2024) is True
    assert ix.enso_available("ONI_curr_MAM", pd.NaT, 2024) is True


def _cids(harvest_year=2024):
    obj = ix.CIDs.__new__(ix.CIDs)
    obj.country = "kenya"
    obj.crop = "maize"
    obj.season = 1
    obj.method = "monthly_r"
    obj.harvest_year = harvest_year
    return obj


def _window(start, end, **cols):
    t = pd.date_range(start, end, freq="D")
    df = pd.DataFrame({"time": t, "Month": t.month})
    for name, value in cols.items():
        df[name] = value
    return df


def test_enso_rows_are_emitted_under_every_stage_window():
    obj = _cids()
    df_hy = pd.DataFrame({"Area": [100.0]})
    key = ("kenya", "nakuru")
    emitted = set()
    early = _window("2023-11-01", "2023-12-31", ONI_curr_MAM=1.5, ONI_prev_JJA=0.7)
    out1 = obj.compute_eo_indices(early, df_hy, "ENSO", key, [12, 11], emitted)
    out2 = obj.compute_eo_indices(early, df_hy, "ENSO", key, [12], emitted)
    assert sorted(out1["Index"]) == ["ONI_curr_MAM", "ONI_prev_JJA"]
    assert sorted(out2["Index"]) == ["ONI_curr_MAM", "ONI_prev_JJA"]
    assert set(out1["Stage"]) == {"12_11"}
    assert set(out2["Stage"]) == {"12"}


def test_enso_current_year_index_is_masked_until_its_season_ends():
    obj = _cids()
    df_hy = pd.DataFrame({"Area": [100.0]})
    key = ("kenya", "nakuru")
    early = _window("2023-11-01", "2023-12-31", ONI_curr_MAM=1.5, ONI_prev_JJA=0.7)
    v = obj.compute_eo_indices(early, df_hy, "ENSO", key, [12, 11], set())
    v = v.set_index("Index")["CID"]
    assert v["ONI_prev_JJA"] == pytest.approx(0.7)
    assert np.isnan(v["ONI_curr_MAM"])

    late = _window("2023-11-01", "2024-05-31", ONI_curr_MAM=1.5, ONI_prev_JJA=0.7)
    v = obj.compute_eo_indices(late, df_hy, "ENSO", key, [5, 4, 3, 2, 1, 12, 11], set())
    v = v.set_index("Index")["CID"]
    assert v["ONI_curr_MAM"] == pytest.approx(1.5)


# --------------------------------------------------------------------------
# dekad numbering / local time
# --------------------------------------------------------------------------
def test_dekad_numbering_matches_compute_time_periods():
    df = pd.DataFrame({
        "adm1_name": "a", "Season": 1, "Month": 1,
        "Doy": [1, 10, 11, 20, 21, 365, 366],
    })
    assert ix.add_season_information(df, "dekad")["dekad"].tolist() == [1, 1, 2, 2, 3, 37, 37]
    assert ix.add_season_information(df, "dekad_r")["dekad_r"].tolist() == [1, 1, 2, 2, 3, 37, 37]


def test_fraction_season_labels_each_season_on_its_own_rows():
    # Deciles are per season (the truncated forecast year is stretched over
    # the same 10..100 ids as a complete year, which is what keys its
    # stages), and the off-season rows (Season NaN) never influence them:
    # sizing on the longest group on file (tried 2026-10-01) picked the
    # off-season group and collapsed every label to 10.
    rows = []
    for season, n_days in ((2010, 20), (2011, 10)):
        for i in range(n_days):
            rows.append({"adm1_name": "a", "Season": season, "Doy": 100 + i, "Month": 4})
    for i in range(300):
        rows.append({"adm1_name": "a", "Season": np.nan, "Doy": 200 + i % 100, "Month": 8})
    out = ix.add_season_information(pd.DataFrame(rows), "fraction_season")
    full = out[out["Season"] == 2010]["fraction_season"].tolist()
    cut = out[out["Season"] == 2011]["fraction_season"].tolist()
    assert full == [10, 10, 20, 20, 30, 30, 40, 40, 50, 50, 60, 60, 70, 70, 80, 80, 90, 90, 100, 100]
    assert cut == [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]


def _indexed(start, end):
    t = pd.date_range(start, end, freq="D")
    df = pd.DataFrame({"lat": -1.0, "lon": 36.0, "time": t, "tg": 20.0})
    return df.set_index(["lat", "lon", "time"])


def test_percentile_base_period_ends_with_the_last_complete_year(monkeypatch):
    import arrow as ar
    monkeypatch.setattr(ix.utils, "local_now", lambda: ar.get("2026-10-01T12:00:00-04:00"))
    study = _indexed("2026-02-01", "2026-03-31")
    # merged file padded with calendar scaffold rows to 2028
    start_br, end_br, start_tr, end_tr = ix.get_icclim_dates(_indexed("2000-01-01", "2028-12-31"), study)
    assert start_br.startswith("2001-01-01")
    assert end_br.startswith("2025-12-31")
    assert start_tr.startswith("2026-02-01") and end_tr.startswith("2026-03-31")
    # file ending mid-2026: same base period, no drift
    _, end_br2, _, _ = ix.get_icclim_dates(_indexed("2000-01-01", "2026-09-30"), study)
    assert end_br2.startswith("2025-12-31")
    # historical file: its own last day
    _, end_br3, _, _ = ix.get_icclim_dates(_indexed("2000-01-01", "2015-06-30"), study)
    assert end_br3.startswith("2015-06-30")


def test_no_utc_month_reads_remain_in_cid_indices():
    src = Path(ix.__file__).read_text(encoding="utf-8")
    assert "utcnow().month" not in src


# --------------------------------------------------------------------------
# leap-year percentile windows (real icclim)
# --------------------------------------------------------------------------
def _daily_series(seed=0):
    rng = np.random.default_rng(seed)
    dates = pd.date_range("2000-01-01", "2024-12-31", freq="D")
    doy = dates.dayofyear.values
    tg = 20 + 8 * np.sin(2 * np.pi * doy / 365.25) + rng.normal(0, 2, len(dates))
    return pd.DataFrame({
        "lat": -1.0, "lon": 36.0, "time": dates, "tg": tg,
        "tasmax": tg + 5, "tasmin": tg - 5,
        "pr": rng.gamma(0.5, 4, len(dates)), "Season": 1,
    })


# 2024 lies outside icclim's bootstrap base period, 2012 inside it; the
# Feb-May window is the 121-vs-120-day shape that motivated the Feb 29
# drop in 0.4.366 (no longer raised by icclim 7).
@pytest.mark.parametrize("year", [2024, 2012])
@pytest.mark.parametrize("window", [("02-01", "03-31"), ("02-01", "05-31")])
@pytest.mark.parametrize("index_name", ["TG90p", "WSDI", "R95p"])
def test_percentile_index_is_not_blanked_on_leap_year_windows(index_name, window, year):
    df = _daily_series()
    start, end = window
    df_tp = df[(df["time"] >= f"{year}-{start}") & (df["time"] <= f"{year}-{end}")]
    ds = ix.compute_indices(df_tp, df, index_name)
    vals = ds.to_dataframe().reset_index()[index_name]
    assert vals.notna().all(), f"{index_name} {year} {window}: {vals.tolist()}"
