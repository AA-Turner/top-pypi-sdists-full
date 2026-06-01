"""Tests for M1 (status precision), M2 (status recall),
M3 (resource-naming rate), M4 (manifest-quoting accuracy),
M5 (POAM scope discipline).
"""

from __future__ import annotations

from evals.ground_truth import GroundTruth, POAMExpectations
from evals.metrics import (
    manifest_quoting_accuracy,
    poam_scope_discipline,
    resource_naming_rate,
    status_precision,
    status_recall,
)


def _gt(**classifications: str) -> GroundTruth:
    """Build a GroundTruth from kwargs (no YAML round-trip)."""
    return GroundTruth(
        fixture_id="test",
        description="test",
        authored_by="t@e",
        authored_at="2026-05-08",
        revision=1,
        frmr_version="0.9.43-beta",
        expected_classifications=dict(classifications),
    )


def _gt_with_extras(
    *,
    expected_rationale_resources: dict[str, list[str]] | None = None,
    expected_manifest_quoting: dict[str, list[str]] | None = None,
) -> GroundTruth:
    """Build a GroundTruth with M3/M4 expectation maps. Used by the
    PR beta tests that exercise resource-naming + manifest-quoting."""
    return GroundTruth(
        fixture_id="test",
        description="test",
        authored_by="t@e",
        authored_at="2026-05-08",
        revision=1,
        frmr_version="0.9.43-beta",
        expected_rationale_resources=expected_rationale_resources or {},
        expected_manifest_quoting=expected_manifest_quoting or {},
    )


# --- M1: status precision ----------------------------------------------------


def test_precision_perfect_score_when_all_match() -> None:
    """Every KSI's actual status matches the expected -- precision 1.0,
    no over-classifications, denominator equals hits."""
    gt = _gt(
        **{
            "KSI-IAM-MFA": "partial",
            "KSI-SVC-VRI": "implemented",
            "KSI-CMT-RVP": "evidence_layer_inapplicable",
        }
    )
    actual = {
        "KSI-IAM-MFA": "partial",
        "KSI-SVC-VRI": "implemented",
        "KSI-CMT-RVP": "evidence_layer_inapplicable",
    }
    m = status_precision(actual, gt)
    assert m.score == 1.0
    assert m.numerator == 3
    assert m.denominator == 3


def test_precision_drops_on_over_classification() -> None:
    """Agent claimed `implemented` for a KSI ground-truth labels as
    `partial`. Over-classification: counts in the denominator but
    not the numerator. 1 hit + 1 over = precision 0.5."""
    gt = _gt(
        **{
            "KSI-IAM-MFA": "partial",  # agent over-claims here
            "KSI-SVC-VRI": "implemented",
        }
    )
    actual = {
        "KSI-IAM-MFA": "implemented",  # over (4 > 3)
        "KSI-SVC-VRI": "implemented",  # hit
    }
    m = status_precision(actual, gt)
    assert m.score == 0.5
    assert m.numerator == 1
    assert m.denominator == 2
    assert "KSI-IAM-MFA" in m.notes  # diagnostic names the offender


def test_precision_does_not_penalize_under_classification() -> None:
    """Under-classification (agent said `not_implemented`, gt says
    `partial`) is recall's problem, not precision's. Precision should
    be unchanged. Lock the asymmetry."""
    gt = _gt(
        **{
            "KSI-IAM-MFA": "partial",
            "KSI-SVC-VRI": "implemented",
        }
    )
    actual = {
        "KSI-IAM-MFA": "not_implemented",  # under (2 < 3) -- invisible to precision
        "KSI-SVC-VRI": "implemented",  # hit
    }
    m = status_precision(actual, gt)
    # Under-classification doesn't count as over-class, so denom = 1 hit.
    assert m.score == 1.0
    assert m.numerator == 1
    assert m.denominator == 1


