"""Tests for _path_assignment_contains_entry."""

from agentic_devtools.cli.setup.shell_profile import _path_assignment_contains_entry


class TestPathAssignmentContainsEntry:
    """Tests for _path_assignment_contains_entry."""

    def test_returns_false_when_line_is_not_assignment(self) -> None:
        """Lines without '=' are not treated as PATH assignments."""
        assert _path_assignment_contains_entry("export PATH", "/home/user/.agdt/bin", "bash") is False

    def test_matches_unquoted_posix_component(self) -> None:
        """Unquoted POSIX PATH entries are matched exactly."""
        assert (
            _path_assignment_contains_entry(
                "PATH=/home/user/.agdt/bin:$PATH",
                "/home/user/.agdt/bin",
                "bash",
            )
            is True
        )

    def test_matches_component_with_component_level_quotes(self) -> None:
        """Quoted components inside the assignment are matched after stripping quotes."""
        assert (
            _path_assignment_contains_entry(
                'PATH="/home/user/.agdt/bin":$PATH',
                "/home/user/.agdt/bin",
                "bash",
            )
            is True
        )

    def test_matches_quoted_assignment_with_trailing_inline_comment(self) -> None:
        """Trailing inline shell comments do not prevent matching the managed PATH entry.

        Lines like 'export PATH="/home/user/.agdt/bin:$PATH"  # managed' must be
        recognized as already containing the entry; without comment-stripping the
        '# managed' fragment becomes part of the last PATH component and causes a
        false-negative that appends a duplicate entry.
        """
        assert (
            _path_assignment_contains_entry(
                'export PATH="/home/user/.agdt/bin:$PATH"  # managed',
                "/home/user/.agdt/bin",
                "bash",
            )
            is True
        )

    def test_matches_single_quoted_assignment_with_trailing_inline_comment(self) -> None:
        """Single-quoted assignments with trailing comments are handled correctly."""
        assert (
            _path_assignment_contains_entry(
                "export PATH='/home/user/.agdt/bin:$PATH'  # managed",
                "/home/user/.agdt/bin",
                "bash",
            )
            is True
        )

    def test_no_closing_quote_still_returns_false_safely(self) -> None:
        """A value that starts with a quote but has no closing quote is handled safely.

        When rfind finds no closing quote (close_idx == -1), the comment-strip block
        is skipped and the value is processed as-is (branch 113->116 in shell_profile).
        The entry should not be matched.
        """
        assert (
            _path_assignment_contains_entry(
                'PATH="/home/user/.agdt/bin',
                "/home/user/.agdt/bin",
                "bash",
            )
            is False
        )

    def test_matches_component_quoted_individually_when_value_starts_unquoted(self) -> None:
        """Components with individual surrounding quotes are matched after per-component stripping.

        When the overall value begins with a non-quote character the outer
        comment-strip block is bypassed; individual components are still
        de-quoted inside the loop (line 122 in shell_profile.py).
        """
        assert (
            _path_assignment_contains_entry(
                'PATH=$PATH:"/home/user/.agdt/bin"',
                "/home/user/.agdt/bin",
                "bash",
            )
            is True
        )
