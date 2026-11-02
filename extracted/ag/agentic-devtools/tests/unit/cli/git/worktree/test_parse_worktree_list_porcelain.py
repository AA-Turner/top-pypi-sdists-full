"""Tests for parse_worktree_list_porcelain."""

from agentic_devtools.cli.git.worktree import parse_worktree_list_porcelain


class TestParseWorktreeListPorcelain:
    """Tests for parse_worktree_list_porcelain."""

    def test_returns_empty_list_for_empty_output(self):
        """Empty porcelain output parses to an empty list."""
        assert parse_worktree_list_porcelain("") == []

    def test_parses_multiple_blank_line_separated_records_and_strips_branch_ref(self):
        """Multiple records are parsed and refs/heads prefixes are stripped."""
        output = """worktree /repo/main
HEAD abc
branch refs/heads/main

worktree /repo/1900
HEAD def
branch refs/heads/feature/1900/tests
"""

        entries = parse_worktree_list_porcelain(output)

        assert [(entry.path, entry.branch) for entry in entries] == [
            ("/repo/main", "main"),
            ("/repo/1900", "feature/1900/tests"),
        ]

    def test_detached_record_has_no_branch(self):
        """A detached marker keeps the parsed branch as None."""
        entries = parse_worktree_list_porcelain("worktree /repo/detached\nHEAD abc\ndetached\n")

        assert entries[0].path == "/repo/detached"
        assert entries[0].branch is None

    def test_trailing_record_is_flushed_without_blank_line(self):
        """The final record is emitted even without a trailing blank line."""
        entries = parse_worktree_list_porcelain("worktree /repo/last\nbranch refs/heads/feature/last")

        assert len(entries) == 1
        assert entries[0].path == "/repo/last"
        assert entries[0].branch == "feature/last"

    def test_new_worktree_line_flushes_prior_record(self):
        """A new worktree line acts as a record boundary even without a blank line."""
        output = """worktree /repo/first
branch refs/heads/feature/first
worktree /repo/second
branch plain-branch
"""

        entries = parse_worktree_list_porcelain(output)

        assert [(entry.path, entry.branch) for entry in entries] == [
            ("/repo/first", "feature/first"),
            ("/repo/second", "plain-branch"),
        ]
