"""Tests for GitHubProvider dry-run manifest flow."""

from __future__ import annotations

import subprocess

from agentic_devtools.adapters.github_provider import GitHubProvider


class TestGitHubDryRunManifestFlow:
    """Verify GitHub provider dry-run produces a correct manifest."""

    def test_github_dry_run_manifest(self):
        """GitHub provider: 10 issues + 8 dependencies all marked dry-run."""

        def mock_run(*args, **kwargs):
            return subprocess.CompletedProcess(args=[], returncode=0, stdout="{}", stderr="")

        provider = GitHubProvider(owner_repo="org/repo", run_command=mock_run)

        # Create 10 issues in dry-run
        for i in range(10):
            result = provider.create_issue(f"Issue {i}", f"Body {i}", "task", dry_run=True)
            assert result.status == "dry-run"

        # Create 8 dependency links in dry-run
        for i in range(8):
            result = provider.add_blocked_by(str(i + 1), str(i), dry_run=True)
            assert result.status == "dry-run"

        manifest = provider.get_dry_run_manifest()
        assert len(manifest["issues"]) == 10
        assert len(manifest["dependencies"]) == 8
        assert all(item["status"] == "dry-run" for item in manifest["issues"])
        assert all(item["status"] == "dry-run" for item in manifest["dependencies"])
