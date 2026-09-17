# -*- coding: utf-8 -*-
"""Tests for geocif/viz/phenology_maps.py (DESIGN.md section 8).

GMT-free by default. Two techniques, both borrowed from the existing suite:

* a render SPY (``tests/test_pygmt_backend.py`` monkeypatches the renderer):
  since the module does ``import pygmt`` INSIDE the drawing function, putting a
  stub in ``sys.modules`` captures every GMT call the maps would make;
* source-structure assertions (``tests/test_map_admin2_styling.py`` reads the
  renderer source): these pin the "one shared skeleton" property that a spy
  cannot see -- a second hand-rolled figure would still pass every call check.

One end-to-end test renders through the real GMT and is skipped when the C
library cannot load in-process.

Every expected number below is hand-computed with the arithmetic in a comment.
"""

import ast
import re
import sys
import unittest
from datetime import date
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import mock

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from geocif.phenology.core import SeasonState
from geocif.viz import _style, phenology_maps as pm

SOURCE = (Path(__file__).resolve().parents[1] / "geocif" / "viz"
          / "phenology_maps.py").read_text(encoding="utf-8")


def _gmt_loadable():
    """True iff PyGMT can open a GMT session in this process."""
    try:
        from pygmt.clib import Session

        with Session():
            pass
        return True
    except Exception:  # noqa: BLE001 -- any failure means "no GMT here"
        return False


# ---------------------------------------------------------------------------
# render spy
# ---------------------------------------------------------------------------
class _SpyFigure:
    """Records every GMT call and writes a stand-in PNG on save."""

    def __init__(self, calls):
        self.calls = calls

    def _record(self, name, kwargs):
        self.calls.append((name, kwargs))

    def basemap(self, **kwargs):
        self._record("basemap", kwargs)

    def coast(self, **kwargs):
        self._record("coast", kwargs)

    def grdimage(self, **kwargs):
        self._record("grdimage", kwargs)

    def plot(self, **kwargs):
        self._record("plot", kwargs)

    def colorbar(self, **kwargs):
        # read the custom-annotation file WHILE it exists: it lives in a
        # TemporaryDirectory that is gone by the time the test asserts
        annot = None
        for entry in kwargs.get("frame", []):
            if str(entry).startswith("xc"):
                annot = Path(str(entry)[2:]).read_text(encoding="utf-8")
        self._record("colorbar", dict(kwargs, annot_text=annot))

    def savefig(self, path, **kwargs):
        Path(path).write_bytes(b"\x89PNG stub")
        self._record("savefig", dict(kwargs, path=str(path)))


class _SpyPygmt:
    """Stand-in for the pygmt module object the drawing function imports."""

    def __init__(self):
        self.calls = []

    def Figure(self):  # noqa: N802 -- mirrors the pygmt API
        self.calls.append(("Figure", {}))
        return _SpyFigure(self.calls)

    def config(self, **kwargs):
        self.calls.append(("config", kwargs))

    def makecpt(self, **kwargs):
        self.calls.append(("makecpt", kwargs))

    def names(self):
        return [name for name, _ in self.calls]

    def only(self, name):
        return [kwargs for call, kwargs in self.calls if call == name]


def _ctx(tmp, **overrides):
    """A 2x3 Kenya-ish window; pixel centres on the 0.05 degree lattice."""
    kwargs = dict(
        lon=np.array([36.025, 36.075, 36.125]),
        lat=np.array([0.075, 0.025]),        # north -> south
        dir_plots=Path(tmp) / "maps",
        dir_csvs=Path(tmp) / "csvs",
        country="kenya",
        crop="maize",
        season=1,
        asof=date(2026, 9, 14),
    )
    kwargs.update(overrides)
    return pm.MapContext(**kwargs)


STATE_GRID = np.array([[0, 1, 2], [3, 4, -1]], dtype=np.int8)


# ---------------------------------------------------------------------------
# SCALE_LABEL (DESIGN: this module encodes the house rule first)
# ---------------------------------------------------------------------------
class TestScaleLabel(unittest.TestCase):
    def test_tokens_map_to_display_names(self):
        self.assertEqual(pm.SCALE_LABEL, {"admin_1": "Admin 1",
                                          "admin_2": "Admin 2"})

    def test_scale_label_is_case_and_space_tolerant(self):
        self.assertEqual(pm.scale_label(" Admin_1 "), "Admin 1")
        self.assertEqual(pm.scale_label("admin_2"), "Admin 2")

    def test_unknown_token_still_never_reaches_a_figure_underscored(self):
        self.assertEqual(pm.scale_label("admin_3"), "Admin 3")

    def test_no_raw_token_in_a_title(self):
        with TemporaryDirectory() as tmp:
            title = pm.map_title("Season State", _ctx(tmp))
        self.assertIn("Admin 1", title)
        self.assertNotIn("admin_1", title)


