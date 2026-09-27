"""Judge calibration — Cohen's kappa over the accuracy ledger.

Research #8 (Arize's protocol, adopted in DECISION-LOG D-14): measure
judge-vs-human agreement with **Cohen's kappa**, not raw agreement. Raw
agreement flatters a lopsided judge — a judge that answers ``better`` every
single time will look 80% accurate on a set where the humans said ``better`` 80%
of the time, while carrying exactly zero information. Kappa subtracts the
agreement you would get by chance from the marginals, which is precisely that
failure.

Reading the number (the adopted bands):

* ``kappa < 0.6``  — not usable as a signal. The judge is not yet a judge.
* ``0.6 - 0.8``   — usable; keep a human in the loop for consequential calls.
* ``> 0.8``       — production.
* ``n < 50``      — no band at all. The protocol wants 50-200 human-labeled
  cases; below 50 this function reports the number AND says it is provisional,
  because a kappa off eight rows is noise with a decimal point.

This is a pure function over ledger rows so it has no ORM, no host, and no
network in it — the host service selects the rows, this decides what they mean.
"""

from __future__ import annotations

from collections import Counter
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

#: Below this many scored rows, a kappa is reported but never banded.
MIN_CASES_FOR_BAND = 50
USABLE_KAPPA = 0.6
PRODUCTION_KAPPA = 0.8

CalibrationBand = Literal["insufficient_data", "not_usable", "usable", "production"]


class LabeledCase(BaseModel):
    """One ledger row that has both a judge verdict and an authoritative one."""

    model_config = ConfigDict(extra="forbid")

    judge_verdict: str
    authority_verdict: str


class Calibration(BaseModel):
    """What the ledger says about one judge (optionally one subject class)."""

    model_config = ConfigDict(extra="forbid")

    judge_key: str
    judge_version: int | None = None
    subject_kind: str | None = None
    cases: int = 0
    raw_agreement: float | None = None
    cohens_kappa: float | None = None
    band: CalibrationBand = "insufficient_data"
    #: judge verdict -> authority verdict -> count. The confusion matrix is the
    #: actionable part: it names WHICH way the judge is wrong.
    confusion: dict[str, dict[str, int]] = Field(default_factory=dict)
    note: str = ""


def cohens_kappa(cases: list[LabeledCase]) -> tuple[float | None, float | None]:
    """Return ``(raw_agreement, cohens_kappa)`` for a set of labeled cases.

    Kappa is ``(po - pe) / (1 - pe)`` where ``po`` is observed agreement and
    ``pe`` is the agreement expected from the two raters' marginals. Returns
    ``(po, None)`` when kappa is undefined — that is ``pe == 1``, which happens
    when both raters used exactly one label and it was the same one. Perfect
    agreement with no variance carries no information, and reporting ``1.0``
    there is the single most misleading thing this function could do.
    """
    n = len(cases)
    if n == 0:
        return None, None
    observed = sum(1 for c in cases if c.judge_verdict == c.authority_verdict)
    po = observed / n

    judge_marginal = Counter(c.judge_verdict for c in cases)
    authority_marginal = Counter(c.authority_verdict for c in cases)
    labels = set(judge_marginal) | set(authority_marginal)
    pe = sum((judge_marginal[x] / n) * (authority_marginal[x] / n) for x in labels)

    if pe >= 1.0:
        return po, None
    return po, (po - pe) / (1.0 - pe)


def _band(
    cases: int, kappa: float | None, *, min_cases: int = MIN_CASES_FOR_BAND
) -> tuple[CalibrationBand, str]:
    if cases < min_cases:
        return (
            "insufficient_data",
            f"{cases} labeled case(s); the calibration protocol wants "
            f"{min_cases}-200 before a band means anything. "
            "Any kappa shown here is provisional.",
        )
    if kappa is None:
        return (
            "insufficient_data",
            "Kappa is undefined: both raters used a single identical label, so there is "
            "no variance to agree about. Collect cases where the verdicts differ.",
        )
    if kappa >= PRODUCTION_KAPPA:
        return "production", "Agreement is at the production bar."
    if kappa >= USABLE_KAPPA:
        return "usable", "Usable as a signal; keep a human on consequential calls."
    return (
        "not_usable",
        "Below the usable bar — this judge's verdicts should not carry routing weight yet. "
        "Read the confusion matrix: it names which direction it is wrong in.",
    )


