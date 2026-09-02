"""Tests for find_cut_index in rederive_deferral_variants."""

from __future__ import annotations

import pytest

from agentic_devtools.cli.github.ccr_review_format import UNKNOWN_FILE
from tests.scripts.rederive_deferral_variants import (
    posted_body,
    record,
    rederive,
    round_,
    suppressed_body,
)


def _metrics(rec):
    return [rederive.measure_round(item) for item in rec.rounds]


def _cut(rec, variant):
    return rederive.find_cut_index(rec, _metrics(rec), variant)


def test_rejects_unknown_variant() -> None:
    """An unrecognised variant name is a programming error, not a silent no-op."""
    rec = record(round_(body=suppressed_body("specs/1/spec.md")))
    with pytest.raises(ValueError, match="Unknown variant"):
        rederive.find_cut_index(rec, _metrics(rec), "Q")


def test_variant_a_cuts_at_first_suppressed_only_round() -> None:
    """A fires on the first suppressed-only round regardless of path class."""
    rec = record(
        round_(review_id=1, body=posted_body(2), posted_paths=("specs/1/spec.md",)),
        round_(review_id=2, body=suppressed_body("agentic_devtools/state.py")),
        round_(review_id=3, body=suppressed_body("specs/1/spec.md")),
    )
    assert _cut(rec, "A") == 1


def test_variant_s_skips_executable_suppressed_paths() -> None:
    """S refuses a cut round carrying an executable suppressed path, and waits."""
    rec = record(
        round_(review_id=1, body=suppressed_body("agentic_devtools/state.py")),
        round_(review_id=2, body=suppressed_body("specs/1/spec.md")),
    )
    assert _cut(rec, "A") == 0
    assert _cut(rec, "S") == 1


def test_variant_s_rejects_non_path_artefact_entries() -> None:
    """A non-path artefact fails closed, so S will not cut on that round."""
    rec = record(
        round_(review_id=1, body=suppressed_body("get_issue_types()")),
        round_(review_id=2, body=suppressed_body("specs/1/spec.md")),
    )
    assert _cut(rec, "S") == 1


def test_variant_sp_fires_when_the_diff_has_only_extensionless_files() -> None:
    """LICENSE / Dockerfile are real API paths outside the executable union."""
    rec = record(
        round_(body=suppressed_body("specs/1/spec.md")),
        changed_files=("LICENSE", "Dockerfile"),
    )
    assert _cut(rec, "SP") == 0


def test_g2_rejects_a_round_whose_declared_count_does_not_match() -> None:
    """G2 gates every variant: an over-declaring round can never be a cut round."""
    rec = record(
        round_(review_id=1, body=suppressed_body("specs/1/spec.md", declared=3)),
        round_(review_id=2, body=suppressed_body("specs/1/plan.md")),
    )
    assert _cut(rec, "A") == 1
    assert _cut(rec, "SP") == 1


def test_g2_rejects_under_declaration_too() -> None:
    """Under-declaration is as disqualifying as over-declaration."""
    rec = record(round_(body=suppressed_body("specs/1/spec.md", "specs/1/plan.md", declared=1)))
    assert _cut(rec, "A") is None


def test_sp_requires_an_executable_free_diff() -> None:
    """Condition 10 blocks SP when the PR's changed files include executable code."""
    rec = record(
        round_(body=suppressed_body("specs/1/spec.md")),
        round_(review_id=2, body=suppressed_body("specs/1/plan.md")),
        changed_files=("specs/1/spec.md", "agentic_devtools/state.py"),
    )
    assert _cut(rec, "S") == 0
    assert _cut(rec, "SP") is None


def test_sp_requires_no_prior_executable_posted_finding() -> None:
    """Condition 7 blocks SP once the PR has posted a finding on executable code."""
    rec = record(
        round_(review_id=1, body=posted_body(1), posted_paths=("agentic_devtools/state.py",)),
        round_(review_id=2, body=suppressed_body("specs/1/spec.md")),
    )
    assert _cut(rec, "S") == 1
    assert _cut(rec, "SP") is None


