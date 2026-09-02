"""Tests for build_reply_request."""

from unittest.mock import MagicMock, patch

import pytest

import agentic_devtools.cli.pull_request_thread as pull_request_thread
from agentic_devtools.adapters.base import PullRequestThreadReplyRequest
from agentic_devtools.cli.pull_request_thread import build_reply_request


class TestBuildReplyRequest:
    """Validate explicit provider selection and normalized state values."""

    @pytest.fixture(autouse=True)
    def _snapshot_legacy_state_mock(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Adapt legacy get_value mocks to the locked snapshot API."""

        def snapshot() -> dict[str, object]:
            keys = (
                "platform.code_hosting",
                "code_hosting",
                "pull_request_id",
                "discussion_id",
                "thread_id",
                "comment_id",
                "content",
                "repository",
                "github.repo",
                "resolve_thread",
                "review_thread_id",
                "github.review_thread_id",
                "dry_run",
                "organization",
                "project",
            )
            return {key: value for key in keys if (value := pull_request_thread.get_value(key)) is not None}

        monkeypatch.setattr(pull_request_thread, "load_state_locked", snapshot)

    @patch(
        "agentic_devtools.cli.pull_request_thread.load_state_locked",
        return_value={
            "organization": "org",
            "project": "project",
            "repository": "repo",
            "content": "reply",
        },
    )
    def test_uses_azure_context_from_the_snapshot(self, _mock_load_state: MagicMock) -> None:
        """Azure organization and project are captured from the same state snapshot."""
        request = build_reply_request(provider="azure_devops", pull_request_id=1, discussion_id=2)

        assert request.azure_organization == "org"
        assert request.azure_project == "project"

    @patch(
        "agentic_devtools.cli.pull_request_thread.load_state_locked",
        return_value={"organization": "org", "project": "project", "content": "reply"},
    )
    @patch(
        "agentic_devtools.cli.azure_devops.config.AzureDevOpsConfig.from_state",
        return_value=MagicMock(organization="org", project="project", repository="repo"),
    )
    def test_uses_configured_repository_when_snapshot_omits_it(
        self, _mock_from_state: MagicMock, _mock_load_state: MagicMock
    ) -> None:
        """Azure repository fallback remains available when only context is snapshotted."""
        request = build_reply_request(provider="azure_devops", pull_request_id=1, discussion_id=2)

        assert request.repository == "repo"
        _mock_from_state.assert_called_once_with(
            state={"organization": "org", "project": "project", "content": "reply"}
        )

    @patch("agentic_devtools.cli.pull_request_thread.load_state_locked")
    def test_reads_provider_neutral_state_aliases(self, mock_load_state: MagicMock) -> None:
        values = {
            "platform.code_hosting": "github",
            "pull_request_id": 12,
            "discussion_id": 34,
            "content": "line 1\n✓ line 2",
            "github": {"repo": "owner/repo", "review_thread_id": "PRRT_kwDO"},
            "resolve_thread": True,
        }
        mock_load_state.return_value = values

        request = build_reply_request()

        assert request == PullRequestThreadReplyRequest(
            provider="github",
            repository="owner/repo",
            pull_request_number=12,
            discussion_id=34,
            body="line 1\n✓ line 2",
            resolve=True,
            review_thread_id="PRRT_kwDO",
        )

    @patch("agentic_devtools.cli.pull_request_thread.load_platform_config", return_value={"code_hosting": "other"})
    @patch("agentic_devtools.cli.pull_request_thread.get_value", return_value=None)
    def test_rejects_missing_provider_before_mutation(
        self, _mock_get_value: MagicMock, _mock_load_config: MagicMock
    ) -> None:
        with pytest.raises(ValueError, match="code_hosting"):
            build_reply_request()

    @patch("agentic_devtools.cli.pull_request_thread.load_platform_config", return_value={"code_hosting": "github"})
    @patch("agentic_devtools.cli.pull_request_thread.get_value", return_value=None)
    @patch("agentic_devtools.cli.github.repo_resolution.resolve_github_repo_safe", return_value="owner/repo")
    def test_resolves_github_repository_from_provider(
        self, _mock_repo: MagicMock, _mock_state: MagicMock, _mock_config: MagicMock
    ) -> None:
        request = build_reply_request(pull_request_id=12, discussion_id=34, content="reply")
        assert request.repository == "owner/repo"
        _mock_repo.assert_called_once_with(state={})

    @patch("agentic_devtools.cli.pull_request_thread.get_value", return_value=None)
    @patch("agentic_devtools.cli.azure_devops.config.AzureDevOpsConfig.from_state")
    def test_snapshots_azure_context(self, mock_from_state: MagicMock, _mock_get_value: MagicMock) -> None:
        mock_from_state.return_value = MagicMock(organization="org", project="project", repository="repo")

        request = build_reply_request(provider="azure_devops", pull_request_id=12, discussion_id=34, content="reply")

        assert request.azure_organization == "org"
        assert request.azure_project == "project"

    @patch("agentic_devtools.cli.pull_request_thread.get_value", return_value=None)
    @pytest.mark.parametrize(
        "kwargs",
        [
            {"repository": ""},
            {"pull_request_id": None},
            {"discussion_id": None},
            {"content": None},
            {"pull_request_id": object()},
            {"discussion_id": object()},
        ],
    )
    def test_rejects_incomplete_request(self, _mock_get_value: MagicMock, kwargs: dict[str, object]) -> None:
        values: dict[str, object] = {
            "provider": "azure_devops",
            "repository": "repo",
            "pull_request_id": 12,
            "discussion_id": 34,
            "content": "reply",
        }
        values.update(kwargs)
        with pytest.raises(ValueError):
            build_reply_request(**values)  # type: ignore[arg-type]

    @patch("agentic_devtools.cli.pull_request_thread.get_value")
    def test_github_repo_alias_ignored_for_azure_devops(self, mock_get_value: MagicMock) -> None:
        """github.repo must not be used when Azure DevOps is selected."""
        mock_from_state = MagicMock(organization="org", project="proj", repository="ado-repo")

        def _state(key: str, **_: object) -> object:
            return {"github.repo": "owner/wrong-repo"}.get(key)

        mock_get_value.side_effect = _state
        with patch(
            "agentic_devtools.cli.azure_devops.config.AzureDevOpsConfig.from_state", return_value=mock_from_state
        ):
            request = build_reply_request(
                provider="azure_devops",
                pull_request_id=1,
                discussion_id=2,
                content="c",
            )
        assert request.repository == "ado-repo"

    @patch("agentic_devtools.cli.pull_request_thread.get_value")
    def test_thread_id_alias_ignored_for_github(self, mock_get_value: MagicMock) -> None:
        """Legacy thread_id state alias must not win over comment_id for GitHub."""
        values: dict[str, object] = {
            "platform.code_hosting": "github",
            "pull_request_id": 12,
            "thread_id": 99,
            "comment_id": 34,
            "content": "c",
            "repository": "owner/repo",
        }
        mock_get_value.side_effect = lambda key, **_: values.get(key)

        request = build_reply_request()

        assert request.discussion_id == 34

    @patch("agentic_devtools.cli.pull_request_thread.get_value")
    def test_review_thread_id_not_loaded_for_azure_devops(self, mock_get_value: MagicMock) -> None:
        """review_thread_id must be None for Azure DevOps even when present in state."""
        values: dict[str, object] = {
            "review_thread_id": "PRRT_kwDO",
            "github.review_thread_id": "PRRT_kwDO",
            "content": "c",
            "resolve_thread": True,
        }
        mock_from_state = MagicMock(organization="org", project="proj", repository="repo")
        mock_get_value.side_effect = lambda key, **_: values.get(key)

        with patch(
            "agentic_devtools.cli.azure_devops.config.AzureDevOpsConfig.from_state", return_value=mock_from_state
        ):
            request = build_reply_request(provider="azure_devops", pull_request_id=1, discussion_id=2, content="c")

        assert request.review_thread_id is None

    @patch("agentic_devtools.cli.pull_request_thread.get_value")
    def test_review_thread_id_defaults_to_none_when_state_value_is_not_string(self, mock_get_value: MagicMock) -> None:
        """Non-string state value for review_thread_id is treated as absent."""
        values: dict[str, object] = {
            "platform.code_hosting": "github",
            "pull_request_id": 12,
            "discussion_id": 34,
            "content": "c",
            "repository": "owner/repo",
            "resolve_thread": True,
            # review_thread_id missing from state → _state_value returns None
        }
        mock_get_value.side_effect = lambda key, **_: values.get(key)

        request = build_reply_request()

        assert request.review_thread_id is None

    @patch("agentic_devtools.cli.pull_request_thread.get_value")
    def test_review_thread_id_not_loaded_when_resolve_false(self, mock_get_value: MagicMock) -> None:
        """review_thread_id must be None for GitHub when resolution is not requested."""
        values: dict[str, object] = {
            "platform.code_hosting": "github",
            "pull_request_id": 12,
            "discussion_id": 34,
            "content": "c",
            "repository": "owner/repo",
            "review_thread_id": "PRRT_kwDO",
            "github.review_thread_id": "PRRT_kwDO",
            "resolve_thread": False,
        }
        mock_get_value.side_effect = lambda key, **_: values.get(key)

        request = build_reply_request()

        assert request.review_thread_id is None

    @patch("agentic_devtools.cli.pull_request_thread.get_value")
    def test_comment_id_alias_ignored_for_azure_devops(self, mock_get_value: MagicMock) -> None:
        """Legacy comment_id state alias must not win over thread_id for Azure DevOps."""
        values: dict[str, object] = {
            "thread_id": 55,
            "comment_id": 99,
            "content": "c",
        }
        mock_from_state = MagicMock(organization="org", project="proj", repository="repo")
        mock_get_value.side_effect = lambda key, **_: values.get(key)

        with patch(
            "agentic_devtools.cli.azure_devops.config.AzureDevOpsConfig.from_state", return_value=mock_from_state
        ):
            request = build_reply_request(
                provider="azure_devops",
                pull_request_id=1,
                content="c",
            )

        assert request.discussion_id == 55