# ---------------------------------------------------------------------------
# pure numeric decisions
# ---------------------------------------------------------------------------
class TestLimits(unittest.TestCase):
    def test_symmetric_limits_round_out_to_the_step(self):
        # peak |−12| = 12 -> ceil(12 / 5) * 5 = 15
        self.assertEqual(pm.symmetric_limits(np.array([-12.0, 3.0, 7.0])),
                         (-15.0, 15.0))

    def test_symmetric_limits_respect_the_floor(self):
        # peak 0.2 -> ceil(0.2 / 5) * 5 = 5, and the floor is 5 too
        self.assertEqual(pm.symmetric_limits(np.array([0.1, -0.2])),
                         (-5.0, 5.0))

    def test_symmetric_limits_ignore_nan_and_survive_an_empty_layer(self):
        self.assertEqual(pm.symmetric_limits(np.array([np.nan, -3.0])),
                         (-5.0, 5.0))
        self.assertEqual(pm.symmetric_limits(np.full(4, np.nan), minimum=7.0),
                         (-7.0, 7.0))

    def test_sequential_limits_clip_the_tails(self):
        # 0..100 in 101 steps: p2 = 2, p98 = 98
        low, high = pm.sequential_limits(np.arange(101.0))
        self.assertEqual((low, high), (2.0, 98.0))

    def test_sequential_limits_widen_a_flat_layer(self):
        # p0 = 1, p100 = 3 -> span 2 < 5 -> midpoint 2 +/- 2.5
        low, high = pm.sequential_limits(
            np.array([1.0, 2.0, 3.0]), lower_pct=0.0, upper_pct=100.0,
            minimum_span=5.0)
        self.assertAlmostEqual(low, -0.5)
        self.assertAlmostEqual(high, 4.5)

    def test_sequential_limits_round_out_to_the_step(self):
        # p0 = 3, p100 = 12 -> floor(3/5)*5 = 0, ceil(12/5)*5 = 15
        low, high = pm.sequential_limits(
            np.array([3.0, 7.0, 12.0]), lower_pct=0.0, upper_pct=100.0,
            step=5.0)
        self.assertEqual((low, high), (0.0, 15.0))

    def test_sequential_limits_on_an_empty_layer(self):
        self.assertEqual(
            pm.sequential_limits(np.full(3, np.nan), minimum_span=2.0),
            (0.0, 2.0))

    def test_nice_day_step(self):
        self.assertEqual(pm.nice_day_step(90), 15)     # 90 / 6 = 15
        self.assertEqual(pm.nice_day_step(30), 5)      # 30 / 6 = 5
        self.assertEqual(pm.nice_day_step(66), 15)     # 66 / 6 = 11 -> 15
        self.assertEqual(pm.nice_day_step(1000), 120)  # off the table


class TestDateTicks(unittest.TestCase):
    REF = date(2026, 10, 15)

    def test_ticks_are_calendar_dates(self):
        # span 90 -> step 15; 2026-10-15 - 30 d = 2026-09-15, + 60 d = 2026-12-14
        ticks = pm.date_tick_annotations(-30, 60, self.REF)
        self.assertEqual(
            ticks,
            [(-30, "15 Sep"), (-15, "30 Sep"), (0, "15 Oct"), (15, "30 Oct"),
             (30, "14 Nov"), (45, "29 Nov"), (60, "14 Dec")])

    def test_first_tick_is_inside_the_range(self):
        # step 10 forced; ceil(-7 / 10) * 10 = 0 is the first tick >= -7
        ticks = pm.date_tick_annotations(-7, 25, self.REF, step=10)
        self.assertEqual([t for t, _ in ticks], [0, 10, 20])

    def test_annotation_file_is_gmt_custom_format(self):
        with TemporaryDirectory() as tmp:
            path = pm.write_annotation_file(
                Path(tmp) / "a.txt", [(0, "15 Oct"), (15, "30 Oct")])
            self.assertEqual(path.read_text(encoding="utf-8"),
                             "0 a 15 Oct\n15 a 30 Oct\n")


