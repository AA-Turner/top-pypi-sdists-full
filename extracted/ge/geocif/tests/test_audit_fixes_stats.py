"""The HarvestStat yield join must filter on country (2026-09-30 audit, A1).

The shared ``hvstat_africa_data_v1.0.csv`` holds every country, and admin-1
names collide (Malawi and Zambia both have Central / Northern / Southern).
The join keyed on (normalised region name, harvest year) only, so a Malawi
maize run area-weighted Zambia's rows into its target: 49 of 121 Malawi
region-years changed (Northern mean -9.5 %, worst -42 %).
"""
import configparser

import numpy as np
import pandas as pd
import pytest

from geocif.ml import stats as ml_stats

_HEADER = (
    "country,product,admin_1,admin_2,harvest_year,yield,area,production,"
    "qc_flag,crop_production_system,season_name"
)
TARGET = "Yield (tn per ha)"


def _fixture(tmp_path, rows, country):
    fn = "stats_fixture.csv"
    (tmp_path / fn).write_text(_HEADER + "\n" + "\n".join(rows) + "\n")
    parser = configparser.ConfigParser()
    parser["DEFAULT"]["production_statistics_file"] = fn
    parser.add_section(country.lower().replace(" ", "_"))
    return parser


def test_colliding_admin1_name_in_another_country_is_ignored(tmp_path):
    parser = _fixture(tmp_path, [
        "Malawi,Maize,Central,c_mw,2019,1.5,100,150,0,none,Main",
        # Same admin-1 name, much larger area: pooled it would dominate
        # the area-weighted yield ((1.5*100 + 4.0*900) / 1000 = 3.75).
        "Zambia,Maize,Central,c_zm,2019,4.0,900,3600,0,none,Main",
    ], "Malawi")
    df = pd.DataFrame({"Region": ["Central"], "Harvest Year": [2019], "Season": 1})
    out = ml_stats.add_statistics(
        tmp_path, df, "Malawi", "Maize", "admin_1", [TARGET], "", parser=parser,
    )
    assert out[TARGET].iloc[0] == pytest.approx(1.5)
    assert out["Area (ha)"].iloc[0] == pytest.approx(100.0)
    assert out["Production (tn)"].iloc[0] == pytest.approx(150.0)


def test_malawi_annual_fallback_does_not_borrow_another_country(tmp_path):
    # "Northern" exists only for Zambia; Malawi's Annual fallback must not
    # pick it up. "Central" has a Malawi Annual row so the fallback is armed.
    parser = _fixture(tmp_path, [
        "Malawi,Maize,Central,c_mw,2019,2.0,100,200,0,none,Annual",
        "Zambia,Maize,Northern,n_zm,2019,5.0,100,500,0,none,Annual",
        "Zambia,Maize,Northern,n_zm,2019,5.0,100,500,0,none,Main",
    ], "Malawi")
    df = pd.DataFrame(
        {"Region": ["Central", "Northern"], "Harvest Year": [2019, 2019], "Season": 1}
    )
    out = ml_stats.add_statistics(
        tmp_path, df, "Malawi", "Maize", "admin_1", [TARGET], "", parser=parser,
    )
    assert out[TARGET].iloc[0] == pytest.approx(2.0)
    assert np.isnan(out[TARGET].iloc[1])