def test_precision_skips_unlabeled_ksis() -> None:
    """KSIs without a ground-truth label are skipped in metric
    calculation -- they neither help nor hurt the score."""
    gt = _gt(**{"KSI-IAM-MFA": "partial"})
    actual = {
        "KSI-IAM-MFA": "partial",  # hit
        "KSI-NEVER-LABELED": "implemented",  # skipped
    }
    m = status_precision(actual, gt)
    assert m.numerator == 1
    assert m.denominator == 1
    assert m.score == 1.0


def test_precision_accepts_status_alternation() -> None:
    """A KSI labeled `partial|not_implemented` accepts EITHER status
    as a hit. Procedural-only KSIs without manifests (like KSI-CMT-RVP
    in govnotes-v1) typically use this pattern."""
    gt = _gt(
        **{
            "KSI-CMT-RVP": "evidence_layer_inapplicable|not_applicable",
        }
    )
    # Both should hit:
    for actual_status in ("evidence_layer_inapplicable", "not_applicable"):
        m = status_precision({"KSI-CMT-RVP": actual_status}, gt)
        assert m.score == 1.0, f"{actual_status!r} should hit"


def test_precision_zero_denominator_returns_zero_score() -> None:
    """If no labeled KSIs match the agent's output (empty denominator),
    score is 0.0. Edge case but should not throw."""
    gt = _gt(**{"KSI-IAM-MFA": "partial"})
    actual: dict[str, str] = {}  # agent emitted nothing
    m = status_precision(actual, gt)
    assert m.score == 0.0
    assert m.denominator == 0


# --- M2: status recall -------------------------------------------------------


def test_recall_perfect_when_all_match() -> None:
    """Mirror of precision-perfect."""
    gt = _gt(**{"KSI-IAM-MFA": "partial", "KSI-SVC-VRI": "implemented"})
    actual = {"KSI-IAM-MFA": "partial", "KSI-SVC-VRI": "implemented"}
    m = status_recall(actual, gt)
    assert m.score == 1.0


def test_recall_drops_on_under_classification() -> None:
    """The KSI-SVC-PRR v0.1.7→v0.1.8 drift case: agent went from
    `partial` to `evidence_layer_inapplicable`. Under-classification:
    counts in denominator but not numerator. This is precisely the
    bug class M2 exists to catch."""
    gt = _gt(
        **{
            "KSI-SVC-PRR": "partial",  # ground truth
        }
    )
    actual = {
        "KSI-SVC-PRR": "evidence_layer_inapplicable",  # under (1 < 3)
    }
    m = status_recall(actual, gt)
    assert m.score == 0.0
    assert m.numerator == 0
    assert m.denominator == 1
    assert "KSI-SVC-PRR" in m.notes


def test_recall_does_not_penalize_over_classification() -> None:
    """Over-classification is precision's problem, not recall's. Lock
    the asymmetry from the other direction."""
    gt = _gt(
        **{
            "KSI-IAM-MFA": "partial",
        }
    )
    actual = {
        "KSI-IAM-MFA": "implemented",  # over (4 > 3) -- invisible to recall
    }
    m = status_recall(actual, gt)
    assert m.numerator == 0
    assert m.denominator == 0  # neither hit nor under-class
    assert m.score == 0.0  # zero-denom → 0.0 by convention


def test_recall_skips_unlabeled_ksis() -> None:
    """Mirror of precision-skips-unlabeled."""
    gt = _gt(**{"KSI-IAM-MFA": "partial"})
    actual = {
        "KSI-IAM-MFA": "partial",
        "KSI-NEVER-LABELED": "not_implemented",
    }
    m = status_recall(actual, gt)
    assert m.score == 1.0


# --- A/B regression locks (the v0.1.7→v0.1.8 bug shapes) ---------------------


