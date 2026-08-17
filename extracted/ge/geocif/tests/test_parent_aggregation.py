"""Tests for parent-level (admin_1 / national) performance aggregation.

geocif/viz/aggregation.py aggregates the yield_outlook predictions frame to
every admin level ABOVE the run level (admin_2 -> admin_1 + national;
admin_1 -> national), producing pooled scatters, per-parent metrics CSVs, a
national time series, per-parent rRMSE%/r² choropleths, and a
plot->CSV lookup table per level directory. County -> state mapping reuses
ml.stats.admin1_lookup (same stats file + normalization as the yield join).

Synthetic fixture: 2 states (Iowa, Missouri) x 2 counties each, 2 years,
with hand-computed area-weighted expectations.
"""
import configparser
import logging

import matplotlib

matplotlib.use("Agg")  # headless: the render tests write real PNGs

import numpy as np
import pandas as pd
import pytest

from geocif.viz import aggregation as agg
from geocif.viz.aggregation import (
    OBS_COL,
    PRED_COL,
    POOLED_LABEL,
    UNKNOWN_PARENT,
    aggregate_predictions,
    build_level_map,
    compute_metrics,
    parent_levels_for,
    render_parent_aggregations,
)

STATS_FN = "parent_agg_stats.csv"

# Same shape as the HvStat production-statistics file admin1_lookup reads:
# admin_2 values are the composite state_county tokens the usa_admin2 project
# uses, admin_1 is the parent state.
_STATS_CSV = """country,product,admin_1,admin_2,harvest_year,yield,area,production,qc_flag,crop_production_system,season_name
United States Of America,Maize,Iowa,iowa_adair,2019,10.0,100,1000,0,none,Main
United States Of America,Maize,Iowa,iowa_boone,2019,12.0,300,3600,0,none,Main
United States Of America,Maize,Missouri,missouri_adair,2019,8.0,200,1600,0,none,Main
United States Of America,Maize,Missouri,missouri_clark,2019,6.0,200,1200,0,none,Main
"""

COUNTRY = "united_states_of_america"
CROP = "maize"
MODEL = "catboost"


def _parser(tmp_path):
    p = configparser.ConfigParser()
    p["DEFAULT"]["production_statistics_file"] = STATS_FN
    p.add_section("PATHS")
    p["PATHS"]["dir_production_statistics"] = str(tmp_path)
    # Boundary dir exists but holds no Level_1.shp -> maps must be skipped.
    p["PATHS"]["dir_boundary_files"] = str(tmp_path / "boundaries")
    (tmp_path / STATS_FN).write_text(_STATS_CSV)
    return p


def _pred_frame(with_area=True):
    """4 counties x 2 years. Iowa Boone 2020 has NO observed yield (its
    prediction must still enter the parent aggregate)."""
    rows = [
        # Region,            year, obs,    pred, area
        ("Iowa Adair",       2019, 10.0,   11.0, 100.0),
        ("Iowa Boone",       2019, 12.0,   11.0, 300.0),
        ("Missouri Adair",   2019,  8.0,    7.0, 200.0),
        ("Missouri Clark",   2019,  6.0,    7.5, 200.0),
        ("Iowa Adair",       2020,  9.0,   10.0, 100.0),
        ("Iowa Boone",       2020, np.nan, 12.0, 300.0),
        ("Missouri Adair",   2020,  7.0,    7.2, 200.0),
        ("Missouri Clark",   2020,  5.0,    5.5, 200.0),
    ]
    df = pd.DataFrame(
        rows, columns=["Region", "Harvest Year", OBS_COL, PRED_COL, "Area (ha)"]
    )
    df["Stage Name"] = "Mar 1-Mar 31"
    df["Country"] = COUNTRY
    if not with_area:
        df = df.drop(columns=["Area (ha)"])
    return df


LEVEL_MAP_ADMIN1 = {
    "iowa adair": "Iowa",
    "iowa boone": "Iowa",
    "missouri adair": "Missouri",
    "missouri clark": "Missouri",
}


def _row(df, region, year):
    sub = df[(df["Region"] == region) & (df["Harvest Year"] == year)]
    assert len(sub) == 1, f"expected exactly one row for {region} {year}"
    return sub.iloc[0]