class TestGridHelpers(unittest.TestCase):
    def test_grid_keeps_the_north_first_row_order(self):
        grid = pm.grid_from_array(np.arange(6.0).reshape(2, 3),
                                  np.array([36.025, 36.075, 36.125]),
                                  np.array([0.075, 0.025]))
        self.assertEqual(grid.dims, ("lat", "lon"))
        self.assertAlmostEqual(float(grid.lat[0]), 0.075)
        self.assertAlmostEqual(float(grid.isel(lat=0, lon=0)), 0.0)

    def test_grid_rejects_a_shape_mismatch(self):
        with self.assertRaises(ValueError):
            pm.grid_from_array(np.zeros((2, 2)), np.array([1.0, 2.0, 3.0]),
                               np.array([1.0, 2.0]))

    def test_region_pads_half_a_pixel(self):
        # centres 36.025..36.125 with dx 0.05 -> edges 36.0 and 36.15
        region = pm.region_from_grid(np.array([36.025, 36.075, 36.125]),
                                     np.array([0.075, 0.025]))
        self.assertEqual([round(v, 6) for v in region],
                         [36.0, 36.15, 0.0, 0.1])

    def test_state_nodata_becomes_nan(self):
        out = pm.state_to_float(STATE_GRID)
        self.assertTrue(np.isnan(out[1, 2]))
        self.assertEqual(out[0, 0], 0.0)
        self.assertEqual(out[1, 1], float(SeasonState.CONFIRMED))

    def test_state_codes_outside_the_enum_become_nan(self):
        out = pm.state_to_float(np.array([[6, 4]], dtype=np.int8))
        self.assertTrue(np.isnan(out[0, 0]))
        self.assertEqual(out[0, 1], 4.0)

    def test_mask_display_blanks_outside_the_mask(self):
        values = np.array([[1.0, 2.0], [3.0, 4.0]])
        keep = np.array([[True, False], [False, True]])
        out = pm.mask_display(values, keep)
        self.assertEqual(out[0, 0], 1.0)
        self.assertTrue(np.isnan(out[0, 1]))
        self.assertEqual(values[0, 1], 2.0, "input must not be mutated")
        self.assertTrue(np.array_equal(pm.mask_display(values, None), values))


# ---------------------------------------------------------------------------
# text: titles, stems, GMT safety
# ---------------------------------------------------------------------------
class TestText(unittest.TestCase):
    def test_gmt_safe_drops_quotes_and_newlines(self):
        self.assertEqual(pm.gmt_safe('a "b"\nc'), "a b c")

    def test_through_text_has_no_leading_zero_on_the_day(self):
        with TemporaryDirectory() as tmp:
            ctx = _ctx(tmp, asof=date(2026, 9, 4))
            self.assertEqual(pm.through_text(ctx), "data through 4 Sep 2026")

    def test_through_text_for_a_climatology(self):
        with TemporaryDirectory() as tmp:
            ctx = _ctx(tmp, asof=None, years=(1981, 2025))
            self.assertEqual(pm.through_text(ctx), "1981-2025")

    def test_title_is_short_factual_and_title_cased(self):
        with TemporaryDirectory() as tmp:
            title = pm.map_title("Season State", _ctx(tmp))
        self.assertEqual(
            title, "Kenya Maize Season State, Admin 1, data through 14 Sep 2026")

    def test_title_font_shrinks_with_the_title_length(self):
        # 12 cm = 12 * 72 / 2.54 = 340.16 pt of map width
        # 59 chars: 340.16 / (59 * 0.52) = 11.09 pt
        title = "Kenya Maize Season State, Admin 1, data through 14 Sep 2026"
        self.assertEqual(len(title), 59)
        self.assertEqual(pm.title_font(title), "11.1p,Helvetica,black")
        # short title is capped at the house 14 pt
        self.assertEqual(pm.title_font("Kenya Maize Onset"),
                         f"{pm.TITLE_MAX_PT:.1f}p,Helvetica,black")
        # very long title stops at the legibility floor
        self.assertEqual(pm.title_font("x" * 400),
                         f"{pm.TITLE_MIN_PT:.1f}p,Helvetica,black")

    def test_stem_follows_the_design_pattern(self):
        with TemporaryDirectory() as tmp:
            self.assertEqual(pm.map_stem("season_state", _ctx(tmp)),
                             "season_state_kenya_maize_s1_asof20260914")
            clim = _ctx(tmp, asof=None, years=(1981, 2025))
            self.assertEqual(pm.map_stem("onset_median", clim),
                             "onset_median_kenya_maize_s1_1981_2025")


