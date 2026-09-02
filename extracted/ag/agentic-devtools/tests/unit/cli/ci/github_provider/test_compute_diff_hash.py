"""Tests for GitHubActionsProvider.compute_diff_hash."""

from unittest.mock import patch

import pytest

from agentic_devtools.cli.ci.github_provider import GitHubActionsProvider


def _git_stub(responses: dict, *, patch_id_output: str = "", patch_id_exc: Exception | None = None):
    """Build a ``_run_git`` side effect from an args→output mapping.

    ``patch_id_exc``, when given, is raised by the ``git patch-id`` invocation.
    """

    def side_effect(args, *, stdin_text=None):
        key = tuple(args)
        if key == ("patch-id", "--verbatim"):
            assert stdin_text is not None
            if patch_id_exc is not None:
                raise patch_id_exc
            return patch_id_output
        if key in responses:
            result = responses[key]
            if isinstance(result, Exception):
                raise result
            return result
        raise RuntimeError(f"unexpected: {args}")

    return side_effect


class TestComputeDiffHash:
    """Tests for compute_diff_hash method."""

    @patch.object(GitHubActionsProvider, "_run_git")
    def test_returns_patch_id_of_diff(self, mock_run_git) -> None:
        diff_output = "diff --git a/foo.py b/foo.py\n+new line"
        mock_run_git.side_effect = _git_stub(
            {
                ("fetch", "origin", "main"): "",
                ("cat-file", "-e", "abc123^{commit}"): "",
                ("diff", "-U1", "origin/main...abc123"): diff_output,
            },
            patch_id_output="1045a6f6deadbeef 0000000000000000000000000000000000000000\n",
        )
        provider = GitHubActionsProvider(repo="owner/repo")

        result = provider.compute_diff_hash(base_branch="main", sha="abc123")

        assert result == "patch-id:1045a6f6deadbeef"

    @patch.object(GitHubActionsProvider, "_run_git")
    def test_passes_diff_to_patch_id_verbatim_on_stdin(self, mock_run_git) -> None:
        """``--verbatim`` is required — ``--stable`` collides on whitespace-only edits."""
        diff_output = "diff --git a/foo.py b/foo.py\n+  spaced  "
        mock_run_git.side_effect = _git_stub(
            {
                ("fetch", "origin", "main"): "",
                ("cat-file", "-e", "abc123^{commit}"): "",
                ("diff", "-U1", "origin/main...abc123"): diff_output,
            },
            patch_id_output="ed1721a8 0000\n",
        )
        provider = GitHubActionsProvider(repo="owner/repo")

        provider.compute_diff_hash(base_branch="main", sha="abc123")

        mock_run_git.assert_any_call(["patch-id", "--verbatim"], stdin_text=diff_output)

    @patch.object(GitHubActionsProvider, "_run_git")
    def test_returns_sha256_fingerprint_when_diff_is_empty(self, mock_run_git) -> None:
        """An empty diff returns a stable sha256 fingerprint for rebase invariance."""
        mock_run_git.side_effect = _git_stub(
            {
                ("fetch", "origin", "main"): "",
                ("cat-file", "-e", "abc123^{commit}"): "",
                ("diff", "-U1", "origin/main...abc123"): "",
            },
            patch_id_output="\n",
        )
        provider = GitHubActionsProvider(repo="owner/repo")

        result = provider.compute_diff_hash(base_branch="main", sha="abc123")

        assert result is not None
        assert result.startswith("sha256:")
        # Two calls with the same (empty) diff must produce the same fingerprint.
        assert result == provider.compute_diff_hash(base_branch="main", sha="abc123")

    @patch.object(GitHubActionsProvider, "_run_git")
    def test_raises_runtime_error_when_fetch_base_fails(self, mock_run_git) -> None:
        mock_run_git.side_effect = RuntimeError("network failure")
        provider = GitHubActionsProvider(repo="owner/repo")

        with pytest.raises(RuntimeError, match="failed to fetch base branch main"):
            provider.compute_diff_hash(base_branch="main", sha="abc123")

    @patch.object(GitHubActionsProvider, "_run_git")
    def test_returns_none_when_sha_unavailable_and_targeted_fetch_fails(self, mock_run_git) -> None:
        mock_run_git.side_effect = _git_stub(
            {
                ("fetch", "origin", "main"): "",
                ("cat-file", "-e", "deadbeef^{commit}"): RuntimeError("unknown object"),
                ("fetch", "--no-tags", "origin", "deadbeef"): RuntimeError("sha not found"),
            }
        )
        provider = GitHubActionsProvider(repo="owner/repo")

        result = provider.compute_diff_hash(base_branch="main", sha="deadbeef")

        assert result is None

    @patch.object(GitHubActionsProvider, "_run_git")
    def test_fetches_sha_when_not_locally_available(self, mock_run_git) -> None:
        mock_run_git.side_effect = _git_stub(
            {
                ("fetch", "origin", "main"): "",
                ("cat-file", "-e", "abc123^{commit}"): RuntimeError("not available"),
                ("fetch", "--no-tags", "origin", "abc123"): "",
                ("diff", "-U1", "origin/main...abc123"): "some diff content",
            },
            patch_id_output="cafebabe 0000\n",
        )
        provider = GitHubActionsProvider(repo="owner/repo")

        result = provider.compute_diff_hash(base_branch="main", sha="abc123")

        assert result == "patch-id:cafebabe"

    @patch.object(GitHubActionsProvider, "_run_git")
    def test_raises_runtime_error_when_git_diff_fails(self, mock_run_git) -> None:
        mock_run_git.side_effect = _git_stub(
            {
                ("fetch", "origin", "main"): "",
                ("cat-file", "-e", "abc123^{commit}"): "",
                ("diff", "-U1", "origin/main...abc123"): RuntimeError("diff command failed"),
            }
        )
        provider = GitHubActionsProvider(repo="owner/repo")

        with pytest.raises(RuntimeError, match="git diff origin/main...abc123 failed"):
            provider.compute_diff_hash(base_branch="main", sha="abc123")

    @patch.object(GitHubActionsProvider, "_run_git")
    def test_raises_runtime_error_when_patch_id_fails(self, mock_run_git) -> None:
        mock_run_git.side_effect = _git_stub(
            {
                ("fetch", "origin", "main"): "",
                ("cat-file", "-e", "abc123^{commit}"): "",
                ("diff", "-U1", "origin/main...abc123"): "diff --git a/foo.py b/foo.py\n+x",
            },
            patch_id_exc=RuntimeError("patch-id unavailable"),
        )
        provider = GitHubActionsProvider(repo="owner/repo")

        with pytest.raises(RuntimeError, match="git patch-id --verbatim failed"):
            provider.compute_diff_hash(base_branch="main", sha="abc123")
