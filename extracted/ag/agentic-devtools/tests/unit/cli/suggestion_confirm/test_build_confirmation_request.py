from unittest.mock import patch

import pytest

from agentic_devtools.cli.suggestion_confirm import build_confirmation_request


@patch("agentic_devtools.cli.suggestion_confirm.resolve_comment_provider", return_value="github")
@patch("agentic_devtools.cli.suggestion_confirm._resolve_repository", return_value="owner/repo")
@patch("agentic_devtools.cli.suggestion_confirm.load_state_locked")
def test_builds_github_request(mock_load_state, mock_repo, mock_provider) -> None:
    mock_load_state.return_value = {
        "pull_request_id": 1,
        "discussion_id": 2,
        "github": {"review_thread_id": "PRRT_1"},
        "suggestion": {"commit_hash": "abcdef"},
    }
    request = build_confirmation_request()
    assert request.provider == "github"
    assert request.discussion_id == 2
    assert request.review_thread_id == "PRRT_1"


def test_rejects_missing_commit() -> None:
    with (
        patch(
            "agentic_devtools.cli.suggestion_confirm.resolve_comment_provider",
            return_value="azure_devops",
        ),
        patch(
            "agentic_devtools.cli.suggestion_confirm.load_state_locked",
            return_value={},
        ),
    ):
        with pytest.raises(ValueError, match="suggestion.commit_hash"):
            build_confirmation_request()


@pytest.mark.parametrize("value", [True, [], "not-a-number", 0])
def test_rejects_invalid_numeric_state(value) -> None:
    with (
        patch(
            "agentic_devtools.cli.suggestion_confirm.resolve_comment_provider",
            return_value="azure_devops",
        ),
        patch(
            "agentic_devtools.cli.suggestion_confirm.load_state_locked",
            return_value={"pull_request_id": value, "thread_id": 2, "suggestion": {"commit_hash": "abc"}},
        ),
        patch(
            "agentic_devtools.cli.suggestion_confirm._resolve_repository",
            return_value="repo",
        ),
    ):
        with pytest.raises(ValueError, match="positive integer"):
            build_confirmation_request()


def test_builds_azure_request_with_explicit_values() -> None:
    with (
        patch(
            "agentic_devtools.cli.suggestion_confirm.resolve_comment_provider",
            return_value="azure_devops",
        ),
        patch(
            "agentic_devtools.cli.suggestion_confirm._resolve_repository",
            return_value="repo",
        ),
        patch(
            "agentic_devtools.cli.suggestion_confirm.load_state_locked",
            return_value={},
        ),
    ):
        request = build_confirmation_request(
            pull_request_id=1,
            discussion_id=2,
            commit_hash="abc",
            dry_run=True,
            organization="https://dev.azure.com/org",
            project="project",
        )
    assert request.provider == "azure_devops"
    assert request.dry_run is True


def test_snapshots_azure_context_from_state() -> None:
    config = type("Config", (), {"organization": "https://dev.azure.com/org", "project": "project"})()
    with (
        patch(
            "agentic_devtools.cli.suggestion_confirm.resolve_comment_provider",
            return_value="azure_devops",
        ),
        patch(
            "agentic_devtools.cli.suggestion_confirm._resolve_repository",
            return_value="repo",
        ),
        patch(
            "agentic_devtools.cli.suggestion_confirm.load_state_locked",
            return_value={},
        ),
        patch("agentic_devtools.cli.suggestion_confirm.AzureDevOpsConfig.from_state", return_value=config),
    ):
        request = build_confirmation_request(
            pull_request_id=1,
            discussion_id=2,
            commit_hash="abc",
        )
    assert request.organization == "https://dev.azure.com/org"
    assert request.project == "project"


