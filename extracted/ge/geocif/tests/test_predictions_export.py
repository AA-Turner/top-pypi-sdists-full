"""Tests for geocif.predictions_export.

Covers the three things that make this export wrong in ways nobody notices:
the lead derivation (reversed stage names would invert it), the upsert
de-duplication (a re-run silently doubles every row), and the experiment-name
filter (``geocif_runner`` writes ``default``, ``yield_outlook`` writes
``outlook`` -- reading the wrong one returns an empty file, not an error).
"""

import configparser
import sqlite3

import pandas as pd
import pytest

from geocif import predictions_export as px

OBS_DB = "Observed Yield (tn per ha)"
PRED_DB = "Predicted Yield (tn per ha)"


# --------------------------------------------------------------------------
# lead / month derivation
# --------------------------------------------------------------------------

@pytest.mark.parametrize("swd,expected", [
    ("Sep 1-Sep 30", (1, "September")),
    ("Sep 1-Dec 31", (4, "December")),
    ("Sep 1-Jan 31", (5, "January")),    # wraps the New Year
    ("Sep 1-Apr 30", (8, "April")),
    ("Mar 1-Mar 31", (1, "March")),
    ("Mar 1-Aug 31", (6, "August")),
])
def test_lead_and_month(swd, expected):
    assert px._lead_and_month(swd) == expected


@pytest.mark.parametrize("bad", [None, "", "10%-100%", "Stages 1-3", "nonsense", 42])
def test_lead_and_month_unparseable(bad):
    assert px._lead_and_month(bad) == (None, None)


def test_lead_is_monotonic_across_the_new_year():
    """The reason lead exists: a month NUMBER sorts Jan(1) before Sep(9)."""
    windows = ["Sep 1-Sep 30", "Sep 1-Oct 31", "Sep 1-Nov 30", "Sep 1-Dec 31",
               "Sep 1-Jan 31", "Sep 1-Feb 28", "Sep 1-Mar 31", "Sep 1-Apr 30"]
    leads = [px._lead_and_month(w)[0] for w in windows]
    assert leads == [1, 2, 3, 4, 5, 6, 7, 8]


# --------------------------------------------------------------------------
# yield column resolution
# --------------------------------------------------------------------------

def test_resolve_yield_columns_canonical():
    cols = ["Region", OBS_DB, PRED_DB, "Median Yield (tn per ha)"]
    assert px._resolve_yield_columns(cols) == (PRED_DB, OBS_DB)


def test_resolve_yield_columns_rename_target():
    """rename_target = True stores the short names; prefix match must find them."""
    cols = ["Region", "Observed Yield", "Predicted Yield"]
    assert px._resolve_yield_columns(cols) == ("Predicted Yield", "Observed Yield")


def test_resolve_yield_columns_ignores_class_column():
    """Classification mode adds 'Observed Yield..._class'; it is not the truth."""
    cols = ["Region", "Observed Yield (tn per ha)_class", OBS_DB, PRED_DB]
    _, obs = px._resolve_yield_columns(cols)
    assert obs == OBS_DB


# --------------------------------------------------------------------------
# end-to-end against a synthetic DB
# --------------------------------------------------------------------------

def _make_parser():
    p = configparser.ConfigParser(interpolation=None)
    p["DEFAULT"] = {"countries": "['brazil']"}
    p["ML"] = {"pool_countries": "False"}
    p["brazil"] = {"crops": "['soybean']"}
    return p


