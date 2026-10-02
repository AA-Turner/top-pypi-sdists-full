"""in_band() — the single definition of the 15% viewport margin."""
import pytest

from testmu_appium._helpers.band import (
    BAND_MARGIN_DENOMINATOR,
    BAND_MARGIN_NUMERATOR,
    BAND_NUDGE_LANDING,
    band_edges,
    in_band,
    nudge_toward_band,
)

# Measured portrait app viewport on RMX1931: y in [67, 2328], height 2261, so a
# 15% margin leaves the band y in [407, 1988] strict, widened to [399, 1996] by
# the 8px tolerance.
PORTRAIT_TOP, PORTRAIT_BOTTOM = 67, 2328
# Measured landscape app viewport: y in [0, 1008], band y in [144, 864].
LANDSCAPE_TOP, LANDSCAPE_BOTTOM = 0, 1008


@pytest.mark.parametrize(
    "centre,expected",
    [
        (1197, True),    # dead centre of the portrait band
        (399, True),     # lowest centre kept by the tolerance (edge 398.15)
        (398, False),    # one pixel below the lower tolerance edge
        (1996, True),    # highest centre kept by the tolerance (edge 1996.85)
        (1997, False),   # one pixel past the upper tolerance edge
        (100, False),    # near the top: out of band
        (2220, False),   # E2 checkout submit: deep in the bottom zone
    ],
)
def test_portrait_band(centre, expected):
    assert in_band(centre, PORTRAIT_TOP, PORTRAIT_BOTTOM) is expected


@pytest.mark.parametrize(
    "centre,expected",
    [
        (500, True),     # centre of the landscape band
        (100, False),    # above the landscape band (edge 143.2)
        (950, False),    # below the landscape band (edge 864.8)
    ],
)
def test_band_is_relative_to_the_span_not_a_fixed_pixel(centre, expected):
    assert in_band(centre, LANDSCAPE_TOP, LANDSCAPE_BOTTOM) is expected


def test_tolerance_zero_rejects_the_boundary_case():
    # With no slack, a centre one pixel past the strict edge (1988.85) is out —
    # the float flip the cross-multiplied form is chosen to make deterministic.
    assert in_band(1989, PORTRAIT_TOP, PORTRAIT_BOTTOM, tolerance=0) is False
    assert in_band(1988, PORTRAIT_TOP, PORTRAIT_BOTTOM, tolerance=0) is True


def test_margin_is_fifteen_percent():
    assert BAND_MARGIN_NUMERATOR / BAND_MARGIN_DENOMINATOR == pytest.approx(0.15)


def test_band_edges_match_the_predicate():
    # in_band(cy) iff lo <= cy <= hi, using the same margin+tolerance.
    lo, hi = band_edges(PORTRAIT_TOP, PORTRAIT_BOTTOM)
    for cy in range(PORTRAIT_TOP, PORTRAIT_BOTTOM + 1, 7):
        assert in_band(cy, PORTRAIT_TOP, PORTRAIT_BOTTOM) == (lo <= cy <= hi)


def test_band_edges_are_a_nonempty_centred_range():
    lo, hi = band_edges(LANDSCAPE_TOP, LANDSCAPE_BOTTOM)
    assert lo < hi
    mid = (LANDSCAPE_TOP + LANDSCAPE_BOTTOM) / 2
    assert lo < mid < hi


def test_nudge_toward_a_below_band_centre_goes_down():
    # 2220 is deep in the bottom zone → scroll "down" (rows move up).
    direction, distance = nudge_toward_band(2220, PORTRAIT_TOP, PORTRAIT_BOTTOM)
    assert direction == "down"
    assert distance > 0


def test_nudge_toward_an_above_band_centre_goes_up():
    direction, distance = nudge_toward_band(100, PORTRAIT_TOP, PORTRAIT_BOTTOM)
    assert direction == "up"
    assert distance > 0


def test_nudge_is_a_noop_when_already_in_band():
    assert nudge_toward_band(1197, PORTRAIT_TOP, PORTRAIT_BOTTOM) == (None, 0.0)


def test_nudge_lands_a_third_into_the_band_from_the_near_edge():
    # Below the band, the landing target is a third of the way from the lower band
    # edge (hi) toward the viewport centre, so the centre ends up inside the band.
    lo, hi = band_edges(PORTRAIT_TOP, PORTRAIT_BOTTOM)
    mid = (PORTRAIT_TOP + PORTRAIT_BOTTOM) / 2
    centre = 2220
    _, distance = nudge_toward_band(centre, PORTRAIT_TOP, PORTRAIT_BOTTOM)
    landed = centre - distance                       # "down" moves the centre up
    assert landed == pytest.approx(hi - BAND_NUDGE_LANDING * (hi - mid))
    assert lo <= landed <= hi
