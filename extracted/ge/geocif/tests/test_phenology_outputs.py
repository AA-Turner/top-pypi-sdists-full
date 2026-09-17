# -*- coding: utf-8 -*-
"""Tests for geocif/phenology/outputs.py (DESIGN.md section 6).

The zonal arithmetic is done by hand on a 4x4 grid so every expected number in
this file can be checked by reading the comment above it.

Layout shared by the table tests (``.`` = outside every unit, id 0)::

    id_grid          weight (km2)     value (days)      state
    1 1 2 2          1 1 | 1 1        10 20 |  1  1     4  4 | 1  1
    1 1 2 2          1 3 | 1 1        30 40 |  1  1     4  1 | 1  1
    1 1 2 2          2 4 | 0 1       NaN 50 |  1 NaN   -1  3 | 1 -1
    . . . .          5 5   5 5         9  9    9  9     0  0   0  0
"""
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

import numpy as np
import pandas as pd
import rasterio
from affine import Affine

from geocif.phenology import outputs
from geocif.phenology.core import SeasonState

TRANSFORM = Affine(0.05, 0, 36.0, 0, -0.05, 1.0)

ID_GRID = np.array(
    [
        [1, 1, 2, 2],
        [1, 1, 2, 2],
        [1, 1, 2, 2],
        [0, 0, 0, 0],
    ],
    dtype=np.int32,
)

WEIGHT = np.array(
    [
        [1.0, 1.0, 1.0, 1.0],
        [1.0, 3.0, 1.0, 1.0],
        [2.0, 4.0, 0.0, 1.0],
        [5.0, 5.0, 5.0, 5.0],
    ],
    dtype=np.float64,
)

VALUE = np.array(
    [
        [10.0, 20.0, 1.0, 1.0],
        [30.0, 40.0, 1.0, 1.0],
        [np.nan, 50.0, 1.0, np.nan],
        [9.0, 9.0, 9.0, 9.0],
    ],
    dtype=np.float64,
)

STATE = np.array(
    [
        [SeasonState.CONFIRMED, SeasonState.CONFIRMED, SeasonState.NOT_STARTED, SeasonState.NOT_STARTED],
        [SeasonState.CONFIRMED, SeasonState.NOT_STARTED, SeasonState.NOT_STARTED, SeasonState.NOT_STARTED],
        [-1, SeasonState.PROVISIONAL, SeasonState.NOT_STARTED, -1],
        [SeasonState.BEFORE_WINDOW] * 4,
    ],
    dtype=np.int8,
)

LOOKUP = pd.DataFrame(
    {
        "id": np.array([1, 2], dtype=np.int32),
        "ADM_ID": [101, 102],
        "ADM1_NAME": ["west_unit", "east_unit"],
    }
)


class TestWriteGeotiff(unittest.TestCase):
    def setUp(self):
        self._tmp = TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.addCleanup(self._tmp.cleanup)

    def test_float_round_trip_with_nan_nodata(self):
        arr = np.array([[1.5, np.nan], [-2.25, 4.0]], dtype=np.float32)
        path = outputs.write_geotiff(
            self.root / "sub" / "sos.tif",
            arr,
            Affine(0.05, 0, 36.0, 0, -0.05, 1.0),
            nodata=-9999.0,
            dtype="float32",
            tags={"variable": "sos", "units": "days since planting start"},
        )
        self.assertTrue(path.is_file())

        with rasterio.open(path) as src:
            data = src.read(1)
            self.assertEqual(src.profile["dtype"], "float32")
            self.assertEqual(src.profile["compress"], "lzw")
            self.assertTrue(src.profile["tiled"])
            self.assertEqual(src.profile["blockxsize"], 256)
            self.assertEqual(src.profile["blockysize"], 256)
            self.assertEqual(src.nodata, -9999.0)
            self.assertEqual(src.crs.to_epsg(), 4326)
            tags = src.tags()

        self.assertAlmostEqual(float(data[0, 0]), 1.5, places=6)
        self.assertAlmostEqual(float(data[0, 1]), -9999.0, places=6)  # NaN -> nodata
        self.assertAlmostEqual(float(data[1, 0]), -2.25, places=6)
        self.assertEqual(tags["variable"], "sos")
        self.assertEqual(tags["units"], "days since planting start")

    def test_int16_day_counts_and_int8_status(self):
        days = np.array([[12.0, np.nan], [400.0, 0.0]], dtype=np.float32)
        path = outputs.write_geotiff(
            self.root / "lgs.tif", days, TRANSFORM,
            nodata=-32768, dtype="int16", tags={"units": "days"},
        )
        with rasterio.open(path) as src:
            data = src.read(1)
            self.assertEqual(src.dtypes[0], "int16")
        self.assertEqual(int(data[0, 0]), 12)
        self.assertEqual(int(data[0, 1]), -32768)  # NaN never becomes garbage
        self.assertEqual(int(data[1, 0]), 400)

        status = np.array([[0, 3], [1, -1]], dtype=np.int8)
        path = outputs.write_geotiff(
            self.root / "state.tif", status, TRANSFORM,
            nodata=-1, dtype="int8", tags={},
        )
        with rasterio.open(path) as src:
            self.assertEqual(src.dtypes[0], "int8")
            self.assertEqual(src.nodata, -1)
            np.testing.assert_array_equal(src.read(1), status)

    def test_rejects_a_non_2d_array(self):
        with self.assertRaises(ValueError):
            outputs.write_geotiff(
                self.root / "bad.tif", np.zeros((2, 3, 4), dtype=np.float32),
                TRANSFORM, nodata=-1, dtype="float32", tags={},
            )