def test_locks_v0_1_7_to_v0_1_8_ksi_svc_prr_drift_pattern() -> None:
    """Reproduces the drift bug shape from the doc/v0.2-eval-harness-
    plan.md: same KSI, two consecutive runs, status flips from
    `partial` (correct) to `evidence_layer_inapplicable` (under-
    classified). Pre-eval-harness: silently shipped. Post-harness:
    M2 recall flips from 1.0 → 0.0 on the regressed run."""
    gt = _gt(**{"KSI-SVC-PRR": "partial"})

    v0_1_7_actual = {"KSI-SVC-PRR": "partial"}
    v0_1_8_actual = {"KSI-SVC-PRR": "evidence_layer_inapplicable"}

    m_pre = status_recall(v0_1_7_actual, gt)
    m_post = status_recall(v0_1_8_actual, gt)

    assert m_pre.score == 1.0, "v0.1.7 baseline should hit"
    assert m_post.score == 0.0, "v0.1.8 regression should flip M2 to 0"
    # The metric drop is the signal a maintainer would see in CI.
    assert m_pre.score - m_post.score == 1.0


def test_locks_v0_1_7_ksi_scr_mit_mixed_reasoning_bug() -> None:
    """Reproduces the v0.1.7 KSI-SCR-MIT bug shape: agent correctly
    identifies a "mixed" pin posture but classifies the KSI as
    `not_implemented` instead of `partial`. Under-classification;
    M2 catches it."""
    gt = _gt(**{"KSI-SCR-MIT": "partial"})
    v0_1_7_actual = {"KSI-SCR-MIT": "not_implemented"}

    m = status_recall(v0_1_7_actual, gt)
    assert m.score == 0.0
    assert "KSI-SCR-MIT" in m.notes


# --- M3: resource-naming rate ------------------------------------------------


def test_m3_perfect_when_rationale_names_an_expected_resource() -> None:
    """The basic happy path: rationale mentions one of the expected
    resource names. Score 1.0."""
    gt = _gt_with_extras(
        expected_rationale_resources={"KSI-SVC-VRI": ["app_uploads", "legacy_export"]},
    )
    rationales = {
        "KSI-SVC-VRI": "The app_uploads bucket has KMS encryption configured.",
    }
    classifications = {"KSI-SVC-VRI": "partial"}
    m = resource_naming_rate(rationales, classifications, gt)
    assert m.score == 1.0
    assert m.numerator == 1
    assert m.denominator == 1


def test_m3_drops_when_rationale_uses_sha256_instead_of_resource_name() -> None:
    """Reproduces the v0.1.5-0.1.9 bug class the M3 metric exists to
    catch: rationale cites evidence by sha256 instead of the human-
    readable resource_name. Score 0.0."""
    gt = _gt_with_extras(
        expected_rationale_resources={"KSI-SVC-VRI": ["app_uploads", "legacy_export"]},
    )
    rationales = {
        "KSI-SVC-VRI": "Evidence sha256:abc12345... shows partial coverage.",
    }
    classifications = {"KSI-SVC-VRI": "partial"}
    m = resource_naming_rate(rationales, classifications, gt)
    assert m.score == 0.0
    assert "KSI-SVC-VRI" in m.notes
    assert "app_uploads" in m.notes  # diagnostic surfaces what was expected


def test_m3_skips_ksi_with_no_emitted_rationale() -> None:
    """If the agent didn't produce a rationale for an expected KSI,
    M3 skips it (M2's territory). Don't double-penalize."""
    gt = _gt_with_extras(
        expected_rationale_resources={
            "KSI-SVC-VRI": ["app_uploads"],
            "KSI-CNA-MAT": ["public_assets"],
        },
    )
    rationales = {
        "KSI-SVC-VRI": "app_uploads is encrypted",  # hit
        # KSI-CNA-MAT skipped by agent -- not in dict
    }
    classifications = {"KSI-SVC-VRI": "partial"}
    m = resource_naming_rate(rationales, classifications, gt)
    assert m.score == 1.0  # only the emitted KSI counts
    assert m.denominator == 1


def test_m3_returns_zero_when_no_expected_rationale_resources_labeled() -> None:
    """A fixture with no M3 expectations should return a 0/0 score
    with an explanatory note rather than crashing."""
    gt = _gt_with_extras(expected_rationale_resources={})
    m = resource_naming_rate({"KSI-FOO": "anything"}, {"KSI-FOO": "partial"}, gt)
    assert m.score == 0.0
    assert m.denominator == 0
    assert "no expected_rationale_resources" in m.notes


