"""Tests for _parse_existing_markers in agentic_devtools.cli.setup.decision_log."""

import pytest

from agentic_devtools.cli.setup.decision_log import _parse_existing_markers


class TestParseExistingMarkers:
    """Direct tests for _parse_existing_markers."""

    def test_empty_content_returns_zero(self) -> None:
        """Empty string returns 0."""
        assert _parse_existing_markers("") == 0

    def test_no_markers_returns_zero(self) -> None:
        """Content without any markers returns 0."""
        assert _parse_existing_markers("Just some text\nMore text\n") == 0

    def test_valid_markers_counted(self) -> None:
        """Valid sequential markers are counted correctly."""
        content = (
            "<!-- agdt-decision-entry:start id:1 -->\nX\n"
            "<!-- agdt-decision-entry:end -->\n"
            "<!-- agdt-decision-entry:start id:2 -->\nY\n"
            "<!-- agdt-decision-entry:end -->\n"
        )
        assert _parse_existing_markers(content) == 2

    def test_stray_end_marker_no_start_raises_valueerror(self) -> None:
        """End marker with no preceding start marker raises ValueError."""
        content = "<!-- agdt-decision-entry:end -->\n"
        with pytest.raises(ValueError, match="stray end marker"):
            _parse_existing_markers(content)

    def test_stray_end_marker_after_complete_entry_raises_valueerror(self) -> None:
        """Extra end marker after a complete entry raises ValueError."""
        content = (
            "<!-- agdt-decision-entry:start id:1 -->\nX\n"
            "<!-- agdt-decision-entry:end -->\n"
            "<!-- agdt-decision-entry:end -->\n"
        )
        with pytest.raises(ValueError, match="stray end marker"):
            _parse_existing_markers(content)

    def test_malformed_start_marker_raises_valueerror(self) -> None:
        """Marker-like start substring without valid marker format raises ValueError."""
        content = "<!-- agdt-decision-entry:start id:\n"
        with pytest.raises(ValueError, match="Malformed marker sequence"):
            _parse_existing_markers(content)

    def test_malformed_start_marker_with_closed_delimiter_raises_valueerror(self) -> None:
        """Malformed marker with closing delimiter raises ValueError."""
        content = "<!-- agdt-decision-entry:start id: -->\n"
        with pytest.raises(ValueError, match="Malformed marker sequence"):
            _parse_existing_markers(content)

    def test_mixed_valid_and_malformed_start_markers_raises_valueerror(self) -> None:
        """Mixed valid and malformed start markers raises ValueError."""
        content = (
            "<!-- agdt-decision-entry:start id:1 -->\nX\n"
            "<!-- agdt-decision-entry:end -->\n"
            "<!-- agdt-decision-entry:start id: -->\n"
        )
        with pytest.raises(ValueError, match="Malformed marker sequence"):
            _parse_existing_markers(content)

    def test_nested_start_markers_raise_valueerror(self) -> None:
        """Nested start markers are rejected."""
        content = (
            "<!-- agdt-decision-entry:start id:1 -->\nX\n"
            "<!-- agdt-decision-entry:start id:2 -->\nY\n"
            "<!-- agdt-decision-entry:end -->\n"
            "<!-- agdt-decision-entry:end -->\n"
        )
        with pytest.raises(ValueError, match="nested start marker"):
            _parse_existing_markers(content)

    def test_end_marker_before_first_start_raises_valueerror(self) -> None:
        """An end marker before the first start marker is rejected."""
        content = "<!-- agdt-decision-entry:end -->\n<!-- agdt-decision-entry:start id:1 -->\n"
        with pytest.raises(ValueError, match="stray end marker"):
            _parse_existing_markers(content)

    def test_truncated_end_marker_alone_raises_valueerror(self) -> None:
        """Truncated end marker (no closing -->) with no start marker raises ValueError."""
        content = "<!-- agdt-decision-entry:end\n"
        with pytest.raises(ValueError, match="Malformed marker sequence"):
            _parse_existing_markers(content)

    def test_truncated_end_marker_after_complete_entry_raises_valueerror(self) -> None:
        """Truncated end marker after a complete entry raises ValueError."""
        content = (
            "<!-- agdt-decision-entry:start id:1 -->\nX\n"
            "<!-- agdt-decision-entry:end -->\n"
            "<!-- agdt-decision-entry:end\n"
        )
        with pytest.raises(ValueError, match="Malformed marker sequence"):
            _parse_existing_markers(content)

    def test_truncated_end_marker_inside_open_entry_raises_valueerror(self) -> None:
        """Truncated end marker inside an open entry (no valid end) raises ValueError."""
        content = "<!-- agdt-decision-entry:start id:1 -->\n<!-- agdt-decision-entry:end\n"
        with pytest.raises(ValueError, match="Malformed marker sequence"):
            _parse_existing_markers(content)

    def test_out_of_order_ids_raises_valueerror(self) -> None:
        """Out-of-order entry IDs (e.g. [2, 1]) raise ValueError with out-of-order message."""
        content = (
            "<!-- agdt-decision-entry:start id:2 -->\nX\n"
            "<!-- agdt-decision-entry:end -->\n"
            "<!-- agdt-decision-entry:start id:1 -->\nY\n"
            "<!-- agdt-decision-entry:end -->\n"
        )
        with pytest.raises(ValueError, match="Out-of-order entry IDs"):
            _parse_existing_markers(content)

    def test_gap_in_ids_raises_valueerror(self) -> None:
        """A gap in entry IDs (e.g. [1, 3]) raises ValueError with gap message."""
        content = (
            "<!-- agdt-decision-entry:start id:1 -->\nX\n"
            "<!-- agdt-decision-entry:end -->\n"
            "<!-- agdt-decision-entry:start id:3 -->\nY\n"
            "<!-- agdt-decision-entry:end -->\n"
        )
        with pytest.raises(ValueError, match="Gap in entry ID sequence"):
            _parse_existing_markers(content)

    def test_gap_and_out_of_order_ids_reports_gap(self) -> None:
        """IDs that are both out-of-order and have a gap (e.g. [3, 1]) report a gap.

        When the sorted IDs do not equal expected [1..N], a gap is reported as the
        more fundamental problem, even if the sequence is also out-of-order.
        """
        content = (
            "<!-- agdt-decision-entry:start id:3 -->\nX\n"
            "<!-- agdt-decision-entry:end -->\n"
            "<!-- agdt-decision-entry:start id:1 -->\nY\n"
            "<!-- agdt-decision-entry:end -->\n"
        )
        with pytest.raises(ValueError, match="Gap in entry ID sequence"):
            _parse_existing_markers(content)
