"""Regression tests for the no-FIPS branch of ``_split_county_region``.

Guards a silent-degradation fallback found on 2026-08-18. The county export
resolves a 5-digit FIPS from ``level2_to_fips_crosswalk.csv``; when a region is
missing from that crosswalk it falls back to parsing the ``"State County"``
region string with an empty FIPS. That fallback split on the first space, so
``"South Dakota Fall River"`` became ``("South", "Dakota Fall River")`` --
the exact multi-word case ``_split_county_region``'s docstring claims to
handle, and a failure that produces a *plausible-looking* wrong state rather
than an error.

The existing suite missed it because its two relevant tests sit either side of
the gap: ``test_multi_word_state`` passes a real FIPS (so it exercises the
FIPS path), and ``test_missing_fips_falls_back_to_first_token`` uses
"Illinois Boone", a single-word state where both behaviours agree.

The fix recovers the state by LONGEST-prefix match against the known state
names when no FIPS is available. These tests pin the no-FIPS branch only; the
FIPS-driven cases are covered in test_county_export.py.
"""

import pytest

from geocif.yield_outlook import _FIPS_TO_STATE, _split_county_region


# ------------------------------------------- multi-word states, no FIPS

@pytest.mark.parametrize(
    "region, state, county",
    [
        ("South Dakota Fall River", "South Dakota", "Fall River"),
        ("South Dakota Aurora", "South Dakota", "Aurora"),
        ("North Dakota Grand Forks", "North Dakota", "Grand Forks"),
        ("West Virginia Kanawha", "West Virginia", "Kanawha"),
        ("New Mexico Dona Ana", "New Mexico", "Dona Ana"),
        ("Rhode Island Providence", "Rhode Island", "Providence"),
    ],
)
def test_multi_word_state_survives_missing_fips(region, state, county):
    assert _split_county_region(region, "") == (state, county)


def test_single_word_state_still_works_without_fips():
    # The pre-existing behaviour this fallback already had — must not regress.
    assert _split_county_region("Illinois Boone", "") == ("Illinois", "Boone")


def test_underscored_region_without_fips():
    assert _split_county_region("south_dakota_fall_river", "") == (
        "South Dakota", "Fall River")


# ------------------------------------------- the longest-match property

def test_longest_state_name_wins():
    """A state whose name prefixes another must not shadow the longer one.

    Without longest-match, a "New York" region could be captured by a shorter
    candidate and leave the county text mangled.
    """
    assert _split_county_region("New York New York", "") == ("New York", "New York")


def test_no_state_prefix_leaves_first_token_split():
    # Region that starts with no known state name: unchanged behaviour.
    state, county = _split_county_region("Neverland Lost Boys", "")
    assert (state, county) == ("Neverland", "Lost Boys")


def test_region_without_county_does_not_crash_without_fips():
    state, county = _split_county_region("Illinois", "")
    assert isinstance(state, str) and isinstance(county, str)


# ------------------------------------------- FIPS path must be unaffected

def test_fips_still_takes_precedence_over_prefix_match():
    """When a FIPS is present it decides the state, not the string prefix."""
    # 17 = Illinois. Even though the text starts with a valid state name,
    # the FIPS is authoritative.
    state, _ = _split_county_region("Illinois Boone", "17007")
    assert state == "Illinois"


def test_every_state_name_round_trips_without_fips():
    """Each known state, given "<state> Somecounty" and no FIPS, splits right."""
    for name in _FIPS_TO_STATE.values():
        region = f"{name} Springfield"
        assert _split_county_region(region, "") == (name, "Springfield"), name