# ---------------------------------------------------------------------------
# Level routing
# ---------------------------------------------------------------------------

def test_level_routing():
    assert parent_levels_for("admin_2") == ["admin_1", "national"]
    assert parent_levels_for("admin_1") == ["national"]
    assert parent_levels_for("national") == []
    assert parent_levels_for("ADMIN_2") == ["admin_1", "national"]  # case-safe
    assert parent_levels_for("something_else") == []


# ---------------------------------------------------------------------------
# Level map (reuses stats.admin1_lookup + _norm_region_series)
# ---------------------------------------------------------------------------

def test_build_level_map_admin1_and_national(tmp_path):
    parser = _parser(tmp_path)
    regions = ["Iowa Adair", "Iowa Boone", "Missouri Adair", "Texas Nowhere"]
    m1 = build_level_map(regions, "admin_1", COUNTRY, parser)
    assert m1["iowa adair"] == "Iowa"
    assert m1["iowa boone"] == "Iowa"
    assert m1["missouri adair"] == "Missouri"
    assert m1["texas nowhere"] == UNKNOWN_PARENT  # unmapped -> 'unknown'

    mn = build_level_map(regions, "national", COUNTRY, parser)
    assert set(mn.values()) == {"United States Of America"}
    assert set(mn.keys()) == {r.lower() for r in regions}


# ---------------------------------------------------------------------------
# Weighted aggregation math (hand-computed)
# ---------------------------------------------------------------------------

def test_aggregate_weighted_math_admin1():
    out = aggregate_predictions(_pred_frame(), LEVEL_MAP_ADMIN1)

    ia19 = _row(out, "Iowa", 2019)
    # obs = (10*100 + 12*300)/400 = 11.5 ; pred = (11*100 + 11*300)/400 = 11.0
    assert ia19[OBS_COL] == pytest.approx(11.5)
    assert ia19[PRED_COL] == pytest.approx(11.0)
    assert ia19["Area (ha)"] == pytest.approx(400.0)
    assert ia19["N Units"] == 2
    assert ia19["Aggregation"] == "area-weighted"
    assert not ia19["Unmapped Parent"]

    mo19 = _row(out, "Missouri", 2019)
    # obs = (8*200 + 6*200)/400 = 7.0 ; pred = (7*200 + 7.5*200)/400 = 7.25
    assert mo19[OBS_COL] == pytest.approx(7.0)
    assert mo19[PRED_COL] == pytest.approx(7.25)

    mo20 = _row(out, "Missouri", 2020)
    # obs = (7*200 + 5*200)/400 = 6.0 ; pred = (7.2*200 + 5.5*200)/400 = 6.35
    assert mo20[OBS_COL] == pytest.approx(6.0)
    assert mo20[PRED_COL] == pytest.approx(6.35)


def test_aggregate_obs_nan_rows_still_contribute_predictions():
    out = aggregate_predictions(_pred_frame(), LEVEL_MAP_ADMIN1)
    ia20 = _row(out, "Iowa", 2020)
    # Predictions aggregate over ALL counties with predictions:
    # pred = (10*100 + 12*300)/400 = 11.5
    assert ia20[PRED_COL] == pytest.approx(11.5)
    assert ia20["N Units"] == 2
    # Observed aggregates only over counties WITH an observation
    # (Iowa Boone 2020 obs is NaN): obs = 9*100/100 = 9.0
    assert ia20[OBS_COL] == pytest.approx(9.0)


def test_aggregate_weighted_math_national():
    level_map = {k: "United States Of America" for k in LEVEL_MAP_ADMIN1}
    out = aggregate_predictions(_pred_frame(), level_map)
    us19 = _row(out, "United States Of America", 2019)
    # obs = (10*100+12*300+8*200+6*200)/800 = 7400/800 = 9.25
    # pred = (11*100+11*300+7*200+7.5*200)/800 = 7300/800 = 9.125
    assert us19[OBS_COL] == pytest.approx(9.25)
    assert us19[PRED_COL] == pytest.approx(9.125)

    us20 = _row(out, "United States Of America", 2020)
    # pred over all 4 counties = (10*100+12*300+7.2*200+5.5*200)/800 = 8.925
    # obs over the 3 counties with obs = (9*100+7*200+5*200)/500 = 6.6
    assert us20[PRED_COL] == pytest.approx(8.925)
    assert us20[OBS_COL] == pytest.approx(6.6)
    assert us20["N Units"] == 4


