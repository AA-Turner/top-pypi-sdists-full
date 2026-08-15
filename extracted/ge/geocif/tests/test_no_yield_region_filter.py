"""Tests for the zero-yield region filter (0.4.910).

regions_with_yields (ml/stats.py) reports which regions have >=1 usable
yield record, sharing file resolution (_resolve_stats_file) and name
normalization (_norm_region_*) with add_statistics itself.
filter_frame_to_yield_regions (cid/indices.py) drops those regions from the
CID input frame, gated by the filter_regions_without_yields config flag.
Scale-genericity: admin_zone names the stats column, so the same code path
serves admin_1 (state) and admin_2 (county) projects.
"""
import configparser

import pandas as pd
import pytest

from geocif.cid.indices import filter_frame_to_yield_regions
from geocif.ml.stats import regions_with_yields

STATS_FN = "test_production_stats.csv"

# iowa_adair: real yields. iowa_ghost: rows exist but yield always NaN.
# iowa_flagged: yields exist but every row fails qc. missouri_adair: yields
# under a state namesake, exercising the admin_1 rollup too.
_STATS_CSV = """country,product,admin_1,admin_2,harvest_year,yield,area,production,qc_flag,crop_production_system,season_name
United States Of America,Maize,Iowa,iowa_adair,2019,11.0,100,1100,0,none,Main
United States Of America,Maize,Iowa,iowa_adair,2020,10.5,100,1050,0,none,Main
United States Of America,Maize,Iowa,iowa_ghost,2019,,100,,0,none,Main
United States Of America,Maize,Iowa,iowa_flagged,2019,9.0,100,900,1,none,Main
United States Of America,Maize,Missouri,missouri_adair,2019,8.4,100,840,0,none,Main
United States Of America,Soybean,Iowa,iowa_adair,2019,3.1,50,155,0,none,Main
"""


@pytest.fixture()
def stats_env(tmp_path):
    (tmp_path / STATS_FN).write_text(_STATS_CSV)
    parser = configparser.ConfigParser()
    parser["DEFAULT"]["production_statistics_file"] = STATS_FN
    parser["DEFAULT"]["filter_regions_without_yields"] = "True"
    parser.add_section("PATHS")
    parser["PATHS"]["dir_production_statistics"] = str(tmp_path)
    parser.add_section("united_states_of_america")
    return tmp_path, parser


def _input_frame(as_category: bool) -> pd.DataFrame:
    df = pd.DataFrame(
        {
            "adm0_name": ["united_states_of_america"] * 4,
            "adm1_name": ["iowa_adair", "iowa_ghost", "iowa_flagged", "missouri_adair"],
            "year": [2020] * 4,
            "pr": [1.0, 2.0, 3.0, 4.0],
        }
    )
    if as_category:
        for c in ("adm0_name", "adm1_name"):
            df[c] = df[c].astype("category")
    return df


def test_regions_with_yields_admin_2(stats_env):
    tmp_path, parser = stats_env
    keep = regions_with_yields(
        tmp_path, "United States Of America", "Maize", "admin_2", parser=parser
    )
    # ghost (all-NaN yield) and flagged (qc_flag!=0) must be absent
    assert keep == {"iowa adair", "missouri adair"}


def test_regions_with_yields_admin_1(stats_env):
    tmp_path, parser = stats_env
    keep = regions_with_yields(
        tmp_path, "United States Of America", "Maize", "admin_1", parser=parser
    )
    assert keep == {"iowa", "missouri"}


def test_regions_with_yields_unknown_crop_returns_none(stats_env):
    tmp_path, parser = stats_env
    assert (
        regions_with_yields(
            tmp_path, "United States Of America", "Sorghum", "admin_2", parser=parser
        )
        is None
    )


def test_regions_with_yields_missing_file_returns_none(tmp_path):
    parser = configparser.ConfigParser()
    parser["DEFAULT"]["production_statistics_file"] = "does_not_exist.csv"
    assert (
        regions_with_yields(
            tmp_path, "United States Of America", "Maize", "admin_2", parser=parser
        )
        is None
    )


@pytest.mark.parametrize("as_category", [False, True])
def test_filter_drops_zero_yield_regions(stats_env, as_category):
    tmp_path, parser = stats_env
    df = _input_frame(as_category)
    out = filter_frame_to_yield_regions(
        df, parser, "admin_2", "united_states_of_america", "maize"
    )
    assert sorted(out["adm1_name"].astype(str)) == ["iowa_adair", "missouri_adair"]
    if as_category:
        # unused levels must be gone, not lingering as phantom categories
        assert set(out["adm1_name"].cat.categories) == {
            "iowa_adair", "missouri_adair",
        }


def test_filter_noop_when_flag_off(stats_env):
    tmp_path, parser = stats_env
    parser["DEFAULT"]["filter_regions_without_yields"] = "False"
    df = _input_frame(False)
    out = filter_frame_to_yield_regions(
        df, parser, "admin_2", "united_states_of_america", "maize"
    )
    assert len(out) == len(df)


def test_filter_noop_when_coverage_unknown(stats_env):
    tmp_path, parser = stats_env
    df = _input_frame(False)
    # crop with no rows in the stats file -> regions_with_yields None -> no-op
    out = filter_frame_to_yield_regions(
        df, parser, "admin_2", "united_states_of_america", "sorghum"
    )
    assert len(out) == len(df)


def test_filter_admin_1_scale(stats_env):
    tmp_path, parser = stats_env
    df = pd.DataFrame(
        {
            "adm0_name": ["united_states_of_america"] * 2,
            "adm1_name": ["iowa", "nevada"],  # nevada: no maize yields
            "year": [2020, 2020],
            "pr": [1.0, 2.0],
        }
    )
    out = filter_frame_to_yield_regions(
        df, parser, "admin_1", "united_states_of_america", "maize"
    )
    assert list(out["adm1_name"]) == ["iowa"]
