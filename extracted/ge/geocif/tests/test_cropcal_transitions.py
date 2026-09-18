"""Numerical core of the crop-calendar validator: circular arithmetic,
transition rules, scoring, features and cross-validation.

These are hand-computed golden values, not regression snapshots, so they say
what the code is *supposed* to do rather than what it happened to do. Where the
port deliberately departs from the GEOGLAM original the test names say so and
the docstring gives the reason.
"""

import numpy as np
import pandas as pd
import pytest

from geocif.cropcal import circular, curve, cv, features, naming, score, transitions


# --------------------------------------------------------------------------
# circular.py
# --------------------------------------------------------------------------
@pytest.mark.parametrize(
    "value,start,end,expected",
    [
        (100, 50, 150, True),      # ordinary interval
        (40, 50, 150, False),
        (50, 50, 150, True),       # inclusive lower
        (150, 50, 150, True),      # inclusive upper
        (5, 350, 20, True),        # wrapped window, early side
        (355, 350, 20, True),      # wrapped window, late side
        (200, 350, 20, False),
    ],
)
def test_check_between_is_circular_and_inclusive(value, start, end, expected):
    assert circular.check_between(value, start, end) is expected


def test_only_one_check_between_exists():
    """The original defined it twice with different return types.

    The first returned an integer width or -1, the second a bool; the later
    definition silently shadowed the earlier at import. Every caller wanted the
    bool, so only that one is ported -- and it must actually return a bool, not
    a truthy int.
    """
    assert isinstance(circular.check_between(10, 0, 20), bool)


@pytest.mark.parametrize(
    "a,b,expected",
    [
        (200, 150, 50),      # ordinary, positive
        (150, 200, -50),     # ordinary, negative
        (10, 360, 15),       # a is 15 days after b, the short way round
        (360, 10, -15),      # and the mirror image keeps its sign
        (100, 100, 0),
    ],
)
def test_signed_difference_wraps_and_keeps_sign(a, b, expected):
    assert circular.signed_difference(a, b) == pytest.approx(expected)


def test_signed_difference_range_is_half_open():
    """Every result lands in (-182, 182] for a 365-day year."""
    for a in range(0, 366, 7):
        for b in range(0, 366, 11):
            d = circular.signed_difference(a, b)
            assert -182 <= d <= 182


def test_legacy_difference_discards_the_sign_when_it_wraps():
    """Reproduced faithfully, and the reason delta_*_signed exists.

    The wrap branch returns ``365 - max + min``, which is non-negative whichever
    way round the pair sits, so half the population has its sign erased.
    """
    assert circular.legacy_difference(10, 360) == 15
    assert circular.legacy_difference(360, 10) == 15     # sign lost
    assert circular.signed_difference(10, 360) == 15
    assert circular.signed_difference(360, 10) == -15    # sign kept
    # Inside the 180-day threshold it is an ordinary signed subtraction.
    assert circular.legacy_difference(200, 150) == 50
    assert circular.legacy_difference(150, 200) == -50


def test_sum_between_is_inclusive_both_ends_and_wraps():
    values = np.ones(366)
    assert circular.sum_between(values, 10, 20) == 11        # inclusive
    assert circular.sum_between(values, 360, 4) == 11        # 360..365 + 0..4


def test_sum_between_ignores_nan():
    values = np.ones(366)
    values[15] = np.nan
    assert circular.sum_between(values, 10, 20) == 10


def test_find_doy_for_gdd_starts_the_day_after_and_wraps():
    """Traversal order is inherited: start+1 .. 365, 1 .. start; day 0 unseen."""
    gdd = np.ones(366)
    assert circular.find_doy_for_gdd(gdd, 0, 10) == 10
    assert circular.find_doy_for_gdd(gdd, 360, 10) == 5   # wraps past new year


def test_find_doy_for_gdd_returns_none_when_unreachable():
    """DEVIATION: the original returned 0, which read as a real date.

    A region too cold to reach its crop's minimum GDD had mid-greendown set to
    day 0 and reported a delta near 365 -- a failure indistinguishable from a
    measurement. None lets the caller leave the date alone and say why.
    """
    assert circular.find_doy_for_gdd(np.zeros(366), 0, 100.0) is None


def test_circular_mask_matches_check_between():
    for start, end in [(50, 150), (350, 20), (0, 365)]:
        mask = circular.circular_mask(366, start, end)
        expected = [circular.check_between(i, start, end) for i in range(366)]
        assert list(mask) == expected


