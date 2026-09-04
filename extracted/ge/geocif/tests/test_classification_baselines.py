"""Tests for CLASSIFICATION mode: init, the class baselines, and DB schema growth.

Three defects are covered, all found running poppy in CLASSIFICATION mode:

1. ``Geocif._setup_feature_dictionaries`` assigned
   ``self.target_column = self.target_class`` at ``__post_init__`` while
   ``target_class`` was only created much later inside
   ``fe.classify_target()`` — so CLASSIFICATION raised AttributeError before
   any work started, on every project.

2. ``null`` / ``trend`` predict on the raw yield scale, so in CLASSIFICATION
   mode they emitted yields (39.8) that can never equal a class label and
   scored 0.0% accuracy. ``null_class`` / ``persistence_class`` are the
   class-valued analogues.

3. ``utils.to_db`` called ``pangres.upsert`` with the default
   ``add_new_columns=False``, so the table could never gain a column after the
   first write fixed the schema. Every later row failed with "no column named
   ..." and the exception handler swallowed it — the run reported success with
   an empty table.

The baseline tests use the same bound-method stub idiom as
``test_trend_baseline.py`` so we don't need a full Geocif + config + DB.
"""
import logging
import sqlite3
import tempfile
import unittest
from pathlib import Path
from types import MethodType, SimpleNamespace

import numpy as np
import pytest
import pandas as pd

from geocif.geocif import Geocif

TARGET = "Yield (tn per ha)"
CLS = f"{TARGET}_class"


def _stub(model_name, df_train, forecast_season=2026, model_type="CLASSIFICATION"):
    stub = SimpleNamespace(
        model_name=model_name,
        model_type=model_type,
        df_train=df_train,
        target=TARGET,
        target_class=CLS,
        forecast_season=forecast_season,
        logger=logging.getLogger("test_classification_baselines"),
    )
    stub._predict_baseline = MethodType(Geocif._predict_baseline, stub)
    return stub


def _train(rows):
    """rows: list of (region, year, class)."""
    return pd.DataFrame(
        [{"Region": r, "Region_ID": 1, "Harvest Year": y, TARGET: 30.0, CLS: c}
         for r, y, c in rows]
    )


def _test_frame(pairs):
    """pairs: list of (region, year). Positional index, as df_region has."""
    return pd.DataFrame(
        [{"Region": r, "Region_ID": 1, "Harvest Year": y} for r, y in pairs]
    ).reset_index(drop=True)


class TestTargetClassInit(unittest.TestCase):
    """Defect 1: target_class must exist by the end of feature-dict setup."""

    def _run_setup(self, model_type):
        # The method continues past the target_column branch into path setup,
        # so give it the handful of path attrs it touches.
        td = Path(tempfile.mkdtemp())
        stub = SimpleNamespace(
            model_type=model_type,
            check_yield_trend=False,
            dir_ml=td,
            dir_db=td,
            db_forecasts="t.db",
            today="September_03_2026",
        )
        stub._setup_feature_dictionaries = MethodType(
            Geocif._setup_feature_dictionaries, stub
        )
        stub._setup_feature_dictionaries()
        return stub

    def test_classification_sets_target_class(self):
        stub = self._run_setup("CLASSIFICATION")
        self.assertEqual(stub.target_class, f"{stub.target}_class")
        self.assertEqual(stub.target_column, stub.target_class)

    def test_regression_unaffected(self):
        stub = self._run_setup("REGRESSION")
        self.assertEqual(stub.target_column, stub.target)


class TestNullClassBaseline(unittest.TestCase):
    """null_class = per-unit MAJORITY training class."""

    def test_majority_per_region(self):
        df_train = _train([
            ("A", 2011, 0), ("A", 2012, 0), ("A", 2013, 0), ("A", 2014, 1),
            ("B", 2011, 2), ("B", 2012, 2), ("B", 2013, 1),
        ])
        dfr = _test_frame([("A", 2026), ("B", 2026)])
        stub = _stub("null_class", df_train)
        y, ci, hp = stub._predict_baseline(dfr, dfr)
        np.testing.assert_array_equal(y, np.array([0.0, 2.0]))
        self.assertIsNone(ci)

    def test_never_pools_across_regions(self):
        # B's single row must not inherit A's overwhelming majority.
        df_train = _train(
            [("A", y, 0) for y in range(2011, 2020)] + [("B", 2011, 2)]
        )
        dfr = _test_frame([("A", 2026), ("B", 2026)])
        y, _, _ = _stub("null_class", df_train)._predict_baseline(dfr, dfr)
        np.testing.assert_array_equal(y, np.array([0.0, 2.0]))

    def test_tie_is_deterministic_lowest_class(self):
        df_train = _train([("A", 2011, 0), ("A", 2012, 1)])
        dfr = _test_frame([("A", 2026)])
        y, _, _ = _stub("null_class", df_train)._predict_baseline(dfr, dfr)
        self.assertEqual(y[0], 0.0)

    def test_region_with_no_training_rows_is_nan(self):
        df_train = _train([("A", 2011, 1)])
        dfr = _test_frame([("Z", 2026)])
        y, _, _ = _stub("null_class", df_train)._predict_baseline(dfr, dfr)
        self.assertTrue(np.isnan(y[0]))


