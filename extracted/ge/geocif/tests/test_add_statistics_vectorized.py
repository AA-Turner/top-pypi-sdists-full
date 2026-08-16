"""Equivalence tests for the vectorized add_statistics yield join.

The statistics-build phase used to loop process_group over every
(Region, Harvest Year[, Season]) combination (~53k groups at US county
scale), each doing boolean-mask scans over the full production-statistics
table. The vectorized rewrite pre-filters the stats table once, collapses
multi-production-system rows per (region, year[, season]) key with the
same area-weighted logic, and performs a single left merge (plus a second
merge for the Malawi-Maize "Annual" fallback).

``_add_statistics_reference`` below is a verbatim copy of the per-group
implementation that was replaced (geocif/ml/stats.py @ f96447f; only the
progress bar wrapper is removed — it has no semantic effect). Every test
runs BOTH implementations on the same fixture and asserts frame equality
(``assert_frame_equal(..., check_like=True)`` — the legacy path emitted
rows sorted by group key while the vectorized path preserves input order,
so frames are aligned on their shared index), then pins expected values.

Covered corners:
  (a) plain single-PS join
  (b) multi-PS area-weighted aggregation (+ non-whitelisted PS excluded)
  (c) season-resolver fallback to "Annual" when no primary name exists
  (d) Malawi Maize per-group "Annual" fallback
  (e) qc_flag exclusion
  (f) region present in df but absent in stats -> NaN
  (g) underscore/space/case normalization on both sides
  (h) zero matches -> yield/area/production columns stay ABSENT
  (i) Season 1/2 resolving to different season_names in one frame
  (j) matched group whose values aggregate to NaN (zeros -> NaN hygiene)
  (k) pre-existing target column: matched rows overwritten, rest kept
"""
import configparser

import numpy as np
import pandas as pd
import pytest

from geocif.ml import stats as ml_stats