def test_m3_first_match_wins_with_multi_resource_label() -> None:
    """Multi-resource labels: at-least-one-name suffices. The
    rationale doesn't have to mention every named resource, just one."""
    gt = _gt_with_extras(
        expected_rationale_resources={
            "KSI-SVC-VRI": ["app_uploads", "legacy_export", "temp_data_pipeline"],
        },
    )
    # Only mentions one of three -- still a hit.
    rationales = {"KSI-SVC-VRI": "temp_data_pipeline lacks encryption."}
    classifications = {"KSI-SVC-VRI": "partial"}
    m = resource_naming_rate(rationales, classifications, gt)
    assert m.score == 1.0


def test_m3_is_case_insensitive_2026_05_09_fix() -> None:
    """2026-05-09 fix: M3's substring matcher is case-insensitive.
    The 5-run noise-floor study revealed that ~half of M3's reported
    misses were actually capitalization mismatches -- the rationale
    said "HTTPS" while the label said "https". Pre-fix this counted
    as a miss; post-fix it counts as a hit. Lock the contract.
    """
    gt = _gt_with_extras(
        expected_rationale_resources={
            "KSI-SVC-VRI": ["https", "TLS"],
        },
    )
    rationales = {
        "KSI-SVC-VRI": "The HTTPS listener uses tls 1.3 with FIPS-compliant ciphers.",
    }
    classifications = {"KSI-SVC-VRI": "partial"}
    m = resource_naming_rate(rationales, classifications, gt)
    assert m.score == 1.0
    assert m.numerator == 1


def test_m3_case_insensitivity_does_not_match_partial_words() -> None:
    """Defense-in-depth: case-insensitive matching MUST still be
    substring-based. Lock that mixed-case identifiers ('Admin_With_MFA')
    still match a lowercase label ('admin_with_mfa').
    """
    gt = _gt_with_extras(
        expected_rationale_resources={"KSI-IAM-MFA": ["admin_with_mfa"]},
    )
    rationales = {"KSI-IAM-MFA": "The Admin_With_MFA policy is in place."}
    classifications = {"KSI-IAM-MFA": "partial"}
    m = resource_naming_rate(rationales, classifications, gt)
    assert m.score == 1.0


def test_m3_skips_eli_classified_ksi_2026_05_09_fix() -> None:
    """2026-05-09 follow-up to PR #189: when the agent classifies a
    KSI as `evidence_layer_inapplicable`, its rationale legitimately
    explains structural absence rather than naming resources. M3
    should skip these (excluded from the denominator) instead of
    counting them as misses. Without this skip, fixture authors would
    have to coordinate every M3 label with every status alternation
    in expected_classifications -- the choreography that
    govnotes-v1 rev 4 + encryption-mixed rev 2 had to do manually.
    """
    gt = _gt_with_extras(
        expected_rationale_resources={
            "KSI-CNA-MAT": ["app_lb", "bastion_open"],
            "KSI-SVC-VRI": ["https", "TLS"],
        },
    )
    rationales = {
        # Hits
        "KSI-SVC-VRI": "The HTTPS listener uses TLS 1.3.",
        # ELI rationale -- talks about structural absence, no resource names
        "KSI-CNA-MAT": (
            "KSI-CNA-MAT's controls are pure-procedural; the scanner has "
            "no IaC surface for this KSI."
        ),
    }
    classifications = {
        "KSI-SVC-VRI": "partial",
        "KSI-CNA-MAT": "evidence_layer_inapplicable",  # skipped by M3
    }
    m = resource_naming_rate(rationales, classifications, gt)
    assert m.score == 1.0  # only the partial-classified KSI counts
    assert m.denominator == 1
    assert "skipped 1 KSI(s)" in m.notes
    assert "KSI-CNA-MAT" in m.notes


