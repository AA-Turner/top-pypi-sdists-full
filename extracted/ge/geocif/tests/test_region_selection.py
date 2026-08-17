"""Tests for config-driven region selection (``run_regions``).

``[<country>] run_regions`` restricts which regions a model run covers,
optionally given at a different admin level than the run itself via
``run_regions_level``. The headline case is an admin_1 (state) selection on an
admin_2 (county) run: only counties inside the selected states survive, mapped
through ``ml.stats.admin1_lookup`` (the same file + normalization the yield
join uses). Unset ``run_regions`` keeps today's behaviour (no filtering).

The filter is exercised the way ``_prepare_ml_dataframe`` calls it — the
unbound ``Geocif._filter_to_selected_regions`` against a SimpleNamespace stand-
in, mirroring tests/test_state_categorical.py.
"""
import configparser
import logging
from types import SimpleNamespace

import pandas as pd
import pytest

from geocif.geocif import Geocif

STATS_FN = "region_selection_stats.csv"

# Two counties in Iowa, one in Missouri, one in South Dakota (an underscore /
# multi-word state, to exercise name normalization).
_CSV = """country,product,admin_1,admin_2,harvest_year,yield,area,production,qc_flag,crop_production_system,season_name
United States Of America,Maize,Iowa,iowa_adair,2019,11.0,100,1100,0,none,Main
United States Of America,Maize,Iowa,iowa_story,2019,12.0,100,1200,0,none,Main
United States Of America,Maize,Missouri,missouri_adair,2019,8.4,100,840,0,none,Main
United States Of America,Maize,South Dakota,south_dakota_brown,2019,9.1,100,910,0,none,Main
"""

COUNTIES = ["Iowa Adair", "Iowa Story", "Missouri Adair", "South Dakota Brown"]
STATES = ["Iowa", "Missouri", "South Dakota"]


def _parser(tmp_path, country_opts=None):
    p = configparser.ConfigParser()
    p["DEFAULT"]["production_statistics_file"] = STATS_FN
    p.add_section("PATHS")
    p["PATHS"]["dir_production_statistics"] = str(tmp_path)
    p.add_section("united_states_of_america")
    for key, value in (country_opts or {}).items():
        p["united_states_of_america"][key] = value
    (tmp_path / STATS_FN).write_text(_CSV)
    return p


class _FakeGeocif(SimpleNamespace):
    """Attribute bag carrying the real Geocif methods under test.

    ``_filter_to_selected_regions`` calls two sibling helpers on ``self``, so a
    bare SimpleNamespace (the tests/test_state_categorical.py pattern) is not
    enough — binding the real functions here keeps method dispatch identical to
    a live Geocif instance without constructing one.
    """

    _config_option = Geocif._config_option
    _normalize_admin_level = staticmethod(Geocif._normalize_admin_level)
    _get_run_region_selection = Geocif._get_run_region_selection
    _filter_to_selected_regions = Geocif._filter_to_selected_regions


def _obj(tmp_path, admin_zone, crop="maize", **country_opts):
    return _FakeGeocif(
        parser=_parser(tmp_path, country_opts),
        country="united_states_of_america",
        crop=crop,
        admin_zone=admin_zone,
        logger=logging.getLogger("geocif.test.region_selection"),
    )


def _frame(regions):
    return pd.DataFrame(
        {
            "Region": regions,
            "Harvest Year": [2019] * len(regions),
            "Yield": [10.0] * len(regions),
        }
    )


def _run(obj, df):
    return Geocif._filter_to_selected_regions(obj, df)


def _regions(df):
    return sorted(df["Region"].astype(str))


# --------------------------------------------------------------------------
# no selection -> identity
# --------------------------------------------------------------------------
def test_unset_run_regions_is_identity(tmp_path):
    obj = _obj(tmp_path, "admin_2")
    df = _frame(COUNTIES)
    out = _run(obj, df)
    assert _regions(out) == sorted(COUNTIES)
    assert len(out) == len(df)


def test_empty_run_regions_is_identity(tmp_path):
    obj = _obj(tmp_path, "admin_2", run_regions="[]")
    df = _frame(COUNTIES)
    assert _regions(_run(obj, df)) == sorted(COUNTIES)


def test_unparseable_run_regions_is_identity(tmp_path):
    obj = _obj(tmp_path, "admin_2", run_regions="illinois, iowa")
    df = _frame(COUNTIES)
    assert _regions(_run(obj, df)) == sorted(COUNTIES)


# --------------------------------------------------------------------------
# selection level == run level
# --------------------------------------------------------------------------
def test_admin1_selection_on_admin1_run(tmp_path):
    obj = _obj(tmp_path, "admin_1", run_regions='["Iowa", "South Dakota"]')
    out = _run(obj, _frame(STATES))
    assert _regions(out) == ["Iowa", "South Dakota"]