# ---------------------------------------------------------------------------
# Reference implementation: the pre-vectorization per-group code, verbatim.
# ---------------------------------------------------------------------------
def _add_statistics_reference(
    dir_stats,
    df,
    country,
    crop,
    admin_zone,
    stats,
    method,
    target_col="Yield (tn per ha)",
    parser=None,
    label="",
):
    # HACK: Bangladesh rice uses GEOGLAM format
    if country == "Bangladesh" and crop == "Rice":
        df = ml_stats.add_GEOGLAM_statistics(
            dir_stats, df, stats, method, admin_zone,
            crop=crop, country=country, label=label,
        )
        for col in ["Area"]:
            df.loc[:, col] = np.nan
        return df

    fn = ml_stats._resolve_stats_file(country, parser)
    df_fewsnet = pd.read_csv(dir_stats / fn, low_memory=False)

    if "product" in df_fewsnet.columns:
        df_fewsnet.loc[:, "product"] = df_fewsnet["product"].replace(
            "Wheat", "Winter Wheat"
        )

    mask = (df_fewsnet["country"] == country) & (df_fewsnet["product"] == crop)

    if "qc_flag" in df_fewsnet.columns:
        df_fewsnet = df_fewsnet[df_fewsnet["qc_flag"] == 0]

    if mask.sum() == 0:
        df = ml_stats.add_GEOGLAM_statistics(
            dir_stats, df, stats, method, admin_zone,
            crop=crop, country=country, label=label,
        )
    else:
        from geocif.utils import PRIMARY_SEASON_NAMES, SECONDARY_SEASON_NAMES

        country_crop_mask = (df_fewsnet["country"] == country) & (
            df_fewsnet["product"] == crop
        )
        available_seasons = set(
            df_fewsnet.loc[country_crop_mask, "season_name"].unique()
        )

        def _resolve_season_filter(season_num):
            if parser is not None:
                country_key = country.lower().replace(" ", "_")
                if parser.has_option(country_key, "hvstat_season_override"):
                    override = parser.get(
                        country_key, "hvstat_season_override"
                    ).strip()
                    if override in available_seasons:
                        return [override]
            if (
                country == "Kenya"
                and crop == "Maize"
                and "Annual" in available_seasons
            ):
                return ["Annual"]
            if season_num == 1:
                for name in PRIMARY_SEASON_NAMES:
                    if name in available_seasons:
                        return [name]
            elif season_num == 2:
                for name in SECONDARY_SEASON_NAMES:
                    if name in available_seasons:
                        return [name]
            if "Annual" in available_seasons:
                return ["Annual"]
            return []

        group_by = ["Region", "Harvest Year"]
        has_season = "Season" in df.columns
        if has_season:
            group_by.append("Season")

        season_filters = {}
        if has_season:
            for s in df["Season"].unique():
                season_filters[s] = _resolve_season_filter(s)
        else:
            season_filters[None] = _resolve_season_filter(1)

        groups = df.groupby(group_by)

        def process_group(group, region, harvest_year, season=None):
            season_filter = season_filters.get(
                season, season_filters.get(None, [])
            )

            mask_region = (
                ml_stats._norm_region_series(df_fewsnet[admin_zone])
                == ml_stats._norm_region_name(region)
            )
            mask_yield = (
                df_fewsnet["crop_production_system"].isin(
                    ml_stats.STANDARD_PRODUCTION_SYSTEMS
                )
                & (df_fewsnet["harvest_year"] == harvest_year)
                & (df_fewsnet["product"] == crop)
                & df_fewsnet["season_name"].isin(season_filter)
            )

            mask_combined = mask_yield & mask_region

            yield_value = df_fewsnet.loc[mask_combined, "yield"]
            area_value = df_fewsnet.loc[mask_combined, "area"]
            prod_value = df_fewsnet.loc[mask_combined, "production"]

            if (
                yield_value.empty
                and country == "Malawi"
                and crop == "Maize"
                and "Annual" in available_seasons
                and "Annual" not in season_filter
            ):
                mask_yield_annual = (
                    df_fewsnet["crop_production_system"].isin(
                        ml_stats.STANDARD_PRODUCTION_SYSTEMS
                    )
                    & (df_fewsnet["harvest_year"] == harvest_year)
                    & (df_fewsnet["product"] == crop)
                    & (df_fewsnet["season_name"] == "Annual")
                )
                mask_combined = mask_yield_annual & mask_region
                yield_value = df_fewsnet.loc[mask_combined, "yield"]
                area_value = df_fewsnet.loc[mask_combined, "area"]
                prod_value = df_fewsnet.loc[mask_combined, "production"]

            yield_series = pd.Series(yield_value)
            if len(yield_series) > 0:
                agg_yield, total_area, total_prod = (
                    ml_stats.aggregate_yield_across_ps(
                        yield_series,
                        pd.Series(area_value),
                        pd.Series(prod_value),
                    )
                )
                group.loc[:, target_col] = agg_yield
                group.loc[:, "Area (ha)"] = (
                    total_area if total_area > 0 else np.nan
                )
                group.loc[:, "Production (tn)"] = (
                    total_prod if total_prod > 0 else np.nan
                )

            return group

        results = []
        for keys, group in groups:
            if has_season:
                region, harvest_year, season = keys
            else:
                region, harvest_year = keys
                season = None
            processed_group = process_group(
                group.copy(), region, harvest_year, season
            )
            results.append(processed_group)

        df = pd.concat(results)

    for col in ["Area"]:
        df.loc[:, col] = np.nan

    return df


# ---------------------------------------------------------------------------
# Fixture harness
# ---------------------------------------------------------------------------
_HEADER = (
    "country,product,admin_1,admin_2,harvest_year,yield,area,production,"
    "qc_flag,crop_production_system,season_name"
)

TARGET = "Yield (tn per ha)"


def _write_stats(tmp_path, rows, fn="stats_fixture.csv"):
    (tmp_path / fn).write_text(_HEADER + "\n" + "\n".join(rows) + "\n")
    return fn


def _make_parser(country, fn):
    parser = configparser.ConfigParser()
    parser["DEFAULT"]["production_statistics_file"] = fn
    parser.add_section(country.lower().replace(" ", "_"))
    return parser