def test_m3_skips_not_applicable_classified_ksi() -> None:
    """Same skip rule applies to `not_applicable` -- a NA rationale
    explains scope exclusion, not specific resources. Excluded from
    the M3 denominator.
    """
    gt = _gt_with_extras(
        expected_rationale_resources={
            "KSI-CMT-RVP": ["change_review_board"],
        },
    )
    rationales = {
        "KSI-CMT-RVP": "Out of scope for this boundary per user declaration.",
    }
    classifications = {"KSI-CMT-RVP": "not_applicable"}
    m = resource_naming_rate(rationales, classifications, gt)
    assert m.score == 0.0
    assert m.denominator == 0  # the only labeled KSI was skipped
    assert "skipped 1 KSI(s)" in m.notes


def test_m3_does_not_skip_partial_or_implemented_classifications() -> None:
    """Regression guard: only ELI/NA are neutral statuses. `partial`,
    `implemented`, `not_implemented` all stay in the M3 denominator
    because their rationales SHOULD be naming resources.
    """
    gt = _gt_with_extras(
        expected_rationale_resources={
            "KSI-A": ["alpha"],
            "KSI-B": ["beta"],
            "KSI-C": ["gamma"],
        },
    )
    rationales = {
        "KSI-A": "alpha is configured",  # hit (partial)
        "KSI-B": "no resource cited here",  # miss (implemented)
        "KSI-C": "gamma is absent",  # hit (not_implemented)
    }
    classifications = {
        "KSI-A": "partial",
        "KSI-B": "implemented",
        "KSI-C": "not_implemented",
    }
    m = resource_naming_rate(rationales, classifications, gt)
    assert m.numerator == 2
    assert m.denominator == 3
    assert "skipped" not in m.notes  # no neutral-status skips occurred


# --- M4: manifest-quoting accuracy -------------------------------------------


def test_m4_perfect_when_narrative_quotes_expected_substring() -> None:
    """Happy path: narrative includes one of the expected manifest
    substrings. Score 1.0."""
    gt = _gt_with_extras(
        expected_manifest_quoting={
            "KSI-AFR-FSI": ["security@example.com", "PagerDuty"],
        },
    )
    narratives = {
        "KSI-AFR-FSI": "The security@example.com inbox is monitored 24/7.",
    }
    m = manifest_quoting_accuracy(narratives, gt)
    assert m.score == 1.0


def test_m4_locks_v0_1_8_f5_cross_wiring_bug() -> None:
    """Reproduces the v0.1.8 F5 bug shape: KSI-AFR-FSI's narrative
    quoted PagerDuty (which belongs to KSI-INR-RIR's manifest) and
    KSI-INR-RIR's narrative DIDN'T quote PagerDuty even though that's
    its OWN manifest. M4 should flip from 1.0 to <1.0 on this regression.

    Pre-bug state: both narratives quote their own manifest's content
    correctly, score 1.0. Post-bug state: AFR-FSI's narrative omits
    its expected substrings; M4 drops."""
    gt = _gt_with_extras(
        expected_manifest_quoting={
            "KSI-AFR-FSI": ["security@govnotes.fed", "15-minute"],
            "KSI-INR-RIR": ["PagerDuty"],
        },
    )

    pre_bug = {
        "KSI-AFR-FSI": "security@govnotes.fed is monitored 24/7 with a 15-minute SLA.",
        "KSI-INR-RIR": "Incidents page on-call via PagerDuty.",
    }
    post_bug = {
        # F5: narrative omits the expected substrings (cross-wiring
        # to a different manifest's content).
        "KSI-AFR-FSI": "The team uses an inbox documented in runbooks.",
        "KSI-INR-RIR": "Incidents page on-call via PagerDuty.",
    }

    m_pre = manifest_quoting_accuracy(pre_bug, gt)
    m_post = manifest_quoting_accuracy(post_bug, gt)

    assert m_pre.score == 1.0
    assert m_post.score == 0.5  # 1 of 2 narratives missed expected substrings
    assert "KSI-AFR-FSI" in m_post.notes


