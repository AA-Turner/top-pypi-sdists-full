"""Tests for _line_blocks_retention in agentic_devtools.cli.issue_template.renderer."""

from __future__ import annotations

from agentic_devtools.cli.issue_template.renderer import _line_blocks_retention


class TestLineBlocksRetention:
    """Tests for excluded-placeholder retention blocking."""

    def test_empty_excluded_fields_do_not_block(self) -> None:
        assert _line_blocks_retention("{{url}} {{priority}}", "url", frozenset()) is False

    def test_independently_excluded_placeholder_blocks_retention(self) -> None:
        assert _line_blocks_retention("{{url}} {{priority}}", "url", frozenset({"priority"})) is True

    def test_unexcluded_placeholder_does_not_block_retention(self) -> None:
        assert _line_blocks_retention("{{url}} {{title}}", "url", frozenset({"priority"})) is False

    def test_same_key_aliases_do_not_block_retention(self) -> None:
        assert _line_blocks_retention("{{id}} {{issue_id}}", "id", frozenset({"priority"})) is False

    def test_unexcluded_placeholder_before_excluded_one_still_blocks(self) -> None:
        assert _line_blocks_retention("{{url}} {{title}} {{priority}}", "url", frozenset({"priority"})) is True