def calibrate(
    cases: list[LabeledCase],
    *,
    judge_key: str,
    judge_version: int | None = None,
    subject_kind: str | None = None,
    min_cases: int = MIN_CASES_FOR_BAND,
) -> Calibration:
    """Summarize one judge's agreement with authoritative labels.

    ``min_cases`` is the band floor. It defaults to the protocol's 50; a host
    passes its organization's knob (``agents.decision_review /
    min_labels_for_agreement``) so the floor is an org choice, not a constant.
    """
    po, kappa = cohens_kappa(cases)
    band, note = _band(len(cases), kappa, min_cases=min_cases)

    confusion: dict[str, dict[str, int]] = {}
    for case in cases:
        confusion.setdefault(case.judge_verdict, {})
        confusion[case.judge_verdict][case.authority_verdict] = (
            confusion[case.judge_verdict].get(case.authority_verdict, 0) + 1
        )

    return Calibration(
        judge_key=judge_key,
        judge_version=judge_version,
        subject_kind=subject_kind,
        cases=len(cases),
        raw_agreement=round(po, 4) if po is not None else None,
        cohens_kappa=round(kappa, 4) if kappa is not None else None,
        band=band,
        confusion=confusion,
        note=note,
    )


# ─────────────────────────────────────────────────────────────────────────────
# PROBABILITY CALIBRATION — "is 85% confident right 85% of the time?"
#
# Kappa answers "does this judge agree with people beyond chance". A decision
# model also states a PROBABILITY for its answer, and consumers route on that
# number with thresholds, so the second question is whether the number is
# honest: among answers stated at ~0.85, were ~85% right? That is a
# reliability curve (predicted-probability bins vs observed accuracy), its
# one-number summary the Brier score, and the operational answer — the lowest
# threshold at which the answers at or above it met a target precision.
# Pure functions over (probability, correct) pairs; the host selects the rows.
# ─────────────────────────────────────────────────────────────────────────────

#: Equal-width bins across [0, 1]. Ten is the reliability-diagram convention.
DEFAULT_RELIABILITY_BINS = 10


class ProbabilityCase(BaseModel):
    """One labeled answer: the probability the model gave it, and whether it was right."""

    model_config = ConfigDict(extra="forbid")

    probability: float = Field(ge=0.0, le=1.0)
    correct: bool


class ReliabilityBin(BaseModel):
    """One bin of the reliability curve. Empty bins are omitted, never zero-filled."""

    model_config = ConfigDict(extra="forbid")

    lower: float
    upper: float
    count: int
    mean_predicted: float
    observed_accuracy: float
    #: observed - predicted. Negative = over-confident in this band.
    gap: float


class ThresholdRecommendation(BaseModel):
    """The lowest cut whose answers at or above it met the target precision."""

    model_config = ConfigDict(extra="forbid")

    target_precision: float
    threshold: float | None = None
    precision: float | None = None
    #: Share of labeled answers at or above the threshold (what would auto-pass).
    coverage: float | None = None
    answers_at_or_above: int = 0
    note: str = ""


class ProbabilityCalibration(BaseModel):
    """Reliability curve + Brier + expected calibration error + threshold."""

    model_config = ConfigDict(extra="forbid")

    cases: int = 0
    accuracy: float | None = None
    mean_predicted: float | None = None
    brier_score: float | None = None
    #: Count-weighted mean |gap| across bins (ECE).
    expected_calibration_error: float | None = None
    bins: list[ReliabilityBin] = Field(default_factory=list)
    recommended_threshold: ThresholdRecommendation | None = None


