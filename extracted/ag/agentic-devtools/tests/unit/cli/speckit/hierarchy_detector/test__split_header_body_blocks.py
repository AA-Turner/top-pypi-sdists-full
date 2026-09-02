"""Tests for _split_header_body_blocks helper."""

from __future__ import annotations

from agentic_devtools.cli.speckit.hierarchy_detector import _split_header_body_blocks


class TestSplitHeaderBodyBlocks:
    """Tests for _split_header_body_blocks helper."""

    def test_single_page_response(self) -> None:
        """Single page response with headers and JSON body."""
        raw = 'HTTP/2 200\ncontent-type: application/json\n\n[{"number": 1}]'
        blocks = _split_header_body_blocks(raw)
        assert len(blocks) == 1
        assert "200" in blocks[0][0]
        assert '[{"number": 1}]' in blocks[0][1]

    def test_multi_page_response(self) -> None:
        """Multi-page response is split into separate blocks."""
        raw = (
            'HTTP/2 200\ncontent-type: application/json\n\n[{"number": 1}]\n'
            'HTTP/2 200\ncontent-type: application/json\n\n[{"number": 2}]'
        )
        blocks = _split_header_body_blocks(raw)
        assert len(blocks) == 2

    def test_empty_input(self) -> None:
        """Empty input returns empty list."""
        assert _split_header_body_blocks("") == []

    def test_no_body_separator(self) -> None:
        """Header block with no empty line (no body separator) returns empty body."""
        raw = "HTTP/2 200\ncontent-type: application/json\nno-empty-line-here"
        blocks = _split_header_body_blocks(raw)
        assert len(blocks) == 1
        headers, body = blocks[0]
        assert "200" in headers
        assert body == ""
