"""Tests for _get_heading_level_simple in agentic_devtools.cli.issue_template.renderer."""

from __future__ import annotations

from agentic_devtools.cli.issue_template.renderer import _get_heading_level_simple


class TestGetHeadingLevelSimple:
    """Tests for _get_heading_level_simple (pre-CommonMark legacy variant)."""

    def test_h1(self) -> None:
        """# heading returns level 1."""
        assert _get_heading_level_simple("# Title") == 1

    def test_h2(self) -> None:
        """## heading returns level 2."""
        assert _get_heading_level_simple("## Section") == 2

    def test_h6(self) -> None:
        """###### heading returns level 6."""
        assert _get_heading_level_simple("###### Deep") == 6

    def test_more_than_6_hashes_not_heading(self) -> None:
        """####### (7 hashes) with a trailing space is not a valid heading."""
        assert _get_heading_level_simple("####### Not a heading") == 0

    def test_no_space_after_hash_not_heading(self) -> None:
        """#NoSpace is not a valid heading (covers the level<=6 branch-false path)."""
        assert _get_heading_level_simple("#NoSpace") == 0

    def test_hash_only_is_heading(self) -> None:
        """A line with just '#' (and nothing else) is a valid heading."""
        assert _get_heading_level_simple("#") == 1

    def test_hashes_only_no_space_returns_level(self) -> None:
        """'##' with no trailing text returns level 2 (for-loop exhausts chars)."""
        assert _get_heading_level_simple("##") == 2

    def test_non_heading_line(self) -> None:
        """Regular text returns 0."""
        assert _get_heading_level_simple("Just text") == 0

    def test_empty_line(self) -> None:
        """Empty line returns 0."""
        assert _get_heading_level_simple("") == 0

    def test_four_space_indented_heading_is_still_heading(self) -> None:
        """Unlike the CommonMark variant, a 4-space indent does NOT suppress the heading."""
        assert _get_heading_level_simple("    ## Example") == 2

    def test_tab_indented_heading_is_still_heading(self) -> None:
        """Unlike the CommonMark variant, a tab indent does NOT suppress the heading."""
        assert _get_heading_level_simple("\t## Section") == 2