# ---------------------------------------------------------------------------
# palette / colourbar keyword building
# ---------------------------------------------------------------------------
class TestCmapKwargs(unittest.TestCase):
    def test_state_palette_has_one_box_per_state_and_no_grey(self):
        spec, labels = pm.state_cmap_spec()
        self.assertEqual(len(labels), len(SeasonState))
        self.assertEqual(spec.series, (0.0, float(len(SeasonState) - 1), 1.0))
        self.assertFalse(spec.continuous)
        # grey already means non-cropland / nodata on these maps
        colors = {c.lower() for c in pm.STATE_COLORS.values()}
        self.assertNotIn(_style.NODATA.lower(), colors)
        before = pm.STATE_COLORS[int(SeasonState.BEFORE_WINDOW)].lstrip("#")
        red, green, blue = (int(before[i:i + 2], 16) for i in (0, 2, 4))
        self.assertGreater(max(red, green, blue) - min(red, green, blue), 20,
                           "BEFORE_WINDOW is achromatic, i.e. a grey")
        self.assertEqual(len(colors), len(pm.STATE_COLORS), "duplicate colour")

    def test_categorical_kwargs_use_the_colour_model(self):
        spec, labels = pm.state_cmap_spec()
        kwargs = pm.makecpt_kwargs(spec, labels)
        self.assertTrue(kwargs["color_model"].startswith("+cBefore window,"))
        self.assertNotIn("continuous", kwargs)
        self.assertNotIn("background", kwargs)

    def test_continuous_kwargs_ask_for_background_extenders(self):
        kwargs = pm.makecpt_kwargs(
            pm.CmapSpec(cmap="hot", series=(0.0, 10.0), reverse=True))
        self.assertEqual(kwargs["cmap"], "hot")
        self.assertEqual(kwargs["series"], [0.0, 10.0])
        self.assertTrue(kwargs["background"])
        self.assertTrue(kwargs["reverse"])
        # -Z with no increment in -T makes GMT warn and ignore it
        self.assertNotIn("continuous", kwargs)

    def test_continuous_is_only_asked_for_when_the_series_has_an_increment(self):
        kwargs = pm.makecpt_kwargs(pm.CmapSpec(cmap="hot", series=(0.0, 10.0, 2.0)))
        self.assertTrue(kwargs["continuous"])

    def test_labels_never_carry_a_comma_into_the_colour_model(self):
        kwargs = pm.makecpt_kwargs(
            pm.CmapSpec(cmap="a,b", series=(0.0, 1.0, 1.0), continuous=False),
            ["one, two", "three"])
        self.assertEqual(kwargs["color_model"], "+cone two,three")

    def test_colorbar_frame_and_position(self):
        kwargs = pm.colorbar_kwargs("Days past median onset")
        self.assertEqual(kwargs["frame"], ["x+lDays past median onset"])
        self.assertEqual(kwargs["position"], _style.CBAR_POS + "+e")
        cat = pm.colorbar_kwargs("Season state", ["a", "b"])
        self.assertEqual(cat["position"], _style.CBAR_POS)

    def test_colorbar_annotation_file_comes_first(self):
        kwargs = pm.colorbar_kwargs("Median onset date", annot_file="/tmp/a.txt")
        self.assertEqual(kwargs["frame"],
                         ["xc/tmp/a.txt", "x+lMedian onset date"])