class TestPersistenceClassBaseline(unittest.TestCase):
    """persistence_class = the unit's most recent PRIOR observed class."""

    def test_uses_latest_prior_year(self):
        df_train = _train([("A", 2011, 0), ("A", 2012, 2), ("A", 2013, 1)])
        dfr = _test_frame([("A", 2014)])
        y, _, _ = _stub("persistence_class", df_train)._predict_baseline(dfr, dfr)
        self.assertEqual(y[0], 1.0)          # 2013, not 2011/2012

    def test_ignores_future_years(self):
        # Only years strictly before the fold year may be used.
        df_train = _train([("A", 2011, 0), ("A", 2020, 2)])
        dfr = _test_frame([("A", 2015)])
        y, _, _ = _stub("persistence_class", df_train)._predict_baseline(dfr, dfr)
        self.assertEqual(y[0], 0.0)

    def test_no_prior_year_is_nan(self):
        df_train = _train([("A", 2020, 2)])
        dfr = _test_frame([("A", 2015)])
        y, _, _ = _stub("persistence_class", df_train)._predict_baseline(dfr, dfr)
        self.assertTrue(np.isnan(y[0]))

    def test_per_row_within_multi_row_region(self):
        df_train = _train([("A", 2011, 0), ("A", 2012, 1), ("A", 2013, 2)])
        dfr = _test_frame([("A", 2012), ("A", 2013), ("A", 2014)])
        y, _, _ = _stub("persistence_class", df_train)._predict_baseline(dfr, dfr)
        np.testing.assert_array_equal(y, np.array([0.0, 1.0, 2.0]))


class TestClassBaselineGuards(unittest.TestCase):
    def test_refuses_regression_mode(self):
        df_train = _train([("A", 2011, 0)])
        dfr = _test_frame([("A", 2026)])
        stub = _stub("null_class", df_train, model_type="REGRESSION")
        with self.assertRaises(ValueError) as cm:
            stub._predict_baseline(dfr, dfr)
        self.assertIn("CLASSIFICATION", str(cm.exception))

    def test_refuses_when_class_column_missing(self):
        df_train = _train([("A", 2011, 0)]).drop(columns=[CLS])
        dfr = _test_frame([("A", 2026)])
        with self.assertRaises(ValueError) as cm:
            _stub("null_class", df_train)._predict_baseline(dfr, dfr)
        self.assertIn("classify_target", str(cm.exception))


class TestToDbAddsNewColumns(unittest.TestCase):
    """Defect 3: a later df with an extra column must not lose every row."""

    def test_second_write_with_extra_column_persists(self):
        pytest.importorskip("pangres")   # runtime dep; present in the pixi env
        from geocif import utils
        with tempfile.TemporaryDirectory() as td:
            db = Path(td) / "t.db"
            first = pd.DataFrame({"Predicted": [1.0], "alpha": [np.nan]})
            first.index.name = "Index"
            utils.to_db(db, "results", first)

            # Mirrors CLASSIFICATION adding a 'CI' column the table lacks.
            second = pd.DataFrame({"Predicted": [2.0], "alpha": [np.nan], "CI": ["0.1, 0.9"]})
            second.index = pd.Index([1], name="Index")
            utils.to_db(db, "results", second)

            con = sqlite3.connect(db)
            cols = [r[1] for r in con.execute("PRAGMA table_info(results)")]
            n = con.execute("SELECT COUNT(*) FROM results").fetchone()[0]
            con.close()

        self.assertIn("CI", cols, "new column was not added to the table")
        self.assertEqual(n, 2, "row with the new column was silently dropped")


if __name__ == "__main__":
    unittest.main()


class TestClassificationFrameDetection(unittest.TestCase):
    """The gate that swaps regression diagnostics for classification ones."""

    def setUp(self):
        from geocif.yield_outlook import _is_classification_frame
        self.fn = _is_classification_frame

    def test_detects_via_observed_class_column(self):
        df = pd.DataFrame({
            f"Observed {CLS}": [0, 1, 2],
            "Predicted Yield (tn per ha)": [0.0, 1.0, 2.0],
        })
        self.assertTrue(self.fn(df))

    def test_detects_small_integer_labels(self):
        df = pd.DataFrame({"Predicted Yield (tn per ha)": [0.0, 1.0, 1.0, 0.0, 2.0]})
        self.assertTrue(self.fn(df))

    def test_regression_yields_are_not_classes(self):
        df = pd.DataFrame({"Predicted Yield (tn per ha)": [38.96, 34.47, 24.86, 31.2]})
        self.assertFalse(self.fn(df))

    def test_empty_and_missing_are_false(self):
        self.assertFalse(self.fn(pd.DataFrame()))
        self.assertFalse(self.fn(None))
        self.assertFalse(self.fn(pd.DataFrame({"Region": ["A"]})))

    def test_integer_valued_yields_are_not_misread(self):
        # Whole-number yields well above the class range must not trip it.
        df = pd.DataFrame({"Predicted Yield (tn per ha)": [30.0, 40.0, 25.0, 35.0]})
        self.assertFalse(self.fn(df))


