"""Metric functions for the eval harness -- Phase 1 ships M1 + M2.

Status precision (M1) and status recall (M2) operate on the gap
agent's `ksi_classifications[]` output and the per-fixture ground-
truth `expected_classifications`. Each returns a 0-1 score.

KSIs the fixture didn't label (`acceptable_statuses` returns None)
are SKIPPED in both precision and recall -- they neither help nor hurt
the score. This lets fixture authors lock down high-confidence KSIs
without committing to label every unlabeled KSI as a side effect.

Per the DECISIONS entry, day-one bar is "metrics compute and produce
useful baseline numbers against the 3 fixtures." Hard-blocking on
metric regression is Phase 3 work after the noise floor is calibrated.
"""

from __future__ import annotations

from dataclasses import dataclass

from evals.ground_truth import GroundTruth

# Status ordering used by the over- vs under-classification decision.
# Higher index = more positive verdict. Matches the gap agent's
# semantic ranking: `implemented` is the most-positive verdict;
# `not_applicable` is the most-explicit-skip.
_STATUS_RANK = {
    "implemented": 4,
    "partial": 3,
    "not_implemented": 2,
    "evidence_layer_inapplicable": 1,
    "not_applicable": 0,
}


@dataclass(frozen=True)
class MetricResult:
    """One metric evaluation against one fixture run.

    `score` is the 0-1 numeric value. `numerator` / `denominator` are
    the raw counts so a future trend dashboard can show "5 of 12
    classifications correct" rather than just "0.42." `notes` is a
    short human-readable diagnostic string (e.g. naming the KSIs that
    drove the score).
    """

    name: str
    score: float
    numerator: int
    denominator: int
    notes: str = ""

    @classmethod
    def from_counts(
        cls,
        name: str,
        numerator: int,
        denominator: int,
        notes: str = "",
    ) -> MetricResult:
        """Construct from raw counts. Score is 0.0 if denominator is 0
        (empty fixture coverage; surfaces as a 0-score with a note).
        """
        score = (numerator / denominator) if denominator > 0 else 0.0
        return cls(
            name=name, score=score, numerator=numerator, denominator=denominator, notes=notes
        )


def _is_over_classification(actual: str, acceptable: set[str]) -> bool:
    """Actual status is more positive than the most-positive acceptable.

    Over-classification = the agent claimed more than ground truth
    says is warranted (e.g., agent said `implemented`, ground-truth
    accepts `partial`). Hits status-precision negatively.
    """
    actual_rank = _STATUS_RANK.get(actual, -1)
    max_acceptable_rank = max(_STATUS_RANK.get(s, -1) for s in acceptable)
    return actual_rank > max_acceptable_rank


def _is_under_classification(actual: str, acceptable: set[str]) -> bool:
    """Actual status is more negative than the most-negative acceptable.

    Under-classification = the agent claimed less than ground truth
    says it should have (e.g., agent said `not_implemented`,
    ground-truth accepts `partial`). Hits status-recall negatively.
    The KSI-SVC-PRR drift in v0.1.7→v0.1.8 surfaces this way.
    """
    actual_rank = _STATUS_RANK.get(actual, -1)
    min_acceptable_rank = min(_STATUS_RANK.get(s, 99) for s in acceptable)
    return actual_rank < min_acceptable_rank


def status_precision(
    gap_classifications: dict[str, str],
    ground_truth: GroundTruth,
) -> MetricResult:
    """M1: status precision.

    `hits / (hits + over_classifications)`. A "hit" is the actual
    status being in the acceptable-statuses set. An over-classification
    is the actual status being MORE POSITIVE than any acceptable status.

    Args:
      gap_classifications: dict of `KSI-id → status` from the gap
        agent's report (read by the harness from
        `.efterlev/reports/gap-*.json`).
      ground_truth: loaded ground-truth fixture.

    Returns:
      MetricResult with score, numerator (hits), denominator
      (hits + over_classifications), and a notes string naming the
      over-classified KSIs (capped to 5 for log brevity).
    """
    hits = 0
    over: list[str] = []

    for ksi_id, actual in gap_classifications.items():
        acceptable = ground_truth.acceptable_statuses(ksi_id)
        if acceptable is None:
            continue  # unlabeled KSI; skip
        if actual in acceptable:
            hits += 1
        elif _is_over_classification(actual, acceptable):
            over.append(f"{ksi_id}({actual} > {sorted(acceptable)})")

    denom = hits + len(over)
    notes = ""
    if over:
        notes = f"over-classified: {', '.join(over[:5])}"
        if len(over) > 5:
            notes += f" (+{len(over) - 5} more)"
    return MetricResult.from_counts("status_precision", hits, denom, notes)


