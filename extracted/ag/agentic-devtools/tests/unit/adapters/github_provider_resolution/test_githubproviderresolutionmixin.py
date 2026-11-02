"""Tests for GitHubProvider."""

from __future__ import annotations

import json

import pytest

from agentic_devtools.adapters.github_provider import GitHubProvider
from tests.unit.adapters.github_provider._fixtures import _make_run_mock


class TestGitHubProviderResolveIdentifier:
    """Tests for GitHubProvider.resolve_identifier."""

    def test_resolve_success(self):
        response = json.dumps(
            {
                "id": 123456,
                "html_url": "https://github.com/org/repo/issues/42",
                "node_id": "I_kwDO654321",
            }
        )
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock(stdout=response))
        result = provider.resolve_identifier("42", dry_run=False)
        assert result.status == "resolved"
        assert result.metadata["database_id"] == 123456
        assert result.metadata["node_id"] == "I_kwDO654321"

    def test_resolve_dry_run(self):
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock())
        result = provider.resolve_identifier("42", dry_run=True)
        assert result.status == "dry-run"

    def test_resolve_dry_run_accepts_hash_prefixed_identifier(self):
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock())
        result = provider.resolve_identifier("#42", dry_run=True)
        assert result.status == "dry-run"
        assert result.identifier == "42"

    def test_resolve_empty_identifier_raises(self):
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock())
        with pytest.raises(ValueError, match="non-empty string"):
            provider.resolve_identifier("  ", dry_run=False)

    def test_resolve_non_dict_response_raises(self):
        """resolve_identifier raises when GitHub returns a non-object response (e.g. a list)."""
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock(stdout=json.dumps([{"id": 1}])))
        with pytest.raises(RuntimeError, match="Expected a JSON object from GitHub issues endpoint"):
            provider.resolve_identifier("42", dry_run=False)

    def test_resolve_zero_database_id_raises(self):
        """resolve_identifier raises when GitHub returns id=0 (invalid database ID)."""
        response = json.dumps({"id": 0, "html_url": "https://github.com/org/repo/issues/42", "node_id": ""})
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock(stdout=response))
        with pytest.raises(RuntimeError, match="valid positive integer database ID"):
            provider.resolve_identifier("42", dry_run=False)

    def test_resolve_not_found_raises_value_error(self):
        """resolve_identifier maps a GitHub HTTP 404 to ValueError per the contract."""
        provider = GitHubProvider(
            owner_repo="org/repo",
            run_command=_make_run_mock(stderr="gh: Not Found (HTTP 404)", returncode=1),
        )
        with pytest.raises(ValueError, match="not found"):
            provider.resolve_identifier("42", dry_run=False)

    def test_resolve_non_404_runtime_error_propagates(self):
        """resolve_identifier re-raises non-404 provider failures as RuntimeError.

        The stderr contains the substring ``4040`` to confirm the whole-token
        ``HTTP 404`` matcher does not misfire on unrelated numeric substrings.
        """
        provider = GitHubProvider(
            owner_repo="org/repo",
            run_command=_make_run_mock(stderr="gh: Server Error (HTTP 500) at issues/4040", returncode=1),
        )
        with pytest.raises(RuntimeError, match="gh command failed"):
            provider.resolve_identifier("42", dry_run=False)