def test_unweighted_fallback_when_area_missing(caplog):
    with caplog.at_level(logging.WARNING, logger="geocif.viz.aggregation"):
        out = aggregate_predictions(_pred_frame(with_area=False), LEVEL_MAP_ADMIN1)
    ia19 = _row(out, "Iowa", 2019)
    assert ia19[OBS_COL] == pytest.approx(11.0)   # mean(10, 12)
    assert ia19[PRED_COL] == pytest.approx(11.0)  # mean(11, 11)
    assert ia19["Aggregation"] == "unweighted"
    assert np.isnan(ia19["Area (ha)"])
    # Logged once per call, not once per group.
    fallback_msgs = [r for r in caplog.records if "unweighted means" in r.message]
    assert len(fallback_msgs) == 1


def test_unweighted_fallback_when_weight_zero_or_nan():
    df = _pred_frame()
    df.loc[
        (df["Region"] == "Iowa Boone") & (df["Harvest Year"] == 2019),
        "Area (ha)",
    ] = 0.0
    out = aggregate_predictions(df, LEVEL_MAP_ADMIN1)
    ia19 = _row(out, "Iowa", 2019)
    # Zero weight in the group -> the whole group falls back to unweighted.
    assert ia19[OBS_COL] == pytest.approx(11.0)
    assert ia19["Aggregation"] == "unweighted"
    # Other groups keep valid weights and stay area-weighted.
    assert _row(out, "Missouri", 2019)["Aggregation"] == "area-weighted"


def test_unknown_parent_kept_and_flagged():
    df = _pred_frame()
    df.loc[len(df)] = ["Texas Nowhere", 2019, 4.0, 5.0, 50.0,
                       "Mar 1-Mar 31", COUNTRY]
    out = aggregate_predictions(df, LEVEL_MAP_ADMIN1)
    unk = _row(out, UNKNOWN_PARENT, 2019)
    assert unk["Unmapped Parent"]
    assert unk[OBS_COL] == pytest.approx(4.0)
    assert unk[PRED_COL] == pytest.approx(5.0)
    # Metrics CSV keeps + flags it too.
    metrics = compute_metrics(out)
    unk_metric = metrics[metrics["Region"] == UNKNOWN_PARENT]
    assert len(unk_metric) == 1
    assert bool(unk_metric.iloc[0]["Unmapped Parent"])


# ---------------------------------------------------------------------------
# Metrics: r2 = 1 - SSE/SST, rRMSE%, MAPE% (hand-computed)
# ---------------------------------------------------------------------------

def _metrics_frame():
    return pd.DataFrame({
        "Region": ["Iowa", "Iowa", "Missouri", "Missouri"],
        "Harvest Year": [2019, 2020, 2019, 2020],
        OBS_COL: [10.0, 12.0, 8.0, 6.0],
        PRED_COL: [11.0, 11.0, 7.0, 7.0],
        "Unmapped Parent": [False] * 4,
    })


def test_metrics_values():
    m = compute_metrics(_metrics_frame())
    iowa = m[m["Region"] == "Iowa"].iloc[0]
    # err = [+1, -1]: RMSE = 1, mean obs = 11 -> rRMSE = 100/11
    # MAPE = mean(1/10, 1/12)*100 ; SSE = 2 = SST -> r2 = 0
    assert iowa["N"] == 2
    assert iowa["rRMSE (%)"] == pytest.approx(100.0 / 11.0)
    assert iowa["MAPE (%)"] == pytest.approx((0.1 + 1.0 / 12.0) / 2 * 100)
    assert iowa["r2"] == pytest.approx(0.0)

    mo = m[m["Region"] == "Missouri"].iloc[0]
    assert mo["rRMSE (%)"] == pytest.approx(100.0 / 7.0)
    assert mo["MAPE (%)"] == pytest.approx((1.0 / 8.0 + 1.0 / 6.0) / 2 * 100)
    assert mo["r2"] == pytest.approx(0.0)

    pooled = m[m["Region"] == POOLED_LABEL].iloc[0]
    assert bool(pooled["Is Pooled"])
    assert pooled["N"] == 4
    # SSE = 4, mean obs = 9, SST = 1+9+1+9 = 20 -> r2 = 0.8; RMSE = 1
    assert pooled["r2"] == pytest.approx(0.8)
    assert pooled["rRMSE (%)"] == pytest.approx(100.0 / 9.0)
    assert pooled["MAPE (%)"] == pytest.approx(
        (0.1 + 1.0 / 12.0 + 1.0 / 8.0 + 1.0 / 6.0) / 4 * 100
    )