def status_recall(
    gap_classifications: dict[str, str],
    ground_truth: GroundTruth,
) -> MetricResult:
    """M2: status recall.

    `hits / (hits + under_classifications)`. An under-classification is
    the actual status being MORE NEGATIVE than any acceptable status.

    KSI-SVC-PRR's v0.1.7→v0.1.8 drift (correctly `partial` then
    incorrectly `evidence_layer_inapplicable`) surfaces here as a
    recall regression on the same fixture across releases.

    Args:
      gap_classifications: dict of `KSI-id → status`.
      ground_truth: loaded ground-truth fixture.

    Returns:
      MetricResult.
    """
    hits = 0
    under: list[str] = []

    for ksi_id, actual in gap_classifications.items():
        acceptable = ground_truth.acceptable_statuses(ksi_id)
        if acceptable is None:
            continue  # unlabeled KSI; skip
        if actual in acceptable:
            hits += 1
        elif _is_under_classification(actual, acceptable):
            under.append(f"{ksi_id}({actual} < {sorted(acceptable)})")

    denom = hits + len(under)
    notes = ""
    if under:
        notes = f"under-classified: {', '.join(under[:5])}"
        if len(under) > 5:
            notes += f" (+{len(under) - 5} more)"
    return MetricResult.from_counts("status_recall", hits, denom, notes)


# ---- M3: resource-naming rate (PR beta) -----------------------------------


_M3_NEUTRAL_STATUSES = frozenset({"evidence_layer_inapplicable", "not_applicable"})


def resource_naming_rate(
    gap_rationales: dict[str, str],
    gap_classifications: dict[str, str],
    ground_truth: GroundTruth,
) -> MetricResult:
    """M3: resource-naming rate (narrative quality).

    For each KSI the fixture expects to name specific resources, check
    whether the gap-agent's rationale mentions AT LEAST ONE of the
    named resources (exact-substring match). Score is the fraction of
    expected-resource rationales that meet the bar.

    Catches the bug class from the v0.1.5-0.1.9 shakedowns where 30
    of 60 narratives still cited evidence by `sha256:abc12345...`
    inline instead of by the human-readable `resource_name` available
    in the cited Evidence's content. Pre-eval-harness this required
    eyeballing 60 KSIs per release; M3 makes it a number.

    Skip rules (excluded from the denominator):
    - KSIs the agent didn't classify at all (M2's territory).
    - KSIs the agent classified as `evidence_layer_inapplicable` or
      `not_applicable`. These rationales legitimately explain
      structural absence ("no IaC surface for this KSI's controls")
      rather than naming specific resources, so the resource-naming
      bar doesn't apply. Without this skip, fixture authors would
      have to coordinate `expected_rationale_resources` labels with
      every alternation in `expected_classifications` — a fragile
      constraint that pre-2026-05-09 forced choreography on
      govnotes-v1 rev 4 and encryption-mixed rev 2 (DECISIONS
      2026-05-09 follow-up).

    Args:
      gap_rationales: dict of `KSI-id -> rationale string` extracted
        from the gap report's `ksi_classifications[]`.
      gap_classifications: dict of `KSI-id -> status string` from the
        same source; used to skip ELI/NA per the rule above.
      ground_truth: loaded ground-truth fixture.

    Returns:
      MetricResult. Denominator is the count of labeled KSIs whose
      gap rationale was emitted AND whose classification is
      resource-naming-relevant (not ELI / NA).
    """
    if not ground_truth.expected_rationale_resources:
        return MetricResult.from_counts(
            "resource_naming_rate", 0, 0, "no expected_rationale_resources labeled"
        )

    hits = 0
    misses: list[str] = []
    skipped_neutral: list[str] = []

    for ksi_id, expected_resources in ground_truth.expected_rationale_resources.items():
        if not expected_resources:
            continue
        rationale = gap_rationales.get(ksi_id)
        if rationale is None:
            continue
        status = gap_classifications.get(ksi_id)
        if status in _M3_NEUTRAL_STATUSES:
            skipped_neutral.append(ksi_id)
            continue
        # 2026-05-09: case-insensitive matching. The 5-run noise-floor
        # study revealed that ~half of M3's "misses" were actually
        # capitalization mismatches (rationale says "HTTPS"; label said
        # "https"). The original case-sensitive matcher was a fixture-
        # quality trap, not a real model gap.
        rationale_lower = rationale.lower()
        if any(name.lower() in rationale_lower for name in expected_resources):
            hits += 1
        else:
            misses.append(f"{ksi_id}(none of {expected_resources[:3]})")

    denom = hits + len(misses)
    note_parts: list[str] = []
    if misses:
        miss_str = f"resource-name miss: {', '.join(misses[:5])}"
        if len(misses) > 5:
            miss_str += f" (+{len(misses) - 5} more)"
        note_parts.append(miss_str)
    if skipped_neutral:
        note_parts.append(
            f"skipped {len(skipped_neutral)} KSI(s) classified as ELI/NA: "
            f"{', '.join(skipped_neutral[:5])}"
            + (f" (+{len(skipped_neutral) - 5} more)" if len(skipped_neutral) > 5 else "")
        )
    return MetricResult.from_counts("resource_naming_rate", hits, denom, "; ".join(note_parts))


