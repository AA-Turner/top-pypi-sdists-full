"""CID contribution: class resolution, scoring, ranking, figure, and the
yield_outlook training loop that feeds them."""

import ast
import configparser
import fnmatch
import logging
import sqlite3

import numpy as np
import pandas as pd
import pytest

from geocif import yield_outlook as yo
from geocif.ml.stages import resolve_excluded_cids
from geocif.viz import cid_contribution as cidc

OBS, PRED = cidc.OBS, cidc.PRED

# Real CID bases: SU = Heat, PRCPTOT = Rain, MEAN_GCVI = VI, MEAN_FPAR = FPAR,
# ONI_prev_JJA = ENSO, SOIL_SAND = Soil (static), IRR_SHARE = Irrigation.
COLS = ["Region", "Harvest Year", "t -1 Yield (tn per ha)", "lat", "Yield Trend",
        "SU Jun 1-Jun 30", "SU Jul 1-Jul 31", "PRCPTOT Jun 1-Jun 30",
        "MEAN_GCVI Jul 1-Jul 31", "MEAN_FPAR Jul 1-Jul 31",
        "ONI_prev_JJA Jun 1-Jun 30", "SOIL_SAND", "IRR_SHARE"]


def _rows(experiment, model, noise, years=range(2010, 2018), regions="ABCDEF",
          stages=("Jun 1-Jun 30",), seed=0):
    rng = np.random.default_rng(seed)
    out = []
    for year in years:
        for i, region in enumerate(regions):
            obs = 5.0 + i + 0.3 * (year - 2010)
            for stage in stages:
                out.append({"Experiment Name": experiment, "Model": model,
                            "Country": "kenya", "Region": region,
                            "Harvest Year": year, "Stage Name": stage,
                            OBS: obs, PRED: obs + rng.normal(0, noise)})
    return out


# ---------------------------------------------------------------------------
# classes
# ---------------------------------------------------------------------------
def test_classes_all_minus_excluded_category():
    drop, _ = resolve_excluded_cids([], ["ENSO"])
    assert cidc.classes_from_columns(COLS, ["all"], drop) == [
        "FPAR", "Heat", "Irrigation", "Rain", "Soil", "VI"]


def test_classes_explicit_list_and_fully_excluded_class():
    drop, _ = resolve_excluded_cids(["PRCPTOT"], [])  # Rain's only index
    assert cidc.classes_from_columns(COLS, ["Heat", "Rain", "VI"], drop) == ["Heat", "VI"]


# ---------------------------------------------------------------------------
# scoring and ranking
# ---------------------------------------------------------------------------
def test_per_year_r2_final_stage_only():
    early = _rows("a", "m", 5.0, stages=("Mar 1-Mar 31",), seed=1)
    late = _rows("a", "m", 0.05, stages=("Jun 1-Jun 30",), seed=2)
    r2 = cidc.per_year_r2(pd.DataFrame(early + late), "Experiment Name")
    assert (r2["R2"] > 0.95).all()


def test_per_year_r2_common_sample_and_nan_season():
    df = pd.DataFrame(_rows("a", "m", 0.5) + _rows("b", "m", 0.5, seed=1))
    df["Season"] = np.nan  # single-season tables: NaN must not drop rows
    drop = (df["Experiment Name"] == "b") & (df["Region"] == "F") & (df["Harvest Year"] == 2015)
    r2 = cidc.per_year_r2(df[~drop], "Experiment Name")
    assert (r2.loc[r2["Harvest Year"] == 2015, "N Regions"] == 5).all()
    assert (r2.loc[r2["Harvest Year"] != 2015, "N Regions"] == 6).all()


def test_rank_classes_best_first_ties_alphabetical():
    df = pd.DataFrame(
        _rows("cidc_single_Rain", "m", 1.0, seed=1)
        + _rows("cidc_single_Heat", "m", 0.2, seed=2)
        + _rows("cidc_single_VI", "m", 0.5, seed=3)
        + _rows("cidc_single_Cold", "m", 0.5, seed=3)   # identical to VI
        + _rows("outlook", "trend", 3.0)                # ignored
    )
    ranking = cidc.rank_classes(df)
    assert ranking["Class"].tolist() == ["Heat", "Cold", "VI", "Rain"]
    assert (ranking["N Years"] == 8).all()


def test_rank_classes_empty():
    assert cidc.rank_classes(pd.DataFrame()).empty


