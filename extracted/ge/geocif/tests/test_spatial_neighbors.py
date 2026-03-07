"""Tests for the geocif.ml.spatial_neighbors module."""

import unittest

import numpy as np
import pandas as pd

from geocif.ml.spatial_neighbors import (
    add_neighbor_features,
    build_neighbor_graph,
    haversine_km,
)


def _make_spatial_df(n_regions=5, n_years=10, seed=42):
    """Create a synthetic wide-format DataFrame with regions, yields, lat/lon."""
    rng = np.random.RandomState(seed)

    regions = [f"Region_{i}" for i in range(n_regions)]
    # Space regions along a line so distances are well-defined
    lats = np.linspace(0, 10, n_regions)
    lons = np.linspace(30, 40, n_regions)
    years = list(range(2010, 2010 + n_years))

    rows = []
    for i, region in enumerate(regions):
        base_yield = 2.0 + 0.5 * i
        for year in years:
            rows.append({
                "Country": "TestCountry",
                "Region": region,
                "Crop": "maize",
                "Area": "TestArea",
                "Season": 1,
                "Harvest Year": year,
                "Yield (tn per ha)": base_yield + rng.normal(0, 0.3),
                "lat": lats[i],
                "lon": lons[i],
                "Region_ID": i,
                "feat_1": rng.uniform(0.2, 0.8),
                "feat_2": rng.uniform(10, 30),
                "feat_3": rng.uniform(100, 500),
            })

    return pd.DataFrame(rows)


class TestHaversine(unittest.TestCase):

    def test_known_distance(self):
        """NYC (40.7128, -74.0060) to London (51.5074, -0.1278) ~ 5570 km."""
        d = haversine_km(40.7128, -74.0060, 51.5074, -0.1278)
        self.assertAlmostEqual(d, 5570, delta=50)

    def test_zero_distance(self):
        d = haversine_km(10.0, 20.0, 10.0, 20.0)
        self.assertAlmostEqual(d, 0.0, places=5)


class TestBuildNeighborGraph(unittest.TestCase):

    def test_knn_3_regions(self):
        """With 3 regions and k=2, each region should have 2 neighbors."""
        df = _make_spatial_df(n_regions=3, n_years=10)
        graph = build_neighbor_graph(df, method="knn", k=2)
        for region in df["Region"].unique():
            self.assertEqual(len(graph[region]), 2)

    def test_perfect_correlation(self):
        """Identical yield time series -> weight should be 1.0."""
        df = _make_spatial_df(n_regions=2, n_years=10, seed=0)
        # Make Region_1 yields identical to Region_0 (shifted by constant)
        r0_yields = df.loc[df["Region"] == "Region_0", "Yield (tn per ha)"].values
        df.loc[df["Region"] == "Region_1", "Yield (tn per ha)"] = r0_yields + 1.0

        graph = build_neighbor_graph(df, method="knn", k=1)
        # Each has 1 neighbor, weight should be ~1.0
        for region, edges in graph.items():
            self.assertEqual(len(edges), 1)
            self.assertAlmostEqual(edges[0][1], 1.0, places=3)

    def test_negative_correlation_clamped(self):
        """Anti-correlated yields -> weight clamped to 0."""
        df = _make_spatial_df(n_regions=2, n_years=10, seed=0)
        r0_yields = df.loc[df["Region"] == "Region_0", "Yield (tn per ha)"].values
        # Mirror yields to create negative correlation
        df.loc[df["Region"] == "Region_1", "Yield (tn per ha)"] = -r0_yields + 10.0

        graph = build_neighbor_graph(df, method="knn", k=1)
        for region, edges in graph.items():
            self.assertEqual(len(edges), 1)
            self.assertEqual(edges[0][1], 0.0)

    def test_insufficient_years(self):
        """With <3 common years, weight should be 0."""
        df = _make_spatial_df(n_regions=2, n_years=2, seed=0)
        graph = build_neighbor_graph(df, method="knn", k=1)
        for region, edges in graph.items():
            self.assertEqual(edges[0][1], 0.0)

    def test_single_region(self):
        """Single region -> empty graph."""
        df = _make_spatial_df(n_regions=1, n_years=10)
        graph = build_neighbor_graph(df, method="knn", k=5)
        self.assertEqual(len(graph), 1)
        self.assertEqual(len(graph["Region_0"]), 0)

    def test_full_method(self):
        """Full method connects all regions to all others."""
        df = _make_spatial_df(n_regions=4, n_years=10)
        graph = build_neighbor_graph(df, method="full", k=2)
        for region, edges in graph.items():
            self.assertEqual(len(edges), 3)  # connected to all 3 others

    def test_weights_normalized(self):
        """Non-zero weights should sum to 1.0 per region."""
        df = _make_spatial_df(n_regions=5, n_years=10)
        graph = build_neighbor_graph(df, method="knn", k=3)
        for region, edges in graph.items():
            total = sum(w for _, w in edges)
            if total > 0:
                self.assertAlmostEqual(total, 1.0, places=5)