def test_interp_nan_circular_bridges_the_year_boundary():
    values = np.full(10, np.nan)
    values[2] = 0.0
    values[7] = 5.0
    linear = circular.interp_nan(values)
    wrapped = circular.interp_nan(values, circular=True)
    # Linear cannot extrapolate: the tails are flat copies of the end values.
    assert linear[0] == linear[1] == 0.0
    assert linear[8] == linear[9] == 5.0
    # Circular interpolates the other way round instead, so the tails slope.
    assert wrapped[9] != wrapped[8]


# --------------------------------------------------------------------------
# transitions.py
# --------------------------------------------------------------------------
def _bell(centre, width=30.0, n=366):
    doy = np.arange(n)
    return 0.2 + 0.6 * np.exp(-0.5 * ((doy - centre) / width) ** 2)


MAIZE = naming.crop_params("maize")


def test_derivative_transitions_bracket_the_peak():
    """Greenup precedes the peak, greendown follows it."""
    up, down = transitions._derivative_transitions(_bell(200))
    assert up < 200 < down


def test_all_nan_window_raises_rather_than_crashing_obscurely():
    """DEVIATION: the original raised IndexError/ValueError from numpy internals.

    A season window that masks away every finite value now reports a specific,
    catchable error the caller turns into a skip reason.
    """
    with pytest.raises(transitions.TransitionError):
        transitions._derivative_transitions(np.full(366, np.nan))


def test_gdd_clamp_moves_greendown_when_the_season_is_too_hot():
    gdd = np.full(366, 20.0)          # 20 GDD/day -> maize max 2000 in 100 days
    out = transitions.Transitions(midgreenup=100, midgreendown=300)
    moved = transitions._clamp_season_gdd(100, 300, gdd, MAIZE, True, out)
    assert moved < 300
    assert circular.sum_between(gdd, 100, moved) <= MAIZE.max_gdd * 1.05
    assert any("gdd_max" in note for note in out.notes)


def test_gdd_clamp_is_tighter_outside_the_tropics():
    """max_gdd and min_gdd are both scaled by 0.75 for temperate regions."""
    gdd = np.full(366, 20.0)
    tropical = transitions._clamp_season_gdd(
        100, 300, gdd, MAIZE, True, transitions.Transitions(100, 300)
    )
    temperate = transitions._clamp_season_gdd(
        100, 300, gdd, MAIZE, False, transitions.Transitions(100, 300)
    )
    assert temperate < tropical
    assert naming.EXTRATROPICAL_GDD_SCALE == 0.75


def test_gdd_clamp_leaves_the_date_alone_when_the_target_is_unreachable():
    """DEVIATION: this is where the original wrote day 0."""
    out = transitions.Transitions(midgreenup=100, midgreendown=300)
    moved = transitions._clamp_season_gdd(100, 300, np.zeros(366), MAIZE, True, out)
    assert moved == 300
    assert any("never reached" in note for note in out.notes)


def test_gdd100_rule_is_skipped_for_cross_year_greenup():
    """Reproduced: the original computed the cross-year sum and discarded it."""
    out = transitions.Transitions(midgreenup=10, midgreendown=100)
    moved = transitions._enforce_gdd_after_planting(
        10, 300, np.full(366, 20.0), out, fix_offset=False
    )
    assert moved == 10
    assert any("cross-year" in note for note in out.notes)


def test_gdd100_legacy_offset_overshoots_and_the_fix_does_not():
    """The offset is measured from planting but added to greenup.

    Reproduced by default because published numbers depend on it; ``fix_offset``
    anchors it to the planting date, which is what the source comment says the
    rule intends.
    """
    gdd = np.full(366, 10.0)   # 100 GDD takes 10 days
    plant, greenup = 100, 105
    legacy = transitions._enforce_gdd_after_planting(
        greenup, plant, gdd, transitions.Transitions(greenup, 0), fix_offset=False
    )
    fixed = transitions._enforce_gdd_after_planting(
        greenup, plant, gdd, transitions.Transitions(greenup, 0), fix_offset=True
    )
    # 10 GDD/day: the cumulative sum reaches 100 at index 9, i.e. the tenth day
    # counting from planting, so the offset is 9 days.
    assert fixed == plant + 9           # 100 GDD after planting
    assert legacy == greenup + 9        # ... but added to greenup instead
    assert legacy - fixed == greenup - plant


def test_winter_wheat_northern_survives_a_region_with_few_thawing_days():
    """DEVIATION: the original indexed [5] unconditionally -> IndexError."""
    gdd = np.zeros(366)
    gdd[100:103] = 5.0                  # only three days above zero
    out = transitions.Transitions(midgreenup=150, midgreendown=250)
    result = transitions._winter_wheat_northern(150, _bell(200), gdd, out)
    assert result == 150
    assert any("fewer than 6 days" in note for note in out.notes)


