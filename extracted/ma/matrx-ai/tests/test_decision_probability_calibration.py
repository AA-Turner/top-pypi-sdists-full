"""The probability half of calibration: reliability curve, Brier, threshold.

A perfectly calibrated synthetic set must come back on the diagonal (every
bin's observed accuracy equals its stated probability, ECE 0); an
over-confident one must not. The threshold is the LOWEST cut meeting the
target precision, and the kappa band floor follows the caller's knob.
"""

from __future__ import annotations

import pytest

from matrx_ai.evaluators.calibration import (
    LabeledCase,
    ProbabilityCase,
    brier_score,
    calibrate,
    calibrate_probabilities,
    reliability_bins,
    threshold_for_precision,
)


def _calibrated_set() -> list[ProbabilityCase]:
    """100 answers at each of 0.05, 0.15 … 0.95, right exactly that share of the time."""
    cases: list[ProbabilityCase] = []
    for tenth in range(10):
        p = round(0.05 + tenth / 10, 2)
        right = round(p * 100)
        cases += [ProbabilityCase(probability=p, correct=True)] * right
        cases += [ProbabilityCase(probability=p, correct=False)] * (100 - right)
    return cases


def test_a_perfectly_calibrated_set_is_the_diagonal() -> None:
    report = calibrate_probabilities(_calibrated_set())
    assert report.cases == 1000
    assert len(report.bins) == 10
    for b in report.bins:
        assert b.count == 100
        assert b.observed_accuracy == pytest.approx(b.mean_predicted, abs=1e-9)
        assert b.gap == pytest.approx(0.0, abs=1e-9)
    assert report.expected_calibration_error == pytest.approx(0.0, abs=1e-9)


def test_an_overconfident_set_is_below_the_diagonal() -> None:
    # Says 0.95 every time, right only 60% of the time.
    cases = [ProbabilityCase(probability=0.95, correct=i < 60) for i in range(100)]
    report = calibrate_probabilities(cases)
    (only,) = report.bins
    assert only.observed_accuracy == pytest.approx(0.6)
    assert only.gap == pytest.approx(-0.35)
    assert report.expected_calibration_error == pytest.approx(0.35)
    # Brier of a constant 0.95 against 60% truth: 0.6*0.05^2 + 0.4*0.95^2
    assert report.brier_score == pytest.approx(0.6 * 0.0025 + 0.4 * 0.9025, abs=1e-4)


def test_probability_one_lands_in_the_top_bin() -> None:
    (b,) = reliability_bins([ProbabilityCase(probability=1.0, correct=True)])
    assert (b.lower, b.upper) == (0.9, 1.0)


def test_brier_is_zero_for_certain_and_right_and_none_for_nothing() -> None:
    assert brier_score([ProbabilityCase(probability=1.0, correct=True)]) == 0.0
    assert brier_score([]) is None


def test_threshold_is_the_lowest_cut_that_meets_the_target() -> None:
    cases = (
        [ProbabilityCase(probability=0.5, correct=i < 5) for i in range(10)]  # 50% right
        + [ProbabilityCase(probability=0.8, correct=i < 9) for i in range(10)]  # 90% right
        + [ProbabilityCase(probability=0.95, correct=True) for _ in range(10)]  # 100% right
    )
    rec = threshold_for_precision(cases, target_precision=0.9)
    # p>=0.5 → 24/30 = 0.8 (miss); p>=0.8 → 19/20 = 0.95 (meets) — and 0.8 < 0.95.
    assert rec.threshold == 0.8
    assert rec.precision == pytest.approx(0.95)
    assert rec.coverage == pytest.approx(20 / 30, abs=1e-4)
    assert rec.answers_at_or_above == 20


def test_no_threshold_when_even_the_top_is_wrong_too_often() -> None:
    cases = [ProbabilityCase(probability=0.99, correct=i < 5) for i in range(10)]
    rec = threshold_for_precision(cases, target_precision=0.9)
    assert rec.threshold is None
    assert "target" in rec.note


def test_kappa_band_floor_follows_the_knob() -> None:
    cases = [LabeledCase(judge_verdict=v, authority_verdict=v) for v in ["a", "b"] * 10]
    default = calibrate(cases, judge_key="agent:x")
    assert default.band == "insufficient_data"
    assert "50-200" in default.note
    lowered = calibrate(cases, judge_key="agent:x", min_cases=20)
    assert lowered.band == "production"
    assert lowered.cohens_kappa == 1.0
