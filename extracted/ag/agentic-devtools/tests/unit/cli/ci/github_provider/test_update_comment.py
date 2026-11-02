"""Tests for GitHubActionsProvider.update_comment() method."""

import json
from unittest.mock import Mock, patch

import pytest

from agentic_devtools.cli.ci.github_provider import _MAX_COMMENT_BODY_CHARS, GitHubActionsProvider
from agentic_devtools.cli.ci.models import IssueCommentInfo
from agentic_devtools.cli.ci.retry import RetryableError


class TestUpdateComment:
    """Tests for GitHubActionsProvider.update_comment()."""

    @pytest.fixture(autouse=True)
    def _use_pat_as_default_local_login(self, monkeypatch) -> None:
        monkeypatch.setattr(
            GitHubActionsProvider,
            "get_local_comment_login",
            lambda provider: provider.get_pr_token_login(),
            raising=False,
        )

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_updates_comment(self, gh_api, monkeypatch) -> None:
        monkeypatch.delenv("GITHUB_ACTIONS", raising=False)
        gh_api.side_effect = [json.dumps({"user": {"login": "pat-owner"}}), "{}"]
        provider = GitHubActionsProvider(repo="owner/repo")
        monkeypatch.setattr(provider, "get_pr_token_login", Mock(return_value="pat-owner"))
        result = provider.update_comment(100, "updated")

        assert result is None

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_uses_patch_method(self, gh_api, monkeypatch) -> None:
        monkeypatch.delenv("GITHUB_ACTIONS", raising=False)
        gh_api.side_effect = [json.dumps({"user": {"login": "pat-owner"}}), "{}"]
        provider = GitHubActionsProvider(repo="owner/repo")
        monkeypatch.setattr(provider, "get_pr_token_login", Mock(return_value="pat-owner"))
        provider.update_comment(100, "new body")

        assert gh_api.call_args.kwargs["method"] == "PATCH"

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_actions_update_routes_to_verified_comment_author(self, gh_api, monkeypatch) -> None:
        monkeypatch.setenv("GITHUB_ACTIONS", "true")
        monkeypatch.setenv("DEFAULT_CLASSIC_REPO_WORKFLOW_PAT", "pat-token")
        monkeypatch.setenv("AI_PR_LOOP_BOOKKEEPING_TOKEN", "bot-token")
        gh_api.side_effect = [
            json.dumps({"id": 100, "user": {"login": "github-actions[bot]"}}),
            "{}",
        ]
        provider = GitHubActionsProvider(repo="owner/repo")
        monkeypatch.setattr(provider, "get_pr_token_login", Mock(return_value="pat-owner"))
        monkeypatch.setattr(provider, "get_bookkeeping_token_login", Mock(return_value="github-actions[bot]"))

        provider.update_comment(100, "updated state")

        assert gh_api.call_args_list[1].kwargs["token"] == "bot-token"
        assert gh_api.call_args_list[1].kwargs["credential_identity"] == "AI_PR_LOOP_BOOKKEEPING_TOKEN"
        assert gh_api.call_args_list[1].kwargs["body"] == {"body": "updated state\n\n🤖 AI PR Loop ·"}

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_actions_update_migrates_legacy_comment_without_editing_it(self, gh_api, monkeypatch) -> None:
        monkeypatch.setenv("GITHUB_ACTIONS", "true")
        monkeypatch.setenv("DEFAULT_CLASSIC_REPO_WORKFLOW_PAT", "pat-token")
        monkeypatch.setenv("AI_PR_LOOP_BOOKKEEPING_TOKEN", "bot-token")
        gh_api.side_effect = [
            json.dumps(
                {
                    "id": 100,
                    "user": {"login": "pat-owner"},
                    "issue_url": "https://api.github.com/repos/owner/repo/issues/42",
                }
            ),
            json.dumps(
                [
                    {
                        "id": 99,
                        "user": {"login": "pat-owner"},
                        "body": "older state\n\n🤖 AI PR Loop ·",
                    }
                ]
            ),
            json.dumps({"id": 101}),
        ]
        provider = GitHubActionsProvider(repo="owner/repo")
        monkeypatch.setattr(provider, "get_pr_token_login", Mock(return_value="pat-owner"))
        monkeypatch.setattr(provider, "get_bookkeeping_token_login", Mock(return_value="github-actions[bot]"))

        provider.update_comment(100, "updated state")

        assert gh_api.call_args_list[2].args[0] == "/repos/owner/repo/issues/42/comments"
        assert gh_api.call_args_list[2].kwargs["method"] == "POST"
        assert gh_api.call_args_list[2].kwargs["token"] == "bot-token"
        assert gh_api.call_args_list[2].kwargs["credential_identity"] == "AI_PR_LOOP_BOOKKEEPING_TOKEN"
        assert gh_api.call_args_list[2].kwargs["body"] == {"body": "updated state\n\n🤖 AI PR Loop ·"}

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_local_update_migrates_actions_comment_to_pat_owned_copy(self, gh_api, monkeypatch) -> None:
        monkeypatch.delenv("GITHUB_ACTIONS", raising=False)
        gh_api.side_effect = [
            json.dumps(
                {
                    "id": 100,
                    "user": {"login": "github-actions[bot]"},
                    "issue_url": "https://api.github.com/repos/owner/repo/issues/42",
                }
            ),
            json.dumps(
                [
                    {
                        "id": 99,
                        "user": {"login": "pat-owner"},
                        "body": "older state\n\n🤖 AI PR Loop ·",
                    }
                ]
            ),
            json.dumps({"id": 101}),
        ]
        provider = GitHubActionsProvider(repo="owner/repo")
        monkeypatch.setattr(provider, "get_pr_token_login", Mock(return_value="pat-owner"))

        migrated_id = provider.update_comment(100, "updated state")

        assert migrated_id == 101
        assert gh_api.call_args_list[1].args[0] == "/repos/owner/repo/issues/42/comments"
        assert gh_api.call_args_list[2].args[0] == "/repos/owner/repo/issues/42/comments"
        assert gh_api.call_args_list[2].kwargs["method"] == "POST"
        assert gh_api.call_args_list[2].kwargs["body"] == {"body": "updated state\n\n🤖 AI PR Loop ·"}
        assert gh_api.call_args_list[2].kwargs.get("token") is None
        assert gh_api.call_args_list[2].kwargs.get("credential_identity") is None

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_local_migration_deduplicates_by_ambient_login_not_workflow_pat(self, gh_api, monkeypatch) -> None:
        monkeypatch.delenv("GITHUB_ACTIONS", raising=False)
        gh_api.side_effect = [
            json.dumps(
                {
                    "id": 100,
                    "user": {"login": "github-actions[bot]"},
                    "issue_url": "https://api.github.com/repos/owner/repo/issues/42",
                }
            ),
            json.dumps(
                [
                    {
                        "id": 101,
                        "user": {"login": "ambient-user"},
                        "body": "updated state\n\n🤖 AI PR Loop ·",
                    }
                ]
            ),
        ]
        provider = GitHubActionsProvider(repo="owner/repo")
        monkeypatch.setattr(provider, "get_pr_token_login", Mock(return_value="workflow-pat-user"))
        monkeypatch.setattr(provider, "get_local_comment_login", Mock(return_value="ambient-user"))

        assert provider.update_comment(100, "updated state") == 101

        assert gh_api.call_count == 2
        assert gh_api.call_args_list[1].args[0] == "/repos/owner/repo/issues/42/comments"

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_local_reads_new_pat_copy_as_canonical_after_actions_migration(self, gh_api, monkeypatch) -> None:
        monkeypatch.delenv("GITHUB_ACTIONS", raising=False)
        marker = "<!-- ai-pr-loop:state -->"
        old_body = f"old state {marker}"
        old_comments = [
            IssueCommentInfo(id=99, author="pat-owner", body=old_body, created_at="", html_url=""),
            IssueCommentInfo(
                id=100,
                author="github-actions[bot]",
                body=f"{old_body}\n\n🤖 AI PR Loop ·",
                created_at="",
                html_url="",
            ),
        ]
        updated_body = f"new state {marker}"
        migrated_comment = IssueCommentInfo(
            id=101,
            author="pat-owner",
            body=f"{updated_body}\n\n🤖 AI PR Loop ·",
            created_at="",
            html_url="",
        )
        gh_api.side_effect = [
            json.dumps(
                {
                    "id": 100,
                    "user": {"login": "github-actions[bot]"},
                    "issue_url": "https://api.github.com/repos/owner/repo/issues/42",
                }
            ),
            json.dumps({"id": 101}),
        ]
        provider = GitHubActionsProvider(repo="owner/repo")
        monkeypatch.setattr(provider, "get_pr_token_login", Mock(return_value="pat-owner"))
        with patch.object(
            provider, "list_issue_comments", side_effect=[old_comments, [], [*old_comments, migrated_comment]]
        ):
            assert provider.find_comment(42, marker) == (100, old_body)
            assert provider.update_comment(100, updated_body) == 101
            assert provider.find_comment(42, marker) == (101, updated_body)

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_local_update_reuses_existing_pat_copy_after_ambiguous_post(self, gh_api, monkeypatch) -> None:
        monkeypatch.delenv("GITHUB_ACTIONS", raising=False)
        migrated_body = "updated state\n\n🤖 AI PR Loop ·"
        migrated_comment = {"id": 101, "user": {"login": "pat-owner"}, "body": migrated_body}
        post_count = 0

        def api_call(endpoint, *, method="GET", body=None, **_kwargs):
            nonlocal post_count
            if endpoint == "/repos/owner/repo/issues/comments/100":
                return json.dumps(
                    {
                        "id": 100,
                        "user": {"login": "github-actions[bot]"},
                        "issue_url": "https://api.github.com/repos/owner/repo/issues/42",
                    }
                )
            if endpoint == "/repos/owner/repo/issues/42/comments" and method == "GET":
                return json.dumps([migrated_comment] if post_count else [])
            if endpoint == "/repos/owner/repo/issues/42/comments" and method == "POST":
                post_count += 1
                assert body == {"body": migrated_body}
                if post_count == 1:
                    raise RetryableError("GitHub API server error (HTTP 502)")
                raise AssertionError("The retry must reuse the existing PAT-authored copy")
            raise AssertionError(f"Unexpected GitHub API request: {method} {endpoint}")

        gh_api.side_effect = api_call
        provider = GitHubActionsProvider(repo="owner/repo")
        monkeypatch.setattr(provider, "get_pr_token_login", Mock(return_value="pat-owner"))

        with patch("agentic_devtools.cli.shared.retry.time.sleep"):
            migrated_id = provider.update_comment(100, "updated state")

        assert migrated_id == 101
        assert post_count == 1

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_local_update_rejects_unverified_comment_author(self, gh_api, monkeypatch) -> None:
        monkeypatch.delenv("GITHUB_ACTIONS", raising=False)
        gh_api.return_value = json.dumps({"id": 100, "user": {"login": "untrusted"}})
        provider = GitHubActionsProvider(repo="owner/repo")
        monkeypatch.setattr(provider, "get_pr_token_login", Mock(return_value="pat-owner"))

        with pytest.raises(RuntimeError, match="unverified author"):
            provider.update_comment(100, "updated state")

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_local_update_rejects_actions_comment_without_issue_url(self, gh_api, monkeypatch) -> None:
        monkeypatch.delenv("GITHUB_ACTIONS", raising=False)
        gh_api.return_value = json.dumps({"id": 100, "user": {"login": "github-actions[bot]"}})
        provider = GitHubActionsProvider(repo="owner/repo")
        monkeypatch.setattr(provider, "get_pr_token_login", Mock(return_value="pat-owner"))

        with pytest.raises(RuntimeError, match="did not return an issue URL for Actions comment #100"):
            provider.update_comment(100, "updated state")

        gh_api.assert_called_once()

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_local_update_rejects_migration_response_without_numeric_id(self, gh_api, monkeypatch) -> None:
        monkeypatch.delenv("GITHUB_ACTIONS", raising=False)
        gh_api.side_effect = [
            json.dumps(
                {
                    "id": 100,
                    "user": {"login": "github-actions[bot]"},
                    "issue_url": "https://api.github.com/repos/owner/repo/issues/42",
                }
            ),
            "[]",
            json.dumps({"id": "101"}),
        ]
        provider = GitHubActionsProvider(repo="owner/repo")
        monkeypatch.setattr(provider, "get_pr_token_login", Mock(return_value="pat-owner"))

        with pytest.raises(RuntimeError, match="response carried no comment ID"):
            provider.update_comment(100, "updated state")

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_local_update_rejects_migration_body_over_limit(self, gh_api, monkeypatch) -> None:
        monkeypatch.delenv("GITHUB_ACTIONS", raising=False)
        gh_api.side_effect = [
            json.dumps(
                {
                    "id": 100,
                    "user": {"login": "github-actions[bot]"},
                    "issue_url": "https://api.github.com/repos/owner/repo/issues/42",
                }
            ),
            "[]",
        ]
        provider = GitHubActionsProvider(repo="owner/repo")
        monkeypatch.setattr(provider, "get_pr_token_login", Mock(return_value="pat-owner"))

        with pytest.raises(ValueError, match="exceeds the"):
            provider.update_comment(100, "x" * _MAX_COMMENT_BODY_CHARS)

        assert gh_api.call_count == 2

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_local_update_rejects_ambiguous_actions_bot_identity(self, gh_api, monkeypatch) -> None:
        monkeypatch.delenv("GITHUB_ACTIONS", raising=False)
        provider = GitHubActionsProvider(repo="owner/repo")
        monkeypatch.setattr(provider, "get_pr_token_login", Mock(return_value="github-actions[bot]"))

        with pytest.raises(RuntimeError, match="identities are ambiguous"):
            provider.update_comment(100, "updated state")

        gh_api.assert_not_called()

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_actions_reuses_migrated_id_for_repeated_stale_id_updates(self, gh_api, monkeypatch) -> None:
        monkeypatch.setenv("GITHUB_ACTIONS", "true")
        monkeypatch.setenv("DEFAULT_CLASSIC_REPO_WORKFLOW_PAT", "pat-token")
        monkeypatch.setenv("AI_PR_LOOP_BOOKKEEPING_TOKEN", "bot-token")
        gh_api.side_effect = [
            json.dumps(
                {
                    "id": 100,
                    "user": {"login": "pat-owner"},
                    "issue_url": "https://api.github.com/repos/owner/repo/issues/42",
                }
            ),
            "[]",
            json.dumps({"id": 101}),
            json.dumps({"id": 101, "user": {"login": "github-actions[bot]"}}),
            "{}",
        ]
        provider = GitHubActionsProvider(repo="owner/repo")
        monkeypatch.setattr(provider, "get_pr_token_login", Mock(return_value="pat-owner"))
        monkeypatch.setattr(provider, "get_bookkeeping_token_login", Mock(return_value="github-actions[bot]"))

        assert provider.update_comment(100, "first state") == 101
        redirected_id = provider.update_comment(100, "second state")

        assert redirected_id == 101
        assert gh_api.call_count == 5
        assert gh_api.call_args_list[3].args[0] == "/repos/owner/repo/issues/comments/101"
        assert gh_api.call_args_list[4].args[0] == "/repos/owner/repo/issues/comments/101"
        assert gh_api.call_args_list[4].kwargs["method"] == "PATCH"
        assert gh_api.call_args_list[4].kwargs["body"] == {"body": "second state\n\n🤖 AI PR Loop ·"}

    @pytest.mark.parametrize(
        ("response", "bookkeeping_login", "pat_login", "message"),
        [
            ("not-json", "github-actions[bot]", "pat-owner", "malformed comment"),
            (json.dumps([]), "github-actions[bot]", "pat-owner", "malformed comment"),
            (json.dumps({"user": {}}), "github-actions[bot]", "pat-owner", "did not return an author"),
            (
                json.dumps(
                    {
                        "user": {"login": "github-actions[bot]"},
                        "issue_url": "https://api.github.com/repos/o/r/issues/42",
                    }
                ),
                "github-actions[bot]",
                "GITHUB-ACTIONS[BOT]",
                "identities are ambiguous",
            ),
            (
                json.dumps({"user": {"login": "pat-owner"}}),
                "github-actions[bot]",
                "pat-owner",
                "did not return an issue URL",
            ),
            (
                json.dumps({"user": {"login": "untrusted"}}),
                "github-actions[bot]",
                "pat-owner",
                "unverified author",
            ),
        ],
    )
    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_actions_update_rejects_unverifiable_ownership(
        self,
        gh_api,
        monkeypatch,
        response,
        bookkeeping_login,
        pat_login,
        message,
    ) -> None:
        monkeypatch.setenv("GITHUB_ACTIONS", "true")
        monkeypatch.setenv("DEFAULT_CLASSIC_REPO_WORKFLOW_PAT", "pat-token")
        monkeypatch.setenv("AI_PR_LOOP_BOOKKEEPING_TOKEN", "bot-token")
        gh_api.return_value = response
        provider = GitHubActionsProvider(repo="owner/repo")
        monkeypatch.setattr(provider, "get_bookkeeping_token_login", lambda: bookkeeping_login)
        monkeypatch.setattr(provider, "get_pr_token_login", lambda: pat_login)

        with pytest.raises(RuntimeError, match=message):
            provider.update_comment(100, "updated state")

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_actions_update_requires_both_verified_identities(self, gh_api, monkeypatch) -> None:
        monkeypatch.setenv("GITHUB_ACTIONS", "true")
        monkeypatch.setenv("DEFAULT_CLASSIC_REPO_WORKFLOW_PAT", "pat-token")
        monkeypatch.setenv("AI_PR_LOOP_BOOKKEEPING_TOKEN", "bot-token")
        provider = GitHubActionsProvider(repo="owner/repo")
        monkeypatch.setattr(provider, "get_bookkeeping_token_login", lambda: "")
        monkeypatch.setattr(provider, "get_pr_token_login", lambda: "pat-owner")

        with pytest.raises(RuntimeError, match="could not both be verified"):
            provider.update_comment(100, "updated state")

        gh_api.assert_not_called()

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_actions_update_rejects_invalid_legacy_issue_url(self, gh_api, monkeypatch) -> None:
        monkeypatch.setenv("GITHUB_ACTIONS", "true")
        monkeypatch.setenv("DEFAULT_CLASSIC_REPO_WORKFLOW_PAT", "pat-token")
        monkeypatch.setenv("AI_PR_LOOP_BOOKKEEPING_TOKEN", "bot-token")
        gh_api.return_value = json.dumps(
            {"user": {"login": "pat-owner"}, "issue_url": "https://api.github.com/repos/other/repo/issues/42"}
        )
        provider = GitHubActionsProvider(repo="owner/repo")
        monkeypatch.setattr(provider, "get_bookkeeping_token_login", lambda: "github-actions[bot]")
        monkeypatch.setattr(provider, "get_pr_token_login", lambda: "pat-owner")

        with pytest.raises(RuntimeError, match="invalid issue URL"):
            provider.update_comment(100, "updated state")

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_actions_update_rejects_migration_response_without_numeric_id(self, gh_api, monkeypatch) -> None:
        monkeypatch.setenv("GITHUB_ACTIONS", "true")
        monkeypatch.setenv("DEFAULT_CLASSIC_REPO_WORKFLOW_PAT", "pat-token")
        monkeypatch.setenv("AI_PR_LOOP_BOOKKEEPING_TOKEN", "bot-token")
        gh_api.side_effect = [
            json.dumps(
                {
                    "id": 100,
                    "user": {"login": "pat-owner"},
                    "issue_url": "https://api.github.com/repos/owner/repo/issues/42",
                }
            ),
            json.dumps({"id": "101"}),
        ]
        provider = GitHubActionsProvider(repo="owner/repo")
        monkeypatch.setattr(provider, "get_bookkeeping_token_login", lambda: "github-actions[bot]")
        monkeypatch.setattr(provider, "get_pr_token_login", lambda: "pat-owner")
        monkeypatch.setattr(provider, "list_issue_comments", lambda _issue: [])

        with pytest.raises(RuntimeError, match="response carried no comment ID"):
            provider.update_comment(100, "updated state")

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_update_breaks_a_self_referential_migration_mapping(self, gh_api, monkeypatch) -> None:
        monkeypatch.delenv("GITHUB_ACTIONS", raising=False)
        gh_api.side_effect = [json.dumps({"id": 100, "user": {"login": "pat-owner"}}), "{}"]
        provider = GitHubActionsProvider(repo="owner/repo")
        monkeypatch.setattr(provider, "get_pr_token_login", Mock(return_value="pat-owner"))
        provider._migrated_loop_comment_ids[100] = 100

        assert provider.update_comment(100, "updated state") is None

        assert gh_api.call_count == 2
        assert gh_api.call_args_list[1].args[0] == "/repos/owner/repo/issues/comments/100"

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_actions_migration_retry_reuses_copy_after_ambiguous_post(
        self,
        gh_api,
        monkeypatch,
    ) -> None:
        monkeypatch.setenv("GITHUB_ACTIONS", "true")
        monkeypatch.setenv("DEFAULT_CLASSIC_REPO_WORKFLOW_PAT", "pat-token")
        monkeypatch.setenv("AI_PR_LOOP_BOOKKEEPING_TOKEN", "bot-token")
        comments: list[dict[str, object]] = []
        post_count = 0

        def api_call(endpoint, *, method="GET", body=None, **_kwargs):
            nonlocal post_count
            if endpoint == "/repos/owner/repo/issues/comments/100":
                return json.dumps(
                    {
                        "id": 100,
                        "user": {"login": "pat-owner"},
                        "issue_url": "https://api.github.com/repos/owner/repo/issues/42",
                    }
                )
            if endpoint == "/repos/owner/repo/issues/42/comments" and method == "GET":
                return json.dumps(comments)
            if endpoint == "/repos/owner/repo/issues/42/comments" and method == "POST":
                post_count += 1
                assert body is not None
                comments.append(
                    {
                        "id": 101,
                        "user": {"login": "github-actions[bot]"},
                        "body": body["body"],
                    }
                )
                if post_count == 1:
                    raise RetryableError("GitHub API server error (HTTP 502)")
                return json.dumps({"id": 102})
            raise AssertionError(f"Unexpected GitHub API request: {method} {endpoint}")

        gh_api.side_effect = api_call
        provider = GitHubActionsProvider(repo="owner/repo")
        monkeypatch.setattr(provider, "get_pr_token_login", Mock(return_value="pat-owner"))
        monkeypatch.setattr(provider, "get_bookkeeping_token_login", Mock(return_value="github-actions[bot]"))

        with patch("agentic_devtools.cli.shared.retry.time.sleep"):
            migrated_id = provider.update_comment(100, "updated state")

        assert migrated_id == 101
        assert post_count == 1
        assert len(comments) == 1

    @pytest.mark.parametrize("is_actions", [False, True])
    @pytest.mark.parametrize(
        ("copies", "expected_id", "posts"),
        [
            ([IssueCommentInfo(100, "target-user", "state A\n\n🤖 AI PR Loop ·")], 104, True),
            (
                [
                    IssueCommentInfo(102, "target-user", "state A\n\n🤖 AI PR Loop ·"),
                    IssueCommentInfo(103, "target-user", "state B\n\n🤖 AI PR Loop ·"),
                ],
                104,
                True,
            ),
            (
                [
                    IssueCommentInfo(102, "target-user", "state A\n\n🤖 AI PR Loop ·"),
                    IssueCommentInfo(103, "source-user", "state B\n\n🤖 AI PR Loop ·"),
                ],
                104,
                True,
            ),
            (
                [
                    IssueCommentInfo(102, "target-user", "state A\n\n🤖 AI PR Loop ·"),
                    IssueCommentInfo(103, "target-user", "state A\n\n🤖 AI PR Loop ·"),
                ],
                103,
                False,
            ),
        ],
    )
    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_migration_reuses_only_latest_unsuperseded_copy(
        self,
        gh_api,
        monkeypatch,
        is_actions,
        copies,
        expected_id,
        posts,
    ) -> None:
        if is_actions:
            monkeypatch.setenv("GITHUB_ACTIONS", "true")
            monkeypatch.setenv("AI_PR_LOOP_BOOKKEEPING_TOKEN", "bot-token")
            source_author = "pat-owner"
            target_author = "github-actions[bot]"
            trusted_logins = {"pat-owner", "github-actions[bot]"}
        else:
            monkeypatch.delenv("GITHUB_ACTIONS", raising=False)
            source_author = "github-actions[bot]"
            target_author = "pat-owner"
            trusted_logins = {"pat-owner", "github-actions[bot]"}
        copies = [
            IssueCommentInfo(
                item.id,
                target_author if item.author == "target-user" else source_author,
                item.body,
            )
            for item in copies
        ]
        source_comment = {
            "id": 101,
            "user": {"login": source_author},
            "issue_url": "https://api.github.com/repos/owner/repo/issues/42",
        }
        gh_api.side_effect = [json.dumps(source_comment), json.dumps({"id": 104})]
        provider = GitHubActionsProvider(repo="owner/repo")
        monkeypatch.setattr(provider, "get_pr_token_login", Mock(return_value="pat-owner"))
        monkeypatch.setattr(provider, "get_bookkeeping_token_login", Mock(return_value="github-actions[bot]"))
        monkeypatch.setattr(provider, "get_trusted_loop_comment_logins", Mock(return_value=trusted_logins))
        monkeypatch.setattr(provider, "list_issue_comments", Mock(return_value=copies))

        result = provider.update_comment(101, "state A")

        assert result == expected_id
        if posts:
            assert gh_api.call_args.kwargs["method"] == "POST"
            assert gh_api.call_args.kwargs["body"] == {"body": "state A\n\n🤖 AI PR Loop ·"}
        else:
            gh_api.assert_called_once()

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_local_migration_reuses_verified_gh_token_identity(self, gh_api, monkeypatch) -> None:
        monkeypatch.delenv("GITHUB_ACTIONS", raising=False)
        gh_api.return_value = json.dumps(
            {
                "id": 101,
                "user": {"login": "github-actions[bot]"},
                "issue_url": "https://api.github.com/repos/owner/repo/issues/42",
            }
        )
        provider = GitHubActionsProvider(repo="owner/repo")
        monkeypatch.setattr(provider, "get_pr_token_login", Mock(return_value=""))
        monkeypatch.setattr(
            provider,
            "get_trusted_loop_comment_logins",
            Mock(return_value={"local-user", "github-actions[bot]"}),
        )
        monkeypatch.setattr(provider, "get_local_comment_login", Mock(return_value="local-user"))
        monkeypatch.setattr(
            provider,
            "list_issue_comments",
            Mock(return_value=[IssueCommentInfo(102, "local-user", "state A\n\n🤖 AI PR Loop ·")]),
        )

        assert provider.update_comment(101, "state A") == 102
        gh_api.assert_called_once()

    @patch("agentic_devtools.cli.ci.github_provider._gh_api")
    def test_local_migration_requires_one_verified_non_bot_identity(self, gh_api, monkeypatch) -> None:
        monkeypatch.delenv("GITHUB_ACTIONS", raising=False)
        gh_api.return_value = json.dumps({"id": 101, "user": {"login": "github-actions[bot]"}})
        provider = GitHubActionsProvider(repo="owner/repo")
        monkeypatch.setattr(provider, "get_pr_token_login", Mock(return_value=""))
        monkeypatch.setattr(provider, "get_trusted_loop_comment_logins", Mock(return_value={"github-actions[bot]"}))

        with pytest.raises(RuntimeError, match="update identity could not be verified"):
            provider.update_comment(101, "state A")

        gh_api.assert_called_once()
