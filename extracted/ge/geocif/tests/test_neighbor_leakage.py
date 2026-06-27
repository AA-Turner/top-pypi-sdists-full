"""Unit tests for geocif.ml.neighbor_leakage."""
import unittest

import numpy as np
import pandas as pd

from geocif.ml.neighbor_leakage import (
    LEAK_COLUMN,
    build_centroid_lookup_from_gdf,
    find_k_nearest_centroids,
    inject_leaked_rows,
)


class TestFindKNearestCentroids(unittest.TestCase):
    """Pure-function tests for the K-nearest helper."""

    def _centroids(self):
        # Four regions arranged in a line: A(0,0) B(0,1) C(0,2) D(0,5)
        # Distances from A: B=1, C=2, D=5
        return {"A": (0.0, 0.0), "B": (0.0, 1.0), "C": (0.0, 2.0), "D": (0.0, 5.0)}

    def test_returns_k_nearest_excluding_self(self):
        out = find_k_nearest_centroids(self._centroids(), "A", k=2)
        self.assertEqual(out, ["B", "C"])

    def test_clamps_when_k_exceeds_other_regions(self):
        out = find_k_nearest_centroids(self._centroids(), "A", k=10)
        self.assertEqual(out, ["B", "C", "D"])  # 3 others, k clamped

    def test_k_zero_returns_empty(self):
        self.assertEqual(find_k_nearest_centroids(self._centroids(), "A", k=0), [])

    def test_unknown_target_returns_empty(self):
        self.assertEqual(find_k_nearest_centroids(self._centroids(), "X", k=2), [])

    def test_target_never_in_result(self):
        out = find_k_nearest_centroids(self._centroids(), "B", k=3)
        self.assertNotIn("B", out)


class TestInjectLeakedRows(unittest.TestCase):
    """Integration of find_k_nearest + row-pull + tag."""

    def _fixture(self):
        regions = ["A", "B", "C", "D"]
        years = [2018, 2019, 2020]
        rows = []
        for r in regions:
            for y in years:
                rows.append({
                    "Region": r,
                    "Harvest Year": y,
                    "Yield": float(years.index(y) + ord(r) * 0.1),
                    "feature_1": float(years.index(y)),
                })
        df_full = pd.DataFrame(rows)
        df_train = df_full[df_full["Harvest Year"] != 2020].copy()
        centroids = {"A": (0.0, 0.0), "B": (0.0, 1.0), "C": (0.0, 2.0), "D": (0.0, 5.0)}
        return df_full, df_train, centroids

    def test_k_zero_is_noop(self):
        df_full, df_train, cent = self._fixture()
        out = inject_leaked_rows(
            df_train=df_train, df_full=df_full,
            test_regions=["A"], target_year=2020, centroids=cent,
            k=0, target_col="Yield",
        )
        pd.testing.assert_frame_equal(out, df_train)

    def test_k_one_injects_nearest_neighbor_row(self):
        # A's nearest is B. Test region [A] → inject B's year=2020.
        df_full, df_train, cent = self._fixture()
        out = inject_leaked_rows(
            df_train=df_train, df_full=df_full,
            test_regions=["A"], target_year=2020, centroids=cent,
            k=1, target_col="Yield",
        )
        leaked = out[out[LEAK_COLUMN].notna()]
        self.assertEqual(len(leaked), 1)
        self.assertEqual(leaked.iloc[0]["Region"], "B")
        self.assertEqual(int(leaked.iloc[0][LEAK_COLUMN]), 2020)

    def test_union_dedupes_overlapping_neighbors(self):
        # Two test regions whose neighbors overlap → unique neighbor set.
        # B nearest to A; A nearest to B. Test [A, B] → union {A, B} for
        # both. But the leak set excludes the test regions themselves —
        # WAIT, the algorithm includes neighbors that may BE other test
        # regions. With test=[A,B]: A's neighbor is B (test), B's
        # neighbor is A (test). Both get leaked. Union = {A, B}.
        df_full, df_train, cent = self._fixture()
        out = inject_leaked_rows(
            df_train=df_train, df_full=df_full,
            test_regions=["A", "B"], target_year=2020, centroids=cent,
            k=1, target_col="Yield",
        )
        leaked = out[out[LEAK_COLUMN].notna()]
        self.assertEqual(len(leaked), 2)
        self.assertEqual(set(leaked["Region"]), {"A", "B"})

    def test_no_op_when_target_year_has_no_finite_yield(self):
        # Simulate real-time forecast: forecast year's yields are all NaN
        # in df_full. Expect no injection + warning logged (we don't
        # capture log here, just assert df_train unchanged).
        df_full, df_train, cent = self._fixture()
        df_full.loc[df_full["Harvest Year"] == 2020, "Yield"] = np.nan
        out = inject_leaked_rows(
            df_train=df_train, df_full=df_full,
            test_regions=["A"], target_year=2020, centroids=cent,
            k=2, target_col="Yield",
        )
        pd.testing.assert_frame_equal(out, df_train)

    def test_clamps_k_for_small_country(self):
        # 4 regions total; with k=10, every test region clamps. The
        # function should NOT crash; should leak min(k, n_others).
        df_full, df_train, cent = self._fixture()
        out = inject_leaked_rows(
            df_train=df_train, df_full=df_full,
            test_regions=["A"], target_year=2020, centroids=cent,
            k=10, target_col="Yield",
        )
        leaked = out[out[LEAK_COLUMN].notna()]
        self.assertEqual(len(leaked), 3)  # 3 other regions in the lookup

    def test_leak_column_tag_added(self):
        df_full, df_train, cent = self._fixture()
        out = inject_leaked_rows(
            df_train=df_train, df_full=df_full,
            test_regions=["A"], target_year=2020, centroids=cent,
            k=2, target_col="Yield",
        )
        self.assertIn(LEAK_COLUMN, out.columns)
        # Historical rows should have NaN/pd.NA in the leak column.
        historical = out[out["Harvest Year"] != 2020]
        self.assertTrue(historical[LEAK_COLUMN].isna().all())


if __name__ == "__main__":
    unittest.main()