def _rows(n_dup=0, experiment="default"):
    base = []
    for year in (2023, 2024):
        for lead, swd in enumerate(["Sep 1-Sep 30", "Sep 1-Oct 31"], start=1):
            base.append({
                "Experiment Name": experiment,
                "Region": "Mato Grosso Sorriso",
                "Harvest Year": str(year),
                "Stage Name": swd,
                "Stage Window Display": swd,
                "Model": "catboost",
                "Date": "September_06_2026",
                "Time": "September-06-2026 11:31:05",
                "Area (ha)": 1000.0 + lead,
                PRED_DB: 3.0 + lead,
                OBS_DB: 3.5,
            })
    # Stale duplicates: same logical key, written EARLIER, different value.
    for r in base[:n_dup]:
        stale = dict(r)
        stale["Date"] = "August_01_2026"
        stale["Time"] = "August-01-2026 09:00:00"
        stale[PRED_DB] = -999.0
        base.append(stale)
    return base


def _write_db(path, rows):
    con = sqlite3.connect(path)
    pd.DataFrame(rows).to_sql("brazil_soybean", con, index=False)
    con.close()


@pytest.fixture
def patched_lookup(monkeypatch):
    """Avoid needing a real shapefile; mirror the real composite-name join."""
    monkeypatch.setattr(
        px, "_region_id_lookup",
        lambda parser, country: ({"mato grosso sorriso": 5107925}, "num_ID"),
    )


def test_export_schema_and_values(tmp_path, patched_lookup):
    db = tmp_path / "geocif_inf2024.db"
    _write_db(db, _rows())
    out = px.export_predictions(_make_parser(), [db], tmp_path / "out.csv",
                                verbose=False)
    df = pd.read_csv(out)

    assert list(df.columns) == [
        "year", "lead", "stage_month_name", "num_ID",
        "observed_yield_t_ha", "predicted_yield_t_ha", "area_ha", "model",
    ]
    # Nothing reachable from the shapefile leaks back in.
    for dropped in ("country", "adm1_name", "region", "cd_mun", "nm_mun",
                    "cluster_id", "Region_ID", "stage", "stage_month_id"):
        assert dropped not in df.columns
    assert len(df) == 4
    assert set(df["num_ID"]) == {5107925}
    assert df["num_ID"].dtype.kind == "i"          # join key must not be a float
    assert set(df["lead"]) == {1, 2}
    assert set(df["stage_month_name"]) == {"September", "October"}


def test_export_dedups_a_rerun(tmp_path, patched_lookup):
    """A re-run appends rather than replaces; the stale copy must not win."""
    db = tmp_path / "geocif_inf2024.db"
    _write_db(db, _rows(n_dup=2))
    out = px.export_predictions(_make_parser(), [db], tmp_path / "out.csv",
                                verbose=False)
    df = pd.read_csv(out)
    assert len(df) == 4                             # not 6
    assert (df["predicted_yield_t_ha"] > 0).all()   # the -999 stale rows lost


def test_export_merges_multiple_dbs(tmp_path, patched_lookup):
    """A per-fold run writes one DB per forecast year."""
    dbs = []
    for year in (2023, 2024):
        db = tmp_path / f"geocif_inf{year}.db"
        rows = [r for r in _rows() if r["Harvest Year"] == str(year)]
        _write_db(db, rows)
        dbs.append(db)
    out = px.export_predictions(_make_parser(), dbs, tmp_path / "out.csv",
                                verbose=False)
    df = pd.read_csv(out)
    assert sorted(df["year"].unique()) == [2023, 2024]
    assert len(df) == 4


def test_export_wrong_experiment_name_raises(tmp_path, patched_lookup):
    """Silently writing an empty CSV is the failure mode this guards."""
    db = tmp_path / "geocif_inf2024.db"
    _write_db(db, _rows(experiment="outlook"))
    with pytest.raises(ValueError, match="no rows for Experiment Name"):
        px.export_predictions(_make_parser(), [db], tmp_path / "out.csv",
                              experiment_name="default", verbose=False)
    # ...and the right name works on the same DB.
    out = px.export_predictions(_make_parser(), [db], tmp_path / "out.csv",
                                experiment_name="outlook", verbose=False)
    assert len(pd.read_csv(out)) == 4