def test_sp_tolerates_a_prior_non_executable_posted_finding() -> None:
    """A prior posted finding on specs does not disqualify SP."""
    rec = record(
        round_(review_id=1, body=posted_body(1), posted_paths=("specs/1/spec.md",)),
        round_(review_id=2, body=suppressed_body("specs/1/plan.md")),
    )
    assert _cut(rec, "SP") == 1


def test_sp_tolerates_a_prior_posted_finding_on_extensionless_api_path() -> None:
    """An authoritative API path like LICENSE or Dockerfile is not executable; SP must not be blocked."""
    rec = record(
        round_(review_id=1, body=posted_body(1), posted_paths=("LICENSE",)),
        round_(review_id=2, body=suppressed_body("specs/1/plan.md")),
    )
    assert _cut(rec, "SP") == 1


def test_sp_rejects_a_prior_pathless_posted_finding() -> None:
    """UNKNOWN_FILE in posted_paths fails closed and blocks SP."""
    rec = record(
        round_(review_id=1, body=posted_body(1), posted_paths=(UNKNOWN_FILE,)),
        round_(review_id=2, body=suppressed_body("specs/1/plan.md")),
    )
    assert _cut(rec, "SP") is None


def test_n4_requires_four_consecutive_suppressed_only_rounds() -> None:
    """N4 fires only at the 4th consecutive suppressed-only round."""
    rounds = [round_(review_id=i, body=suppressed_body("specs/1/spec.md")) for i in range(1, 5)]
    assert _cut(record(*rounds), "N4") == 3


def test_n4_run_resets_on_a_posted_bearing_round() -> None:
    """A posted-bearing round breaks the consecutive run."""
    rounds = [
        round_(review_id=1, body=suppressed_body("specs/1/spec.md")),
        round_(review_id=2, body=suppressed_body("specs/1/spec.md")),
        round_(review_id=3, body=suppressed_body("specs/1/spec.md")),
        round_(review_id=4, body=posted_body(1), posted_paths=("specs/1/spec.md",)),
        round_(review_id=5, body=suppressed_body("specs/1/spec.md")),
    ]
    assert _cut(record(*rounds), "N4") is None


def test_s4_combines_the_run_and_the_path_restriction() -> None:
    """S4 needs both a 4-round run and a safe cut round."""
    rounds = [
        round_(review_id=1, body=suppressed_body("specs/1/spec.md")),
        round_(review_id=2, body=suppressed_body("specs/1/spec.md")),
        round_(review_id=3, body=suppressed_body("specs/1/spec.md")),
        round_(review_id=4, body=suppressed_body("agentic_devtools/state.py")),
        round_(review_id=5, body=suppressed_body("specs/1/spec.md")),
    ]
    assert _cut(record(*rounds), "N4") == 3
    assert _cut(record(*rounds), "S4") == 4


def test_returns_none_when_no_round_is_suppressed_only() -> None:
    """A PR whose rounds all post findings is never cut."""
    rec = record(round_(body=posted_body(2), posted_paths=("specs/1/spec.md", "specs/1/plan.md")))
    assert _cut(rec, "A") is None


def test_a_round_with_both_posted_and_suppressed_is_not_suppressed_only() -> None:
    """Condition 1: a posted-bearing round can never trigger a deferral."""
    rec = record(round_(body=suppressed_body("specs/1/spec.md"), posted_paths=("specs/1/plan.md",)))
    assert _cut(rec, "A") is None


def test_a_body_reporting_posted_comments_without_inline_comments_is_not_cut() -> None:
    """A self-reported posted count with no inline comment is a retrieval gap.

    Treating it as suppressed-only would manufacture a cut round wherever the
    fetch missed the inline comments, inflating every saving in the table.
    """
    rec = record(round_(body=suppressed_body("specs/1/spec.md", posted=3), posted_paths=()))
    assert _cut(rec, "A") is None


def test_a_body_without_a_posted_count_is_still_cut() -> None:
    """An unparsed count is a legacy body, not a disagreement, so it stays eligible."""
    rec = record(round_(body=suppressed_body("specs/1/spec.md"), posted_paths=()))
    assert _cut(rec, "A") == 0
