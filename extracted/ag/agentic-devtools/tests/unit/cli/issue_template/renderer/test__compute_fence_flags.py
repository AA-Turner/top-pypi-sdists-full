"""Tests for _compute_fence_flags in agentic_devtools.cli.issue_template.renderer."""

from __future__ import annotations

from agentic_devtools.cli.issue_template.renderer import _compute_fence_flags


class TestComputeFenceFlags:
    """Tests for _compute_fence_flags."""

    def test_no_fences_all_false(self) -> None:
        """Lines without fences are all False."""
        assert _compute_fence_flags(["hello", "world"]) == [False, False]

    def test_fenced_block_marked_true(self) -> None:
        """Opening and content lines inside a fenced block are True."""
        lines = ["```", "code", "```", "after"]
        assert _compute_fence_flags(lines) == [True, True, True, False]

    def test_crlf_closing_fence_recognized(self) -> None:
        """A closing fence line with a trailing \\r (CRLF split) closes the block."""
        lines = ["```\r", "code", "```\r", "after"]
        flags = _compute_fence_flags(lines)
        # The closing ``` with trailing \r must still be recognised, so the
        # line after the block is NOT marked as fenced.
        assert flags == [True, True, True, False]

    def test_crlf_tilde_fence_closes(self) -> None:
        """A tilde fence with a trailing \\r also closes correctly."""
        lines = ["~~~\r", "text\r", "~~~\r", "outside\r"]
        flags = _compute_fence_flags(lines)
        assert flags == [True, True, True, False]

    def test_backtick_fence_with_backtick_in_info_string_is_not_a_fence(self) -> None:
        """A backtick fence whose info string contains a backtick is not a fence (CommonMark §4.5)."""
        lines = ["``` lang`", "code", "after"]
        assert _compute_fence_flags(lines) == [False, False, False]

    def test_tilde_fence_with_tilde_in_info_string_is_a_fence(self) -> None:
        """A tilde fence may contain tildes in its info string (CommonMark §4.6)."""
        lines = ["~~~ lang~", "code", "~~~", "after"]
        assert _compute_fence_flags(lines) == [True, True, True, False]

    def test_unclosed_fence_remaining_lines_true(self) -> None:
        """Lines after an unclosed fence remain True."""
        lines = ["```", "code"]
        assert _compute_fence_flags(lines) == [True, True]

    def test_empty_input(self) -> None:
        """Empty input produces empty output."""
        assert _compute_fence_flags([]) == []
