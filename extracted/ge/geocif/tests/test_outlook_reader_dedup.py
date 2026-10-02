"""Audit A8 — the outlook-DB READERS must de-duplicate upsert copies.

The writer's upsert key includes the wall-clock ``Time`` (geocif.py), so a
re-run into the same outlook DB appends a SECOND copy of every logical row
instead of replacing it. ``_outlook_db.dedup_upserts`` existed but only the
viz loaders and predictions_export used it; ``_query_predictions``, the FDW
reader, compare_forecasts and report_lite read raw rows, so metrics
double-weighted every region and ``.last()`` picked an arbitrary copy.

Every reader below is fed a tiny SQLite DB holding a STALE and a FRESH copy
of the same logical row (fresh inserted FIRST so insertion order cannot
rescue the assertion) and must return exactly one row with the fresh value.
The writer's timestamp formats are month-name-first
(``Date='September_06_2026'``, ``Time='September-06-2026 11:31:05'``).
"""
import sqlite3

import pandas as pd
import pytest

OBS = "Observed Yield (tn per ha)"
PRED = "Predicted Yield (tn per ha)"
FRESH = ("September_06_2026", "September-06-2026 11:31:05")
STALE = ("February_10_2026", "February-10-2026 08:00:00")


def _write(db_path, table, rows):
    con = sqlite3.connect(str(db_path))
    pd.DataFrame(rows).to_sql(table, con, index=False)
    con.close()
    return db_path


def _swd(stage):
    """Calendar-order display label of a reverse-cumulative Stage Name:
    "Aug 1-Mar 31" (as-of Aug, planting Mar) -> "Mar 1-Aug 31"."""
    asof, planting = (p.split()[0] for p in stage.split("-"))
    return f"{planting} 1-{asof} 31"


def _row(pred, date_time, *, region="Iowa", year=2024, stage="Aug 1-Mar 31",
         season=None, model="tabpfn", experiment="outlook"):
    return {
        "Experiment Name": experiment, "Model": model, "Country": "usa",
        "Region": region, "Season": season, "Harvest Year": year,
        "Stage Name": stage, "Stage Window Display": _swd(stage),
        PRED: pred, OBS: 10.0, "Area (ha)": 100.0,
        "Last Observed Yield (tn per ha)": 9.5, "Last Observed Year": 2023,
        "Median Yield (tn per ha)": 9.8,
        "Date": date_time[0], "Time": date_time[1],
    }


def test_query_predictions_keeps_latest_written_copy(tmp_path):
    from geocif.yield_outlook import _query_predictions

    db = _write(tmp_path / "o.db", "usa_maize",
                [_row(4.0, FRESH), _row(1.0, STALE),
                 _row(7.0, FRESH, region="Ohio")])
    df = _query_predictions(db, "usa_maize", "tabpfn", experiment_name="outlook")
    assert len(df) == 2
    assert float(df.loc[df["Region"] == "Iowa", PRED].iloc[0]) == 4.0
    # Bookkeeping columns do not leak into the canonical frame.
    assert "Date" not in df.columns and "Time" not in df.columns


def test_query_predictions_keeps_both_seasons(tmp_path):
    """Season is part of a row's identity: Gu and Deyr are not duplicates."""
    from geocif.yield_outlook import _query_predictions

    db = _write(tmp_path / "o.db", "somalia_maize",
                [_row(2.0, FRESH, season=1), _row(1.5, FRESH, season=2)])
    df = _query_predictions(db, "somalia_maize", "tabpfn", experiment_name="outlook")
    assert len(df) == 2
    assert sorted(df["Season"].astype(int)) == [1, 2]


def test_fdw_query_forecast_dedups(tmp_path):
    from geocif.fdw_export import _query_forecast

    db = _write(tmp_path / "o.db", "usa_maize",
                [_row(4.0, FRESH), _row(1.0, STALE)])
    df = _query_forecast(db, "usa_maize", "tabpfn", "outlook", 2024)
    assert len(df) == 1
    assert float(df[PRED].iloc[0]) == 4.0
    assert "Date" in df.columns and "Time" not in df.columns


def test_compare_forecasts_reader_dedups(tmp_path):
    from geocif.compare_forecasts import _query_mape_by_stage

    db = _write(tmp_path / "o.db", "usa_maize",
                [_row(4.0, FRESH), _row(1.0, STALE)])
    df = _query_mape_by_stage(db, "usa_maize", "tabpfn", experiment_name="outlook")
    assert len(df) == 1
    assert float(df[PRED].iloc[0]) == 4.0
    assert float(df["MAPE"].iloc[0]) == pytest.approx(60.0)
    assert not {"Date", "Time", "Season"} & set(df.columns)


def test_report_lite_table_dedups_and_keeps_one_row_per_region(tmp_path):
    """Two bugs in one reader: upsert copies AND one row per STAGE per region
    under ``run_time_steps = all`` (the lexical-max stage "May" would win)."""
    from geocif.report_lite import _read_predicted_yield_table

    rows = [
        _row(4.0, FRESH),                                  # Aug, fresh
        _row(1.0, STALE),                                  # Aug, stale copy
        _row(9.0, FRESH, stage="May 1-Mar 31"),            # earlier stage
        _row(3.0, FRESH, region="Ohio", stage="Jul 1-Mar 31"),
        _row(8.0, FRESH, region="Ohio", stage="Sep 1-Mar 31"),  # latest
    ]
    for r in rows:
        r["Season"] = 1
    db = _write(tmp_path / "o.db", "usa_maize", rows)
    df, seasons = _read_predicted_yield_table(db, "usa", "maize", "tabpfn", 2024)
    assert len(df) == 2
    got = dict(zip(df["Region"], df[PRED]))
    assert got == {"Iowa": 4.0, "Ohio": 8.0}
    assert seasons == [1]
    # Helper columns never reach the table builder.
    assert not {"Stage Name", "Stage Window Display", "Date", "Time"} & set(df.columns)
    assert "Last Observed Yield (tn per ha)" in df.columns


def test_dedup_upserts_without_timestamp_columns_keeps_last_inserted():
    from geocif.viz._outlook_db import dedup_upserts

    df = pd.DataFrame({"Region": ["a", "a", "b"], PRED: [1.0, 2.0, 3.0]})
    out = dedup_upserts(df, ["Region"], "t")
    assert out[PRED].tolist() == [2.0, 3.0]
    # Date only (no Time) still orders by the parsed date.
    df2 = pd.DataFrame({"Region": ["a", "a"], PRED: [5.0, 6.0],
                        "Date": ["December_01_2026", "February_15_2026"]})
    assert dedup_upserts(df2, ["Region"], "t")[PRED].tolist() == [5.0]
