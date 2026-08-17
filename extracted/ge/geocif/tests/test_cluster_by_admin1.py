"""Tests for cluster_strategy = admin_1 (one pooled model per state).

Third arm of the pooling experiment: `single` (all counties in one model) vs
`admin_1` (one model per state) vs `crop_calendar_region` (one per calendar
zone) vs `individual` (one per county). Parent lookup reuses
ml.stats.admin1_lookup so the grouping agrees with the State categorical and
the run_regions filter by construction.
"""
import configparser
from types import SimpleNamespace

import pandas as pd

from geocif.geocif import Geocif

STATS_FN = "stats.csv"
_CSV = """country,product,admin_1,admin_2,harvest_year,yield,area,production,qc_flag,crop_production_system,season_name
United States Of America,Maize,Iowa,iowa_adair,2019,11.0,100,1100,0,none,Main
United States Of America,Maize,Iowa,iowa_adams,2019,10.0,100,1000,0,none,Main
United States Of America,Maize,Missouri,missouri_adair,2019,8.4,100,840,0,none,Main
"""


def _obj(tmp_path):
    (tmp_path / STATS_FN).write_text(_CSV)
    p = configparser.ConfigParser()
    p["DEFAULT"]["production_statistics_file"] = STATS_FN
    p.add_section("PATHS")
    p["PATHS"]["dir_production_statistics"] = str(tmp_path)
    logged = []
    return SimpleNamespace(
        parser=p,
        country="united_states_of_america",
        crop="maize",
        logger=SimpleNamespace(
            info=lambda m, *a: logged.append(m),
            warning=lambda m, *a: logged.append(m),
            error=lambda m, *a: logged.append(m),
        ),
        _logged=logged,
    )


def test_counties_group_by_parent_state(tmp_path):
    obj = _obj(tmp_path)
    df = pd.DataFrame(
        {"Region": ["Iowa Adair", "Iowa Adams", "Missouri Adair"]}
    )
    out = Geocif._cluster_by_admin1(obj, df)
    ids = dict(zip(out["Region"], out["Region_ID"]))
    # the two Iowa counties share a pool; Missouri is its own
    assert ids["Iowa Adair"] == ids["Iowa Adams"]
    assert ids["Missouri Adair"] != ids["Iowa Adair"]
    assert out["Region_ID"].nunique() == 2


def test_unresolvable_region_gets_singleton(tmp_path):
    obj = _obj(tmp_path)
    df = pd.DataFrame({"Region": ["Iowa Adair", "Iowa Adams", "Nowhere County"]})
    out = Geocif._cluster_by_admin1(obj, df)
    ids = dict(zip(out["Region"], out["Region_ID"]))
    # never silently merged into a real state's pool
    assert ids["Nowhere County"] not in (ids["Iowa Adair"],)
    assert out["Region_ID"].nunique() == 2  # iowa pool + singleton


def test_empty_mapping_logs_error_and_singletons(tmp_path):
    obj = _obj(tmp_path)
    obj.country = "atlantis"  # no rows in the stats file
    df = pd.DataFrame({"Region": ["A County", "B County"]})
    out = Geocif._cluster_by_admin1(obj, df)
    assert out["Region_ID"].nunique() == 2
    assert any("no admin_2 -> admin_1 mapping" in m for m in obj._logged)


def test_returns_region_and_region_id_columns(tmp_path):
    obj = _obj(tmp_path)
    df = pd.DataFrame({"Region": ["Iowa Adair"]})
    out = Geocif._cluster_by_admin1(obj, df)
    assert list(out.columns) == ["Region", "Region_ID"]