# ---- M4: manifest-quoting accuracy (PR beta) -------------------------------


def manifest_quoting_accuracy(
    doc_narratives: dict[str, str],
    ground_truth: GroundTruth,
) -> MetricResult:
    """M4: manifest-quoting accuracy.

    For each KSI the fixture expects to quote from a specific manifest,
    check whether the documentation-agent's narrative for that KSI
    contains AT LEAST ONE of the expected substrings. Catches the F5
    cross-wiring bug from v0.1.8 where KSI-AFR-FSI's narrative quoted
    PagerDuty (which belongs to KSI-INR-RIR's manifest) and KSI-INR-RIR
    didn't quote PagerDuty even though that's its OWN manifest.

    Args:
      doc_narratives: dict of `KSI-id -> narrative string` extracted
        from the documentation report's `attestations[]`.
      ground_truth: loaded ground-truth fixture.

    Returns:
      MetricResult. Same skip-don't-penalize semantics as M3 for KSIs
      where the agent produced no narrative.
    """
    if not ground_truth.expected_manifest_quoting:
        return MetricResult.from_counts(
            "manifest_quoting_accuracy", 0, 0, "no expected_manifest_quoting labeled"
        )

    hits = 0
    misses: list[str] = []

    for ksi_id, expected_quotes in ground_truth.expected_manifest_quoting.items():
        if not expected_quotes:
            continue
        narrative = doc_narratives.get(ksi_id)
        if narrative is None:
            continue
        if any(quote in narrative for quote in expected_quotes):
            hits += 1
        else:
            misses.append(f"{ksi_id}(none of {expected_quotes[:3]})")

    denom = hits + len(misses)
    notes = ""
    if misses:
        notes = f"manifest-quote miss: {', '.join(misses[:5])}"
        if len(misses) > 5:
            notes += f" (+{len(misses) - 5} more)"
    return MetricResult.from_counts("manifest_quoting_accuracy", hits, denom, notes)


# ---- M5: POAM scope discipline (PR gamma) ---------------------------------

import re  # noqa: E402  -- after the metric defs to keep them grouped

_POAM_EXCLUDED_RE = re.compile(
    r"\*\*Excluded as out-of-boundary:\*\*\s+(\d+)\s+item",
)


def poam_scope_discipline(
    poam_markdown: str,
    ground_truth: GroundTruth,
) -> MetricResult:
    """M5: POAM scope discipline.

    Two checks combined into a 0-2-scale score normalized to 0-1:

      Check A (boolean): no `must_not_mention` substring appears in
        the POAM markdown body. Catches boundary-leak regressions
        where out-of-boundary resource names slip into in-boundary
        narrative.

      Check B (range): the actual `out-of-boundary excluded` count
        falls within `expected_poam.excluded_count_min` /
        `excluded_count_max`. Catches "boundary check disappeared"
        regressions where post-v0.1.8 the POAM stops reporting
        excluded counts at all.

    Score is `(check_a + check_b) / 2`. Both pass = 1.0; one passes
    = 0.5; both fail = 0.0. The notes string names which check failed
    and what was found.
    """
    expected = ground_truth.expected_poam

    # Check A: must_not_mention substrings.
    leaked = [s for s in expected.must_not_mention if s in poam_markdown]
    check_a_pass = not leaked

    # Check B: excluded count in range. Absent header line means count
    # is 0 (the body only adds the bullet when count > 0; that's the
    # POAM generator's contract per generate_poam_markdown.py).
    match = _POAM_EXCLUDED_RE.search(poam_markdown)
    actual_excluded = int(match.group(1)) if match else 0
    check_b_pass = expected.excluded_count_min <= actual_excluded <= expected.excluded_count_max

    notes_parts = []
    if not check_a_pass:
        # Cap leak diagnostic at 3 substrings for log brevity.
        notes_parts.append(f"boundary-leak: {leaked[:3]}")
    if not check_b_pass:
        notes_parts.append(
            f"excluded count {actual_excluded} outside "
            f"[{expected.excluded_count_min}, {expected.excluded_count_max}]"
        )
    notes = "; ".join(notes_parts)

    # M5's denominator is conceptually 2 (two checks); numerator is
    # the count of passing checks. MetricResult.from_counts handles
    # the division.
    return MetricResult.from_counts(
        "poam_scope_discipline",
        int(check_a_pass) + int(check_b_pass),
        2,
        notes,
    )