def test_metrics_exclude_observed_nan_rows():
    df = _metrics_frame()
    df.loc[len(df)] = ["Iowa", 2021, np.nan, 13.0, False]
    m = compute_metrics(df)
    assert m[m["Region"] == "Iowa"].iloc[0]["N"] == 2  # NaN-obs row not scored


def test_metrics_single_year_r2_nan():
    df = _metrics_frame().iloc[[0]]
    m = compute_metrics(df)
    assert np.isnan(m[m["Region"] == "Iowa"].iloc[0]["r2"])


# ---------------------------------------------------------------------------
# End-to-end render: files written into the expected tree, maps skipped
# when the boundary is missing
# ---------------------------------------------------------------------------

def _render(tmp_path, monkeypatch, admin_zone="admin_2", parser=None):
    """Run render_parent_aggregations with metric_choropleth recorded (never
    actually rendering a map — pygmt may be unavailable locally)."""
    from geocif.viz import diagnostics as diag

    calls = []
    monkeypatch.setattr(
        diag, "metric_choropleth",
        lambda *a, **k: calls.append((a, k)),
    )
    dir_outlook = tmp_path / "outlook"
    render_parent_aggregations(
        _pred_frame(), COUNTRY, CROP, MODEL, dir_outlook,
        parser if parser is not None else _parser(tmp_path),
        admin_zone=admin_zone, yield_units="Mg/ha",
    )
    return dir_outlook, calls


def test_files_written_admin2_run(tmp_path, monkeypatch, caplog):
    with caplog.at_level(logging.WARNING, logger="geocif.viz.aggregation"):
        dir_outlook, map_calls = _render(tmp_path, monkeypatch)

    base_plots = dir_outlook / "plots" / MODEL / COUNTRY / CROP
    base_csvs = dir_outlook / "csvs" / MODEL / COUNTRY / CROP

    for level in ("admin_1", "national"):
        stem = f"{level}_{COUNTRY}_{CROP}_{MODEL}"
        assert (base_plots / level / f"scatter_{stem}.png").is_file()
        assert (base_plots / level / f"scatter_{stem}_hexbin.png").is_file()
        assert (base_csvs / level / f"scatter_{stem}.csv").is_file()
        assert (base_csvs / level / f"metrics_{stem}.csv").is_file()
        assert (base_csvs / level / f"aggregated_predictions_{stem}.csv").is_file()
        # Lookup table in BOTH level dirs
        for d in (base_plots / level, base_csvs / level):
            lookup = pd.read_csv(d / "lookup_plots_csvs.csv")
            assert list(lookup.columns) == ["plot_file", "csv_file", "description"]
            assert f"scatter_{stem}.png" in set(lookup["plot_file"])

    # National extras: yearly time series plot + companion CSV
    nat_stem = f"national_{COUNTRY}_{CROP}_{MODEL}"
    assert (base_plots / "national" / f"timeseries_{nat_stem}.png").is_file()
    assert (base_csvs / "national" / f"timeseries_{nat_stem}.csv").is_file()
    nat_lookup = pd.read_csv(base_plots / "national" / "lookup_plots_csvs.csv")
    ts_rows = nat_lookup[nat_lookup["plot_file"] == f"timeseries_{nat_stem}.png"]
    assert len(ts_rows) == 1
    assert ts_rows.iloc[0]["csv_file"] == f"timeseries_{nat_stem}.csv"

    # Boundary shapefile missing -> maps skipped with a warning, no crash.
    assert map_calls == []
    assert any("maps skipped" in r.message for r in caplog.records)

    # Metrics CSV content sanity: pooled row present, hand-checked value.
    m = pd.read_csv(base_csvs / "admin_1" / f"metrics_admin_1_{COUNTRY}_{CROP}_{MODEL}.csv")
    assert POOLED_LABEL in set(m["Region"])
    ia = m[m["Region"] == "Iowa"].iloc[0]
    # Iowa scored years: 2019 (obs 11.5 / pred 11.0), 2020 (obs 9.0 / pred 11.5)
    err = np.array([11.0 - 11.5, 11.5 - 9.0])
    rmse = float(np.sqrt(np.mean(err ** 2)))
    assert ia["rRMSE (%)"] == pytest.approx(100.0 * rmse / np.mean([11.5, 9.0]))


