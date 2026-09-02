"""Tests for _cleanup_orphaned_headings in agentic_devtools.cli.issue_template.renderer."""

from __future__ import annotations

from agentic_devtools.cli.issue_template.renderer import _cleanup_orphaned_headings


class TestCleanupOrphanedHeadings:
    """Tests for _cleanup_orphaned_headings (FR-010 micro-pass 2)."""

    def test_orphaned_heading_removed(self) -> None:
        """Heading with no data lines before next heading is removed."""
        lines = [
            "## Section A",
            "",
            "## Section B",
            "",
            "Content here",
        ]
        result = _cleanup_orphaned_headings(lines)
        assert "## Section A" not in result
        assert "## Section B" in result
        assert "Content here" in result

    def test_heading_with_data_retained(self) -> None:
        """Heading followed by data content is kept."""
        lines = [
            "## Properties",
            "",
            "Some property value",
            "",
            "## Next",
        ]
        result = _cleanup_orphaned_headings(lines)
        assert "## Properties" in result
        assert "Some property value" in result

    def test_end_of_document_boundary(self) -> None:
        """Orphaned heading at end of document is removed."""
        lines = [
            "## Section",
            "",
            "Content",
            "",
            "## Orphaned At End",
            "",
        ]
        result = _cleanup_orphaned_headings(lines)
        assert "## Orphaned At End" not in result
        assert "## Section" in result
        assert "Content" in result

    def test_bold_label_orphan_removed(self) -> None:
        """Bold-label pattern with no following data is removed."""
        lines = [
            "**Priority**:",
            "",
            "## Next",
            "",
            "Data",
        ]
        result = _cleanup_orphaned_headings(lines)
        assert "**Priority**:" not in result
        assert "## Next" in result

    def test_bold_label_with_data_retained(self) -> None:
        """Bold-label followed by data is kept."""
        lines = [
            "**Priority**:",
            "High",
            "",
            "## Next",
        ]
        result = _cleanup_orphaned_headings(lines)
        assert "**Priority**:" in result
        assert "High" in result

    def test_nested_heading_levels(self) -> None:
        """Higher-level heading is boundary for lower-level orphan check."""
        lines = [
            "# Top",
            "",
            "Content",
            "",
            "### Sub Without Content",
            "",
            "# Another Top",
            "",
            "More content",
        ]
        result = _cleanup_orphaned_headings(lines)
        assert "### Sub Without Content" not in result
        assert "# Top" in result
        assert "# Another Top" in result

    def test_bold_label_as_boundary_for_previous_heading(self) -> None:
        """A bold-label acts as boundary for a preceding orphaned heading."""
        lines = [
            "## Empty Heading",
            "",
            "**Label**:",
            "Some value",
        ]
        result = _cleanup_orphaned_headings(lines)
        assert "## Empty Heading" not in result
        assert "**Label**:" in result
        assert "Some value" in result

    def test_inline_bold_value_is_not_treated_as_orphaned_label(self) -> None:
        """Inline bold values remain content, not empty label boundaries."""
        lines = [
            "## Details",
            "",
            "**Priority**: High",
            "",
            "## Next",
            "",
            "More content",
        ]
        result = _cleanup_orphaned_headings(lines)
        assert "## Details" in result
        assert "**Priority**: High" in result
        assert "## Next" in result

    def test_indented_heading_line_is_heading_boundary_not_data(self) -> None:
        """SC-003 regression: indented '    ## Example' is a heading boundary, not data.

        Before the CommonMark-aware _get_heading_level was introduced, ``lstrip()``
        was used, so a 4-space-indented heading line like ``    ## Example`` was
        classified as level-2 heading.  ``_cleanup_orphaned_headings`` must
        preserve that behaviour (via _get_heading_level_simple) so that the
        no-mapping output remains byte-identical to the pre-PR output (SC-003).

        Both ``## Section`` and ``    ## Example`` are orphaned in the original
        implementation: the former has no data before the indented heading
        boundary, and the latter has nothing after it.
        """
        lines = [
            "## Section",
            "",
            "    ## Example",
        ]
        result = _cleanup_orphaned_headings(lines)
        # With legacy behavior both headings are orphaned and removed.
        assert "## Section" not in result
        assert "    ## Example" not in result

    def test_lower_level_heading_is_not_treated_as_data(self) -> None:
        """SC-003 regression: nested headings do not count as heading content."""
        lines = [
            "# Parent",
            "## Empty",
        ]
        result = _cleanup_orphaned_headings(lines)
        assert "# Parent" not in result
        assert "## Empty" not in result
