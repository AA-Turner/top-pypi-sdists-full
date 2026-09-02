"""Tests for evaluate_variant in rederive_deferral_variants."""

from __future__ import annotations

import pytest

from agentic_devtools.cli.github.ccr_review_format import UNKNOWN_FILE
from tests.scripts.rederive_deferral_variants import (
    measured,
    posted_body,
    record,
    rederive,
    round_,
    suppressed_body,
)


def _three_round_pr(number: int = 1):
    """A PR cut at round 0 by A/S/SP, losing two rounds and three posted findings."""
    return record(
        round_(review_id=1, body=suppressed_body("specs/1/spec.md", "specs/1/plan.md")),
        round_(
            review_id=2,
            body=posted_body(2),
            posted_paths=("specs/1/spec.md", "agentic_devtools/state.py"),
        ),
        round_(review_id=3, body=posted_body(1), posted_paths=("specs/1/tasks.md",)),
        number=number,
    )


def test_counts_prs_rounds_findings_and_losses() -> None:
    """Every column of the variant table is derived from the same cut."""
    result = rederive.evaluate_variant(measured(_three_round_pr()), "A")
    assert result.prs == 1
    assert result.rounds_saved == 2
    assert result.findings_captured == 2
    assert result.posted_lost == 3
    assert result.executable_posted_lost == 1


def test_the_cut_round_itself_is_not_counted_as_saved() -> None:
    """The cut round runs; only the rounds after it are the saving."""
    rec = record(round_(body=suppressed_body("specs/1/spec.md")))
    assert rederive.evaluate_variant(measured(rec), "A").rounds_saved == 0


def test_skips_pull_requests_the_variant_never_fires_on() -> None:
    """A PR with no qualifying round contributes nothing to any column."""
    rec = record(round_(body=posted_body(1), posted_paths=("specs/1/spec.md",)))
    result = rederive.evaluate_variant(measured(rec), "A")
    assert (result.prs, result.rounds_saved, result.posted_lost) == (0, 0, 0)


def test_aggregates_across_the_corpus() -> None:
    """Results accumulate over every record."""
    result = rederive.evaluate_variant(measured(_three_round_pr(1), _three_round_pr(2)), "A")
    assert (result.prs, result.rounds_saved, result.posted_lost) == (2, 4, 6)


def test_sp_removes_the_executable_path_loss() -> None:
    """SP declines the PR whose diff is not executable-free, so it loses nothing."""
    rec = record(
        round_(review_id=1, body=suppressed_body("specs/1/spec.md")),
        round_(review_id=2, body=posted_body(1), posted_paths=("agentic_devtools/state.py",)),
        changed_files=("specs/1/spec.md", "agentic_devtools/state.py"),
    )
    assert rederive.evaluate_variant(measured(rec), "A").executable_posted_lost == 1
    assert rederive.evaluate_variant(measured(rec), "SP").executable_posted_lost == 0
    assert rederive.evaluate_variant(measured(rec), "SP").prs == 0


def test_extensionless_api_posted_path_is_not_counted_as_executable_loss() -> None:
    """LICENSE in posted_paths must not be counted as executable loss (API paths use direct classifier)."""
    rec = record(
        round_(review_id=1, body=suppressed_body("specs/1/spec.md")),
        round_(review_id=2, body=posted_body(1), posted_paths=("LICENSE",)),
        changed_files=("specs/1/spec.md",),
    )
    assert rederive.evaluate_variant(measured(rec), "A").executable_posted_lost == 0


def test_pathless_api_posted_path_is_counted_as_executable_loss() -> None:
    """UNKNOWN_FILE in posted_paths fails closed and counts as executable loss."""
    rec = record(
        round_(review_id=1, body=suppressed_body("specs/1/spec.md")),
        round_(review_id=2, body=posted_body(1), posted_paths=(UNKNOWN_FILE,)),
        changed_files=("specs/1/spec.md",),
    )
    assert rederive.evaluate_variant(measured(rec), "A").executable_posted_lost == 1


def test_raises_when_a_later_round_reports_more_posted_comments_than_were_retrieved() -> None:
    """A retrieval gap in later rounds must fail fast to avoid under-counting losses."""
    rec = record(
        round_(review_id=1, body=suppressed_body("specs/1/spec.md")),
        round_(review_id=2, body=posted_body(3), posted_paths=("specs/1/spec.md",)),
    )
    with pytest.raises(ValueError, match="retrieval gap"):
        rederive.evaluate_variant(measured(rec), "A")