def test_admin2_selection_on_admin2_run(tmp_path):
    obj = _obj(
        tmp_path, "admin_2", run_regions='["Iowa Adair", "South Dakota Brown"]'
    )
    out = _run(obj, _frame(COUNTIES))
    assert _regions(out) == ["Iowa Adair", "South Dakota Brown"]


def test_explicit_run_regions_level_matching_run_level(tmp_path):
    obj = _obj(
        tmp_path,
        "admin_2",
        run_regions_level="admin_2",
        run_regions='["Iowa Story"]',
    )
    assert _regions(_run(obj, _frame(COUNTIES))) == ["Iowa Story"]


# --------------------------------------------------------------------------
# THE headline case: admin_1 selection, admin_2 run
# --------------------------------------------------------------------------
def test_admin1_selection_on_admin2_run_keeps_counties_of_states(tmp_path):
    obj = _obj(
        tmp_path,
        "admin_2",
        run_regions_level="admin_1",
        run_regions='["Iowa"]',
    )
    out = _run(obj, _frame(COUNTIES))
    assert _regions(out) == ["Iowa Adair", "Iowa Story"]


def test_admin1_selection_on_admin2_run_multiple_states(tmp_path):
    obj = _obj(
        tmp_path,
        "admin_2",
        run_regions_level="admin_1",
        run_regions='["Iowa", "South Dakota"]',
    )
    out = _run(obj, _frame(COUNTIES))
    assert _regions(out) == ["Iowa Adair", "Iowa Story", "South Dakota Brown"]


def test_admin1_selection_on_admin2_run_without_mapping_is_identity(tmp_path, caplog):
    obj = _obj(
        tmp_path,
        "admin_2",
        run_regions_level="admin_1",
        run_regions='["Iowa"]',
    )
    # point at a stats file that does not exist -> admin1_lookup returns {}
    obj.parser["DEFAULT"]["production_statistics_file"] = "absent.csv"
    with caplog.at_level(logging.ERROR, logger="geocif.test.region_selection"):
        out = _run(obj, _frame(COUNTIES))
    assert _regions(out) == sorted(COUNTIES)
    assert "no admin_2->admin_1 mapping" in caplog.text


# --------------------------------------------------------------------------
# finer selection than run level: admin_2 names, admin_1 run -> map up
# --------------------------------------------------------------------------
def test_admin2_selection_on_admin1_run_maps_up_to_states(tmp_path, caplog):
    obj = _obj(
        tmp_path,
        "admin_1",
        run_regions_level="admin_2",
        run_regions='["Iowa Adair", "Missouri Adair"]',
    )
    with caplog.at_level(logging.INFO, logger="geocif.test.region_selection"):
        out = _run(obj, _frame(STATES))
    assert _regions(out) == ["Iowa", "Missouri"]
    assert "mapped" in caplog.text


# --------------------------------------------------------------------------
# unsupported level combination
# --------------------------------------------------------------------------
def test_unsupported_level_combination_is_identity(tmp_path, caplog):
    obj = _obj(
        tmp_path,
        "admin_2",
        run_regions_level="admin_0",
        run_regions='["United States Of America"]',
    )
    with caplog.at_level(logging.WARNING, logger="geocif.test.region_selection"):
        out = _run(obj, _frame(COUNTIES))
    assert _regions(out) == sorted(COUNTIES)
    assert "cannot be reconciled" in caplog.text


# --------------------------------------------------------------------------
# flat list vs per-crop dict
# --------------------------------------------------------------------------
def test_per_crop_dict_selection(tmp_path):
    cfg = '{"maize": ["Iowa Adair"], "soybean": ["Missouri Adair"]}'
    maize = _obj(tmp_path, "admin_2", crop="maize", run_regions=cfg)
    soy = _obj(tmp_path, "admin_2", crop="soybean", run_regions=cfg)
    assert _regions(_run(maize, _frame(COUNTIES))) == ["Iowa Adair"]
    assert _regions(_run(soy, _frame(COUNTIES))) == ["Missouri Adair"]


def test_crop_absent_from_dict_is_identity(tmp_path):
    obj = _obj(
        tmp_path,
        "admin_2",
        crop="winter_wheat",
        run_regions='{"maize": ["Iowa Adair"]}',
    )
    assert _regions(_run(obj, _frame(COUNTIES))) == sorted(COUNTIES)


def test_flat_list_applies_to_every_crop(tmp_path):
    for crop in ("maize", "soybean"):
        obj = _obj(tmp_path, "admin_2", crop=crop, run_regions='["Iowa Story"]')
        assert _regions(_run(obj, _frame(COUNTIES))) == ["Iowa Story"]