def _run_both(tmp_path, df, country, crop, admin_zone="admin_1", parser=None):
    """Run reference and vectorized implementations; assert equivalence."""
    ref = _add_statistics_reference(
        tmp_path, df.copy(deep=True), country, crop, admin_zone,
        [TARGET], "", parser=parser,
    )
    new = ml_stats.add_statistics(
        tmp_path, df.copy(deep=True), country, crop, admin_zone,
        [TARGET], "", parser=parser,
    )
    # KNOWN, DOCUMENTED dtype deviation (values are identical): the legacy
    # per-group path wrote ``group.loc[:, col] = total_area`` where
    # total_area inherited the CSV column dtype — int64 when the fixture's
    # area/production columns parse as int64 AND that group's slice had no
    # zeros for replace(0, NaN) to promote. That makes the legacy output
    # dtype a per-group, data-dependent accident (any unmatched row or any
    # zero anywhere promotes it to float64 via concat). Real hvstat files
    # always parse these columns as float64 (they contain NaNs), so
    # production output was float64 all along; the vectorized path emits
    # float64 unconditionally. Normalize before comparing.
    for col in ("Area (ha)", "Production (tn)"):
        if col in ref.columns:
            ref[col] = ref[col].astype(float)

    # Legacy emits rows sorted by group key, vectorized preserves input
    # order; both keep the original index labels, so align on index and
    # ignore column order.
    pd.testing.assert_frame_equal(
        ref.sort_index(), new.sort_index(), check_like=True
    )
    return new


def _df(regions, years, season=1, **extra):
    data = {
        "Region": regions,
        "Harvest Year": years,
        "Season": season,
        "x": range(len(regions)),
    }
    data.update(extra)
    return pd.DataFrame(data)


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------
def test_plain_single_ps_join_and_missing_region_nan(tmp_path):
    # (a) + (f): one PS row per (region, year); Ghost region absent -> NaN.
    fn = _write_stats(tmp_path, [
        "Angola,Maize,Huambo,huambo_x,2019,2.0,100,200,0,none,Main",
        "Angola,Maize,Huambo,huambo_x,2020,2.5,100,250,0,none,Main",
    ])
    parser = _make_parser("Angola", fn)
    df = _df(["Huambo", "Huambo", "Ghost"], [2019, 2020, 2019])
    out = _run_both(tmp_path, df, "Angola", "Maize", parser=parser)

    assert list(out[TARGET]) == pytest.approx([2.0, 2.5, np.nan], nan_ok=True)
    assert list(out["Area (ha)"]) == pytest.approx(
        [100.0, 100.0, np.nan], nan_ok=True
    )
    assert list(out["Production (tn)"]) == pytest.approx(
        [200.0, 250.0, np.nan], nan_ok=True
    )
    assert out["Area"].isna().all()
    assert out[TARGET].dtype == np.float64


def test_input_row_order_and_index_preserved(tmp_path):
    # Vectorized contract: output rows keep the INPUT order/index (the
    # legacy path sorted by group key; callers are order-agnostic, and
    # the equivalence assert aligns on index).
    fn = _write_stats(tmp_path, [
        "Angola,Maize,Bie,bie_x,2019,1.0,10,10,0,none,Main",
        "Angola,Maize,Huambo,huambo_x,2019,2.0,10,20,0,none,Main",
    ])
    parser = _make_parser("Angola", fn)
    df = _df(["Huambo", "Bie"], [2019, 2019])
    df.index = [7, 3]  # non-monotonic labels
    out = _run_both(tmp_path, df, "Angola", "Maize", parser=parser)
    assert list(out.index) == [7, 3]
    assert list(out[TARGET]) == [2.0, 1.0]


def test_multi_ps_area_weighted_aggregation(tmp_path):
    # (b): irrigated + rainfed collapse area-weighted; the non-whitelisted
    # "Estate (PS)" row must not contribute.
    fn = _write_stats(tmp_path, [
        "Angola,Maize,Huambo,huambo_x,2019,4.0,50,200,0,irrigated,Main",
        "Angola,Maize,Huambo,huambo_x,2019,2.0,150,300,0,rainfed,Main",
        "Angola,Maize,Huambo,huambo_x,2019,100.0,1000,100000,0,Estate (PS),Main",
    ])
    parser = _make_parser("Angola", fn)
    df = _df(["Huambo"], [2019])
    out = _run_both(tmp_path, df, "Angola", "Maize", parser=parser)

    # (4*50 + 2*150) / 200 = 2.5 ; area 200 ; production 500
    assert out[TARGET].iloc[0] == pytest.approx(2.5)
    assert out["Area (ha)"].iloc[0] == pytest.approx(200.0)
    assert out["Production (tn)"].iloc[0] == pytest.approx(500.0)


