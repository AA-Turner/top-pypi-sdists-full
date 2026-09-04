"""Tests for _parse_finalized_review_marker."""

from agentic_devtools.cli.ci.finalization_state import _parse_finalized_review_marker


def test_returns_none_for_malformed_payload() -> None:
    assert _parse_finalized_review_marker(123) is None  # type: ignore[arg-type]
    assert _parse_finalized_review_marker('<!-- ai-pr-loop:finalized-review {"repo":} -->') is None
    assert _parse_finalized_review_marker("<!-- ai-pr-loop:finalized-review [1,2,3] -->") is None
    assert _parse_finalized_review_marker("plain text") is None


def test_returns_none_for_invalid_types() -> None:
    assert (
        _parse_finalized_review_marker('<!-- ai-pr-loop:finalized-review {"repo":"","pr":0,"review_id":0} -->') is None
    )
    assert (
        _parse_finalized_review_marker(
            '<!-- ai-pr-loop:finalized-review {"repo":"owner/repo","pr":true,"review_id":7} -->'
        )
        is None
    )
    assert (
        _parse_finalized_review_marker(
            '<!-- ai-pr-loop:finalized-review {"repo":"owner/repo","pr":42,"review_id":false} -->'
        )
        is None
    )