# ---------------------------------------------------------------------------
# companion tables
# ---------------------------------------------------------------------------
class TestSummaries(unittest.TestCase):
    VALUES = np.array([[1.0, 2.0, np.nan], [3.0, 4.0, 100.0]])

    def test_pixel_summary_counts_and_percentiles(self):
        table = pm.pixel_summary(self.VALUES, units="days")
        got = dict(zip(table["statistic"], table["value"]))
        # 6 pixels, 5 finite -> valid share 5/6
        self.assertEqual(got["n_pixels"], 6.0)
        self.assertEqual(got["n_valid"], 5.0)
        self.assertEqual(got["n_nodata"], 1.0)
        self.assertAlmostEqual(got["valid_share"], 5.0 / 6.0)
        # sorted finite values: 1, 2, 3, 4, 100 (linear interpolation)
        self.assertEqual(got["minimum"], 1.0)
        self.assertAlmostEqual(got["p10"], 1.4)    # 0.10*(5-1)=0.4 -> 1+0.4*1
        self.assertAlmostEqual(got["p25"], 2.0)    # 0.25*4 = 1.0 -> 2
        self.assertAlmostEqual(got["median"], 3.0)
        self.assertAlmostEqual(got["p75"], 4.0)    # 0.75*4 = 3.0 -> 4
        self.assertAlmostEqual(got["p90"], 61.6)   # 3.6 -> 4 + 0.6*96
        self.assertEqual(got["maximum"], 100.0)
        self.assertAlmostEqual(got["mean"], 22.0)  # 110 / 5
        self.assertEqual(set(table["units"]), {"days"})

    def test_pixel_summary_on_an_all_nan_layer(self):
        got = dict(zip(*pm.pixel_summary(np.full((2, 2), np.nan))
                       [["statistic", "value"]].to_numpy().T))
        self.assertEqual(got["n_valid"], 0.0)
        self.assertTrue(np.isnan(got["median"]))

    def test_state_summary_shares_sum_to_one(self):
        state = pm.state_to_float(
            np.array([[0, 1, 2], [3, 4, 5], [4, 4, -1]], dtype=np.int8))
        table = pm.state_summary(state)
        counts = dict(zip(table["state"], table["n_pixels"]))
        # 9 pixels: one each of five states, three CONFIRMED, one nodata
        self.assertEqual(counts["Confirmed"], 3)
        self.assertEqual(counts["Before window"], 1)
        self.assertEqual(counts["nodata"], 1)
        self.assertEqual(table["n_pixels"].sum(), 9)
        self.assertAlmostEqual(table["share"].sum(), 1.0)
        self.assertAlmostEqual(
            float(table.loc[table["state"] == "Confirmed", "share"].iloc[0]),
            3.0 / 9.0)


