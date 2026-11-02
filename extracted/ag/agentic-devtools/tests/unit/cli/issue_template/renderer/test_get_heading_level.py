"""Tests for _get_heading_level in agentic_devtools.cli.issue_template.renderer."""

from __future__ import annotations

from agentic_devtools.cli.issue_template.renderer import _get_heading_level


class TestGetHeadingLevel:
    """Tests for _get_heading_level helper."""

    def test_h1(self) -> None:
        """# heading returns level 1."""
        assert _get_heading_level("# Title") == 1

    def test_h2(self) -> None:
        """## heading returns level 2."""
        assert _get_heading_level("## Section") == 2

    def test_h6(self) -> None:
        """###### heading returns level 6."""
        assert _get_heading_level("###### Deep") == 6

    def test_more_than_6_hashes_not_heading(self) -> None:
        """####### (7 hashes) is not a valid heading."""
        assert _get_heading_level("####### Not a heading") == 0

    def test_no_space_after_hash_not_heading(self) -> None:
        """#NoSpace is not a valid heading."""
        assert _get_heading_level("#NoSpace") == 0

    def test_hash_only_is_heading(self) -> None:
        """A line with just '#' (and nothing else) is a valid heading."""
        assert _get_heading_level("#") == 1

    def test_non_heading_line(self) -> None:
        """Regular text returns 0."""
        assert _get_heading_level("Just text") == 0

    def test_empty_line(self) -> None:
        """Empty line returns 0."""
        assert _get_heading_level("") == 0

    def test_indented_heading_1_space(self) -> None:
        """One leading space is stripped, heading still detected."""
        assert _get_heading_level(" ## Section") == 2

    def test_indented_heading_3_spaces(self) -> None:
        """Three leading spaces are stripped, heading still detected (CommonMark max)."""
        assert _get_heading_level("   ## Section") == 2

    def test_indented_heading_4_spaces_is_code_block(self) -> None:
        """Four leading spaces are an indented code block — not a heading."""
        assert _get_heading_level("    ## Links") == 0

    def test_indented_heading_tab_is_code_block(self) -> None:
        """A leading tab is an indented code block — not a heading."""
        assert _get_heading_level("\t## Links") == 0

    def test_space_then_tab_prefix_is_code_block(self) -> None:
        """A tab inside the indent still makes the line a code block, not a heading."""
        assert _get_heading_level(" \t## Links") == 0

    def test_tab_after_marker_is_valid_heading_spacing(self) -> None:
        """A tab after the ATX marker is valid heading whitespace."""
        assert _get_heading_level("##\tLinks") == 2
