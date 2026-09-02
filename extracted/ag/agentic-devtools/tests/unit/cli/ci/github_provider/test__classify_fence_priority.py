"""Tests for _classify_fence_priority()."""

from agentic_devtools.cli.ci.github_provider import _classify_fence_priority


class TestClassifyFencePriority:
    """Tests for the shared section -> trim-priority rule."""

    def test_ci_failure_section_is_zero(self) -> None:
        assert _classify_fence_priority("Failure") == 0

    def test_comment_section_is_two(self) -> None:
        """Every fence inside a review-comment section is actionable content."""
        assert _classify_fence_priority("Comment") == 2

    def test_unknown_section_is_two(self) -> None:
        assert _classify_fence_priority("") == 2
