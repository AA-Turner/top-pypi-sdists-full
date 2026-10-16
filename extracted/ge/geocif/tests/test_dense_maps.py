"""Dense (county / municipality scale) maps and fixed predicted-yield classes.

User request 2026-10-15, from the Brazil soybean municipality maps: a colour
scale from 0 shared by every year, impossible negative predictions left
blank, and at ~2,500 units hairline outlines with state lines from the
admin-1 file instead of a black mesh.
"""
import configparser
import os
import sys
import types
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
import pytest
from shapely.geometry import box

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from geocif.viz import plot  # noqa: E402


@pytest.fixture
def seq_cmap():
    from palettable.scientific.sequential import Bamako_20_r
    return Bamako_20_r


@pytest.fixture(autouse=True)
def _no_admin1():
    plot.set_admin1_boundaries(None)
    yield
    plot.set_admin1_boundaries(None)


# ------------------------------------------------------------- class edges


def test_class_edges_span_vmin_to_vmax():
    assert plot.class_edges(0.0, 5.0, 0.5) == [i * 0.5 for i in range(11)]


def test_class_edges_snap_vmax_up_to_the_step():
    assert plot.class_edges(0.0, 4.3, 0.5)[-1] == 4.5


def test_class_norm_gives_one_colour_per_class(seq_cmap):
    attr = gpd.GeoDataFrame({"k": list("abcd")},
                            geometry=[box(i, 0, i + 1, 1) for i in range(4)])
    df = pd.DataFrame({"k": list("abcd"), "v": [0.2, 0.4, 4.9, 7.0]})
    _, norm, breaks = plot._compute_norm(
        df, attr, "k", "v", "sequential", 0.0, 5.0, "region", True,
        seq_cmap, fixed_range=True, class_step=0.5)
    assert breaks[0] == 0.0 and breaks[-1] == 5.0
    assert norm(0.2) == norm(0.4)          # same class
    assert norm(4.9) == norm(7.0)          # above vmax -> top class
    assert norm(0.2) != norm(4.9)


# ------------------------------------------------- predicted-yield scale


def test_scale_starts_at_zero_and_rounds_up_to_a_class_edge():
    from geocif.yield_outlook import _predicted_yield_scale
    vmax, step = _predicted_yield_scale([1.0, 2.0, 3.0, 4.0, 4.4])
    assert (vmax, step) == (4.5, 0.5)


def test_scale_ignores_negative_predictions():
    from geocif.yield_outlook import _predicted_yield_scale
    assert _predicted_yield_scale([-3.0, 1.0, 2.0, 4.4]) == (4.5, 0.5)


def test_scale_is_not_stretched_by_a_few_outliers():
    from geocif.yield_outlook import _predicted_yield_scale
    vals = np.r_[np.linspace(1.5, 4.5, 2000), [8.4, 8.0]]
    vmax, _ = _predicted_yield_scale(vals)
    assert vmax <= 5.0


def test_scale_in_bushels_per_acre():
    from geocif.yield_outlook import _predicted_yield_scale
    assert _predicted_yield_scale([150, 180, 200, 240]) == (250.0, 25)


def test_scale_with_nothing_positive():
    from geocif.yield_outlook import _predicted_yield_scale
    assert _predicted_yield_scale([-1.0, np.nan]) == (None, None)
    assert _predicted_yield_scale([]) == (None, None)


# ------------------------------------------------- _plot_map_pygmt params


