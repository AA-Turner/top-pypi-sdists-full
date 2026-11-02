"""Tests for assemble_context in retro_spec/synthesis.py."""

from __future__ import annotations

from unittest.mock import patch

from agentic_devtools.cli.speckit.retro_spec.artifact_collector import (
    IssueArtifact,
    PRArtifact,
)
from agentic_devtools.cli.speckit.retro_spec.synthesis import assemble_context


class TestAssembleContext:
    """Tests for the assemble_context function."""

    def test_includes_issue_title_and_body(self) -> None:
        """Test that issue title and body are included."""
        issue = IssueArtifact(number=42, title="Fix the bug", body="The bug is here.", state="closed")
        context = assemble_context(issue, [], [], [])
        assert "Fix the bug" in context
        assert "The bug is here." in context

    def test_includes_pr_info(self) -> None:
        """Test that PR information is included."""
        issue = IssueArtifact(number=42, title="Issue", body="Body", state="closed")
        prs = [PRArtifact(number=10, title="Fix PR", body="PR body")]
        context = assemble_context(issue, prs, [], [])
        assert "PR #10" in context
        assert "Fix PR" in context

    def test_includes_diffs(self) -> None:
        """Test that diffs are included."""
        issue = IssueArtifact(number=42, title="Issue", body="Body", state="closed")
        diffs = ["diff --git a/file.py b/file.py\n+new line"]
        context = assemble_context(issue, [], diffs, [])
        assert "diff --git" in context

    def test_includes_commit_messages(self) -> None:
        """Test that commit messages are included."""
        issue = IssueArtifact(number=42, title="Issue", body="Body", state="closed")
        commits = ["feat: add feature", "fix: correct typo"]
        context = assemble_context(issue, [], [], commits)
        assert "feat: add feature" in context
        assert "fix: correct typo" in context

    def test_truncates_large_context(self) -> None:
        """Test that context is truncated for very large inputs."""
        issue = IssueArtifact(number=42, title="Issue", body="Body", state="closed")
        # Create a very large diff
        large_diff = "x" * 200_000
        context = assemble_context(issue, [], [large_diff], [])
        # Final truncation adds "[TRUNCATED]" suffix so allow small overshoot
        assert len(context) <= 100_020

    def test_includes_labels_and_limited_comments(self) -> None:
        """Test that labels and up to ten truncated comments are included."""
        issue = IssueArtifact(
            number=42,
            title="Issue",
            body="Body",
            comments=["x" * 2500 for _ in range(11)],
            labels=["bug", "retro"],
            state="closed",
        )

        context = assemble_context(issue, [], [], [])

        assert "Labels: bug, retro" in context
        assert "**Comment 10:**" in context
        assert "**Comment 11:**" not in context
        assert "x" * 2000 in context
        assert "x" * 2001 not in context

    def test_handles_pr_without_body(self) -> None:
        """Test that PRs without bodies still render headings cleanly."""
        issue = IssueArtifact(number=42, title="Issue", body="Body", state="closed")
        prs = [PRArtifact(number=10, title="Fix PR", body="")]

        context = assemble_context(issue, prs, [], [])

        assert "### PR #10: Fix PR" in context
        assert "## Related Pull Requests" in context

    def test_marks_remaining_diffs_as_truncated_when_budget_is_exhausted(self) -> None:
        """Test that remaining diffs are skipped once the diff budget reaches zero."""
        issue = IssueArtifact(number=42, title="Issue", body="Body", state="closed")

        def fake_len(value: object) -> int:
            if isinstance(value, str) and "## Code Changes (Diffs)" in value and "diff one" not in value:
                return 118
            if isinstance(value, str) and "[Remaining diffs truncated due to size limits]" in value:
                return 10
            return len(str(value))

        with (
            patch("agentic_devtools.cli.speckit.retro_spec.synthesis._MAX_CONTEXT_CHARS", 120),
            patch("agentic_devtools.cli.speckit.retro_spec.synthesis.len", side_effect=fake_len, create=True),
        ):
            context = assemble_context(issue, [], ["diff one", "diff two"], [])

        assert "[Remaining diffs truncated due to size limits]" in context


class TestAssembleContextMilestone:
    """Tests for milestone inclusion in assemble_context."""

    def test_includes_milestone_when_present(self) -> None:
        """Test that milestone is included in context."""
        from agentic_devtools.cli.speckit.retro_spec.artifact_collector import IssueArtifact
        from agentic_devtools.cli.speckit.retro_spec.synthesis import assemble_context

        issue = IssueArtifact(number=1, title="T", body="b", milestone="v2.0", state="closed")
        ctx = assemble_context(issue, [], [], [])
        assert "Milestone: v2.0" in ctx