@pytest.mark.parametrize(
    ("organization", "project", "expected_organization", "expected_project"),
    [
        ("https://dev.azure.com/explicit-org", None, "https://dev.azure.com/explicit-org", "state-project"),
        (None, "explicit-project", "https://dev.azure.com/state-org", "explicit-project"),
    ],
)
def test_fills_only_missing_azure_snapshot_values(
    organization: str | None,
    project: str | None,
    expected_organization: str,
    expected_project: str,
) -> None:
    config = type("Config", (), {"organization": "https://dev.azure.com/state-org", "project": "state-project"})()
    with (
        patch(
            "agentic_devtools.cli.suggestion_confirm.resolve_comment_provider",
            return_value="azure_devops",
        ),
        patch(
            "agentic_devtools.cli.suggestion_confirm._resolve_repository",
            return_value="repo",
        ),
        patch(
            "agentic_devtools.cli.suggestion_confirm.load_state_locked",
            return_value={},
        ),
        patch("agentic_devtools.cli.suggestion_confirm.AzureDevOpsConfig.from_state", return_value=config),
    ):
        request = build_confirmation_request(
            pull_request_id=1,
            discussion_id=2,
            commit_hash="abc",
            organization=organization,
            project=project,
        )
    assert request.organization == expected_organization
    assert request.project == expected_project


def test_uses_github_comment_alias() -> None:
    with (
        patch(
            "agentic_devtools.cli.suggestion_confirm.resolve_comment_provider",
            return_value="github",
        ),
        patch(
            "agentic_devtools.cli.suggestion_confirm._resolve_repository",
            return_value="owner/repo",
        ),
        patch(
            "agentic_devtools.cli.suggestion_confirm.load_state_locked",
            return_value={
                "pull_request_id": 1,
                "github": {"comment_id": 2, "review_thread_id": "PRRT_1"},
                "suggestion": {"commit_hash": "abc"},
            },
        ),
    ):
        request = build_confirmation_request()
    assert request.discussion_id == 2


def test_prefers_canonical_discussion_id_over_legacy_aliases() -> None:
    with (
        patch(
            "agentic_devtools.cli.suggestion_confirm.resolve_comment_provider",
            return_value="github",
        ),
        patch(
            "agentic_devtools.cli.suggestion_confirm._resolve_repository",
            return_value="owner/repo",
        ),
        patch(
            "agentic_devtools.cli.suggestion_confirm.load_state_locked",
            return_value={
                "pull_request_id": 1,
                "discussion_id": 2,
                "github": {"comment_id": 9, "review_thread_id": "PRRT_1"},
                "comment_id": 10,
                "thread_id": 11,
                "suggestion": {"commit_hash": "abc"},
            },
        ),
    ):
        request = build_confirmation_request()
    assert request.discussion_id == 2


def test_github_does_not_fall_back_to_azure_thread_id() -> None:
    """GitHub discussion resolution must never fall back to the Azure-only ``thread_id`` alias."""
    with (
        patch(
            "agentic_devtools.cli.suggestion_confirm.resolve_comment_provider",
            return_value="github",
        ),
        patch(
            "agentic_devtools.cli.suggestion_confirm._resolve_repository",
            return_value="owner/repo",
        ),
        patch(
            "agentic_devtools.cli.suggestion_confirm.load_state_locked",
            return_value={
                "pull_request_id": 1,
                "thread_id": 11,
                "suggestion": {"commit_hash": "abc"},
                "github": {"review_thread_id": "PRRT_1"},
            },
        ),
    ):
        with pytest.raises(ValueError, match="discussion_id"):
            build_confirmation_request()


