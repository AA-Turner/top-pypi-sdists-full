"""Tests for filtering post-review Copilot session summaries."""

from agentic_devtools.cli.ci.github_provider import _filter_post_review_session_summaries
from agentic_devtools.cli.ci.models import CopilotSessionSummary


def _summary(session_id: str, started_at: str, text: str, task_id: str = "task-1") -> CopilotSessionSummary:
    return CopilotSessionSummary(task_id, session_id, 42, started_at, finishing_text=text)


def test_filters_deduplicates_limits_and_orders_summaries() -> None:
    """Keeps newest unique summaries that fit, then returns them chronologically."""
    summaries = [
        _summary("old", "2026-01-02T00:00:00Z", "old"),
        _summary("same", "2026-01-04T00:00:00Z", "duplicate"),
        _summary("same", "2026-01-05T00:00:00Z", "duplicate-newer"),
        _summary("new", "2026-01-06T00:00:00Z", "new"),
        _summary("", "2026-01-07T00:00:00Z", "fallback", task_id="fallback-task"),
        _summary("empty", "2026-01-08T00:00:00Z", ""),
    ]

    result = _filter_post_review_session_summaries(summaries, "2026-01-01T00:00:00Z", max_summaries=3, max_chars=20)

    assert [summary.session_id for summary in result] == ["new", ""]


def test_newest_duplicate_wins_before_budget_filtering() -> None:
    """Uses the newest duplicate and continues past an oversized candidate."""
    summaries = [
        _summary("same", "2026-01-02T00:00:00Z", "old"),
        _summary("same", "2026-01-03T00:00:00Z", "new"),
        _summary("later", "2026-01-04T00:00:00Z", "x"),
    ]

    newest_result = _filter_post_review_session_summaries(
        summaries,
        "2026-01-01T00:00:00Z",
        max_summaries=3,
        max_chars=100,
    )
    assert [summary.finishing_text for summary in newest_result if summary.session_id == "same"] == ["new"]

    result = _filter_post_review_session_summaries(
        summaries,
        "2026-01-01T00:00:00Z",
        max_summaries=2,
        max_chars=1,
    )

    assert [summary.session_id for summary in result] == ["later"]


def test_rejects_missing_or_invalid_review_timestamp_and_budget() -> None:
    """Returns no summaries when correlation metadata or budgets are unusable."""
    summary = _summary("s", "2026-01-02T00:00:00Z", "text")

    assert _filter_post_review_session_summaries([summary], None) == ()
    assert _filter_post_review_session_summaries([summary], "invalid") == ()
    assert _filter_post_review_session_summaries([summary], "2026-01-01T00:00:00Z", 0) == ()
    assert _filter_post_review_session_summaries([summary], "2026-01-01T00:00:00Z", max_chars=0) == ()


def test_skips_invalid_and_pre_review_timestamps() -> None:
    """Skips summaries without usable timestamps and summaries at or before review."""
    assert (
        _filter_post_review_session_summaries(
            [
                _summary("invalid", "not-a-timestamp", "text"),
                _summary("equal", "2026-01-01T00:00:00Z", "text"),
                _summary("naive", "2026-01-02T00:00:00", "text"),
            ],
            "2026-01-01T00:00:00",
        )[0].session_id
        == "naive"
    )


def test_skips_summary_without_any_identifier_and_honors_summary_limit() -> None:
    """Skips unidentifiable summaries and stops after the configured result limit."""
    assert (
        _filter_post_review_session_summaries(
            [_summary("", "2026-01-02T00:00:00Z", "text", task_id="")],
            "2026-01-01T00:00:00Z",
        )
        == ()
    )
    result = _filter_post_review_session_summaries(
        [
            _summary("first", "2026-01-02T00:00:00Z", "first"),
            _summary("second", "2026-01-03T00:00:00Z", "second"),
        ],
        "2026-01-01T00:00:00Z",
        max_summaries=1,
    )
    assert [summary.session_id for summary in result] == ["second"]