# ---------------------------------------------------------------------------
# render spy: what the maps actually ask GMT to do
# ---------------------------------------------------------------------------
class TestRenderSpy(unittest.TestCase):
    def _render(self, fn, *args, **kwargs):
        spy = _SpyPygmt()
        with mock.patch.dict(sys.modules, {"pygmt": spy}):
            result = fn(*args, **kwargs)
        return spy, result

    def test_season_state_map_call_sequence(self):
        with TemporaryDirectory() as tmp:
            ctx = _ctx(tmp, admin_gdf=["one-polygon"])
            spy, row = self._render(pm.season_state_map, STATE_GRID, ctx)

            names = spy.names()
            self.assertEqual(
                names,
                ["Figure", "config", "basemap", "coast", "makecpt", "grdimage",
                 "plot", "coast", "colorbar", "savefig"])
            # land goes down before the grid, or NaN would read as ocean
            self.assertEqual(spy.only("coast")[0]["land"], _style.NODATA)
            self.assertEqual(spy.only("coast")[0]["shorelines"],
                             _style.COAST_KW["shorelines"])
            # national borders last, over the raster
            self.assertEqual(spy.only("coast")[1]["borders"], _style.BORDER_PEN)
            self.assertEqual(spy.only("plot")[0]["pen"], _style.POLY_PEN)

            grd = spy.only("grdimage")[0]
            self.assertTrue(grd["nan_transparent"])
            self.assertEqual(grd["grid"].shape, (2, 3))
            self.assertTrue(np.isnan(float(grd["grid"][1, 2])))

            cpt = spy.only("makecpt")[0]
            self.assertIn("+cBefore window,", cpt["color_model"])
            self.assertEqual(cpt["series"], [0.0, 5.0, 1.0])

            # the title is sized to the map width, not left at a fixed 14 pt
            self.assertEqual(spy.only("config")[0]["FONT_TITLE"],
                             pm.title_font(spy.only("basemap")[0]["frame"][1][2:]))

            self.assertEqual(spy.only("savefig")[0]["dpi"], pm.DEFAULT_DPI)
            png, csv, desc = row
            self.assertEqual(png, "season_state_kenya_maize_s1_asof20260914.png")
            self.assertEqual(csv, "season_state_kenya_maize_s1_asof20260914.csv")
            self.assertIn("Kenya Maize season 1", desc)
            self.assertTrue((ctx.dir_plots / png).exists())
            self.assertTrue((ctx.dir_csvs / csv).exists())

    def test_no_admin_overlay_when_there_is_no_boundary(self):
        with TemporaryDirectory() as tmp:
            spy, _ = self._render(pm.season_state_map, STATE_GRID, _ctx(tmp))
            self.assertEqual(spy.only("plot"), [])

    def test_titles_and_labels_carry_no_quotes(self):
        with TemporaryDirectory() as tmp:
            spy, _ = self._render(pm.season_state_map, STATE_GRID, _ctx(tmp))
            frame = spy.only("basemap")[0]["frame"]
            self.assertEqual(
                frame[1],
                "+tKenya Maize Season State, Admin 1, data through 14 Sep 2026")
            for text in frame + spy.only("colorbar")[0]["frame"]:
                for bad in ('+t"', '+L"', '+l"', '"'):
                    self.assertNotIn(bad, str(text))

    def test_companion_csv_is_the_zonal_table_when_given(self):
        table = pd.DataFrame({"ADM1_NAME": ["Baringo"], "share_confirmed": [0.4]})
        with TemporaryDirectory() as tmp:
            ctx = _ctx(tmp)
            _, row = self._render(pm.season_state_map, STATE_GRID, ctx,
                                  table=table)
            written = pd.read_csv(ctx.dir_csvs / row[1])
            self.assertEqual(list(written.columns),
                             ["ADM1_NAME", "share_confirmed"])

    def test_companion_csv_is_a_pixel_summary_when_not(self):
        with TemporaryDirectory() as tmp:
            ctx = _ctx(tmp)
            _, row = self._render(
                pm.onset_anomaly_map,
                np.array([[-10.0, 0.0, 5.0], [np.nan, 20.0, 3.0]]), ctx)
            written = pd.read_csv(ctx.dir_csvs / row[1])
            self.assertEqual(list(written.columns),
                             ["statistic", "value", "units"])
            self.assertEqual(set(written["units"]), {"days"})

    def test_anomaly_palette_is_symmetric_and_late_is_warm(self):
        with TemporaryDirectory() as tmp:
            spy, _ = self._render(
                pm.onset_anomaly_map,
                np.array([[-10.0, 0.0, 5.0], [np.nan, 22.0, 3.0]]), _ctx(tmp))
            cpt = spy.only("makecpt")[0]
            # peak 22 -> ceil(22 / 5) * 5 = 25
            self.assertEqual(cpt["series"], [-25.0, 25.0])
            # GMT polar runs blue -> white -> red, so positive (late) is red
            self.assertEqual(cpt["cmap"], "polar")
            self.assertNotIn("reverse", cpt)

    def test_probability_bar_is_pinned_to_zero_one(self):
        with TemporaryDirectory() as tmp:
            spy, row = self._render(
                pm.p_onset_map, np.full((2, 3), 0.3), _ctx(tmp))
            self.assertEqual(spy.only("makecpt")[0]["series"], [0.0, 1.0])
            self.assertTrue(row[0].startswith("p_onset_28d_"))

    def test_rain_percentile_is_reversed_diverging_on_a_fixed_range(self):
        with TemporaryDirectory() as tmp:
            spy, row = self._render(
                pm.rain_percentile_map, np.full((2, 3), 40.0), _ctx(tmp))
            cpt = spy.only("makecpt")[0]
            self.assertEqual(cpt["series"], [0.0, 100.0])
            self.assertTrue(cpt["reverse"], "dry must be the warm end")
            self.assertTrue(row[0].startswith("rain_30d_percentile_"))

    def test_forecast_map_is_skipped_without_a_forecast(self):
        with TemporaryDirectory() as tmp:
            spy, row = self._render(pm.fcst_trigger_map, None, _ctx(tmp))
            self.assertIsNone(row)
            self.assertEqual(spy.names(), [])

    def test_forecast_map_is_skipped_when_nothing_triggers(self):
        with TemporaryDirectory() as tmp:
            spy, row = self._render(pm.fcst_trigger_map,
                                    np.full((2, 3), np.nan), _ctx(tmp))
            self.assertIsNone(row)
            self.assertEqual(spy.names(), [])

    def test_monitor_maps_render_the_whole_family_and_the_manifest(self):
        with TemporaryDirectory() as tmp:
            ctx = _ctx(tmp)
            spy, rows = self._render(
                pm.monitor_maps, ctx,
                state=STATE_GRID,
                onset_anomaly_days=np.full((2, 3), 4.0),
                days_past_median=np.full((2, 3), 12.0),
                p_onset=np.full((2, 3), 0.6),
                rain_percentile=np.full((2, 3), 30.0),
                fcst_trigger_days=np.full((2, 3), 3.0),
            )
            self.assertEqual(len(rows), 6)
            self.assertEqual(spy.names().count("Figure"), 6)
            stems = [r[0] for r in rows]
            self.assertEqual(
                [s.split("_kenya_")[0] for s in stems],
                ["season_state", "onset_anomaly_days", "days_past_median",
                 "p_onset_28d", "rain_30d_percentile", "fcst_trigger_days"])
            for png, csv, _ in rows:
                self.assertTrue((ctx.dir_plots / png).exists(), png)
                self.assertTrue((ctx.dir_csvs / csv).exists(), csv)
            manifest = pd.read_csv(ctx.dir_plots / "lookup_plots_csvs.csv")
            self.assertEqual(list(manifest.columns),
                             ["plot_file", "csv_file", "description"])
            self.assertEqual(len(manifest), 6)
            self.assertTrue((ctx.dir_csvs / "lookup_plots_csvs.csv").exists())

    def test_monitor_maps_skip_missing_layers(self):
        with TemporaryDirectory() as tmp:
            _, rows = self._render(pm.monitor_maps, _ctx(tmp), state=STATE_GRID)
            self.assertEqual(len(rows), 1)

    def test_climatology_set_and_the_date_labelled_bar(self):
        with TemporaryDirectory() as tmp:
            ctx = _ctx(tmp, asof=None, years=(1981, 2025))
            onset = np.array([[0.0, 15.0, 30.0], [45.0, np.nan, 60.0]])
            spy, rows = self._render(
                pm.climatology_maps, ctx,
                planting_reference=date(2026, 10, 15),
                onset_median=onset,
                onset_p75_minus_p25=np.full((2, 3), 8.0),
                eos_median=np.full((2, 3), 120.0),
                lgs_median=np.full((2, 3), 100.0),
                false_start_rate=np.full((2, 3), 0.4),
                onset_n_valid=np.full((2, 3), 41.0),
            )
            self.assertEqual(len(rows), 6)
            self.assertEqual(
                [r[0].split("_kenya_")[0] for r in rows],
                ["onset_median", "onset_p75_minus_p25", "eos_median",
                 "lgs_median", pm.FALSE_START_RATE_LAYER, "onset_n_valid"])
            self.assertTrue(rows[0][0].endswith("_1981_2025.png"))

            # only the onset map gets a custom-annotation colourbar
            bars = spy.only("colorbar")
            self.assertEqual(sum(b["annot_text"] is not None for b in bars), 1)
            # p2..p98 of 0,15,30,45,60 -> 1.5 and 58.5, rounded out to 0 and 60;
            # span 60 -> step 10 -> ticks 0,10,...,60 with 0 = 15 Oct
            self.assertTrue(bars[0]["frame"][0].startswith("xc"))
            lines = bars[0]["annot_text"].strip().splitlines()
            self.assertEqual(lines[0], "0 a 15 Oct")
            self.assertEqual(lines[-1], "60 a 14 Dec")
            self.assertTrue(all(" a " in ln for ln in lines))

    def test_climatology_manifest_covers_every_map(self):
        with TemporaryDirectory() as tmp:
            ctx = _ctx(tmp, asof=None, years=(1981, 2025))
            _, rows = self._render(
                pm.climatology_maps, ctx,
                planting_reference=date(2026, 10, 15),
                lgs_median=np.full((2, 3), 100.0))
            manifest = pd.read_csv(ctx.dir_csvs / "lookup_plots_csvs.csv")
            self.assertEqual(manifest["plot_file"].tolist(),
                             [r[0] for r in rows])