def _grid(n, x0=0.0):
    side = int(np.ceil(np.sqrt(n)))
    return [box(x0 + (i % side) * 0.1, (i // side) * 0.1,
                x0 + (i % side) * 0.1 + 0.1, (i // side) * 0.1 + 0.1)
            for i in range(n)]


def _capture_render(monkeypatch):
    seen = {}
    mod = types.ModuleType("geocif.viz._pygmt_render")

    def render(gj, params):
        seen["params"] = params
        seen["files"] = {k: os.path.exists(params[k])
                         for k in ("admin1_lines", "national_lines") if k in params}
        seen["n"] = len(gpd.read_file(gj))

    mod.render = render
    monkeypatch.setitem(sys.modules, "geocif.viz._pygmt_render", mod)
    import geocif.viz as viz_pkg
    monkeypatch.setattr(viz_pkg, "_pygmt_render", mod, raising=False)
    monkeypatch.setattr(plot, "_gmt_available", lambda: True)
    return seen


def _inputs(tmp_path, cmap, n, values=None, **kw):
    attr = gpd.GeoDataFrame(
        {"k": [f"r{i}" for i in range(n)], "ADM0_NAME": "Brazil"},
        geometry=_grid(n), crs="EPSG:4326")
    vals = values if values is not None else np.linspace(1, 4, n)
    df = pd.DataFrame({"k": [f"r{i}" for i in range(n)], "v": vals})
    args = dict(
        attribute_df=attr, df=df, dict_lup=None, merge_col="k",
        name_country=["Brazil"], name_col="v",
        dir_out=str(tmp_path / "maps"), fname="m.png", title="", label="l",
        vmin=0.0, vmax=5.0, cmap=cmap, series="sequential", do_borders=True,
        annotate_regions=False, annotate_region_column="ADM1_NAME",
        continuous_colorbar=True, classify_by="region", fixed_range=True,
        use_key=False,
    )
    args.update(kw)
    return args


def test_state_scale_map_is_not_dense(monkeypatch, tmp_path, seq_cmap):
    seen = _capture_render(monkeypatch)
    plot._plot_map_pygmt(**_inputs(tmp_path, seq_cmap, 27))
    p = seen["params"]
    assert p["dense"] is False and p["admin1_borders"] is False
    assert "admin1_lines" not in p


def test_dense_map_without_admin1_file_falls_back_to_gmt(monkeypatch, tmp_path, seq_cmap):
    seen = _capture_render(monkeypatch)
    plot._plot_map_pygmt(**_inputs(tmp_path, seq_cmap, 300))
    p = seen["params"]
    assert p["dense"] is True and p["admin1_borders"] is True
    assert "admin1_lines" not in p


def test_dense_map_draws_registered_state_lines(monkeypatch, tmp_path, seq_cmap):
    plot.set_admin1_boundaries(gpd.GeoDataFrame(
        {"ADM0_NAME": ["Brazil", "Brazil", "Argentina"],
         "ADM1_NAME": ["a", "b", "c"]},
        geometry=[box(0, 0, 1, 2), box(1, 0, 2, 2), box(5, 5, 6, 6)],
        crs="EPSG:4326"))
    seen = _capture_render(monkeypatch)
    plot._plot_map_pygmt(**_inputs(tmp_path, seq_cmap, 300))
    assert seen["files"] == {"admin1_lines": True, "national_lines": True}


def test_admin1_lines_only_for_the_mapped_country():
    plot.set_admin1_boundaries(gpd.GeoDataFrame(
        {"ADM0_NAME": ["Brazil", "Brazil", "Argentina"],
         "ADM1_NAME": ["a", "b", "c"]},
        geometry=[box(0, 0, 1, 2), box(1, 0, 2, 2), box(5, 5, 6, 6)],
        crs="EPSG:4326"))
    states, national = plot._admin1_line_frames(["Brazil"])
    assert len(states) == 2 and len(national) == 1
    assert states.total_bounds[2] <= 2.0          # Argentina's state dropped
    assert plot._admin1_line_frames(["Kenya"]) == (None, None)


def test_dense_count_includes_units_without_a_value(monkeypatch, tmp_path, seq_cmap):
    """A municipality map stays dense in a year when many units are blank."""
    seen = _capture_render(monkeypatch)
    vals = np.r_[np.linspace(1, 4, 150), [np.nan] * 150]
    plot._plot_map_pygmt(**_inputs(tmp_path, seq_cmap, 300, values=vals))
    assert seen["params"]["dense"] is True
    assert seen["n"] == 150                       # blank units are not drawn


def test_class_colorbar_params(monkeypatch, tmp_path, seq_cmap):
    seen = _capture_render(monkeypatch)
    plot._plot_map_pygmt(**_inputs(tmp_path, seq_cmap, 27, class_step=0.5,
                                   extend="max"))
    cb = seen["params"]["colorbar"]
    assert cb["type"] == "classes" and cb["extend"] == "max"
    assert cb["edges"] == [i * 0.5 for i in range(11)]
    assert len(cb["colors"]) == 10 and len(set(cb["colors"])) == 10


# ------------------------------------------------- admin-1 from the config


def _parser(tmp_path, countries, levels):
    cp = configparser.ConfigParser()
    cp["DEFAULT"] = {"countries": str(countries)}
    cp["PATHS"] = {"dir_boundary_files": str(tmp_path)}
    cp["ML"] = {}
    for c, lvl in levels.items():
        cp[c] = {"admin_level": lvl}
    return cp


@pytest.fixture
def plain_boundary_reader(monkeypatch):
    """Real configs carry a boundary column-mapping section; this test config
    does not, so read the file as is (columns are already ADM0/ADM1_NAME)."""
    import geocif.utils as ut
    monkeypatch.setattr(ut, "load_country_boundary_gdf",
                        lambda parser, path, **kw: gpd.read_file(path))


def _level1(tmp_path):
    gpd.GeoDataFrame(
        {"ADM0_NAME": ["Brazil", "Brazil", "Kenya"],
         "ADM1_NAME": ["Goias", "Parana", "Nakuru"]},
        geometry=[box(0, 0, 1, 1), box(1, 0, 2, 1), box(5, 5, 6, 6)],
        crs="EPSG:4326").to_file(tmp_path / "Level_1.shp")


def test_admin1_boundaries_for_admin2_countries_only(tmp_path, plain_boundary_reader):
    from geocif.yield_outlook import _admin1_boundaries
    _level1(tmp_path)
    out = _admin1_boundaries(_parser(
        tmp_path, ["brazil", "kenya"], {"brazil": "admin_2", "kenya": "admin_1"}))
    assert sorted(out["ADM1_NAME"]) == ["Goias", "Parana"]
    assert set(out["ADM0_NAME"]) == {"Brazil"}


def test_admin1_boundaries_none_when_country_missing(tmp_path, plain_boundary_reader):
    from geocif.yield_outlook import _admin1_boundaries
    _level1(tmp_path)
    assert _admin1_boundaries(_parser(
        tmp_path, ["malawi"], {"malawi": "admin_2"})) is None