def test_export_keeps_forecast_rows_without_truth(tmp_path, patched_lookup):
    """The live forecast year has no observed yield and must not be dropped."""
    rows = _rows()
    for r in rows:
        r[OBS_DB] = None
    db = tmp_path / "geocif_inf2026.db"
    _write_db(db, rows)
    out = px.export_predictions(_make_parser(), [db], tmp_path / "out.csv",
                                verbose=False)
    df = pd.read_csv(out)
    assert len(df) == 4
    assert df["observed_yield_t_ha"].isna().all()


def test_export_drops_rows_without_a_prediction(tmp_path, patched_lookup):
    rows = _rows()
    rows[0][PRED_DB] = None
    db = tmp_path / "geocif_inf2024.db"
    _write_db(db, rows)
    df = pd.read_csv(px.export_predictions(_make_parser(), [db],
                                           tmp_path / "out.csv", verbose=False))
    assert len(df) == 3


def test_export_requires_stage_window_display(tmp_path, patched_lookup):
    """Deriving lead from 'Stage Name' would invert it for _r methods."""
    rows = [{k: v for k, v in r.items() if k != "Stage Window Display"}
            for r in _rows()]
    db = tmp_path / "geocif_inf2024.db"
    _write_db(db, rows)
    with pytest.raises(ValueError, match="Stage Window Display"):
        px.export_predictions(_make_parser(), [db], tmp_path / "out.csv",
                              verbose=False)


def test_export_model_filter(tmp_path, patched_lookup):
    rows = _rows()
    for r in list(rows):
        other = dict(r)
        other["Model"] = "tabpfn_gsa"
        rows.append(other)
    db = tmp_path / "geocif_inf2024.db"
    _write_db(db, rows)
    df = pd.read_csv(px.export_predictions(
        _make_parser(), [db], tmp_path / "out.csv",
        models=["catboost"], verbose=False))
    assert set(df["model"]) == {"catboost"}


def test_export_drops_regions_absent_from_boundary(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(px, "_region_id_lookup",
                        lambda parser, country: ({"somewhere else": 1}, "num_ID"))
    db = tmp_path / "geocif_inf2024.db"
    _write_db(db, _rows())
    with pytest.raises(ValueError, match="none of the 1 region"):
        px.export_predictions(_make_parser(), [db], tmp_path / "out.csv",
                              verbose=False)
    assert "absent from the boundary file" in capsys.readouterr().out


# --------------------------------------------------------------------------
# CLI wiring
# --------------------------------------------------------------------------

def test_cli_expands_globs_and_writes(tmp_path, monkeypatch, patched_lookup):
    """The CLI is a real entry point: glob -> N DBs -> one merged CSV."""
    for year in (2023, 2024):
        _write_db(tmp_path / f"geocif_inf{year}.db",
                  [r for r in _rows() if r["Harvest Year"] == str(year)])
    # A DB that must NOT be picked up by the geocif_inf* glob.
    _write_db(tmp_path / "geocif_gsa_x1.db", _rows())

    import geocif.logger as log
    monkeypatch.setattr(log, "setup_logger_parser",
                        lambda cfgs: (None, _make_parser()))
    monkeypatch.chdir(tmp_path)

    out = tmp_path / "cli.csv"
    rc = px.main(["--config", "geocif.txt", "--db", "geocif_inf*.db",
                  "--model", "catboost", "--out", str(out)])
    assert rc == 0
    df = pd.read_csv(out)
    assert sorted(df["year"].unique()) == [2023, 2024]
    assert len(df) == 4


def test_cli_errors_when_no_db_matches(tmp_path, monkeypatch):
    import geocif.logger as log
    monkeypatch.setattr(log, "setup_logger_parser",
                        lambda cfgs: (None, _make_parser()))
    monkeypatch.chdir(tmp_path)
    with pytest.raises(SystemExit, match="no databases matched"):
        px.main(["--config", "geocif.txt", "--db", "nothing_here*.db",
                 "--out", str(tmp_path / "x.csv")])
