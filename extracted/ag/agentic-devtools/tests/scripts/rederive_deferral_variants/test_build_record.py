"""Tests for build_record in rederive_deferral_variants."""

from __future__ import annotations

from agentic_devtools.cli.github.ccr_review_format import UNKNOWN_FILE
from tests.scripts.rederive_deferral_variants import rederive


def _review(
    review_id: int,
    *,
    login: str = "copilot-pull-request-reviewer[bot]",
    submitted_at: str = "2026-08-01T00:00:00Z",
) -> dict:
    return {"id": review_id, "user": {"login": login}, "submitted_at": submitted_at, "body": "body"}


def test_attaches_inline_comments_to_their_review() -> None:
    """Posted paths come from the inline comments, keyed by review id."""
    record = rederive.build_record(
        7,
        [_review(100), _review(101, submitted_at="2026-08-02T00:00:00Z")],
        [
            {"pull_request_review_id": 100, "path": "specs/7/spec.md"},
            {"pull_request_review_id": 101, "path": "agentic_devtools/state.py"},
            {"pull_request_review_id": 100, "path": "specs/7/plan.md"},
        ],
        [{"filename": "specs/7/spec.md"}],
    )
    assert record.rounds[0].posted_paths == ("specs/7/spec.md", "specs/7/plan.md")
    assert record.rounds[1].posted_paths == ("agentic_devtools/state.py",)


def test_drops_reviews_from_other_authors() -> None:
    """Only CCR reviews are rounds; human reviews are not."""
    record = rederive.build_record(7, [_review(100), _review(101, login="a-human")], [], [])
    assert [round_.review_id for round_ in record.rounds] == [100]


def test_orders_rounds_by_submission_time() -> None:
    """Rounds are ordered by submission, not by API order."""
    record = rederive.build_record(
        7,
        [_review(200, submitted_at="2026-08-03T00:00:00Z"), _review(100, submitted_at="2026-08-01T00:00:00Z")],
        [],
        [],
    )
    assert [round_.review_id for round_ in record.rounds] == [100, 200]


def test_records_the_authoritative_changed_file_list() -> None:
    """The changed-file list comes from the PR API, never from finding paths."""
    record = rederive.build_record(7, [], [], [{"filename": "specs/7/spec.md"}, {"filename": ".gitignore"}])
    assert record.changed_files == ("specs/7/spec.md", ".gitignore")


def test_ignores_comments_that_are_not_attached_to_a_review() -> None:
    """A standalone comment has no review id and belongs to no round."""
    record = rederive.build_record(7, [_review(100)], [{"pull_request_review_id": None, "path": "specs/7/spec.md"}], [])
    assert record.rounds[0].posted_paths == ()


def test_ignores_review_comment_replies() -> None:
    """Reply comments are not top-level posted findings for the review round."""
    record = rederive.build_record(
        7,
        [_review(100)],
        [
            {"pull_request_review_id": 100, "path": "specs/7/spec.md"},
            {"pull_request_review_id": 100, "path": "specs/7/tasks.md", "in_reply_to_id": 99},
        ],
        [],
    )
    assert record.rounds[0].posted_paths == ("specs/7/spec.md",)


def test_a_pathless_comment_is_recorded_as_unknown_file() -> None:
    """A comment without a path is retained, and fails closed downstream."""
    record = rederive.build_record(7, [_review(100)], [{"pull_request_review_id": 100, "path": None}], [])
    assert record.rounds[0].posted_paths == (UNKNOWN_FILE,)


def test_keeps_both_current_and_previous_filenames_for_renames() -> None:
    """A rename carries both paths so executable deletions are still visible."""
    record = rederive.build_record(
        7,
        [],
        [],
        [{"filename": "specs/new-name.md", "previous_filename": "agentic_devtools/old_name.py"}],
    )
    assert record.changed_files == ("specs/new-name.md", "agentic_devtools/old_name.py")


def test_tolerates_a_missing_body() -> None:
    """A review with a null body parses as an empty body rather than crashing."""
    record = rederive.build_record(
        7, [{"id": 100, "user": {"login": "copilot-pull-request-reviewer[bot]"}, "body": None}], [], []
    )
    assert record.rounds[0].body == ""
