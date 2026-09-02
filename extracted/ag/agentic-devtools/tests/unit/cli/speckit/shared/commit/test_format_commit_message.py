"""Tests for format_commit_message in shared/commit.py."""

from __future__ import annotations

from agentic_devtools.cli.speckit.shared.commit import format_commit_message


class TestFormatCommitMessage:
    """Tests for the format_commit_message function."""

    def test_basic_message_format(self) -> None:
        """Test basic Conventional Commits format."""
        msg = format_commit_message(
            commit_type="refactor",
            scope="#1864",
            description="migrate 5 flat specs to nested hierarchy",
            issue="#1864",
        )
        assert msg.startswith("refactor(#1864): migrate 5 flat specs to nested hierarchy")
        assert msg.endswith("#1864")

    def test_co_authored_trailer_before_issue_footer(self) -> None:
        """Test that Co-authored-by appears before the issue footer."""
        msg = format_commit_message(
            commit_type="docs",
            scope="#142",
            description="generate retroactive spec from implementation artifacts",
            issue="#142",
            co_authored=True,
        )
        lines = msg.splitlines()
        co_author_idx = next(i for i, line in enumerate(lines) if "Co-authored-by" in line)
        issue_idx = next(i for i, line in enumerate(lines) if line.strip() == "#142")
        assert co_author_idx < issue_idx
        assert lines[-1].strip() == "#142"

    def test_issue_footer_is_last_line(self) -> None:
        """Test that the issue reference is always the last line."""
        msg = format_commit_message(
            commit_type="feat",
            scope="#99",
            description="add feature",
            issue="#99",
            co_authored=True,
        )
        assert msg.strip().endswith("#99")

    def test_integer_issue_converted_to_hash_ref(self) -> None:
        """Test that integer issue numbers get '#' prefix."""
        msg = format_commit_message(
            commit_type="fix",
            scope="#42",
            description="fix bug",
            issue=42,
        )
        assert "#42" in msg

    def test_no_co_authored_by_default(self) -> None:
        """Test that Co-authored-by is not included by default."""
        msg = format_commit_message(
            commit_type="docs",
            scope="#1",
            description="update docs",
            issue="#1",
        )
        assert "Co-authored-by" not in msg

    def test_no_issue_footer_when_issue_is_none(self) -> None:
        """Test that no issue footer is appended when issue is None."""
        msg = format_commit_message(
            commit_type="refactor",
            scope="speckit",
            description="migrate flat specs to nested hierarchy",
        )
        assert msg.startswith("refactor(speckit): migrate flat specs to nested hierarchy")
        # No footer line — the message ends right after the blank line
        lines = [line for line in msg.splitlines() if line.strip()]
        assert len(lines) == 1
        assert "Co-authored-by" not in msg