def test_admin1_run_gets_national_only(tmp_path, monkeypatch):
    dir_outlook, _ = _render(tmp_path, monkeypatch, admin_zone="admin_1")
    base_plots = dir_outlook / "plots" / MODEL / COUNTRY / CROP
    assert (base_plots / "national").is_dir()
    assert not (base_plots / "admin_1").exists()


def test_no_outputs_when_admin1_mapping_empty(tmp_path, monkeypatch, caplog):
    # Stats file absent -> admin1_lookup returns {} -> every parent would be
    # 'unknown' -> the admin_1 level is skipped entirely (national still runs).
    parser = configparser.ConfigParser()
    parser["DEFAULT"]["production_statistics_file"] = "absent.csv"
    parser.add_section("PATHS")
    parser["PATHS"]["dir_production_statistics"] = str(tmp_path)
    parser["PATHS"]["dir_boundary_files"] = str(tmp_path / "boundaries")

    with caplog.at_level(logging.WARNING, logger="geocif.viz.aggregation"):
        dir_outlook, _ = _render(tmp_path, monkeypatch, parser=parser)
    base_plots = dir_outlook / "plots" / MODEL / COUNTRY / CROP
    assert not (base_plots / "admin_1").exists()
    assert (base_plots / "national").is_dir()
    assert any("no admin_2->admin_1 mapping" in r.message for r in caplog.records)


# ---------------------------------------------------------------------------
# Map invocation + skip logic (plot_map itself is never exercised)
# ---------------------------------------------------------------------------

def test_maps_invoked_with_matching_boundary(tmp_path, monkeypatch):
    from geocif.viz import diagnostics as diag

    fake_boundary = pd.DataFrame({"ADM1_NAME": ["Iowa", "Missouri"]})
    monkeypatch.setattr(
        agg, "_load_parent_boundary", lambda parser, country: (fake_boundary, None)
    )
    calls = []
    monkeypatch.setattr(
        diag, "metric_choropleth",
        lambda dg, df, countries, annot, dir_out, fname, **kw:
            calls.append({"dg": dg, "df": df, "fname": fname, **kw}),
    )

    dir_outlook = tmp_path / "outlook"
    render_parent_aggregations(
        _pred_frame(), COUNTRY, CROP, MODEL, dir_outlook, _parser(tmp_path),
        admin_zone="admin_2",
    )

    assert len(calls) == 2  # one rRMSE% map + one r² map
    cols = {c["col"] for c in calls}
    assert cols == {"rRMSE (%)", "r2"}
    for c in calls:
        # Merge key built with the shared normalization on both sides.
        assert "Country Region" in c["df"].columns
        assert "united states of america iowa" in set(c["df"]["Country Region"])
        assert "Country Region" in c["dg"].columns
        # Pooled + unknown rows never reach the map.
        assert POOLED_LABEL not in set(c["df"]["Region"])
        assert UNKNOWN_PARENT not in set(c["df"]["Region"])

    # Both map plots recorded in the lookup, pointing at the metrics CSV.
    lookup = pd.read_csv(
        dir_outlook / "plots" / MODEL / COUNTRY / CROP / "admin_1"
        / "lookup_plots_csvs.csv"
    )
    stem = f"admin_1_{COUNTRY}_{CROP}_{MODEL}"
    by_plot = dict(zip(lookup["plot_file"], lookup["csv_file"]))
    assert by_plot.get(f"rrmse_map_{stem}.png") == f"metrics_{stem}.csv"
    assert by_plot.get(f"r2_map_{stem}.png") == f"metrics_{stem}.csv"