def test_m4_skips_ksi_with_no_emitted_narrative() -> None:
    """Mirror of M3's skip-don't-penalize semantics."""
    gt = _gt_with_extras(
        expected_manifest_quoting={
            "KSI-AFR-FSI": ["security@example.com"],
            "KSI-INR-RIR": ["PagerDuty"],
        },
    )
    narratives = {
        "KSI-AFR-FSI": "security@example.com SLA",  # hit
        # KSI-INR-RIR omitted by doc-agent -- skipped, not penalized
    }
    m = manifest_quoting_accuracy(narratives, gt)
    assert m.score == 1.0
    assert m.denominator == 1


def test_m4_returns_zero_when_no_expected_manifest_quoting_labeled() -> None:
    """No M4 expectations -> 0/0 with explanatory note."""
    gt = _gt_with_extras(expected_manifest_quoting={})
    m = manifest_quoting_accuracy({"KSI-FOO": "any"}, gt)
    assert m.score == 0.0
    assert "no expected_manifest_quoting" in m.notes


def test_m4_partial_score_on_partial_misses() -> None:
    """Multiple KSIs labeled, some quote correctly, some don't.
    Score reflects the fraction."""
    gt = _gt_with_extras(
        expected_manifest_quoting={
            "KSI-A": ["alpha"],
            "KSI-B": ["bravo"],
            "KSI-C": ["charlie"],
            "KSI-D": ["delta"],
        },
    )
    narratives = {
        "KSI-A": "alpha is documented",  # hit
        "KSI-B": "bravo team operates",  # hit
        "KSI-C": "redacted narrative",  # miss
        "KSI-D": "redacted narrative",  # miss
    }
    m = manifest_quoting_accuracy(narratives, gt)
    assert m.score == 0.5
    assert m.numerator == 2
    assert m.denominator == 4


def test_encryption_mixed_fixture_loads_clean() -> None:
    """The PR-beta encryption-mixed fixture must load + validate. Locks
    fixture/schema sync (regression on either fails this test)."""
    from pathlib import Path

    from evals.ground_truth import load_ground_truth

    fixtures_dir = Path(__file__).resolve().parent.parent / "evals" / "fixtures"
    gt = load_ground_truth(fixtures_dir / "encryption-mixed" / "GROUND_TRUTH.yaml")
    assert gt.fixture_id == "encryption-mixed"
    # Sanity: the fixture exercises bucket-by-bucket variance via M3.
    # Rev 2 (2026-05-09) moved expected resources from KSI-SVC-VRI/CNA-MAT/
    # SVC-PRR (which get zero S3 evidence on this S3-only fixture and
    # legitimately classify as ELI) to KSI-AFR-UCM (the KSI whose
    # detector mapping does attach S3 evidence here).
    assert "KSI-AFR-UCM" in gt.expected_rationale_resources
    assert "app_uploads" in gt.expected_rationale_resources["KSI-AFR-UCM"]


def test_iam_dynamic_policy_fixture_loads_clean() -> None:
    """PR-gamma iam-dynamic-policy fixture must load + validate."""
    from pathlib import Path

    from evals.ground_truth import load_ground_truth

    fixtures_dir = Path(__file__).resolve().parent.parent / "evals" / "fixtures"
    gt = load_ground_truth(fixtures_dir / "iam-dynamic-policy" / "GROUND_TRUTH.yaml")
    assert gt.fixture_id == "iam-dynamic-policy"
    # Sanity: exercises the data-source-resolution path the v0.1.7
    # fix enabled.
    assert "KSI-IAM-MFA" in gt.expected_classifications
    assert "scoped_admin" in gt.expected_rationale_resources["KSI-IAM-MFA"]


# --- M5: POAM scope discipline ----------------------------------------------


def _gt_with_poam(
    *,
    must_not_mention: list[str] | None = None,
    excluded_count_min: int = 0,
    excluded_count_max: int = 60,
) -> GroundTruth:
    return GroundTruth(
        fixture_id="test",
        description="test",
        authored_by="t@e",
        authored_at="2026-05-08",
        revision=1,
        frmr_version="0.9.43-beta",
        expected_poam=POAMExpectations(
            must_not_mention=must_not_mention or [],
            excluded_count_min=excluded_count_min,
            excluded_count_max=excluded_count_max,
        ),
    )


