"""Tests for GitHubActionsProvider.find_comment() method."""

import json
from unittest.mock import Mock, patch

import pytest

from agentic_devtools.cli.ci.github_provider import GitHubActionsProvider


def _mock_run_safe_response(data):
    class _Result:
        returncode = 0
        stdout = json.dumps(data)
        stderr = ""

    return _Result()


class TestFindComment:
    """Tests for GitHubActionsProvider.find_comment()."""

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_finds_comment_with_marker(self, mock_run_safe, monkeypatch) -> None:
        monkeypatch.setenv("GITHUB_ACTIONS", "true")
        mock_run_safe.return_value = _mock_run_safe_response(
            [
                {"id": 1, "body": "normal comment"},
                {
                    "id": 2,
                    "body": "<!-- repair-dispatch:abc:1 --> status update\n\n🤖 AI PR Loop ·",
                    "user": {"login": "pat-owner"},
                },
                {"id": 3, "body": "another comment"},
            ]
        )

        provider = GitHubActionsProvider(repo="owner/repo")
        monkeypatch.setattr(provider, "get_pr_token_login", Mock(return_value="pat-owner"))
        monkeypatch.setattr(provider, "get_bookkeeping_token_login", Mock(return_value="github-actions[bot]"))
        result = provider.find_comment(42, "<!-- repair-dispatch:")

        assert result is not None
        assert result[0] == 2
        assert result[1] == "<!-- repair-dispatch:abc:1 --> status update"

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_prefers_newest_matching_comment(self, mock_run_safe, monkeypatch) -> None:
        monkeypatch.setenv("GITHUB_ACTIONS", "true")
        mock_run_safe.return_value = _mock_run_safe_response(
            [
                {"id": 1, "body": "<!-- repair-dispatch:abc:1 --> oldest", "user": {"login": "pat-owner"}},
                {"id": 2, "body": "normal comment"},
                {"id": 3, "body": "<!-- repair-dispatch:abc:2 --> newest", "user": {"login": "github-actions[bot]"}},
            ]
        )

        provider = GitHubActionsProvider(repo="owner/repo")
        monkeypatch.setattr(provider, "get_pr_token_login", Mock(return_value="pat-owner"))
        monkeypatch.setattr(provider, "get_bookkeeping_token_login", Mock(return_value="github-actions[bot]"))
        result = provider.find_comment(42, "<!-- repair-dispatch:")

        assert result is not None
        assert result[0] == 3
        assert "repair-dispatch:abc:2" in result[1]

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_returns_none_when_not_found(self, mock_run_safe) -> None:
        mock_run_safe.return_value = _mock_run_safe_response(
            [
                {"id": 1, "body": "no marker here"},
            ]
        )

        provider = GitHubActionsProvider(repo="owner/repo")
        result = provider.find_comment(42, "<!-- missing-marker -->")

        assert result is None

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_empty_comments(self, mock_run_safe) -> None:
        mock_run_safe.return_value = _mock_run_safe_response([])

        provider = GitHubActionsProvider(repo="owner/repo")
        result = provider.find_comment(1, "marker")

        assert result is None

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_ignores_marker_comments_by_untrusted_authors(self, mock_run_safe, monkeypatch) -> None:
        monkeypatch.setenv("GITHUB_ACTIONS", "true")
        mock_run_safe.return_value = _mock_run_safe_response(
            [{"id": 1, "body": "<!-- repair-dispatch:forged -->", "user": {"login": "attacker"}}]
        )
        provider = GitHubActionsProvider(repo="owner/repo")
        monkeypatch.setattr(provider, "get_pr_token_login", Mock(return_value="pat-owner"))
        monkeypatch.setattr(provider, "get_bookkeeping_token_login", Mock(return_value="github-actions[bot]"))

        assert provider.find_comment(42, "<!-- repair-dispatch:") is None

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_rejects_malformed_label_on_trusted_marker_comment(self, mock_run_safe, monkeypatch) -> None:
        monkeypatch.setenv("GITHUB_ACTIONS", "true")
        mock_run_safe.return_value = _mock_run_safe_response(
            [
                {
                    "id": 1,
                    "body": "<!-- repair-dispatch:abc:1 --> status update\n🤖 AI PR Loop ·",
                    "user": {"login": "pat-owner"},
                }
            ]
        )
        provider = GitHubActionsProvider(repo="owner/repo")
        monkeypatch.setattr(provider, "get_pr_token_login", Mock(return_value="pat-owner"))
        monkeypatch.setattr(provider, "get_bookkeeping_token_login", Mock(return_value="github-actions[bot]"))

        with pytest.raises(RuntimeError, match="trusted loop comment has a malformed terminal label"):
            provider.find_comment(42, "<!-- repair-dispatch:")

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_does_not_match_terminal_label_after_normalization(self, gh_api, monkeypatch) -> None:
        monkeypatch.delenv("GITHUB_ACTIONS", raising=False)
        gh_api.return_value = json.dumps(
            [
                {
                    "id": 1,
                    "body": "protocol state\n\n🤖 AI PR Loop ·",
                    "user": {"login": "local-user"},
                }
            ]
        )
        provider = GitHubActionsProvider(repo="owner/repo")
        monkeypatch.setattr(provider, "get_pr_token_login", Mock(return_value="local-user"))
        monkeypatch.setattr(provider, "get_local_comment_login", Mock(return_value="local-user"))

        assert provider.find_comment(42, "🤖 AI PR Loop ·") is None

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_ignores_malformed_marker_from_untrusted_author(self, mock_run_safe, monkeypatch) -> None:
        monkeypatch.setenv("GITHUB_ACTIONS", "true")
        mock_run_safe.return_value = _mock_run_safe_response(
            [
                {
                    "id": 1,
                    "body": "<!-- repair-dispatch:forged --> status\n🤖 AI PR Loop ·",
                    "user": {"login": "attacker"},
                }
            ]
        )
        provider = GitHubActionsProvider(repo="owner/repo")
        monkeypatch.setattr(provider, "get_pr_token_login", Mock(return_value="pat-owner"))
        monkeypatch.setattr(provider, "get_bookkeeping_token_login", Mock(return_value="github-actions[bot]"))

        assert provider.find_comment(42, "<!-- repair-dispatch:") is None

    def test_resolves_local_fallback_identity_once_for_matching_comments(self, monkeypatch) -> None:
        monkeypatch.delenv("GITHUB_ACTIONS", raising=False)
        with patch("agentic_devtools.cli.ci.github_provider._gh_api") as mock_gh_api:
            mock_gh_api.side_effect = [
                json.dumps(
                    [
                        {
                            "id": 1,
                            "body": "<!-- repair-dispatch:first --> status",
                            "user": {"login": "local-user"},
                        },
                        {
                            "id": 2,
                            "body": "<!-- repair-dispatch:second --> status",
                            "user": {"login": "local-user"},
                        },
                    ]
                ),
                json.dumps({"login": "local-user"}),
                json.dumps({"login": "local-user"}),
            ]
            provider = GitHubActionsProvider(repo="owner/repo")
            monkeypatch.setattr(provider, "get_pr_token_login", Mock(return_value=""))

            result = provider.find_comment(42, "<!-- repair-dispatch:")

        assert result is not None
        assert result[0] == 2
        assert [call.args[0] for call in mock_gh_api.call_args_list].count("/user") == 1
