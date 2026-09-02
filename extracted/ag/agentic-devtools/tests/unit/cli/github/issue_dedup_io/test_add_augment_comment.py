"""Tests for add_augment_comment."""

from __future__ import annotations

from unittest.mock import patch

import pytest

_MOD = "agentic_devtools.cli.github.issue_dedup_io"


class TestAddAugmentComment:
    """Tests for the add_augment_comment function."""

    @patch(f"{_MOD}.resolve_github_repo", return_value="owner/repo")
    @patch(f"{_MOD}._gh_api")
    def test_posts_fenced_comment(self, mock_api, mock_repo) -> None:
        """Posts comment with ~~~~ fencing around body."""
        from agentic_devtools.cli.github.issue_dedup_io import add_augment_comment

        mock_api.return_value = ""
        add_augment_comment(42, "Error details here", repo="owner/repo")
        mock_api.assert_called_once_with(
            "/repos/owner/repo/issues/42/comments",
            method="POST",
            body={"body": "~~~~\nError details here\n~~~~"},
        )

    @patch(f"{_MOD}.resolve_github_repo", return_value="owner/repo")
    @patch(f"{_MOD}._gh_api")
    def test_preserves_body_verbatim(self, mock_api, mock_repo) -> None:
        """Body content is preserved verbatim (no trimming)."""
        from agentic_devtools.cli.github.issue_dedup_io import add_augment_comment

        mock_api.return_value = ""
        body = "  leading spaces\n  and indentation  \n"
        add_augment_comment(42, body, repo="owner/repo")
        expected_body = f"~~~~\n{body}~~~~"
        posted_body = mock_api.call_args.kwargs["body"]["body"]
        assert posted_body == expected_body
        assert posted_body[len("~~~~\n") : -len("~~~~")] == body

    @patch(f"{_MOD}.resolve_github_repo", return_value="owner/repo")
    @patch(f"{_MOD}._gh_api")
    def test_exact_fence_format(self, mock_api, mock_repo) -> None:
        """Uses exactly ~~~~ (4 tildes) for fencing."""
        from agentic_devtools.cli.github.issue_dedup_io import add_augment_comment

        mock_api.return_value = ""
        add_augment_comment(42, "content", repo="owner/repo")
        posted_body = mock_api.call_args.kwargs["body"]["body"]
        assert posted_body.startswith("~~~~\n")
        assert posted_body.endswith("\n~~~~")

    @patch(f"{_MOD}.resolve_github_repo", return_value="owner/repo")
    @patch(f"{_MOD}._gh_api")
    def test_expands_fence_when_body_contains_tilde_fence(self, mock_api, mock_repo) -> None:
        """Chooses a longer fence when body already contains ~~~~."""
        from agentic_devtools.cli.github.issue_dedup_io import add_augment_comment

        mock_api.return_value = ""
        body = "before\n~~~~\nafter"
        add_augment_comment(42, body, repo="owner/repo")
        posted_body = mock_api.call_args.kwargs["body"]["body"]
        assert posted_body.startswith("~~~~~\n")
        assert posted_body.endswith("\n~~~~~")

    @patch(f"{_MOD}.resolve_github_repo", return_value="owner/repo")
    @patch(f"{_MOD}._gh_api")
    def test_api_failure_raises(self, mock_api, mock_repo) -> None:
        """RuntimeError propagates from _gh_api."""
        from agentic_devtools.cli.github.issue_dedup_io import add_augment_comment

        mock_api.side_effect = RuntimeError("API error")
        with pytest.raises(RuntimeError, match="API error"):
            add_augment_comment(42, "body", repo="owner/repo")

    @patch(f"{_MOD}.resolve_github_repo", return_value="owner/repo")
    @patch(f"{_MOD}.run_safe")
    def test_run_safe_uses_shell_false(self, mock_run_safe, mock_repo) -> None:
        """All run_safe calls use shell=False."""
        from agentic_devtools.cli.github.issue_dedup_io import add_augment_comment

        class FakeResult:
            returncode = 0
            stdout = ""
            stderr = ""

        mock_run_safe.return_value = FakeResult()
        add_augment_comment(42, "body", repo="owner/repo")
        for call_item in mock_run_safe.call_args_list:
            assert call_item.kwargs.get("shell") is False

    @patch(f"{_MOD}.resolve_github_repo", return_value="owner/repo")
    @patch(f"{_MOD}._gh_api")
    def test_empty_body(self, mock_api, mock_repo) -> None:
        """Empty body is wrapped in fences."""
        from agentic_devtools.cli.github.issue_dedup_io import add_augment_comment

        mock_api.return_value = ""
        add_augment_comment(42, "", repo="owner/repo")
        posted_body = mock_api.call_args.kwargs["body"]["body"]
        assert posted_body == "~~~~\n\n~~~~"

    @patch(f"{_MOD}.resolve_github_repo", return_value="owner/repo")
    @patch(f"{_MOD}._gh_api")
    def test_multiline_body(self, mock_api, mock_repo) -> None:
        """Multiline body is preserved."""
        from agentic_devtools.cli.github.issue_dedup_io import add_augment_comment

        mock_api.return_value = ""
        body = "line1\nline2\nline3"
        add_augment_comment(42, body, repo="owner/repo")
        posted_body = mock_api.call_args.kwargs["body"]["body"]
        assert posted_body == "~~~~\nline1\nline2\nline3\n~~~~"

    @patch(f"{_MOD}.resolve_github_repo", return_value="owner/repo")
    @patch(f"{_MOD}._gh_api")
    def test_preserves_existing_trailing_newline_without_extra_blank_line(
        self,
        mock_api,
        mock_repo,
    ) -> None:
        """Trailing newline in body does not gain an extra blank line."""
        from agentic_devtools.cli.github.issue_dedup_io import add_augment_comment

        mock_api.return_value = ""
        body = "line1\nline2\n"
        add_augment_comment(42, body, repo="owner/repo")
        posted_body = mock_api.call_args.kwargs["body"]["body"]
        assert posted_body == "~~~~\nline1\nline2\n~~~~"

    @patch(f"{_MOD}.resolve_github_repo", return_value="owner/repo")
    @patch(f"{_MOD}._gh_api")
    def test_preserves_multiple_trailing_newlines_without_adding_another(
        self,
        mock_api,
        mock_repo,
    ) -> None:
        """Multiple trailing newlines are preserved without an extra blank line."""
        from agentic_devtools.cli.github.issue_dedup_io import add_augment_comment

        mock_api.return_value = ""
        body = "line1\nline2\n\n\n"
        add_augment_comment(42, body, repo="owner/repo")
        posted_body = mock_api.call_args.kwargs["body"]["body"]
        assert posted_body == "~~~~\nline1\nline2\n\n\n~~~~"
