"""Annotated SHAP waterfall (viz/shap_explained) read straight from an outlook DB,
plus the two ml/xai changes it relies on: the background each base value
averages over is stored with the SHAP rows, and the plain waterfall is saved
without shrinking the plot after shap placed its bar numbers.
"""

import inspect
import sqlite3

import matplotlib
import pandas as pd
import pytest

matplotlib.use("Agg")  # no display needed
pytest.importorskip("shap")

from geocif.ml import xai  # noqa: E402
from geocif.viz import shap_explained as se  # noqa: E402

from .test_xai_mixed_type import FEATURES, _frame, _StrictModel  # noqa: E402


@pytest.fixture
def outlook_db(tmp_path):
    """An outlook DB as yield_outlook leaves it: SHAP rows from xai.explain
    (kumo, 2019 held out) and a config table with the display units."""
    df = _frame()
    train, test = df[df["Harvest Year"] < 2019].copy(), df[df["Harvest Year"] == 2019].copy()
    model = _StrictModel()
    db = tmp_path / "outlook.db"
    xai.explain(
        train, test, model=model, model_name="kumo", forecast_season=2019, crop="poppy",
        country="afghanistan", analysis_dir=tmp_path, db_path=db,
        feature_names=FEATURES, predict_fn=model.predict,
    )
    with sqlite3.connect(db) as con:
        pd.DataFrame({
            "Section": ["ML", "ML", "DEFAULT"],
            "Option": ["yield_units", "yield_display", "yield_units"],
            "Value": ["kg/ha  ; per-project display unit", "{}", "Mg/ha"],
        }).to_sql("config_October_12_2026", con, index=False)
    return db


def test_background_is_stored_with_the_shap_rows(outlook_db):
    with sqlite3.connect(outlook_db) as con:
        df = pd.read_sql("select * from shap_values", con)
    # kumo: 10 background rows from the last five training years (2014-2018).
    assert (df["Background Rows"] == 10).all()
    assert (df["Background Years"] == "2014-2018").all()


def test_plain_waterfall_is_not_shrunk_after_shap_drew_it():
    src = inspect.getsource(xai.explain)
    block = src[src.index("SHAP waterfall plot"):src.index("Persist SHAP values")]
    assert "tight_layout" not in block.replace("No tight_layout", "")
    assert 'bbox_inches="tight"' in block


def test_load_row_and_errors(outlook_db, tmp_path):
    row = se.load_row(outlook_db, "kumo", "Eastern", 2019)
    assert row["Region"] == "Eastern" and int(row["Harvest Year"]) == 2019
    with pytest.raises(ValueError, match="models \\['kumo'\\]"):
        se.load_row(outlook_db, "tabpfn", "Eastern", 2019)
    empty = tmp_path / "empty.db"
    sqlite3.connect(empty).close()
    with pytest.raises(ValueError, match="do_xai"):
        se.load_row(empty, "kumo", "Eastern", 2019)
    with pytest.raises(FileNotFoundError):  # never creates an empty DB
        se.load_row(tmp_path / "missing.db", "kumo", "Eastern", 2019)
    assert not (tmp_path / "missing.db").exists()


def test_display_units_follow_yield_outlook(outlook_db, tmp_path):
    assert se.display_units(outlook_db, "poppy") == ("kg/ha", 1.0)
    db = tmp_path / "usa.db"
    with sqlite3.connect(db) as con:
        pd.DataFrame({
            "Section": ["ML", "ML"], "Option": ["yield_units", "yield_display"],
            "Value": ["Mg/ha", "{'maize': ['bu/ac', 15.9318]}"],
        }).to_sql("config_October_04_2026", con, index=False)
    assert se.display_units(db, "maize") == ("bu/ac", 15.9318)
    assert se.display_units(db, "soybean") == ("Mg/ha", 1.0)


def test_window_families_sum_the_stage_windows():
    names = ["MIN_ESI4WK Jan 1-Jan 31", "MIN_ESI4WK Feb 1-Feb 28", "Trend All",
             "PRCPTOT Mar 1-Mar 31", "Harvest Year"]
    fams = se.window_families(names, [0.5, 0.25, 0.2, -0.1, 4.0])
    assert [k for k, _ in fams] == ["MIN_ESI4WK"]  # one window of PRCPTOT is not a family
    assert sum(v for _, v in fams[0][1]) == pytest.approx(0.75)


def test_background_text():
    row = pd.Series({"Background Rows": 10, "Background Years": "2017-2021"})
    assert "10 training region-years from 2017-2021" in se.background_text(row, "Kumo")
    assert "over its 120 training" in se.background_text(
        pd.Series({"Background Rows": 120, "Background Years": "all"}), "CatBoost")
    assert "SHAP background" in se.background_text(pd.Series({}), "Kumo")
    assert "my note" in se.background_text(row, "Kumo", background_note="my note")


def test_draw_writes_the_figure_and_the_numbers_add_up(outlook_db, tmp_path):
    row = se.load_row(outlook_db, "kumo", "Eastern", 2019)
    units, factor = se.display_units(outlook_db, "poppy")
    out = tmp_path / "explained.png"
    notes = se.draw(row, out, units=units, factor=factor, max_display=3, model_label="Kumo", dpi=60)
    assert out.exists() and out.stat().st_size > 10_000

    shap_cols = [c for c in row.index if c.startswith("SHAP_") and pd.notna(row[c])]
    fx = row["Base Value"] + row[shap_cols].astype(float).sum()
    assert "[[Start here]]" in notes["start"][0] and "kg/ha" in notes["start"][0]
    assert f"{fx:.1f} kg/ha" in notes["end"][0] or f"{fx:.2f} kg/ha" in notes["end"][0]
    assert "10 training region-years from 2014-2018" in " ".join(notes["start"])
    # Five inputs, three bars: two shown and one bar for the other three.
    assert notes["others"][0].startswith("**3 small inputs")


def test_run_names_the_file_after_the_forecast(outlook_db, tmp_path):
    out = se.run(outlook_db, "kumo", "Eastern", 2019, tmp_path / "figs", dpi=60)
    assert out.name == "shap_explained_afghanistan_poppy_kumo_Eastern_2019.png"
    assert out.exists()