def test_season_resolver_falls_back_to_annual(tmp_path):
    # (c): no PRIMARY_SEASON_NAMES entry exists for this country/crop, so
    # _resolve_season_filter falls through to "Annual".
    fn = _write_stats(tmp_path, [
        "Angola,Maize,Huambo,huambo_x,2019,3.3,80,264,0,none,Annual",
    ])
    parser = _make_parser("Angola", fn)
    df = _df(["Huambo"], [2019])
    out = _run_both(tmp_path, df, "Angola", "Maize", parser=parser)
    assert out[TARGET].iloc[0] == pytest.approx(3.3)


def test_malawi_maize_per_group_annual_fallback(tmp_path):
    # (d): region A has a primary-season ("Main") row -> uses it, NOT the
    # coexisting Annual row; region B exists only under Annual -> per-group
    # fallback fills it; region C matches nothing -> NaN.
    fn = _write_stats(tmp_path, [
        "Malawi,Maize,Aaa,aaa_x,2019,1.5,100,150,0,none,Main",
        "Malawi,Maize,Aaa,aaa_x,2019,9.0,100,900,0,none,Annual",
        "Malawi,Maize,Bbb,bbb_x,2019,3.0,200,600,0,none,Annual",
    ])
    parser = _make_parser("Malawi", fn)
    df = _df(["Aaa", "Bbb", "Ccc"], [2019, 2019, 2019])
    out = _run_both(tmp_path, df, "Malawi", "Maize", parser=parser)

    assert out[TARGET].iloc[0] == pytest.approx(1.5)   # primary wins
    assert out[TARGET].iloc[1] == pytest.approx(3.0)   # Annual fallback
    assert np.isnan(out[TARGET].iloc[2])
    assert out["Area (ha)"].iloc[1] == pytest.approx(200.0)


def test_qc_flag_exclusion(tmp_path):
    # (e): the qc_flag=1 row is invisible to the join.
    fn = _write_stats(tmp_path, [
        "Angola,Maize,Ddd,ddd_x,2019,7.0,100,700,1,none,Main",
        "Angola,Maize,Eee,eee_x,2019,3.0,100,300,0,none,Main",
    ])
    parser = _make_parser("Angola", fn)
    df = _df(["Ddd", "Eee"], [2019, 2019])
    out = _run_both(tmp_path, df, "Angola", "Maize", parser=parser)
    assert np.isnan(out[TARGET].iloc[0])
    assert out[TARGET].iloc[1] == pytest.approx(3.0)


def test_zero_matches_leaves_columns_absent(tmp_path):
    # (h): country/crop rows exist pre-qc (so the hvstat branch runs, not
    # GEOGLAM) but every row fails qc -> no group matches -> the yield/
    # area/production columns must stay ABSENT (threshold_optimizer's
    # compute_metric contract).
    fn = _write_stats(tmp_path, [
        "Angola,Maize,Huambo,huambo_x,2019,2.0,100,200,1,none,Main",
    ])
    parser = _make_parser("Angola", fn)
    df = _df(["Huambo"], [2019])
    out = _run_both(tmp_path, df, "Angola", "Maize", parser=parser)
    assert TARGET not in out.columns
    assert "Area (ha)" not in out.columns
    assert "Production (tn)" not in out.columns
    assert "Area" in out.columns  # the trailing NaN column is always added