def reliability_bins(
    cases: list[ProbabilityCase], *, bins: int = DEFAULT_RELIABILITY_BINS
) -> list[ReliabilityBin]:
    """Group cases into equal-width probability bins; 1.0 falls in the top bin."""
    if bins < 1:
        raise ValueError("reliability_bins needs at least one bin")
    grouped: dict[int, list[ProbabilityCase]] = {}
    for case in cases:
        index = min(int(case.probability * bins), bins - 1)
        grouped.setdefault(index, []).append(case)
    out: list[ReliabilityBin] = []
    for index in sorted(grouped):
        members = grouped[index]
        predicted = sum(c.probability for c in members) / len(members)
        observed = sum(1 for c in members if c.correct) / len(members)
        out.append(
            ReliabilityBin(
                lower=round(index / bins, 4),
                upper=round((index + 1) / bins, 4),
                count=len(members),
                mean_predicted=round(predicted, 4),
                observed_accuracy=round(observed, 4),
                gap=round(observed - predicted, 4),
            )
        )
    return out


def brier_score(cases: list[ProbabilityCase]) -> float | None:
    """Mean squared gap between stated probability and outcome. 0 is perfect."""
    if not cases:
        return None
    return sum((c.probability - (1.0 if c.correct else 0.0)) ** 2 for c in cases) / len(cases)


def threshold_for_precision(
    cases: list[ProbabilityCase], *, target_precision: float
) -> ThresholdRecommendation:
    """The LOWEST stated probability t such that answers with p >= t were right
    at least ``target_precision`` of the time. Lowest, because every step up
    sends more answers to a person; the point is the cheapest honest cut.
    """
    if not cases:
        return ThresholdRecommendation(
            target_precision=target_precision, note="No labeled answers yet."
        )
    candidates = sorted({c.probability for c in cases})
    total = len(cases)
    for cut in candidates:
        above = [c for c in cases if c.probability >= cut]
        precision = sum(1 for c in above if c.correct) / len(above)
        if precision >= target_precision:
            return ThresholdRecommendation(
                target_precision=target_precision,
                threshold=round(cut, 4),
                precision=round(precision, 4),
                coverage=round(len(above) / total, 4),
                answers_at_or_above=len(above),
            )
    return ThresholdRecommendation(
        target_precision=target_precision,
        note="No threshold reaches the target: even the most confident answers were wrong too often.",
    )


def calibrate_probabilities(
    cases: list[ProbabilityCase],
    *,
    bins: int = DEFAULT_RELIABILITY_BINS,
    target_precision: float = 0.9,
) -> ProbabilityCalibration:
    """Everything the calibration view shows for one (version, question) group."""
    if not cases:
        return ProbabilityCalibration(
            recommended_threshold=threshold_for_precision(cases, target_precision=target_precision)
        )
    curve = reliability_bins(cases, bins=bins)
    total = len(cases)
    ece = sum(b.count * abs(b.gap) for b in curve) / total
    brier = brier_score(cases)
    return ProbabilityCalibration(
        cases=total,
        accuracy=round(sum(1 for c in cases if c.correct) / total, 4),
        mean_predicted=round(sum(c.probability for c in cases) / total, 4),
        brier_score=round(brier, 4) if brier is not None else None,
        expected_calibration_error=round(ece, 4),
        bins=curve,
        recommended_threshold=threshold_for_precision(cases, target_precision=target_precision),
    )


__all__ = [
    "DEFAULT_RELIABILITY_BINS",
    "MIN_CASES_FOR_BAND",
    "ProbabilityCalibration",
    "ProbabilityCase",
    "ReliabilityBin",
    "ThresholdRecommendation",
    "brier_score",
    "calibrate_probabilities",
    "reliability_bins",
    "threshold_for_precision",
    "PRODUCTION_KAPPA",
    "USABLE_KAPPA",
    "Calibration",
    "CalibrationBand",
    "LabeledCase",
    "calibrate",
    "cohens_kappa",
]