class TestClassificationOutputs(unittest.TestCase):
    """Accuracy / confusion CSVs. Map rendering needs GMT, so it is not asserted."""

    def _frame(self):
        rows = []
        for region, obs, pred in [("A", 0, 0), ("A", 1, 1), ("A", 0, 1),
                                  ("B", 1, 0), ("B", 1, 1), ("B", 0, 0)]:
            rows.append({"Region": region, "Harvest Year": 2020,
                         f"Observed {CLS}": obs,
                         "Predicted Yield (tn per ha)": float(pred)})
        return pd.DataFrame(rows)

    def test_writes_confusion_and_accuracy(self):
        from geocif.viz import diagnostics as diag
        df = self._frame()
        with tempfile.TemporaryDirectory() as td:
            dm, dc = Path(td) / "maps", Path(td) / "csvs"
            try:
                diag.classification_outputs(
                    None, df, ["Afghanistan"], dm, dc,
                    country="afghanistan", crop="poppy", model="catboost",
                    forecast_year=2020,
                )
            except Exception:
                pass       # map rendering may fail without GMT; CSVs come first
            conf = dc / "confusion_afghanistan_poppy_catboost.csv"
            acc = dc / "accuracy_by_region_afghanistan_poppy_catboost.csv"
            self.assertTrue(conf.exists(), "confusion matrix not written")
            self.assertTrue(acc.exists(), "per-region accuracy not written")
            a = pd.read_csv(acc).set_index("Region")
            # A: 2/3 correct, B: 2/3 correct
            self.assertAlmostEqual(a.loc["A", "Accuracy"], 200 / 3, places=4)
            self.assertAlmostEqual(a.loc["B", "Accuracy"], 200 / 3, places=4)
            self.assertEqual(int(a.loc["A", "n"]), 3)
            c = pd.read_csv(conf, index_col=0)
            self.assertEqual(int(c.to_numpy().sum()), 6)

    def test_no_observed_class_still_writes_class_map_csv(self):
        from geocif.viz import diagnostics as diag
        df = self._frame().drop(columns=[f"Observed {CLS}"])
        with tempfile.TemporaryDirectory() as td:
            dm, dc = Path(td) / "maps", Path(td) / "csvs"
            try:
                diag.classification_outputs(
                    None, df, ["Afghanistan"], dm, dc,
                    country="afghanistan", crop="poppy", model="catboost",
                    forecast_year=2020,
                )
            except Exception:
                pass
            self.assertTrue((dc / "class_map_afghanistan_poppy_catboost.csv").exists())
            self.assertFalse((dc / "confusion_afghanistan_poppy_catboost.csv").exists())


class TestTrainingDataAlignment(unittest.TestCase):
    """X_train must align to y_train when the target has NaNs.

    CLASSIFICATION drops rows whose qcut class is NaN (a region with too few
    training rows), so y shrinks while X did not — killing the whole fold in
    CatBoostFitter.train_test_split. That silently removed the 2019 and 2021
    folds from poppy.
    """

    def _trainer(self, y):
        from geocif.geocif import ModelTrainer
        obj = SimpleNamespace(
            selected_features=["f1", "f2"],
            cat_features=["Region"],
            y_train=y,
            model_name="catboost",
            logger=logging.getLogger("test_align"),
        )
        return ModelTrainer(obj)

    def _frame(self, n):
        return pd.DataFrame({
            "f1": np.arange(n, dtype=float),
            "f2": np.arange(n, dtype=float) * 2,
            "Region": ["A"] * n,
        })

    def test_aligns_when_target_has_nan_rows(self):
        df = self._frame(5)
        y = pd.Series([1.0, 0.0, 1.0, 0.0], index=[0, 1, 2, 4])   # row 3 dropped
        X = self._trainer(y)._prepare_training_data(df)
        self.assertEqual(len(X), len(y))
        self.assertListEqual(list(X.index), list(y.index))

    def test_no_change_when_lengths_already_match(self):
        df = self._frame(4)
        y = pd.Series([1.0, 0.0, 1.0, 0.0], index=[0, 1, 2, 3])
        X = self._trainer(y)._prepare_training_data(df)
        self.assertEqual(len(X), 4)
        self.assertListEqual(list(X.index), [0, 1, 2, 3])

    def test_survives_missing_y_train(self):
        df = self._frame(3)
        from geocif.geocif import ModelTrainer
        obj = SimpleNamespace(selected_features=["f1", "f2"],
                              cat_features=["Region"],
                              model_name="catboost",
                              logger=logging.getLogger("test_align"))
        X = ModelTrainer(obj)._prepare_training_data(df)
        self.assertEqual(len(X), 3)