# ---------------------------------------------------------------------------
# source structure: the one shared skeleton
# ---------------------------------------------------------------------------
class TestSourceStructure(unittest.TestCase):
    def test_exactly_one_drawing_skeleton(self):
        """A second hand-rolled figure would pass every spy assertion above,
        so the single-skeleton property is pinned in the source itself (the
        technique tests/test_map_admin2_styling.py uses on the renderer)."""
        self.assertEqual(len(re.findall(r"^def raster_map\(", SOURCE, re.M)), 1)
        self.assertEqual(SOURCE.count("pygmt.Figure()"), 1)
        self.assertEqual(SOURCE.count("fig.grdimage("), 1)
        self.assertEqual(SOURCE.count("fig.basemap("), 1)
        self.assertEqual(SOURCE.count("fig.colorbar("), 1)
        self.assertEqual(SOURCE.count("fig.savefig("), 1)
        # one definition, one call site
        self.assertEqual(SOURCE.count("raster_map(")
                         - SOURCE.count("def raster_map("), 1)

    def test_every_family_goes_through_the_shared_renderer(self):
        calls = SOURCE.count("_render_layer(") - SOURCE.count("def _render_layer(")
        # 6 monitor layers (5 named + the forecast) + 6 climatology layers
        self.assertEqual(calls, 12)

    def test_pygmt_is_imported_inside_the_drawing_function_only(self):
        tree = ast.parse(SOURCE)
        in_function = {n for f in ast.walk(tree)
                       if isinstance(f, ast.FunctionDef) for n in ast.walk(f)}
        top_level = set()
        for node in ast.walk(tree):
            if node in in_function:
                continue
            if isinstance(node, ast.Import):
                top_level |= {a.name.split(".")[0] for a in node.names}
            elif isinstance(node, ast.ImportFrom) and node.module:
                top_level.add(node.module.split(".")[0])
        self.assertNotIn("pygmt", top_level)
        lazy = {a.name for f in ast.walk(tree)
                if isinstance(f, ast.FunctionDef)
                for n in ast.walk(f) if isinstance(n, ast.Import)
                for a in n.names}
        self.assertIn("pygmt", lazy)

    def test_style_constants_are_never_restated(self):
        code = "\n".join(ln for ln in SOURCE.splitlines()
                         if not ln.lstrip().startswith("#"))
        self.assertNotIn('"#d9d9d9"', code)
        self.assertNotIn("0.3p,gray60", code)
        self.assertNotIn("JBC+w12c", code)
        for name in ("NODATA", "COAST_KW", "POLY_PEN", "BORDER_PEN", "CBAR_POS"):
            self.assertIs(getattr(pm, name), getattr(_style, name))

    def test_no_shell_quotes_in_gmt_arguments(self):
        """Quotes inside a GMT modifier render literally on the canvas."""
        for bad in ('+t"', '+L"', '+l"'):
            self.assertNotIn(bad, SOURCE)

    def test_no_icclim_dependency(self):
        self.assertNotIn("icclim", SOURCE)