def test_maps_skipped_when_names_do_not_match(tmp_path, monkeypatch, caplog):
    from geocif.viz import diagnostics as diag

    fake_boundary = pd.DataFrame({"ADM1_NAME": ["Aaa", "Bbb"]})
    monkeypatch.setattr(
        agg, "_load_parent_boundary", lambda parser, country: (fake_boundary, None)
    )
    calls = []
    monkeypatch.setattr(diag, "metric_choropleth", lambda *a, **k: calls.append(1))

    with caplog.at_level(logging.WARNING, logger="geocif.viz.aggregation"):
        render_parent_aggregations(
            _pred_frame(), COUNTRY, CROP, MODEL, tmp_path / "outlook",
            _parser(tmp_path), admin_zone="admin_2",
        )
    assert calls == []
    assert any(
        "parent names match" in r.message and "skipped" in r.message
        for r in caplog.records
    )


# ---------------------------------------------------------------------------
# Multi-stage frames: one row per (Region, Harvest Year), latest stage
# (same rule as yield_outlook's native MAPE diagnostics)
# ---------------------------------------------------------------------------

def test_multi_stage_frame_not_double_counted(tmp_path, monkeypatch):
    df = _pred_frame()
    early = df.copy()
    early["Stage Name"] = "Feb 1-Feb 28"
    early[PRED_COL] = 99.0  # would wreck the aggregate if double-counted
    stacked = pd.concat([early, df], ignore_index=True)

    from geocif.viz import diagnostics as diag
    monkeypatch.setattr(diag, "metric_choropleth", lambda *a, **k: None)

    dir_outlook = tmp_path / "outlook"
    render_parent_aggregations(
        stacked, COUNTRY, CROP, MODEL, dir_outlook, _parser(tmp_path),
        admin_zone="admin_2",
    )
    stem = f"admin_1_{COUNTRY}_{CROP}_{MODEL}"
    out = pd.read_csv(
        dir_outlook / "csvs" / MODEL / COUNTRY / CROP / "admin_1"
        / f"aggregated_predictions_{stem}.csv"
    )
    ia19 = out[(out["Region"] == "Iowa") & (out["Harvest Year"] == 2019)]
    assert len(ia19) == 1
    # "Mar 1-Mar 31" sorts after "Feb 1-Feb 28" -> latest-stage rows win.
    assert ia19.iloc[0][PRED_COL] == pytest.approx(11.0)


# ---------------------------------------------------------------------------
# Call-site wiring in yield_outlook (structural)
# ---------------------------------------------------------------------------

def test_yield_outlook_call_site_wiring():
    import sys
    import types

    # yield_outlook -> viz.plot lazily imports pygeoutil in cartopy-path
    # helpers only, but stub it defensively like test_outlook_metric_maps.
    try:  # pragma: no cover - environment dependent
        import pygeoutil  # noqa: F401
    except ModuleNotFoundError:  # pragma: no cover
        _pg = types.ModuleType("pygeoutil")
        _rgeo = types.ModuleType("pygeoutil.rgeo")
        _rgeo.get_country_lat_lon_extent = lambda *a, **k: [-180, 180, -90, 90]
        _pg.rgeo = _rgeo
        sys.modules["pygeoutil"] = _pg
        sys.modules["pygeoutil.rgeo"] = _rgeo

    import inspect
    from geocif import yield_outlook

    src = inspect.getsource(yield_outlook._generate_diagnostics)
    # Config gate with fallback True + the render call + never-fail wrapper.
    assert "plot_parent_aggregations" in src
    assert 'fallback=True' in src
    assert "render_parent_aggregations(" in src
    assert "admin_zone=admin_level" in src
    # Wrapped so it can never fail the diagnostics stage.
    gate_idx = src.index("render_parent_aggregations(")
    assert "try:" in src[:gate_idx]
    assert "except Exception" in src[gate_idx:]