@pytest.fixture
def df_series():
    return pd.DataFrame(
        _rows("outlook", "trend", 2.0)
        + _rows("cidc_single_Heat", "tabpfn", 0.6, seed=1)
        + _rows("cidc_single_VI", "tabpfn", 0.8, seed=2)
        + _rows("cidc_single_Rain", "tabpfn", 1.2, seed=3)
        + _rows("cidc_cum_02_VI", "tabpfn", 0.4, seed=4)
        + _rows("cidc_cum_03_Rain", "tabpfn", 0.3, seed=5)
    )


def test_cumulative_steps(df_series):
    r2, ranking = cidc.cumulative_r2(df_series, "tabpfn")
    steps = r2[["Step", "Class"]].drop_duplicates().sort_values("Step")
    assert steps["Class"].tolist() == ["Trend", "Heat", "VI", "Rain"]
    assert ranking["Class"].tolist() == ["Heat", "VI", "Rain"]
    med = r2.groupby("Step")["R2"].median()
    assert med[3] > med[2] > med[1] > med[0]


def test_render_writes_png_csvs_lookup(df_series, tmp_path):
    written = cidc.render(df_series, "kenya", "maize", tmp_path)
    sub = "tabpfn/kenya/maize/cid_contribution"
    png = tmp_path / "plots" / sub / "r2_kenya_maize_tabpfn_cid_contribution.png"
    assert written == [png] and png.stat().st_size > 0
    csvs = tmp_path / "csvs" / sub
    assert len(pd.read_csv(csvs / "r2_kenya_maize_tabpfn_cid_contribution.csv")) == 32
    ranking = pd.read_csv(csvs / "ranking_kenya_maize_tabpfn_cid_contribution.csv")
    assert ranking["Class"].tolist() == ["Heat", "VI", "Rain"]
    for root in ("plots", "csvs"):
        lookup = pd.read_csv(tmp_path / root / sub / "lookup_plots_csvs.csv")
        assert set(lookup["plot_file"]) == {png.name}


def test_render_nothing_without_cidc_rows(tmp_path):
    df = pd.DataFrame(_rows("outlook", "trend", 2.0))
    assert cidc.render(df, "kenya", "maize", tmp_path) == []


# ---------------------------------------------------------------------------
# yield_outlook helpers
# ---------------------------------------------------------------------------
def test_parser_overrides_restore_exactly():
    p = configparser.ConfigParser()
    p.read_dict({"DEFAULT": {"use_cids": "['all']"},
                 "ML": {"run_time_steps": "all"}, "tabpfn": {}})
    overrides = {("DEFAULT", "use_cids"): "['Heat']",
                 ("tabpfn", "use_cids"): "['Heat']",
                 ("ML", "run_time_steps"): "latest",
                 ("ML", "experiment_name"): "cidc_single_Heat"}
    with pytest.raises(RuntimeError):
        with yo._parser_overrides(p, overrides):
            assert p.get("tabpfn", "use_cids") == "['Heat']"
            assert p.get("ML", "run_time_steps") == "latest"
            raise RuntimeError
    assert p.get("DEFAULT", "use_cids") == "['all']"
    assert p.get("ML", "run_time_steps") == "all"
    assert not p.remove_option("tabpfn", "use_cids")  # inherited again, not pinned
    assert not p.has_option("ML", "experiment_name")


def test_cidc_db_never_matches_outlook_glob():
    path = yo._cidc_db_path("/x/ml/db/outlook_10_03_2026_14h05.db")
    assert path.name == "cidc_outlook_10_03_2026_14h05.db"
    assert not fnmatch.fnmatch(path.name, "outlook_*.db")


def _parser(tmp_path):
    p = configparser.ConfigParser()
    p.read_dict({
        "DEFAULT": {"project_name": "proj", "db": "outlook_test.db",
                    "countries": "['kenya']", "use_cids": "['all']",
                    "select_cid_by": "Type", "experiment_name": "outlook"},
        "PATHS": {"dir_output": str(tmp_path)},
        "ML": {"run_time_steps": "all", "exclude_cid_categories": "['ENSO']"},
        "kenya": {"crops": "['maize']",
                  "models": "['tabpfn', 'catboost', 'curated_tabpfn', 'top10_tabpfn', 'trend']"},
        "tabpfn": {"ML_model": "True"},
        "catboost": {"ML_model": "True"},
        "curated_tabpfn": {"ML_model": "True", "use_cids": "['PRCPTOT']",
                           "select_cid_by": "Index"},
        "top10_tabpfn": {"ML_model": "True"},
        "trend": {"ML_model": "False"},
    })
    return p


