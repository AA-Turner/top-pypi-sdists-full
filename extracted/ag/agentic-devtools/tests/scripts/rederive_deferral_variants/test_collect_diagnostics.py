"""Tests for collect_diagnostics in rederive_deferral_variants."""

from __future__ import annotations

from tests.scripts.rederive_deferral_variants import (
    measured,
    posted_body,
    record,
    rederive,
    round_,
    suppressed_body,
)


def test_counts_corpus_totals() -> None:
    """Total PRs and total rounds are the denominators for every rate."""
    diagnostics = rederive.collect_diagnostics(
        measured(
            record(round_(body=suppressed_body("specs/1/spec.md")), number=1),
            record(
                round_(review_id=1, body=posted_body(1), posted_paths=("specs/2/spec.md",)),
                round_(review_id=2, body=suppressed_body("specs/2/spec.md")),
                number=2,
            ),
        )
    )
    assert diagnostics.total_prs == 2
    assert diagnostics.total_rounds == 3


def test_g2_rejection_rate_counts_the_round_sp_would_have_cut_on() -> None:
    """The denominator is the SP cut round a G2-free variant would have used."""
    passing = record(round_(body=suppressed_body("specs/1/spec.md")), number=1)
    rejected = record(round_(body=suppressed_body("specs/2/spec.md", declared=4)), number=2)
    diagnostics = rederive.collect_diagnostics(measured(passing, rejected))
    assert diagnostics.sp_candidate_rounds == 2
    assert diagnostics.sp_g2_rejected == 1
    assert diagnostics.g2_rejection_rate == 0.5


def test_g2_rate_is_zero_when_no_pull_request_is_sp_eligible() -> None:
    """A corpus with no SP candidate reports 0.0 rather than dividing by zero."""
    rec = record(round_(body=posted_body(1), posted_paths=("specs/1/spec.md",)))
    assert rederive.collect_diagnostics(measured(rec)).g2_rejection_rate == 0.0


def test_non_path_artefact_rate_measures_deferred_entries() -> None:
    """The artefact rate is measured over the entries SP actually defers."""
    rec = record(round_(body=suppressed_body("specs/1/spec.md", "specs/1/plan.md")))
    diagnostics = rederive.collect_diagnostics(measured(rec))
    assert diagnostics.deferred_entries == 2
    assert diagnostics.non_path_entries == 0
    assert diagnostics.non_path_artefact_rate == 0.0


def test_non_path_artefact_rate_counts_non_path_shaped_entries() -> None:
    """Entries without a path shape are counted even though SP would filter them out."""
    # "get_issue_types()" has parentheses and therefore fails looks_like_path.
    # find_cut_index("SP") would never fire on this round because _cut_round_is_deferrable
    # rejects it, but the pre-detector population must still count the entry.
    rec = record(round_(body=suppressed_body("specs/1/spec.md", "get_issue_types()")))
    diagnostics = rederive.collect_diagnostics(measured(rec))
    assert diagnostics.deferred_entries == 2
    assert diagnostics.non_path_entries == 1
    assert diagnostics.non_path_artefact_rate == 0.5


def test_non_path_artefact_rate_is_zero_when_nothing_is_deferred() -> None:
    """No deferral means no denominator, and the rate reports 0.0."""
    rec = record(round_(body=posted_body(1), posted_paths=("specs/1/spec.md",)))
    assert rederive.collect_diagnostics(measured(rec)).non_path_artefact_rate == 0.0


def test_a_path_shaped_executable_entry_is_not_counted_as_a_deferral() -> None:
    """A round SP would reject on an executable path is skipped by the artefact loop."""
    # agentic_devtools/state.py is path-shaped and executable, so SP rejects the
    # round; its entries must not be counted as deferred artefacts.
    rec = record(round_(body=suppressed_body("agentic_devtools/state.py", "get_issue_types()")))
    diagnostics = rederive.collect_diagnostics(measured(rec))
    assert diagnostics.deferred_entries == 0
    assert diagnostics.non_path_entries == 0


def test_artefact_loop_skips_executable_rounds_and_measures_a_later_one() -> None:
    """An early executable round is skipped; the rate reflects a later clean round."""
    rec = record(
        round_(review_id=1, body=suppressed_body("agentic_devtools/state.py")),
        round_(review_id=2, body=suppressed_body("specs/2/spec.md", "get_issue_types()")),
    )
    diagnostics = rederive.collect_diagnostics(measured(rec))
    assert diagnostics.deferred_entries == 2
    assert diagnostics.non_path_entries == 1


def test_an_extensionless_changed_file_does_not_disqualify_an_sp_candidate() -> None:
    """A LICENSE / Dockerfile in the diff is not executable, so SP still fires."""
    rec = record(
        round_(body=suppressed_body("specs/1/spec.md")),
        changed_files=("LICENSE", "Dockerfile", "specs/1/spec.md"),
    )
    diagnostics = rederive.collect_diagnostics(measured(rec))
    assert diagnostics.sp_candidate_rounds == 1
    assert diagnostics.deferred_entries == 1


def test_a_pull_request_with_an_executable_diff_is_not_an_sp_candidate() -> None:
    """Condition 10 removes the PR before G2 is ever consulted."""
    rec = record(
        round_(body=suppressed_body("specs/1/spec.md")),
        changed_files=("agentic_devtools/state.py",),
    )
    diagnostics = rederive.collect_diagnostics(measured(rec))
    assert diagnostics.sp_candidate_rounds == 0


def test_a_prior_executable_posted_finding_removes_the_candidate() -> None:
    """Condition 7 disqualifies the PR from the G2 denominator too."""
    rec = record(
        round_(review_id=1, body=posted_body(1), posted_paths=("agentic_devtools/state.py",)),
        round_(review_id=2, body=suppressed_body("specs/1/spec.md")),
    )
    assert rederive.collect_diagnostics(measured(rec)).sp_candidate_rounds == 0


def test_an_executable_suppressed_path_removes_the_candidate() -> None:
    """A round SP could not defer on is not counted against G2."""
    rec = record(round_(body=suppressed_body("agentic_devtools/state.py")))
    assert rederive.collect_diagnostics(measured(rec)).sp_candidate_rounds == 0