# ---------------------------------------------------------------------------
# end to end through the real GMT
# ---------------------------------------------------------------------------
@unittest.skipIf(not _gmt_loadable(), "GMT not loadable in-process")
class TestEndToEnd(unittest.TestCase):
    """Renders through the real library: the categorical path and the
    date-labelled continuous path, which exercise both CPT flavours."""

    @staticmethod
    def _real_ctx(tmp, **overrides):
        # 40 x 40 pixels of the 0.05 degree lattice over central Kenya
        lon = 36.0 + 0.025 + 0.05 * np.arange(40)
        lat = 0.5 - 0.025 - 0.05 * np.arange(40)
        return _ctx(tmp, lon=lon, lat=lat, **overrides)

    def test_categorical_state_map_renders(self):
        with TemporaryDirectory() as tmp:
            ctx = self._real_ctx(tmp)
            rng = np.random.default_rng(0)
            state = rng.integers(0, 6, size=(40, 40)).astype(np.int8)
            state[rng.random((40, 40)) > 0.6] = -1      # non-cropland
            png, csv, _ = pm.season_state_map(state, ctx)
            out = ctx.dir_plots / png
            self.assertTrue(out.exists())
            self.assertGreater(out.stat().st_size, 20_000)
            self.assertTrue((ctx.dir_csvs / csv).exists())

    def test_date_labelled_climatology_map_renders(self):
        with TemporaryDirectory() as tmp:
            ctx = self._real_ctx(tmp, asof=None, years=(1981, 2025))
            rng = np.random.default_rng(1)
            onset = rng.normal(20.0, 15.0, size=(40, 40)).astype(np.float32)
            onset[rng.random((40, 40)) > 0.6] = np.nan
            rows = pm.climatology_maps(ctx, planting_reference=date(2026, 10, 15),
                                       onset_median=onset)
            self.assertEqual(len(rows), 1)
            out = ctx.dir_plots / rows[0][0]
            self.assertTrue(out.exists())
            self.assertGreater(out.stat().st_size, 20_000)


if __name__ == "__main__":
    unittest.main()