class TestZonalTable(unittest.TestCase):
    def setUp(self):
        self.table = outputs.zonal_table(VALUE, WEIGHT, ID_GRID, LOOKUP)
        self.row1 = self.table[self.table["id"] == 1].iloc[0]
        self.row2 = self.table[self.table["id"] == 2].iloc[0]

    def test_one_row_per_unit_with_display_names(self):
        self.assertEqual(list(self.table["id"]), [1, 2])
        self.assertEqual(list(self.table["ADM_ID"]), [101, 102])
        # _display_name: "west_unit".title() -> "West_Unit" -> "West Unit"
        self.assertEqual(list(self.table[outputs.DISPLAY_COL]), ["West Unit", "East Unit"])

    def test_unit_1_weighted_mean(self):
        # Unit 1 pixels (w, v): (1,10) (1,20) (1,30) (3,40) (2,NaN) (4,50)
        # valid weight = 1 + 1 + 1 + 3 + 4 = 10
        # sum(w*v) = 1*10 + 1*20 + 1*30 + 3*40 + 4*50 = 10 + 20 + 30 + 120 + 200 = 380
        # weighted mean = 380 / 10 = 38.0
        self.assertAlmostEqual(float(self.row1["weighted_mean"]), 38.0, places=9)

    def test_unit_1_weighted_median(self):
        # sorted values 10, 20, 30, 40, 50 with weights 1, 1, 1, 3, 4
        # cumulative 1, 2, 3, 6, 10; half of the total weight is 10 / 2 = 5
        # the first cumulative weight >= 5 is 6, at value 40
        self.assertAlmostEqual(float(self.row1["weighted_median"]), 40.0, places=9)

    def test_unit_1_valid_weight_share(self):
        # total weight in unit 1 = 1 + 1 + 1 + 3 + 2 + 4 = 12
        # weight carrying a finite value = 10  ->  10 / 12 = 0.8333...
        self.assertAlmostEqual(float(self.row1["valid_weight_share"]), 10.0 / 12.0, places=9)
        self.assertAlmostEqual(float(self.row1["valid_weight_km2"]), 10.0, places=9)
        self.assertAlmostEqual(float(self.row1["total_weight_km2"]), 12.0, places=9)
        self.assertEqual(int(self.row1["n_pixels"]), 6)

    def test_unit_2_drops_zero_weight_and_nan_value_pixels(self):
        # Unit 2 pixels (w, v): (1,1) (1,1) (1,1) (1,1) (0,1) (1,NaN)
        # the w = 0 pixel and the NaN-value pixel both drop out
        # valid weight = 4, total weight = 5, mean = 4 / 4 = 1.0
        self.assertAlmostEqual(float(self.row2["weighted_mean"]), 1.0, places=9)
        self.assertAlmostEqual(float(self.row2["weighted_median"]), 1.0, places=9)
        self.assertAlmostEqual(float(self.row2["valid_weight_share"]), 4.0 / 5.0, places=9)

    def test_pixels_outside_every_unit_are_ignored(self):
        # Row 3 carries weight 5 and value 9 everywhere but has id 0, so no
        # unit's total may include it: 12 + 5 = 17 != 12 + 5*4.
        self.assertAlmostEqual(
            float(self.row1["total_weight_km2"]) + float(self.row2["total_weight_km2"]),
            17.0,
            places=9,
        )

    def test_statuses_join_the_state_shares(self):
        table = outputs.zonal_table(VALUE, WEIGHT, ID_GRID, LOOKUP, statuses=STATE)
        row1 = table[table["id"] == 1].iloc[0]
        # see TestStatusAreaTable for the arithmetic
        self.assertAlmostEqual(float(row1["share_confirmed"]), 0.3, places=9)
        self.assertIn(outputs.NODATA_SHARE_COL, table.columns)

    def test_shape_mismatch_raises(self):
        with self.assertRaises(ValueError):
            outputs.zonal_table(VALUE[:2], WEIGHT, ID_GRID, LOOKUP)


