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


def _band(cases: int, kappa: float | None) -> tuple[CalibrationBand, str]:
    if cases < MIN_CASES_FOR_BAND:
        return (
            "insufficient_data",
            f"{cases} labeled case(s); the calibration protocol wants "
            f"{MIN_CASES_FOR_BAND}-200 before a band means anything. "
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
) -> Calibration:
    """Summarize one judge's agreement with authoritative labels."""
    po, kappa = cohens_kappa(cases)
    band, note = _band(len(cases), kappa)

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


__all__ = [
    "MIN_CASES_FOR_BAND",
    "PRODUCTION_KAPPA",
    "USABLE_KAPPA",
    "Calibration",
    "CalibrationBand",
    "LabeledCase",
    "calibrate",
    "cohens_kappa",
]