def test_candidate_models(tmp_path):
    assert yo._cidc_candidate_models(_parser(tmp_path), "kenya") == ["tabpfn", "catboost"]


def test_run_cid_contribution_end_to_end(tmp_path, monkeypatch):
    parser = _parser(tmp_path)
    dir_ml = tmp_path / "proj" / "ml"
    (dir_ml / "db").mkdir(parents=True)
    outlook_db = dir_ml / "db" / "outlook_test.db"

    # Main outlook run: tabpfn beats catboost; 2018 is the live year (no obs).
    main = (_rows("outlook", "tabpfn", 0.3, years=range(2010, 2019))
            + _rows("outlook", "catboost", 0.9, seed=1)
            + _rows("outlook", "trend", 2.0, seed=2))
    main = pd.DataFrame(main)
    main.loc[main["Harvest Year"] == 2018, OBS] = np.nan
    with sqlite3.connect(outlook_db) as con:
        main.to_sql("kenya_maize", con, index=False)

    frame = dir_ml / "analysis" / "October_03_2026" / "outlook" / "runs" / "kenya" / "maize" / "tabpfn" / "2010"
    frame.mkdir(parents=True)
    pd.DataFrame(columns=["Region", "SU Jun 1-Jun 30", "PRCPTOT Jun 1-Jun 30",
                          "MEAN_GCVI Jul 1-Jul 31", "ONI_prev_JJA Jun 1-Jun 30"]
                 ).to_csv(frame / "kenya_maize_2010.csv", index=False)

    strength = {"Heat": 3, "VI": 2, "Rain": 1}
    calls = []

    def fake_execute_models(inputs, logger, p, loop_fn=None, desc=None):
        model = inputs[0][4]
        classes = ast.literal_eval(p.get(model, "use_cids"))
        call = {"experiment": p.get("ML", "experiment_name"), "classes": classes,
                "db": p.get("DEFAULT", "db"), "steps": p.get("ML", "run_time_steps"),
                "model": model, "seasons": [row[3] for row in inputs]}
        calls.append(call)
        noise = 1.0 / (1 + sum(strength[c] for c in classes))
        rows = pd.DataFrame(_rows(call["experiment"], model, noise,
                                  years=call["seasons"], seed=len(calls)))
        with sqlite3.connect(dir_ml / "db" / call["db"]) as con:
            rows.to_sql("kenya_maize", con, index=False, if_exists="append")

    monkeypatch.setattr(yo.gc, "execute_models", fake_execute_models)
    yo._run_cid_contribution(parser, logging.getLogger("test"))

    assert [c["experiment"] for c in calls] == [
        "cidc_single_Heat", "cidc_single_Rain", "cidc_single_VI",
        "cidc_cum_02_VI", "cidc_cum_03_Rain"]
    assert calls[-1]["classes"] == ["Heat", "VI", "Rain"]
    assert all(c["model"] == "tabpfn" and c["steps"] == "latest"
               and c["db"] == "cidc_outlook_test.db"
               and c["seasons"] == list(range(2010, 2018)) for c in calls)

    # Parser back as it was; nothing written into the outlook DB itself.
    assert parser.get("DEFAULT", "db") == "outlook_test.db"
    assert parser.get("DEFAULT", "experiment_name") == "outlook"
    assert parser.get("DEFAULT", "use_cids") == "['all']"
    assert parser.get("ML", "run_time_steps") == "all"
    assert not parser.remove_option("ML", "experiment_name")
    assert not parser.remove_option("tabpfn", "use_cids")
    with sqlite3.connect(outlook_db) as con:
        names = pd.read_sql('SELECT DISTINCT "Experiment Name" FROM kenya_maize', con)
    assert names["Experiment Name"].tolist() == ["outlook"]

    # The plot side reads both DBs back into the full series.
    df = yo._query_cidc_rows(outlook_db, "kenya_maize")
    r2, _ = cidc.cumulative_r2(df, "tabpfn")
    steps = r2[["Step", "Class"]].drop_duplicates().sort_values("Step")
    assert steps["Class"].tolist() == ["Trend", "Heat", "VI", "Rain"]
