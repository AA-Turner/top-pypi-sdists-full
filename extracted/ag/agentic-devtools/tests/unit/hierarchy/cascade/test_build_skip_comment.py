"""Tests for _build_skip_comment static method (FR-005)."""

from agentic_devtools.hierarchy.cascade import CascadeProcessor


class TestBuildSkipComment:
    """Tests for the skip comment builder."""

    def test_with_target(self) -> None:
        """When target is specified, comment mentions cascading to target."""
        comment = CascadeProcessor._build_skip_comment([10, 20], target=30)
        assert "#10" in comment
        assert "#20" in comment
        assert "#30" in comment
        assert "Cascading to" in comment

    def test_exhausted(self) -> None:
        """When exhausted=True, comment mentions no further target."""
        comment = CascadeProcessor._build_skip_comment([10], target=None, exhausted=True)
        assert "#10" in comment
        assert "No further cascade target remains" in comment

    def test_no_target_not_exhausted_fallback(self) -> None:
        """When no target and not exhausted, uses generic fallback text."""
        comment = CascadeProcessor._build_skip_comment([5, 6], target=None, exhausted=False)
        assert "#5" in comment
        assert "#6" in comment
        assert "not eligible for cascade" in comment
        # Should not contain "Cascading to" or "No further"
        assert "Cascading to" not in comment
        assert "No further" not in comment
