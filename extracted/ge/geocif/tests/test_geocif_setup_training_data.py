"""Regression tests for ``_setup_training_data``'s last_observed_map loop.

The Wolayita-maize cluster run (2026-06-04) crashed with:

    ValueError: attempt to get argmax of an empty sequence
    File "geocif/geocif.py", line 4075, in _setup_training_data
        last_row = grp.loc[grp["Harvest Year"].idxmax()]

Root cause: `_add_region_clusters` casts ``df["Region"]`` to a pandas
Categorical, so the default ``groupby("Region", observed=False)`` returns
ALL category levels — including empty ones for admin names whose rows
got dropped by ``df_valid = df_region_train.dropna(subset=[target])``.
``grp.empty == True`` ⇒ ``grp["Harvest Year"].idxmax()`` raises.

The three-guard fix locks in:
  1. ``observed=True`` — drops empty Categorical levels at the groupby.
  2. ``years.dropna()`` + ``years.empty`` — guards all-NaN Harvest Year
     within a non-empty group.
  3. ``years.idxmax()`` — runs on the pre-dropna'd Series, guaranteed
     non-empty.

These tests exercise the loop in isolation via the same SimpleNamespace
+ MethodType stub pattern used in tests/test_trend_baseline.py and
tests/test_threshold_optimizer.py.
"""
import logging
import unittest
from types import MethodType, SimpleNamespace

import numpy as np
import pandas as pd

from geocif.geocif import Geocif


def _build_stub():
    """Minimum attrs needed for _setup_training_data to enter the
    last_observed_map loop. Bypasses the region_anomaly transform
    (target_mode != "region_anomaly") and the gam/linear/gpr
    fill-missing branch (dispatch_name = "catboost").
    """
    target_col = "Yield (tn per ha)"
    stub = SimpleNamespace(
        target_column=target_col,
        target=target_col,
        target_mode="absolute",
        check_yield_trend=False,
        _region_target_means=None,
        countries_pooled=None,
        feature_names=[],
        dispatch_name="catboost",
        logger=logging.getLogger("test_setup_training_data"),
    )
    stub._setup_training_data = MethodType(Geocif._setup_training_data, stub)
    stub._clean_training_features = MethodType(
        Geocif._clean_training_features, stub,
    )
    return stub


def _make_df(rows, region_categories=None):
    """Build a df_region_train with Region as Categorical.

    ``rows``: iterable of (region_name, harvest_year, yield_value).
    ``region_categories``: full list of Categorical levels (including
    levels with zero rows). Defaults to the unique region names in
    ``rows`` — i.e. no empty levels. Pass an extended list to simulate
    the Categorical-with-empty-levels case the fix targets.
    """
    df = pd.DataFrame(
        rows,
        columns=["Region", "Harvest Year", "Yield (tn per ha)"],
    )
    if region_categories is None:
        region_categories = sorted(df["Region"].unique())
    df["Region"] = pd.Categorical(df["Region"], categories=region_categories)
    return df


class SetupTrainingDataLastObservedMapTests(unittest.TestCase):

    def test_empty_categorical_level_skipped(self):
        """The Wolayita crash repro: Region is Categorical with 3 levels
        ['A', 'B', 'C'], but only A and C have rows with non-NaN target.
        The old code crashed iterating over level B's empty group; the
        fix skips it via observed=True. last_observed_map should have
        keys {A, C} only — never B."""
        rows = [
            ("A", 2018, 1.0), ("A", 2019, 1.5), ("A", 2020, 2.0),
            ("C", 2018, 3.0), ("C", 2019, 3.5),
        ]
        df = _make_df(rows, region_categories=["A", "B", "C"])
        stub = _build_stub()
        try:
            stub._setup_training_data(df)
        except ValueError as exc:
            self.fail(f"_setup_training_data raised on empty-level df: {exc}")
        self.assertEqual(set(stub.last_observed_map.keys()), {"A", "C"})
        self.assertEqual(stub.last_observed_map["A"], (2020, 2.0))
        self.assertEqual(stub.last_observed_map["C"], (2019, 3.5))
        self.assertNotIn("B", stub.last_observed_map)

    def test_all_nan_harvest_year_within_group_skipped(self):
        """Second-order edge case: a Region has rows passing the
        target-NaN filter, but every row has Harvest Year == NaN. The
        years.empty guard should skip the region without crashing."""
        rows = [
            ("A", 2018, 1.0), ("A", 2019, 1.5),
            # Region B has rows with valid target but all-NaN Harvest Year.
            ("B", np.nan, 5.0), ("B", np.nan, 6.0),
            ("C", 2020, 3.0),
        ]
        df = _make_df(rows)
        stub = _build_stub()
        try:
            stub._setup_training_data(df)
        except ValueError as exc:
            self.fail(
                f"_setup_training_data raised on all-NaN Harvest Year "
                f"within a non-empty Region group: {exc}"
            )
        self.assertEqual(set(stub.last_observed_map.keys()), {"A", "C"})
        self.assertNotIn("B", stub.last_observed_map)

    def test_all_regions_valid_positive_regression(self):
        """Positive regression: when every Region has valid target rows
        and non-NaN Harvest Year, last_observed_map should still be
        populated correctly for all of them. Same key/value invariant
        as the pre-fix code."""
        rows = [
            ("A", 2018, 1.0), ("A", 2020, 2.0),    # max year = 2020
            ("B", 2019, 1.5), ("B", 2021, 2.5),    # max year = 2021
            ("C", 2018, 3.0), ("C", 2019, 3.5),    # max year = 2019
        ]
        df = _make_df(rows)
        stub = _build_stub()
        stub._setup_training_data(df)
        self.assertEqual(set(stub.last_observed_map.keys()), {"A", "B", "C"})
        self.assertEqual(stub.last_observed_map["A"], (2020, 2.0))
        self.assertEqual(stub.last_observed_map["B"], (2021, 2.5))
        self.assertEqual(stub.last_observed_map["C"], (2019, 3.5))

    def test_empty_df_returns_early(self):
        """When every row has NaN target, df_valid is empty and the
        early-return keeps last_observed_map as an empty dict."""
        rows = [
            ("A", 2018, np.nan), ("A", 2019, np.nan),
            ("B", 2020, np.nan),
        ]
        df = _make_df(rows)
        stub = _build_stub()
        stub._setup_training_data(df)
        self.assertEqual(stub.last_observed_map, {})


if __name__ == "__main__":
    unittest.main()