class TestStatusAreaTable(unittest.TestCase):
    def setUp(self):
        self.table = outputs.status_area_table(STATE, WEIGHT, ID_GRID, LOOKUP)
        self.row1 = self.table[self.table["id"] == 1].iloc[0]
        self.row2 = self.table[self.table["id"] == 2].iloc[0]

    def test_unit_1_shares(self):
        # Unit 1 (w, state): (1,CONFIRMED) (1,CONFIRMED) (1,CONFIRMED)
        #                    (3,NOT_STARTED) (2,nodata) (4,PROVISIONAL)
        # total weight = 12, valid weight = 1 + 1 + 1 + 3 + 4 = 10
        # confirmed   = (1 + 1 + 1) / 10 = 0.3
        # not_started = 3 / 10 = 0.3
        # provisional = 4 / 10 = 0.4
        self.assertAlmostEqual(float(self.row1["share_confirmed"]), 0.3, places=9)
        self.assertAlmostEqual(float(self.row1["share_not_started"]), 0.3, places=9)
        self.assertAlmostEqual(float(self.row1["share_provisional"]), 0.4, places=9)
        self.assertAlmostEqual(float(self.row1["share_false_start"]), 0.0, places=9)
        self.assertAlmostEqual(float(self.row1["share_before_window"]), 0.0, places=9)
        self.assertAlmostEqual(float(self.row1["share_no_onset"]), 0.0, places=9)

    def test_unit_1_nodata_share_is_over_the_total_weight(self):
        # nodata weight = 2, total weight = 12 -> 2 / 12 = 0.1666...
        self.assertAlmostEqual(float(self.row1[outputs.NODATA_SHARE_COL]), 2.0 / 12.0, places=9)
        self.assertAlmostEqual(float(self.row1["valid_weight_km2"]), 10.0, places=9)
        self.assertAlmostEqual(float(self.row1["total_weight_km2"]), 12.0, places=9)

    def test_unit_2_shares(self):
        # Unit 2 (w, state): (1,NOT_STARTED) x4, (0,NOT_STARTED), (1,nodata)
        # valid weight = 4 -> not_started = 4 / 4 = 1.0
        # nodata share = 1 / 5 = 0.2
        self.assertAlmostEqual(float(self.row2["share_not_started"]), 1.0, places=9)
        self.assertAlmostEqual(float(self.row2[outputs.NODATA_SHARE_COL]), 0.2, places=9)

    def test_state_shares_sum_to_one_per_unit(self):
        share_cols = [
            f"{outputs.SHARE_PREFIX}{member.name.lower()}" for member in SeasonState
        ]
        self.assertEqual(len(share_cols), 6)
        totals = self.table[share_cols].sum(axis=1)
        np.testing.assert_allclose(totals.to_numpy(), np.ones(len(self.table)), atol=1e-12)

    def test_display_names_and_slugs_both_present(self):
        self.assertIn("ADM1_NAME", self.table.columns)
        self.assertIn(outputs.DISPLAY_COL, self.table.columns)
        self.assertEqual(list(self.table["ADM1_NAME"]), ["west_unit", "east_unit"])
        self.assertEqual(list(self.table[outputs.DISPLAY_COL]), ["West Unit", "East Unit"])

    def test_a_unit_with_no_weight_yields_nan_not_a_crash(self):
        table = outputs.status_area_table(STATE, np.zeros_like(WEIGHT), ID_GRID, LOOKUP)
        self.assertTrue(np.isnan(float(table.iloc[0]["share_confirmed"])))
        self.assertTrue(np.isnan(float(table.iloc[0][outputs.NODATA_SHARE_COL])))

    def test_shape_mismatch_raises(self):
        with self.assertRaises(ValueError):
            outputs.status_area_table(STATE[:2], WEIGHT, ID_GRID, LOOKUP)


class TestWeightedMedianHelper(unittest.TestCase):
    def test_empty_and_zero_weight_are_nan(self):
        self.assertTrue(np.isnan(outputs._weighted_median(np.array([]), np.array([]))))
        self.assertTrue(
            np.isnan(outputs._weighted_median(np.array([1.0, 2.0]), np.array([0.0, 0.0])))
        )

    def test_equal_weights_match_the_lower_median(self):
        # values 1, 2, 3, 4 with weight 1 each; total 4, half 2
        # cumulative 1, 2, 3, 4 -> first >= 2 is at value 2
        self.assertEqual(
            outputs._weighted_median(np.array([1.0, 2.0, 3.0, 4.0]), np.ones(4)), 2.0
        )

    def test_negative_weights_are_dropped_upstream(self):
        cleaned = outputs._clean_weight(np.array([1.0, -2.0, np.nan, 3.0]))
        np.testing.assert_array_equal(cleaned, np.array([1.0, 0.0, 0.0, 3.0]))


if __name__ == "__main__":
    unittest.main()