def test_prefers_canonical_review_thread_id_over_provider_alias() -> None:
    """A stale ``github.review_thread_id`` must not override the canonical key."""
    with (
        patch(
            "agentic_devtools.cli.suggestion_confirm.resolve_comment_provider",
            return_value="github",
        ),
        patch(
            "agentic_devtools.cli.suggestion_confirm._resolve_repository",
            return_value="owner/repo",
        ),
        patch(
            "agentic_devtools.cli.suggestion_confirm.load_state_locked",
            return_value={
                "pull_request_id": 1,
                "discussion_id": 2,
                "review_thread_id": "PRRT_canonical",
                "github": {"review_thread_id": "PRRT_stale"},
                "suggestion": {"commit_hash": "abc"},
            },
        ),
    ):
        request = build_confirmation_request()
    assert request.review_thread_id == "PRRT_canonical"


def test_resolves_full_state_snapshot_without_mocking_helpers() -> None:
    """Exercise the real state-lookup closure passed to the provider/repository helpers."""
    with patch(
        "agentic_devtools.cli.suggestion_confirm.load_state_locked",
        return_value={
            "platform": {"code_hosting": "github"},
            "github": {"repo": "owner/repo"},
            "pull_request_id": 5,
            "discussion_id": 6,
            "review_thread_id": "PRRT_snapshot",
            "suggestion": {"commit_hash": "abcdef"},
        },
    ):
        request = build_confirmation_request()
    assert request.provider == "github"
    assert request.repository == "owner/repo"
    assert request.pull_request_id == 5
    assert request.discussion_id == 6
    assert request.review_thread_id == "PRRT_snapshot"


def test_passes_snapshot_to_github_repository_fallback() -> None:
    state = {
        "platform": {"code_hosting": "github"},
        "pull_request_id": 5,
        "discussion_id": 6,
        "review_thread_id": "PRRT_snapshot",
        "suggestion": {"commit_hash": "abcdef"},
    }
    with (
        patch.dict("os.environ", {"GITHUB_REPOSITORY": ""}, clear=False),
        patch("agentic_devtools.cli.suggestion_confirm.load_state_locked", return_value=state),
        patch(
            "agentic_devtools.cli.pull_request_comments.resolve_github_repo_safe",
            side_effect=lambda snapshot: "snapshot-org/snapshot-repo" if snapshot is state else None,
        ) as resolve_repo,
    ):
        request = build_confirmation_request()
    assert request.repository == "snapshot-org/snapshot-repo"
    resolve_repo.assert_called_once_with(state)


def test_passes_snapshot_to_azure_repository_fallback() -> None:
    state = {
        "platform": {"code_hosting": "azure_devops"},
        "pull_request_id": 5,
        "discussion_id": 6,
        "suggestion": {"commit_hash": "abcdef"},
    }
    snapshot_config = type(
        "Config",
        (),
        {
            "organization": "https://dev.azure.com/state-org",
            "project": "state-project",
            "repository": "state-repo",
        },
    )()

    def from_state(*, state=None):
        return snapshot_config if state is state_snapshot else None

    state_snapshot = state
    with (
        patch("agentic_devtools.cli.suggestion_confirm.load_state_locked", return_value=state),
        patch(
            "agentic_devtools.cli.pull_request_comments.AzureDevOpsConfig.from_state",
            side_effect=from_state,
        ) as from_state,
    ):
        request = build_confirmation_request(
            organization="https://dev.azure.com/explicit-org",
            project="explicit-project",
        )
    assert request.repository == "state-repo"
    from_state.assert_called_once_with(state=state)


def test_rejects_unrecognised_dry_run_state_value() -> None:
    with (
        patch(
            "agentic_devtools.cli.suggestion_confirm.resolve_comment_provider",
            return_value="azure_devops",
        ),
        patch(
            "agentic_devtools.cli.suggestion_confirm._resolve_repository",
            return_value="repo",
        ),
        patch(
            "agentic_devtools.cli.suggestion_confirm.load_state_locked",
            return_value={
                "pull_request_id": 1,
                "discussion_id": 2,
                "suggestion": {"commit_hash": "abc"},
                "dry_run": "maybe",
            },
        ),
    ):
        with pytest.raises(ValueError, match="Unrecognised boolean value"):
            build_confirmation_request()
