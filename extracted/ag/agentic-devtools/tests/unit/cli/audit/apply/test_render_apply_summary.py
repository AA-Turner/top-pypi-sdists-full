"""Tests for render_apply_summary()."""

from agentic_devtools.cli.audit.apply import (
    OUTCOME_INVALID_OUTPUT,
    OUTCOME_MISSING_OUTPUT,
    OUTCOME_NO_CHANGES,
    OUTCOME_PR_FAILED,
    OUTCOME_PR_READY,
    render_apply_summary,
)


class TestRenderApplySummary:
    """Markdown rendering of an apply result for the CI job summary."""

    def test_includes_header(self) -> None:
        out = render_apply_summary({"outcome": OUTCOME_NO_CHANGES})
        assert "Review Feedback Audit" in out

    def test_pr_ready_includes_url_and_modified_files(self) -> None:
        out = render_apply_summary(
            {
                "outcome": OUTCOME_PR_READY,
                "pr_url": "https://github.com/o/r/pull/9",
                "files_modified": ["a.md"],
                "files_created": [],
            }
        )
        assert "https://github.com/o/r/pull/9" in out
        assert "a.md" in out
        assert "Files modified:** 1" in out

    def test_created_files_listed(self) -> None:
        out = render_apply_summary({"outcome": OUTCOME_PR_READY, "files_created": ["new.md"]})
        assert "new.md" in out
        assert "(new)" in out

    def test_missing_output_headline_is_failure(self) -> None:
        assert "Failed" in render_apply_summary({"outcome": OUTCOME_MISSING_OUTPUT})

    def test_invalid_output_headline_is_failure(self) -> None:
        assert "Failed" in render_apply_summary({"outcome": OUTCOME_INVALID_OUTPUT})

    def test_pr_failed_headline_is_failure(self) -> None:
        assert "Failed" in render_apply_summary({"outcome": OUTCOME_PR_FAILED})

    def test_unknown_outcome_fallback(self) -> None:
        assert "weird" in render_apply_summary({"outcome": "weird"})

    def test_empty_result_does_not_crash(self) -> None:
        out = render_apply_summary({})
        assert "unknown" in out
        assert "Files modified:** 0" in out
        assert "Files created:** 0" in out
