"""Tests for dispatch_conflict_repair() in GitHubActionsProvider."""

import json
from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.cli.ci.github_provider import GitHubActionsProvider
from agentic_devtools.cli.ci.guards import CONFLICT_REPAIR_MARKER_PREFIX


def _api_response(data: dict) -> str:
    return json.dumps(data)


class TestDispatchConflictRepair:
    """Tests for GitHubActionsProvider.dispatch_conflict_repair()."""

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    @patch("agentic_devtools.cli.ci.github_provider._read_repo_file")
    def test_raises_when_speckit_pr_token_missing(self, mock_read_file, mock_run_safe) -> None:
        provider = GitHubActionsProvider(repo="owner/repo")

        with patch.dict("os.environ", {}, clear=True):
            with pytest.raises(RuntimeError, match="SPECKIT_PR_TOKEN"):
                provider.dispatch_conflict_repair(
                    pr_number=42,
                    head_sha="abc123",
                    base_sha="def456",
                    base_branch="main",
                    head_branch="feature/test",
                )

        mock_read_file.assert_not_called()
        mock_run_safe.assert_not_called()

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    @patch("agentic_devtools.cli.ci.github_provider._read_repo_file")
    @patch.dict("os.environ", {"SPECKIT_PR_TOKEN": "test-pat-token"}, clear=False)
    def test_posts_comment_starting_with_copilot(self, mock_read_file, mock_run_safe) -> None:
        """The posted comment body must begin with '@copilot'."""
        mock_read_file.return_value = "## Prompt content"
        mock_run_safe.return_value = MagicMock(returncode=0, stdout=_api_response({"id": 999}), stderr="")

        provider = GitHubActionsProvider(repo="owner/repo")
        comment_id = provider.dispatch_conflict_repair(
            pr_number=42,
            head_sha="abc123",
            base_sha="def456",
            base_branch="main",
            head_branch="feature/test",
        )

        assert comment_id == 999
        # Find the POST call to the comments API
        post_call = next(c for c in mock_run_safe.call_args_list if "--method" in c[0][0] and "POST" in c[0][0])
        posted_body = json.loads(post_call[1]["input"])["body"]
        assert posted_body.startswith("@copilot")

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    @patch("agentic_devtools.cli.ci.github_provider._read_repo_file")
    @patch.dict("os.environ", {"SPECKIT_PR_TOKEN": "test-pat-token"}, clear=False)
    def test_embeds_conflict_repair_marker(self, mock_read_file, mock_run_safe) -> None:
        """The comment body must embed the conflict-repair idempotency marker."""
        mock_read_file.return_value = "Prompt content"
        mock_run_safe.return_value = MagicMock(returncode=0, stdout=_api_response({"id": 42}), stderr="")

        provider = GitHubActionsProvider(repo="owner/repo")
        provider.dispatch_conflict_repair(
            pr_number=10,
            head_sha="aaa111",
            base_sha="bbb222",
            base_branch="main",
            head_branch="feature/x",
        )

        post_call = next(c for c in mock_run_safe.call_args_list if "--method" in c[0][0] and "POST" in c[0][0])
        posted_body = json.loads(post_call[1]["input"])["body"]
        assert CONFLICT_REPAIR_MARKER_PREFIX in posted_body
        assert "aaa111" in posted_body
        assert "bbb222" in posted_body

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    @patch("agentic_devtools.cli.ci.github_provider._read_repo_file")
    @patch.dict("os.environ", {"SPECKIT_PR_TOKEN": "test-pat-token"}, clear=False)
    def test_embeds_prompt_file_content(self, mock_read_file, mock_run_safe) -> None:
        """When the prompt file is readable, its content is embedded in the comment."""
        mock_read_file.return_value = "# Cloud Agent Conflict Resolution Prompt"
        mock_run_safe.return_value = MagicMock(returncode=0, stdout=_api_response({"id": 77}), stderr="")

        provider = GitHubActionsProvider(repo="owner/repo")
        provider.dispatch_conflict_repair(
            pr_number=5,
            head_sha="ccc333",
            base_sha="ddd444",
            base_branch="main",
            head_branch="feature/y",
        )

        post_call = next(c for c in mock_run_safe.call_args_list if "--method" in c[0][0] and "POST" in c[0][0])
        posted_body = json.loads(post_call[1]["input"])["body"]
        assert "Cloud Agent Conflict Resolution Prompt" in posted_body

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    @patch("agentic_devtools.cli.ci.github_provider._read_repo_file")
    @patch.dict("os.environ", {"SPECKIT_PR_TOKEN": "test-pat-token"}, clear=False)
    def test_graceful_fallback_when_prompt_file_missing(self, mock_read_file, mock_run_safe) -> None:
        """When the prompt file cannot be read, the comment is still posted."""
        mock_read_file.return_value = ""  # _read_repo_file returns "" on error
        mock_run_safe.return_value = MagicMock(returncode=0, stdout=_api_response({"id": 55}), stderr="")

        provider = GitHubActionsProvider(repo="owner/repo")
        comment_id = provider.dispatch_conflict_repair(
            pr_number=3,
            head_sha="eee555",
            base_sha="fff666",
            base_branch="main",
            head_branch="feature/z",
        )

        assert comment_id == 55
        post_call = next(c for c in mock_run_safe.call_args_list if "--method" in c[0][0] and "POST" in c[0][0])
        posted_body = json.loads(post_call[1]["input"])["body"]
        assert posted_body.startswith("@copilot")

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    @patch("agentic_devtools.cli.ci.github_provider._read_repo_file")
    @patch.dict("os.environ", {"SPECKIT_PR_TOKEN": "test-speckit-pat"}, clear=False)
    def test_uses_speckit_pr_token(self, mock_read_file, mock_run_safe) -> None:
        """Authentication uses SPECKIT_PR_TOKEN (has issues:write permission)."""
        mock_read_file.return_value = ""
        mock_run_safe.return_value = MagicMock(returncode=0, stdout=_api_response({"id": 1}), stderr="")

        provider = GitHubActionsProvider(repo="owner/repo")
        provider.dispatch_conflict_repair(
            pr_number=1,
            head_sha="111",
            base_sha="222",
            base_branch="main",
            head_branch="feat",
        )

        # The POST call environment should have GH_TOKEN set to our PAT
        post_call = next(c for c in mock_run_safe.call_args_list if "--method" in c[0][0] and "POST" in c[0][0])
        call_env = post_call[1].get("env", {})
        assert call_env.get("GH_TOKEN") == "test-speckit-pat"

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    @patch("agentic_devtools.cli.ci.github_provider._read_repo_file")
    @patch.dict("os.environ", {"SPECKIT_PR_TOKEN": "test-pat"}, clear=False)
    def test_returns_comment_id(self, mock_read_file, mock_run_safe) -> None:
        """The method returns the integer comment ID from the API response."""
        mock_read_file.return_value = ""
        mock_run_safe.return_value = MagicMock(returncode=0, stdout=_api_response({"id": 12345}), stderr="")

        provider = GitHubActionsProvider(repo="owner/repo")
        result = provider.dispatch_conflict_repair(
            pr_number=7,
            head_sha="sha7",
            base_sha="basesha7",
            base_branch="main",
            head_branch="br7",
        )

        assert result == 12345

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    @patch("agentic_devtools.cli.ci.github_provider._read_repo_file")
    @patch.dict("os.environ", {"SPECKIT_PR_TOKEN": "test-pat", "GITHUB_REPOSITORY": ""}, clear=False)
    def test_no_repo_uses_plain_prompt_path(self, mock_read_file, mock_run_safe) -> None:
        """When no repo is available the prompt link falls back to a plain path (no URL)."""
        mock_read_file.return_value = ""
        mock_run_safe.return_value = MagicMock(returncode=0, stdout=_api_response({"id": 1}), stderr="")

        provider = GitHubActionsProvider(repo="")
        provider.dispatch_conflict_repair(
            pr_number=1,
            head_sha="sha1",
            base_sha="base1",
            base_branch="main",
            head_branch="feat",
        )

        post_call = next(c for c in mock_run_safe.call_args_list if "--method" in c[0][0] and "POST" in c[0][0])
        posted_body = json.loads(post_call[1]["input"])["body"]
        # Without a valid repo slug the link must NOT contain a github.com URL
        assert "github.com" not in posted_body
        assert ".github/prompts/agdt.resolve-merge-conflicts.cloud-agent.prompt.md" in posted_body

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    @patch("agentic_devtools.cli.ci.github_provider._read_repo_file")
    @patch.dict("os.environ", {"SPECKIT_PR_TOKEN": "test-pat"}, clear=False)
    def test_prompt_link_uses_head_sha_when_available(self, mock_read_file, mock_run_safe) -> None:
        """The prompt URL should use the PR head SHA to match the embedded prompt content."""
        mock_read_file.return_value = ""
        mock_run_safe.return_value = MagicMock(returncode=0, stdout=_api_response({"id": 1}), stderr="")

        provider = GitHubActionsProvider(repo="owner/repo")
        provider.dispatch_conflict_repair(
            pr_number=1,
            head_sha="sha1",
            base_sha="base1",
            base_branch="develop",
            head_branch="feat",
        )

        post_call = next(c for c in mock_run_safe.call_args_list if "--method" in c[0][0] and "POST" in c[0][0])
        posted_body = json.loads(post_call[1]["input"])["body"]
        assert "blob/sha1/" in posted_body
        assert "blob/develop/" not in posted_body

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    @patch("agentic_devtools.cli.ci.github_provider._read_repo_file")
    @patch.dict("os.environ", {"SPECKIT_PR_TOKEN": "test-pat"}, clear=False)
    def test_conflict_marker_appended_at_end_after_details(self, mock_read_file, mock_run_safe) -> None:
        """The conflict-repair marker is the final line, after the closing </details>.

        End placement keeps the marker out of the quoted top-of-comment region so a
        cloud agent's truncated quote can never split the HTML comment.
        """
        mock_read_file.return_value = "Prompt content"
        mock_run_safe.return_value = MagicMock(returncode=0, stdout=_api_response({"id": 5}), stderr="")

        provider = GitHubActionsProvider(repo="owner/repo")
        provider.dispatch_conflict_repair(
            pr_number=7,
            head_sha="head777",
            base_sha="base888",
            base_branch="main",
            head_branch="feature/y",
        )

        post_call = next(c for c in mock_run_safe.call_args_list if "--method" in c[0][0] and "POST" in c[0][0])
        posted_body = json.loads(post_call[1]["input"])["body"]
        marker_start = posted_body.rindex(CONFLICT_REPAIR_MARKER_PREFIX)
        # Marker comes after the last closing </details>.
        assert posted_body.rindex("</details>") < marker_start
        # Marker is the final line — nothing follows it.
        assert "\n" not in posted_body[marker_start:]
        assert posted_body.rstrip().endswith(" -->")
