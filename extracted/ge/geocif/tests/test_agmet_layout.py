"""Tests for the opt-in county layout of geocif.agmet.geoagmet (region_folder,
group_by_admin_1, id_width, district_file, district_folder) and for the default
path, which must stay as it was for every other project."""

import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

import matplotlib

matplotlib.use("Agg")

import numpy as np
import pandas as pd


def _boundary():
    import geopandas as gpd
    from shapely.geometry import box

    return gpd.GeoDataFrame(
        {
            "ADM_ID": [27067, 27093, 19169],
            "ADM1_NAME": ["Minnesota", "Minnesota", "Iowa"],
            "ADM2_NAME": ["minnesota kandiyohi", "minnesota meeker", "iowa story"],
        },
        geometry=[box(0, 0, 1, 1), box(1, 0, 2, 1), box(0, -2, 1, -1)],
        crs="EPSG:4326",
    )


def _write_district_file(tmpdir, rows=None):
    path = Path(tmpdir) / "districts.csv"
    pd.DataFrame(rows or {
        "region_id": [27067, 27093, 19169],
        "admin_1": ["Minnesota", "Minnesota", "Iowa"],
        "district_id": ["2740", "2740", "1950"],
        "district_name": ["West Central", "West Central", "Central"],
    }).to_csv(path, index=False)
    return path


def _obj(tmpdir, **overrides):
    """Stand-in for AgmetGeo after setup_region, with parse_config's defaults."""
    meta = Path(tmpdir)
    pd.DataFrame({
        "Country": ["united_states_of_america"], "Crop": ["mz"], "Season": [1], "Name": ["Corn"],
    }).to_csv(meta / "crop_per_season.csv", index=False)
    obj = SimpleNamespace(
        dir_agmet=meta / "plots" / "mz_s1_2026" / "condition",
        dir_metadata=meta,
        region_folder="",
        scale_short="adm2",
        group_by_admin_1=False,
        id_width=0,
        district_table=None,
        district_folder="district",
        filename_with_state=False,
        region="minnesota_kandiyohi",
        region_id=27067,
        calendar_region="minnesota",
        country="united_states_of_america",
        crop="maize",
        growing_season=1,
        plot_season=2026,
    )
    for key, value in overrides.items():
        setattr(obj, key, value)
    return obj


class TestDefaultLayoutUnchanged(unittest.TestCase):
    def test_region_figure_spec_default(self):
        from geocif.agmet.geoagmet import _region_figure_spec

        with tempfile.TemporaryDirectory() as tmp:
            obj = _obj(tmp)
            gdf = _boundary()
            folder, fname, title, locator, outlines = _region_figure_spec(obj, gdf, {})
            self.assertEqual(folder, obj.dir_agmet / "adm2")
            self.assertEqual(fname, "minnesota_kandiyohi.png")
            self.assertEqual(
                title, "Minnesota Kandiyohi (Minnesota, United States Of America)\nCorn 2026"
            )
            self.assertIs(locator, gdf)
            self.assertFalse(outlines)

    def test_region_folder_alone_only_renames_the_folder(self):
        from geocif.agmet.geoagmet import _region_figure_spec

        with tempfile.TemporaryDirectory() as tmp:
            obj = _obj(tmp, region_folder="county")
            folder, fname, _, _, _ = _region_figure_spec(obj, _boundary(), {})
            self.assertEqual(folder, obj.dir_agmet / "county")
            self.assertEqual(fname, "minnesota_kandiyohi.png")

    def test_district_title_default(self):
        from geocif.agmet.geoagmet import _create_district_title

        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(
                _create_district_title(_obj(tmp), "central_plains"),
                "Central Plains (United States Of America)\nCorn 2026",
            )

    def test_aggregate_district_matches_previous_inline_code(self):
        from geocif.agmet.geoagmet import _aggregate_district, _district_columns

        dates = pd.date_range("2026-05-01", periods=3)
        df = pd.DataFrame({
            "country": "usa",
            "calendar_region": "iowa",
            "region": np.repeat(["a", "b"], 3),
            "harvest_season": 2026,
            "doy": np.tile(dates.dayofyear, 2),
            "datetime": np.tile(dates, 2),
            "month": np.tile(dates.month, 2),
            "day": np.tile(dates.day, 2),
            "yield": [10.0] * 3 + [12.0] * 3,
            "chirps": [1.0, 2.0, 3.0, 3.0, 4.0, 5.0],
            "chirts_era5_tmax": [30.0, 31.0, 32.0, 28.0, 29.0, 30.0],
            "chirts_era5_tmin": [10.0, 11.0, 12.0, 8.0, 9.0, 10.0],
        }, index=np.tile(dates, 2))
        obj = SimpleNamespace(
            eo_model=["chirps", "chirts_era5_tmax", "chirts_era5_tmin"],
            plot_season=2026,
            check_date=lambda d, s: (False, False),
        )
        got = _aggregate_district(obj, df, "calendar_region")

        # The block _aggregate_district replaced in the calendar-region loop
        columns = _district_columns(obj.eo_model, df.columns, False)
        want = (
            df.groupby(["country", "calendar_region", "harvest_season", "doy", "datetime"])[columns]
            .mean()
            .reset_index()
        )
        want.loc[:, "average_temperature"] = (
            want["chirts_era5_tmax"] + want["chirts_era5_tmin"]
        ) / 2.0
        want.set_index(pd.DatetimeIndex(want["datetime"]), inplace=True, drop=True)
        want.index.name = None
        want.sort_values(by="datetime", inplace=True)
        pd.testing.assert_frame_equal(got, want)
        self.assertEqual(got["chirps"].tolist(), [2.0, 3.0, 4.0])

    def test_district_share_sums_one_value_per_region(self):
        from geocif.agmet.geoagmet import _district_share

        df = pd.DataFrame({"region": ["a", "a", "b"], "production_share_pct": [1.5, 1.5, 2.0]})
        self.assertAlmostEqual(_district_share(df), 3.5)
        self.assertIsNone(_district_share(df.drop(columns="production_share_pct")))