def test_dict_crop_key_normalized(tmp_path):
    obj = _obj(
        tmp_path,
        "admin_2",
        crop="winter_wheat",
        run_regions='{"Winter Wheat": ["Iowa Adair"]}',
    )
    assert _regions(_run(obj, _frame(COUNTIES))) == ["Iowa Adair"]


# --------------------------------------------------------------------------
# normalization variants
# --------------------------------------------------------------------------
@pytest.mark.parametrize(
    "name", ["South Dakota", "south_dakota", "SOUTH DAKOTA", "South_Dakota"]
)
def test_name_normalization_variants_admin1_run(tmp_path, name):
    obj = _obj(tmp_path, "admin_1", run_regions=f'["{name}"]')
    assert _regions(_run(obj, _frame(STATES))) == ["South Dakota"]


@pytest.mark.parametrize("name", ["South Dakota", "south_dakota", "SOUTH DAKOTA"])
def test_name_normalization_variants_admin1_selection_admin2_run(tmp_path, name):
    obj = _obj(
        tmp_path,
        "admin_2",
        run_regions_level="admin_1",
        run_regions=f'["{name}"]',
    )
    assert _regions(_run(obj, _frame(COUNTIES))) == ["South Dakota Brown"]


@pytest.mark.parametrize("level", ["admin_1", "Admin_1", "ADMIN 1", "admin1"])
def test_run_regions_level_spelling_variants(tmp_path, level):
    obj = _obj(
        tmp_path, "admin_2", run_regions_level=level, run_regions='["Iowa"]'
    )
    assert _regions(_run(obj, _frame(COUNTIES))) == ["Iowa Adair", "Iowa Story"]


# --------------------------------------------------------------------------
# typo protection + hard failure
# --------------------------------------------------------------------------
def test_unmatched_selected_name_is_logged(tmp_path, caplog):
    obj = _obj(
        tmp_path, "admin_2", run_regions='["Iowa Adair", "Ohio Nowhere"]'
    )
    with caplog.at_level(logging.WARNING, logger="geocif.test.region_selection"):
        out = _run(obj, _frame(COUNTIES))
    assert _regions(out) == ["Iowa Adair"]
    assert "matched no region" in caplog.text
    assert "Ohio Nowhere" in caplog.text
    # a name that DID match must not be reported as unmatched
    assert "Iowa Adair, Ohio Nowhere" not in caplog.text


def test_unmatched_state_reported_on_admin2_run(tmp_path, caplog):
    obj = _obj(
        tmp_path,
        "admin_2",
        run_regions_level="admin_1",
        run_regions='["Iowa", "Ohio"]',
    )
    with caplog.at_level(logging.WARNING, logger="geocif.test.region_selection"):
        out = _run(obj, _frame(COUNTIES))
    assert _regions(out) == ["Iowa Adair", "Iowa Story"]
    assert "Ohio" in caplog.text


def test_zero_match_selection_raises(tmp_path):
    obj = _obj(tmp_path, "admin_2", run_regions='["Ohio Nowhere"]')
    with pytest.raises(ValueError) as exc:
        _run(obj, _frame(COUNTIES))
    msg = str(exc.value)
    assert "run_regions selected 0 regions" in msg
    assert "united_states_of_america" in msg and "maize" in msg
    assert "Ohio Nowhere" in msg
    assert "Iowa Adair" in msg  # example Region values from the frame


def test_zero_match_selection_raises_on_admin1_selection(tmp_path):
    obj = _obj(
        tmp_path,
        "admin_2",
        run_regions_level="admin_1",
        run_regions='["Ohio"]',
    )
    with pytest.raises(ValueError):
        _run(obj, _frame(COUNTIES))


# --------------------------------------------------------------------------
# misc robustness
# --------------------------------------------------------------------------
def test_empty_frame_is_returned_untouched(tmp_path):
    obj = _obj(tmp_path, "admin_2", run_regions='["Iowa Adair"]')
    df = _frame([]).astype({"Region": object})
    assert len(_run(obj, df)) == 0


def test_categorical_region_column(tmp_path):
    obj = _obj(
        tmp_path,
        "admin_2",
        run_regions_level="admin_1",
        run_regions='["Iowa"]',
    )
    df = _frame(COUNTIES)
    df["Region"] = df["Region"].astype("category")
    out = _run(obj, df)
    assert sorted(out["Region"].astype(str)) == ["Iowa Adair", "Iowa Story"]


def test_default_section_selection_applies(tmp_path):
    """run_regions set only in [DEFAULT] still filters."""
    obj = _obj(tmp_path, "admin_1")
    obj.parser["DEFAULT"]["run_regions"] = '["Iowa"]'
    assert _regions(_run(obj, _frame(STATES))) == ["Iowa"]