def test_winter_wheat_northern_uses_the_sixth_thawing_day_with_a_floor():
    gdd = np.zeros(366)
    gdd[100:130] = 5.0
    out = transitions.Transitions(midgreenup=200, midgreendown=300)
    result = transitions._winter_wheat_northern(200, _bell(250), gdd, out)
    assert result == 105                # sixth positive day, above the day-60 floor
    gdd_early = np.zeros(366)
    gdd_early[10:40] = 5.0
    out2 = transitions.Transitions(midgreenup=200, midgreendown=300)
    assert transitions._winter_wheat_northern(200, _bell(250), gdd_early, out2) == 60


def test_winter_wheat_southern_uses_the_coldest_window():
    gdd = np.full(366, 10.0)
    gdd[200:210] = 0.0                  # coldest ten-day window
    out = transitions.Transitions(midgreenup=0, midgreendown=0)
    assert transitions._winter_wheat_southern(gdd, out) == 200 + transitions.MOVING_WINDOW_SIZE


def test_leading_flat_run_is_inert_on_a_fitted_curve():
    """Reproduced: the constraint it guards never actually fires.

    ``group_consecutives(..., stepsize=0.0)`` tests exact float equality, so on
    a Fourier-fitted curve the leading run is one sample and the caller's
    ``< 30`` guard replaces it with 366.
    """
    assert transitions.leading_flat_run(_bell(200)) == 1
    assert transitions.leading_flat_run(np.array([1.0, 1.0, 1.0, 2.0, 3.0])) == 3


# --------------------------------------------------------------------------
# score.py
# --------------------------------------------------------------------------
@pytest.mark.parametrize(
    "delta,expected", [(0, 1), (15, 1), (15.5, 2), (30, 2), (31, 3), (45, 3), (46, 4)]
)
def test_agreement_classes_are_right_closed(delta, expected):
    """One scheme only. The original also built a left-closed pd.cut set of
    columns that disagreed at every boundary."""
    assert score.agreement_class(delta) == expected


def test_assessment_requires_both_transitions():
    common = dict(
        geoglam={"midgreenup": 100, "midgreendown": 200, "plant": 80, "harvest": 220,
                 "len_stage1": 30, "len_stage2": 60, "len_stage3": 30},
        fitted=_bell(150),
        masked=_bell(150),
        gdd=np.full(366, 5.0),
    )
    both = score.score_region(rs_midgreenup=110, rs_midgreendown=210, **common)
    assert both["Assessment"] == score.ALGO_WORKS
    assert both["Assessment_midgreenup"] == score.ALGO_WORKS

    one = score.score_region(rs_midgreenup=110, rs_midgreendown=10, **common)
    assert np.isnan(one["Assessment"])
    assert one["Assessment_midgreenup"] == score.ALGO_WORKS
    assert np.isnan(one["Assessment_midgreendown"])


def test_algo_works_is_one_because_the_summary_depends_on_it():
    assert score.ALGO_WORKS == 1


def test_circular_correlation_detects_a_shifted_but_ordered_relationship():
    """A constant lag is a perfect circular correlation."""
    days = np.arange(80, 200, 5, dtype=float)
    r2_same, _ = score.circular_r2(days, days)
    r2_shift, _ = score.circular_r2((days + 30) % 365, days)
    r2_noise, _ = score.circular_r2(np.full_like(days, 100.0), days)
    assert r2_same == pytest.approx(1.0, abs=1e-6)
    assert r2_shift == pytest.approx(1.0, abs=1e-6)
    assert np.isnan(r2_noise) or r2_noise < 0.1


def test_circular_correlation_is_degenerate_for_year_spanning_days():
    """A caveat the summary table inherits, pinned so nobody trusts it blindly.

    The statistic is built around the circular mean, which is undefined when the
    days are spread evenly around the year: the resultant vector length goes to
    zero and the "mean angle" becomes numerical noise. A crop whose transitions
    occur in every month therefore gets an r-squared that is not meaningfully
    1 even under a perfect constant lag.
    """
    spread = np.arange(0, 365, 5, dtype=float)
    angles = spread * 2 * np.pi / 365
    resultant = np.hypot(np.sin(angles).sum(), np.cos(angles).sum()) / angles.size
    assert resultant < 1e-6, "test premise: these days are uniform on the circle"

    r2_shift, _ = score.circular_r2((spread + 30) % 365, spread)
    assert r2_shift < 1.0 - 1e-3


# --------------------------------------------------------------------------
# features.py
# --------------------------------------------------------------------------
@pytest.mark.parametrize("day", [0, 1, 90, 182, 300, 364])
def test_day_circle_round_trip(day):
    sin_value, cos_value = features.day_to_circle(day)
    assert features.circle_to_day(sin_value, cos_value) == pytest.approx(day, abs=1e-6)