class TestGroupByAdmin1(unittest.TestCase):
    def test_county_in_state_folder_named_by_fips(self):
        from geocif.agmet.geoagmet import _region_figure_spec, read_district_file

        with tempfile.TemporaryDirectory() as tmp:
            obj = _obj(
                tmp, region_folder="county", group_by_admin_1=True, id_width=5,
                district_table=read_district_file(_write_district_file(tmp)),
            )
            folder, fname, title, locator, outlines = _region_figure_spec(obj, _boundary(), {})
            self.assertEqual(folder, obj.dir_agmet / "county" / "minnesota")
            self.assertEqual(fname, "27067_kandiyohi.png")
            self.assertEqual(title, "Kandiyohi, Minnesota (West Central)\nCorn 2026")
            self.assertEqual(sorted(locator["ADM_ID"]), [27067, 27093])
            self.assertTrue(outlines)

    def test_title_names_calendar_region_without_district_file(self):
        from geocif.agmet.geoagmet import _region_figure_spec

        with tempfile.TemporaryDirectory() as tmp:
            obj = _obj(tmp, group_by_admin_1=True)
            _, _, title, _, _ = _region_figure_spec(obj, _boundary(), {})
            self.assertEqual(title, "Kandiyohi, Minnesota (Minnesota)\nCorn 2026")

    def test_unknown_admin_1_stays_in_region_folder(self):
        from geocif.agmet.geoagmet import _region_figure_spec

        with tempfile.TemporaryDirectory() as tmp:
            obj = _obj(tmp, group_by_admin_1=True, id_width=5, region="nowhere_x", region_id=99999)
            gdf = _boundary()
            folder, fname, _, locator, outlines = _region_figure_spec(obj, gdf, {})
            self.assertEqual(folder, obj.dir_agmet / "adm2")
            self.assertEqual(fname, "99999_nowhere_x.png")
            self.assertIs(locator, gdf)
            self.assertFalse(outlines)

    def test_district_figure_spec(self):
        from geocif.agmet.geoagmet import _district_figure_spec, read_district_file

        with tempfile.TemporaryDirectory() as tmp:
            table = read_district_file(_write_district_file(tmp))
            obj = _obj(tmp, group_by_admin_1=True, district_table=table, district_folder="asd")
            folder, fname, title, locator, outlines, highlight = _district_figure_spec(
                obj, "2740", [27067, 27093], _boundary(), {}
            )
            self.assertEqual(folder, obj.dir_agmet / "asd" / "minnesota")
            self.assertEqual(fname, "2740_west_central.png")
            self.assertEqual(title, "West Central, Minnesota\nCorn 2026")
            self.assertEqual(sorted(locator["ADM_ID"]), [27067, 27093])
            self.assertTrue(outlines)
            self.assertEqual(len(highlight), 1)
            self.assertEqual(list(highlight.total_bounds), [0.0, 0.0, 2.0, 1.0])

            obj.group_by_admin_1 = False
            folder, _, title, locator, outlines, _ = _district_figure_spec(
                obj, "2740", [27067, 27093], _boundary(), {}
            )
            self.assertEqual(folder, obj.dir_agmet / "asd")
            self.assertEqual(title, "West Central (United States Of America)\nCorn 2026")
            self.assertEqual(len(locator), 3)
            self.assertFalse(outlines)


