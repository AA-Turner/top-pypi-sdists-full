"""Tests for the optional 'State' (admin_1) categorical on admin_2 runs.

Opt-in via [ML] cat_features containing "State". Mapping comes from the
production-statistics file (admin_2 -> admin_1) through ml.stats.admin1_lookup,
sharing file resolution + normalization with the yield join.
"""
import configparser
from pathlib import Path
from types import SimpleNamespace

import pandas as pd

from geocif.geocif import Geocif
from geocif.ml.stats import admin1_lookup

STATS_FN = "state_stats.csv"
_CSV = """country,product,admin_1,admin_2,harvest_year,yield,area,production,qc_flag,crop_production_system,season_name
United States Of America,Maize,Iowa,iowa_adair,2019,11.0,100,1100,0,none,Main
United States Of America,Maize,Missouri,missouri_adair,2019,8.4,100,840,0,none,Main
United States Of America,Soybean,Arkansas,arkansas_ashley,2019,3.0,50,150,0,none,Main
"""


def _parser(tmp_path):
    p = configparser.ConfigParser()
    p["DEFAULT"]["production_statistics_file"] = STATS_FN
    p.add_section("PATHS")
    p["PATHS"]["dir_production_statistics"] = str(tmp_path)
    (tmp_path / STATS_FN).write_text(_CSV)
    return p


def test_admin1_lookup(tmp_path):
    m = admin1_lookup(tmp_path, "United States Of America", parser=_parser(tmp_path))
    assert m == {
        "iowa adair": "Iowa",
        "missouri adair": "Missouri",
        "arkansas ashley": "Arkansas",
    }


def test_admin1_lookup_missing_file(tmp_path):
    p = configparser.ConfigParser()
    p["DEFAULT"]["production_statistics_file"] = "absent.csv"
    assert admin1_lookup(tmp_path, "United States Of America", parser=p) == {}


def _fake_geocif(tmp_path, cat_features):
    obj = SimpleNamespace(
        cat_features=cat_features,
        parser=_parser(tmp_path),
        country="united_states_of_america",
        logger=SimpleNamespace(warning=lambda *a, **k: None,
                               info=lambda *a, **k: None),
    )
    return obj


def test_state_column_added(tmp_path):
    obj = _fake_geocif(tmp_path, ["Harvest Year", "Region", "State"])
    df = pd.DataFrame({"Region": ["Iowa Adair", "Missouri Adair", "Texas Nowhere"],
                       "Harvest Year": [2019, 2019, 2019]})
    out = Geocif._add_state_column(obj, df)
    assert list(out["State"]) == ["Iowa", "Missouri", "unknown"]


def test_state_column_opt_out(tmp_path):
    obj = _fake_geocif(tmp_path, ["Harvest Year", "Region"])
    df = pd.DataFrame({"Region": ["Iowa Adair"], "Harvest Year": [2019]})
    out = Geocif._add_state_column(obj, df)
    assert "State" not in out.columns
