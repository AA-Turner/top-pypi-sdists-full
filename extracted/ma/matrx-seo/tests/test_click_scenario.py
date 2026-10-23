"""Click-share scenarios: the one average click curve at its edges, missing inputs
said (never invented), and an organization's own curve honored."""

from __future__ import annotations

import pytest
from matrx_scraper.click_curve import GSC_EXPECTED_CTR_CURVE, expected_ctr_for_position
from matrx_seo.click_scenario import SCENARIO_LABEL, parse_click_curve, traffic_scenario


def test_curve_edges_position_one_and_one_hundred() -> None:
    assert expected_ctr_for_position(1) == 0.28
    assert expected_ctr_for_position(10) == 0.025
    assert expected_ctr_for_position(11) == 0.015
    assert expected_ctr_for_position(20) == 0.015
    assert expected_ctr_for_position(21) == 0.008
    assert expected_ctr_for_position(100) == 0.008  # past the curve: its last entry


def test_curve_rounds_decimal_positions_half_up_and_clamps_to_one() -> None:
    assert expected_ctr_for_position(1.4) == 0.28
    assert expected_ctr_for_position(1.5) == 0.15
    assert expected_ctr_for_position(2.5) == 0.11  # half-up, not banker's (2.5 → 3)
    assert expected_ctr_for_position(0.4) == 0.28


def test_scenario_now_target_and_delta_carry_the_label() -> None:
    s = traffic_scenario(1000, 8, 3)
    assert (s.clicks_now, s.clicks_at_target, s.delta) == (32.0, 110.0, 78.0)
    assert s.label == SCENARIO_LABEL == "hypothetical, from an average click curve"
    assert s.to_dict()["label"] == SCENARIO_LABEL
    assert s.missing == ()


def test_scenario_at_position_one_hundred_and_decimals() -> None:
    assert traffic_scenario(1000, 100, 1).clicks_now == 8.0
    assert traffic_scenario(1000, 2.5, 1.2).clicks_now == 110.0


def test_missing_volume_estimates_nothing_and_says_so() -> None:
    s = traffic_scenario(None, 8, 3)
    assert (s.clicks_now, s.clicks_at_target, s.delta) == (None, None, None)
    assert "volume" in s.missing
    assert any("volume is unknown" in n for n in s.notes)


def test_missing_current_position_is_total_potential_not_additional() -> None:
    s = traffic_scenario(1000, None, 3)
    assert s.clicks_now is None and s.delta is None
    assert s.clicks_at_target == 110.0
    assert "current_position" in s.missing
    assert any("total potential" in n for n in s.notes)


def test_a_target_no_better_than_now_shows_no_negative_gain_and_keeps_the_note() -> None:
    s = traffic_scenario(1000, 1, 5)
    assert s.delta is None and s.already_at_target
    assert any("already at or above the target" in n.lower() for n in s.notes)
    row = s.compact()
    assert row["gain"] is None and "already at or above the target" in row["note"]
    assert "note" not in traffic_scenario(1000, 8, 3).compact()
    assert traffic_scenario(1000, 3.4, 3).delta is None  # same rank after rounding


OWN = [0.5, 0.2, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]


def test_an_organizations_own_curve_overrides_the_default() -> None:
    own = parse_click_curve(OWN)
    s = traffic_scenario(1000, 12, 2, own)
    assert (s.clicks_now, s.clicks_at_target) == (100.0, 200.0)  # 12 → the last entry, 0.1
    assert traffic_scenario(1000, 12, 2).clicks_at_target == 150.0  # the default curve differs


_TEN = [0.3, 0.2, 0.1, 0.09, 0.08, 0.07, 0.06, 0.05, 0.04, 0.03]


@pytest.mark.parametrize(
    "bad",
    [
        [],
        "0.3",
        None,
        [0.3, 0.2],  # too short
        [0.3] * 101,  # too long
        _TEN[:-1] + [0],  # a zero would divide by zero in the CTR check
        _TEN[:-1] + ["x"],
        _TEN[:-1] + [True],
        [1.5] + _TEN[1:],
        [0.2, 0.3] + _TEN[2:],  # rising
    ],
)
def test_a_malformed_curve_knob_raises_naming_the_knob(bad) -> None:
    with pytest.raises(ValueError, match="seo.click_curve"):
        parse_click_curve(bad)


def test_bad_inputs_raise() -> None:
    with pytest.raises(ValueError):
        traffic_scenario(-1, 3, 1)
    with pytest.raises(ValueError):
        traffic_scenario(10, 0, 1)


def test_the_default_curve_is_the_one_declaration() -> None:
    assert parse_click_curve(list(GSC_EXPECTED_CTR_CURVE)) == GSC_EXPECTED_CTR_CURVE
    assert len(GSC_EXPECTED_CTR_CURVE) == 21


def test_a_bad_stored_curve_reads_as_the_platform_curve_with_a_notice() -> None:
    from matrx_scraper.click_curve import curve_or_platform

    resolved = curve_or_platform(_TEN[:-1] + [0])
    assert resolved.curve == GSC_EXPECTED_CTR_CURVE
    assert resolved.notice and "value 10 is 0" in resolved.notice
    assert curve_or_platform(_TEN).notice is None