class TestNamesAndIds(unittest.TestCase):
    def test_slug(self):
        from geocif.agmet.geoagmet import _slug

        self.assertEqual(_slug("St. Clair"), "st_clair")
        self.assertEqual(_slug("Miami-Dade"), "miami-dade")
        self.assertEqual(_slug("Coastal Plains & Gulf Coast"), "coastal_plains_gulf_coast")
        self.assertEqual(_slug("O'Brien"), "obrien")
        self.assertEqual(_slug("North Dakota"), "north_dakota")

    def test_format_id(self):
        from geocif.agmet.geoagmet import _format_id

        self.assertEqual(_format_id(1001, 5), "01001")
        self.assertEqual(_format_id(1001.0, 5), "01001")
        self.assertEqual(_format_id("27067", 5), "27067")
        self.assertEqual(_format_id(1001, 0), "1001")
        self.assertEqual(_format_id("BD456120", 5), "BD456120")

    def test_id_key(self):
        from geocif.agmet.geoagmet import _id_key

        self.assertEqual({_id_key(1001), _id_key(1001.0), _id_key("1001")}, {"1001"})
        self.assertEqual(_id_key("BD456120"), "bd456120")

    def test_unit_name_drops_admin_1_prefix(self):
        import geopandas as gpd
        from shapely.geometry import box
        from geocif.agmet.geoagmet import _unit_name

        gdf = gpd.GeoDataFrame(
            {"ADM_ID": [38017], "ADM1_NAME": ["North Dakota"], "ADM2_NAME": ["north dakota cass"]},
            geometry=[box(0, 0, 1, 1)],
        )
        self.assertEqual(_unit_name("north_dakota_cass", 38017, "North Dakota", gdf), "cass")
        self.assertEqual(_unit_name("north_dakota_cass", None, "North Dakota", None), "cass")
        self.assertEqual(_unit_name("story", 1, None, None), "story")


class TestReadDistrictFile(unittest.TestCase):
    def test_keeps_leading_zeros(self):
        from geocif.agmet.geoagmet import read_district_file

        with tempfile.TemporaryDirectory() as tmp:
            path = _write_district_file(tmp, {
                "region_id": [1001], "admin_1": ["Alabama"],
                "district_id": ["0140"], "district_name": ["Black Belt"],
            })
            self.assertEqual(read_district_file(path)["district_id"].tolist(), ["0140"])

    def test_rejects_duplicates_and_missing_columns(self):
        from geocif.agmet.geoagmet import read_district_file

        with tempfile.TemporaryDirectory() as tmp:
            path = _write_district_file(tmp, {
                "region_id": [1001, 1001], "admin_1": ["Alabama"] * 2,
                "district_id": ["0140", "0150"], "district_name": ["Black Belt", "Wiregrass"],
            })
            with self.assertRaises(ValueError):
                read_district_file(path)
            path = _write_district_file(tmp, {"region_id": [1001], "district_id": ["0140"]})
            with self.assertRaises(ValueError):
                read_district_file(path)


class TestInsetOutlines(unittest.TestCase):
    def _inset_collections(self, outlines):
        import matplotlib.pyplot as plt
        from geocif.agmet.plot import AgmetPlotter

        plotter = AgmetPlotter.__new__(AgmetPlotter)
        gdf = _boundary()
        plotter.boundary_gdf = gdf[gdf["ADM1_NAME"] == "Minnesota"]
        plotter.admin_level = "admin_2"
        plotter.highlight_gdf = None
        plotter.region_id = 27067
        plotter.region = "minnesota_kandiyohi"
        plotter.inset_outlines = outlines

        fig, _ = plt.subplots(figsize=(20, 10))
        fig.suptitle("Kandiyohi, Minnesota (West Central)\nCorn 2026")
        plotter._add_inset_map(fig)
        n_axes, n_collections = len(fig.axes), len(fig.axes[-1].collections)
        plt.close(fig)
        return n_axes, n_collections

    def test_outlines_draw_units_and_admin_1_outline(self):
        # units + admin_1 outline + highlight
        self.assertEqual(self._inset_collections(True), (2, 3))

    def test_default_draws_one_dissolved_outline(self):
        # dissolved outline + highlight
        self.assertEqual(self._inset_collections(False), (2, 2))


if __name__ == "__main__":
    unittest.main()
