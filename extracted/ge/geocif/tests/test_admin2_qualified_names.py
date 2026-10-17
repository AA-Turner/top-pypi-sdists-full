"""admin_2 joins match geoprepare's "<admin_1> <admin_2>" region names.

When admin_2 names repeat within a country, geoprepare names every admin_2
region "<ADM1_NAME> <ADM2_NAME>" (Kaliganj is an upazila of four Bangladesh
districts: gazipur_kaliganj, jhenaidah_kaliganj, ...). Yield files keep the
bare upazila in admin_2, as the boundary does, so admin_2 joins key their rows
both ways. A bare-name key always wins, so existing matches never change.
"""
import configparser

import numpy as np
import pandas as pd
import pytest

from geocif.ml import stats as ml_stats

TARGET = "Yield (tn per ha)"
HEADER = ("country,product,admin_1,admin_2,harvest_year,yield,area,production,"
          "qc_flag,crop_production_system,season_name")


@pytest.fixture(autouse=True)
def _fresh_state(monkeypatch):
    monkeypatch.setattr(ml_stats, "_WARNED", set())


def _stats(tmp_path, rows):
    (tmp_path / "s.csv").write_text(HEADER + "\n" + "\n".join(rows) + "\n")
    parser = configparser.ConfigParser()
    parser["bangladesh"] = {"production_statistics_file": "s.csv"}
    return parser


UPAZILAS = [
    "Bangladesh,Rice,Gazipur,Kaliganj,2020,4.0,100,400,0,none,Boro",
    "Bangladesh,Rice,Jhenaidah,Kaliganj,2020,5.0,300,1500,0,none,Boro",
    "Bangladesh,Rice,Dhaka,Savar,2020,3.0,50,150,0,none,Boro",
]


def _join(tmp_path, parser, regions, admin_zone="admin_2"):
    df = pd.DataFrame({"Region": regions, "Harvest Year": 2020, "Season": 1})
    return ml_stats.add_statistics(
        tmp_path, df, "Bangladesh", "Rice", admin_zone, [TARGET], "", parser=parser,
    )


def test_qualified_regions_get_their_own_district(tmp_path):
    parser = _stats(tmp_path, UPAZILAS)
    out = _join(tmp_path, parser, ["gazipur_kaliganj", "jhenaidah_kaliganj", "dhaka_savar"])
    assert out[TARGET].tolist() == pytest.approx([4.0, 5.0, 3.0])
    assert out["Area (ha)"].tolist() == pytest.approx([100.0, 300.0, 50.0])


def test_bare_regions_match_as_before(tmp_path):
    parser = _stats(tmp_path, UPAZILAS)
    out = _join(tmp_path, parser, ["savar", "kaliganj"])
    # a bare repeated name still pools its namesakes, area-weighted, as before
    assert out[TARGET].tolist() == pytest.approx([3.0, (4.0 * 100 + 5.0 * 300) / 400])


def test_bare_key_wins_over_an_equal_qualified_key(tmp_path):
    parser = _stats(tmp_path, [
        "Bangladesh,Rice,North,Hill,2020,1.0,10,10,0,none,Boro",       # qualified: "north hill"
        "Bangladesh,Rice,East,North Hill,2020,2.0,10,20,0,none,Boro",  # bare: "north hill"
    ])
    assert _join(tmp_path, parser, ["north_hill"])[TARGET].tolist() == pytest.approx([2.0])


def test_admin_1_runs_do_not_qualify(tmp_path):
    parser = _stats(tmp_path, UPAZILAS)
    out = _join(tmp_path, parser, ["gazipur_kaliganj"], admin_zone="admin_1")
    assert TARGET not in out.columns or out[TARGET].isna().all()


def test_admin1_lookup_has_qualified_keys(tmp_path):
    parser = _stats(tmp_path, UPAZILAS + [
        "Bangladesh,Rice,North,Hill,2020,1.0,10,10,0,none,Boro",
        "Bangladesh,Rice,East,North Hill,2020,2.0,10,20,0,none,Boro",
    ])
    lookup = ml_stats.admin1_lookup(tmp_path, "Bangladesh", parser=parser)
    assert lookup["gazipur kaliganj"] == "Gazipur"
    assert lookup["jhenaidah kaliganj"] == "Jhenaidah"
    assert lookup["dhaka savar"] == "Dhaka"
    assert lookup["savar"] == "Dhaka"
    assert lookup["north hill"] == "East"  # the bare key wins


def test_regions_with_yields_has_qualified_names_at_admin_2_only(tmp_path):
    parser = _stats(tmp_path, UPAZILAS)
    a2 = ml_stats.regions_with_yields(tmp_path, "Bangladesh", "Rice", "admin_2", parser=parser)
    assert {"kaliganj", "savar", "gazipur kaliganj", "jhenaidah kaliganj", "dhaka savar"} <= a2
    a1 = ml_stats.regions_with_yields(tmp_path, "Bangladesh", "Rice", "admin_1", parser=parser)
    assert a1 == {"gazipur", "jhenaidah", "dhaka"}


def test_blank_admin_1_is_not_qualified(tmp_path):
    out = ml_stats._qualified_region_series(
        pd.Series(["Gazipur", " ", np.nan, "Dhaka"]),
        pd.Series(["Kaliganj", "Savar", "Savar", np.nan]),
    )
    assert out.iloc[0] == "gazipur kaliganj"
    assert out.iloc[1:].isna().all()