def test_region_name_normalization_both_directions(tmp_path):
    # (g): underscore/space and case drift on either side must still join.
    fn = _write_stats(tmp_path, [
        "Brazil,Maize,Mato Grosso,mg_x,2019,5.0,100,500,0,none,Main",
        "Brazil,Maize,SAO_PAULO,sp_x,2019,4.0,100,400,0,none,Main",
    ])
    parser = _make_parser("Brazil", fn)
    df = _df(["mato_grosso", "Sao Paulo"], [2019, 2019])
    out = _run_both(tmp_path, df, "Brazil", "Maize", parser=parser)
    assert out[TARGET].iloc[0] == pytest.approx(5.0)
    assert out[TARGET].iloc[1] == pytest.approx(4.0)


def test_two_seasons_resolve_to_different_names(tmp_path):
    # (i): Season 1 -> "Long", Season 2 -> "Short" within one frame.
    fn = _write_stats(tmp_path, [
        "Kenya,Sorghum,Nakuru,nk_x,2019,1.1,100,110,0,none,Long",
        "Kenya,Sorghum,Nakuru,nk_x,2019,0.7,100,70,0,none,Short",
    ])
    parser = _make_parser("Kenya", fn)
    df = _df(["Nakuru", "Nakuru"], [2019, 2019], season=[1, 2])
    out = _run_both(tmp_path, df, "Kenya", "Sorghum", parser=parser)
    assert out[TARGET].iloc[0] == pytest.approx(1.1)
    assert out[TARGET].iloc[1] == pytest.approx(0.7)


def test_matched_group_with_all_zero_values_writes_nan(tmp_path):
    # (j): zeros -> NaN hygiene. The group MATCHES (a stats row exists),
    # so the columns are written — as NaN — which is different from an
    # unmatched group only in that the columns exist at all.
    fn = _write_stats(tmp_path, [
        "Angola,Maize,Fff,fff_x,2019,0,0,0,0,none,Main",
    ])
    parser = _make_parser("Angola", fn)
    df = _df(["Fff"], [2019])
    out = _run_both(tmp_path, df, "Angola", "Maize", parser=parser)
    assert TARGET in out.columns
    assert np.isnan(out[TARGET].iloc[0])
    assert np.isnan(out["Area (ha)"].iloc[0])
    assert np.isnan(out["Production (tn)"].iloc[0])


def test_preexisting_target_column_only_matched_rows_overwritten(tmp_path):
    # (k): legacy wrote into matched groups and left the rest untouched —
    # a pre-existing target column keeps its values on unmatched rows.
    fn = _write_stats(tmp_path, [
        "Angola,Maize,Huambo,huambo_x,2019,2.0,100,200,0,none,Main",
    ])
    parser = _make_parser("Angola", fn)
    df = _df(["Huambo", "Ghost"], [2019, 2019])
    df[TARGET] = [99.0, 99.0]
    out = _run_both(tmp_path, df, "Angola", "Maize", parser=parser)
    assert out[TARGET].iloc[0] == pytest.approx(2.0)   # overwritten
    assert out[TARGET].iloc[1] == pytest.approx(99.0)  # kept


def test_no_season_column_uses_season_one_filter(tmp_path):
    # No "Season" column in df -> grouping on (Region, Harvest Year) and
    # the Season-1 filter applies.
    fn = _write_stats(tmp_path, [
        "Angola,Maize,Huambo,huambo_x,2019,2.2,100,220,0,none,Main",
    ])
    parser = _make_parser("Angola", fn)
    df = pd.DataFrame(
        {"Region": ["Huambo"], "Harvest Year": [2019], "x": [0]}
    )
    out = _run_both(tmp_path, df, "Angola", "Maize", parser=parser)
    assert out[TARGET].iloc[0] == pytest.approx(2.2)


def test_admin_2_zone_column(tmp_path):
    # The admin_zone argument names the stats column the regions live in.
    fn = _write_stats(tmp_path, [
        "United States Of America,Maize,Iowa,iowa_adair,2019,11.0,100,1100,"
        "0,none,Main",
    ])
    parser = _make_parser("United States Of America", fn)
    df = _df(["Iowa_Adair"], [2019])
    out = _run_both(
        tmp_path, df, "United States Of America", "Maize",
        admin_zone="admin_2", parser=parser,
    )
    assert out[TARGET].iloc[0] == pytest.approx(11.0)