def test_m5_perfect_when_no_leak_and_count_in_range() -> None:
    """Both checks pass: no leaked substrings, count within range."""
    gt = _gt_with_poam(must_not_mention=["dev_scratch"], excluded_count_max=10)
    poam = "POAM body. - **Excluded as out-of-boundary:** 3 item(s) (cited evidence...)"
    m = poam_scope_discipline(poam, gt)
    assert m.score == 1.0
    assert m.numerator == 2
    assert m.denominator == 2


def test_m5_drops_to_half_on_leak() -> None:
    """Boundary-leak: an OOB resource name appears in the POAM body
    even though the fixture's must_not_mention says it shouldn't.
    Check A fails; Check B passes; score 0.5."""
    gt = _gt_with_poam(must_not_mention=["dev_scratch"], excluded_count_max=10)
    poam = (
        "POAM mentions dev_scratch in some KSI rationale. "
        "- **Excluded as out-of-boundary:** 2 item(s)"
    )
    m = poam_scope_discipline(poam, gt)
    assert m.score == 0.5
    assert "boundary-leak" in m.notes
    assert "dev_scratch" in m.notes


def test_m5_drops_to_half_when_count_out_of_range() -> None:
    """Excluded count is 0 because the POAM doesn't have the bullet,
    but the fixture expected at least 5. Check B fails; Check A
    vacuously passes; score 0.5."""
    gt = _gt_with_poam(excluded_count_min=5)
    poam = "POAM body with no out-of-boundary header bullet at all."
    m = poam_scope_discipline(poam, gt)
    assert m.score == 0.5
    assert "outside [5, 60]" in m.notes


def test_m5_zero_when_both_checks_fail() -> None:
    """Worst-case: leaked substring AND wrong excluded count. 0.0."""
    gt = _gt_with_poam(
        must_not_mention=["dev_scratch"],
        excluded_count_min=5,
        excluded_count_max=10,
    )
    poam = "POAM mentions dev_scratch + - **Excluded as out-of-boundary:** 12 item(s)"
    m = poam_scope_discipline(poam, gt)
    assert m.score == 0.0


def test_m5_treats_missing_excluded_header_as_zero_count() -> None:
    """The POAM generator only adds the 'Excluded as out-of-boundary'
    bullet when count > 0 (per src/efterlev/primitives/generate/
    generate_poam_markdown.py:259). M5 must read absence as 0, not
    as 'unknown'. Lock that contract."""
    gt = _gt_with_poam(excluded_count_min=0, excluded_count_max=0)
    poam = "POAM body, all 60 KSIs in scope, no exclusions header at all."
    m = poam_scope_discipline(poam, gt)
    # Count=0 is in [0,0] so Check B passes; no leaked substrings so
    # Check A passes vacuously; score 1.0.
    assert m.score == 1.0


def test_m5_locks_v0_1_4_boundary_leak_pattern() -> None:
    """Reproduces the boundary-leak bug shape: an out-of-boundary
    resource (`dev_sandbox` from a typical mid-journey FedRAMP
    fixture) leaks into POAM rationale text even though it should
    have been filtered out at the boundary stage. M5 catches it
    immediately; pre-eval-harness this required eyeballing the POAM
    end-to-end."""
    gt = _gt_with_poam(must_not_mention=["dev_sandbox", "internal_qa_bucket"])

    pre_bug = "POAM body discussing app_uploads, audit_logs."
    post_bug = "POAM body discussing app_uploads, audit_logs, and dev_sandbox."

    m_pre = poam_scope_discipline(pre_bug, gt)
    m_post = poam_scope_discipline(post_bug, gt)

    assert m_pre.score == 1.0
    assert m_post.score == 0.5
    assert "dev_sandbox" in m_post.notes