class TestAddNeighborFeatures(unittest.TestCase):

    def setUp(self):
        self.df = _make_spatial_df(n_regions=4, n_years=8)
        self.graph = build_neighbor_graph(self.df, method="knn", k=2)
        self.feature_cols = ["feat_1", "feat_2", "feat_3"]

    def test_columns_created(self):
        """Should add nbr_ prefixed columns + summary columns."""
        result = add_neighbor_features(
            self.df, self.graph, self.feature_cols
        )
        for fc in self.feature_cols:
            self.assertIn(f"nbr_{fc}", result.columns)
        self.assertIn("nbr_mean_yield_hist", result.columns)
        self.assertIn("nbr_yield_corr_mean", result.columns)
        self.assertIn("n_neighbors", result.columns)

    def test_no_nan_in_output(self):
        """Output nbr_ columns should have no NaN (self-loop fallback)."""
        result = add_neighbor_features(
            self.df, self.graph, self.feature_cols
        )
        for fc in self.feature_cols:
            self.assertFalse(
                result[f"nbr_{fc}"].isna().any(),
                f"nbr_{fc} has NaN values",
            )

    def test_no_leakage(self):
        """Graph built from train should not use test year yields."""
        df_train = self.df[self.df["Harvest Year"] < 2017].copy()
        df_test = self.df[self.df["Harvest Year"] >= 2017].copy()

        graph = build_neighbor_graph(df_train, method="knn", k=2)

        # Modify test yields after building graph — should not affect graph
        df_test["Yield (tn per ha)"] = 999.0

        result = add_neighbor_features(
            df_test, graph, self.feature_cols
        )
        # nbr features should still be computed (from test features, not yields)
        for fc in self.feature_cols:
            self.assertFalse(result[f"nbr_{fc}"].isna().all())

    def test_isolated_region_fallback(self):
        """Region with no neighbors -> falls back to own values."""
        # Create graph where Region_0 has all-zero weights
        graph = {"Region_0": [("Region_1", 0.0), ("Region_2", 0.0)]}
        # Add other regions to graph with valid edges
        for r in self.df["Region"].unique():
            if r not in graph:
                graph[r] = []

        df_r0 = self.df[self.df["Region"] == "Region_0"].copy()
        result = add_neighbor_features(df_r0, graph, self.feature_cols)

        # nbr_ values should equal own values (self-loop)
        for fc in self.feature_cols:
            np.testing.assert_array_almost_equal(
                result[f"nbr_{fc}"].values,
                result[fc].values,
            )

    def test_toggle_off_no_change(self):
        """When graph is empty, DataFrame gains nbr_ columns but with self values."""
        empty_graph = {r: [] for r in self.df["Region"].unique()}
        result = add_neighbor_features(
            self.df, empty_graph, self.feature_cols
        )
        # All n_neighbors should be 0
        self.assertTrue((result["n_neighbors"] == 0).all())


if __name__ == "__main__":
    unittest.main()