def test_circular_encoding_makes_new_year_adjacent():
    """The whole reason targets are modelled as (sin, cos)."""
    a = np.array(features.day_to_circle(364))
    b = np.array(features.day_to_circle(1))
    far = np.array(features.day_to_circle(180))
    assert np.linalg.norm(a - b) < np.linalg.norm(a - far)


def test_curve_features_describe_a_single_season():
    values = _bell(200)
    peaks, valleys = curve.detect_peaks_valleys(values)
    out = features.curve_features(values, peaks, valleys)
    assert out["doy_peak"] == pytest.approx(200, abs=2)
    assert out["ndvi_amplitude"] == pytest.approx(0.6, abs=0.01)
    assert out["doy_max_rise"] < out["doy_peak"] < out["doy_max_fall"]


# --------------------------------------------------------------------------
# cv.py
# --------------------------------------------------------------------------
def _cv_frame():
    return pd.DataFrame(
        {
            "country": ["a"] * 4 + ["b"] * 4 + ["c"] * 4,
            "lat": [5, 6, 7, 8] + [45, 46, 47, 48] + [-20, -21, -22, -23],
            "lon": [30, 31, 32, 33] + [2, 3, 4, 5] + [140, 141, 142, 143],
        }
    )


def test_leave_one_country_out_never_shares_a_country():
    schemes = cv.build_schemes(_cv_frame(), n_splits=3)
    frame = _cv_frame()
    for train_idx, test_idx in schemes["country"].splits:
        assert not set(frame.country[train_idx]) & set(frame.country[test_idx])
    assert schemes["country"].n_splits == 3


def test_spatial_blocks_group_by_tile():
    labels = cv.spatial_blocks([5, 6, 45, -20], [30, 31, 2, 140], block_degrees=10.0)
    assert labels[0] == labels[1]      # same 10-degree tile
    assert len({*labels}) == 3


def test_random_kfold_is_flagged_leaky():
    """It is reported precisely so the gap against the spatial schemes is visible."""
    schemes = cv.build_schemes(_cv_frame(), n_splits=3)
    assert schemes["random"].leaky is True
    assert schemes["country"].leaky is False
    assert schemes["spatial_block"].leaky is False


def test_a_scheme_that_cannot_be_built_is_omitted_not_fatal():
    single = pd.DataFrame({"country": ["a", "a"], "lat": [1.0, 1.1], "lon": [2.0, 2.1]})
    schemes = cv.build_schemes(single, n_splits=2)
    assert "country" not in schemes          # only one group
    assert "random" in schemes


# --------------------------------------------------------------------------
# models.py metrics
# --------------------------------------------------------------------------
def test_circular_metrics_handle_the_year_boundary():
    from geocif.cropcal import models

    out = models.circular_metrics([1.0, 364.0], [364.0, 1.0])
    assert out["mae_days"] == pytest.approx(2.0)
    assert out["bias_days"] == pytest.approx(0.0)      # +2 and -2 cancel
    assert out["pct_within_45d"] == 100.0


# --------------------------------------------------------------------------
# models.py: the factory does not fit
# --------------------------------------------------------------------------
def test_fit_one_actually_fits_the_model():
    """Regression: ``auto_train`` builds an estimator, it does not fit it.

    The yield pipeline fits separately through its ``BaseFitter`` hierarchy.
    Omitting that here produced a configured-but-unfitted model for every name
    in the roster, and ``predict`` raised ``NotFittedError`` on the first fold
    of all 2,480 -- catboost, cubist, tabpfn and tabicl alike.
    """
    import inspect

    from geocif.cropcal import models

    source = inspect.getsource(models._fit_one)
    assert "model.fit(" in source, "the estimator returned by auto_train must be fitted"
    # transform_output is global in sklearn; pin-and-restore, never set-and-leak.
    assert 'sklearn.set_config(transform_output="default")' in source
    assert "finally:" in source
    assert "sklearn.set_config(transform_output=previous)" in source


def test_fit_one_round_trips_a_trivial_regression():
    """A fitted model must predict; this is the assertion the probe made."""
    import numpy as np
    import pandas as pd

    from geocif.cropcal import models

    rng = np.random.default_rng(0)
    X = pd.DataFrame(rng.normal(size=(60, 4)), columns=list("abcd"))
    y = pd.Series(2.0 * X["a"] - X["b"])
    model = models._fit_one("linear", X, y, list(X.columns))
    predicted = np.asarray(model.predict(X)).ravel()
    assert np.isfinite(predicted).all()
    assert np.corrcoef(predicted, y)[0, 1] > 0.9
