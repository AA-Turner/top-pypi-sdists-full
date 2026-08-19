"""
Tests for the admin_2 county yield export (geocif/yield_outlook.py).

Schema requested 2026-08-18:
    crop, year, state_name, county_name, state_fips, county_fips, fips,
    observed_yield, predicted_yield, lower_ci, upper_ci

The county name is derived from the FIPS prefix rather than by splitting the
"State County" region string on whitespace — that split is ambiguous for
multi-word states and multi-word counties alike.
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from geocif.yield_outlook import (
    _COUNTY_EXPORT_COLS,
    _CROP_DISPLAY,
    _FIPS_TO_STATE,
    _crop_display_name,
    _split_county_region,
)


# ----------------------------------------------------------- schema


def test_requested_columns_come_first_in_order():
    """The first 11 columns must match the requested product exactly."""
    assert _COUNTY_EXPORT_COLS[:11] == [
        "crop", "year", "state_name", "county_name", "state_fips",
        "county_fips", "fips", "observed_yield", "predicted_yield",
        "lower_ci", "upper_ci",
    ]


def test_provenance_columns_follow():
    assert _COUNTY_EXPORT_COLS[11:] == ["units", "model", "alpha", "ci_coverage"]


# ------------------------------------------------------ crop naming


def test_maize_is_exported_as_corn():
    """USA convention — the product says Corn, not maize."""
    assert _crop_display_name("maize") == "Corn"


def test_soybean_is_exported_as_soybeans():
    assert _crop_display_name("soybean") == "Soybeans"


def test_crop_name_is_case_and_separator_insensitive():
    assert _crop_display_name("Maize") == "Corn"
    assert _crop_display_name("winter wheat") == "Winter Wheat"
    assert _crop_display_name("winter_wheat") == "Winter Wheat"


def test_unknown_crop_falls_back_to_title_case():
    assert _crop_display_name("millet") == "Millet"
    assert _crop_display_name("pearl_millet") == "Pearl Millet"


# ------------------------------------------- state/county name split


def test_simple_state_and_county():
    assert _split_county_region("Illinois Boone", "17007") == ("Illinois", "Boone")


def test_multi_word_state():
    """'South Dakota Aurora' must not split after 'South'."""
    assert _split_county_region("South Dakota Aurora", "46003") == (
        "South Dakota", "Aurora")


def test_multi_word_county():
    assert _split_county_region("Illinois Jo Daviess", "17085") == (
        "Illinois", "Jo Daviess")


def test_multi_word_state_and_multi_word_county():
    """The case a whitespace split cannot get right."""
    assert _split_county_region("South Dakota Fall River", "46047") == (
        "South Dakota", "Fall River")


def test_underscored_region_names():
    assert _split_county_region("south_dakota_fall_river", "46047") == (
        "South Dakota", "Fall River")


def test_internal_capitals_are_preserved():
    """.title() would wreck these, so cased input must be left alone."""
    assert _split_county_region("Illinois McLean", "17113") == ("Illinois", "McLean")
    assert _split_county_region("Illinois DeKalb", "17037") == ("Illinois", "DeKalb")


def test_state_comes_from_fips_not_from_the_string():
    """FIPS is authoritative — a mismatched prefix must not win."""
    state, _ = _split_county_region("Illinois Boone", "19001")
    assert state == "Iowa"


def test_missing_fips_falls_back_to_first_token():
    assert _split_county_region("Illinois Boone", "") == ("Illinois", "Boone")


def test_region_without_county_does_not_crash():
    state, county = _split_county_region("Illinois", "17000")
    assert state == "Illinois"
    assert isinstance(county, str)


# ------------------------------------------------------- FIPS lookup


def test_fips_to_state_covers_every_state():
    from geocif.yield_outlook import _STATE_FIPS

    assert len(_FIPS_TO_STATE) == len(_STATE_FIPS)


def test_known_state_fips_codes():
    assert _FIPS_TO_STATE["17"] == "Illinois"
    assert _FIPS_TO_STATE["19"] == "Iowa"
    assert _FIPS_TO_STATE["46"] == "South Dakota"


def test_leading_zero_states_survive():
    """Alabama is '01', not 1 — the reason FIPS is carried as a string."""
    assert _FIPS_TO_STATE["01"] == "Alabama"
    assert _split_county_region("Alabama Autauga", "01001") == ("Alabama", "Autauga")


# --------------------------------------------------- end-to-end shape


def test_county_fips_derivation_matches_the_product():
    """fips 17007 -> state_fips '17', county_fips 7 (int, no leading zeros)."""
    import pandas as pd

    fips = pd.Series(["17007", "17009", "01001", "46047"])
    state_fips = fips.str[:2]
    county_fips = pd.to_numeric(fips.str[2:], errors="coerce").astype("Int64")

    assert list(state_fips) == ["17", "17", "01", "46"]
    assert list(county_fips) == [7, 9, 1, 47]
