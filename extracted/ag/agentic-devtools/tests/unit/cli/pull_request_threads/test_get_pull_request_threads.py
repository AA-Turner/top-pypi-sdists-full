from unittest.mock import patch

import pytest

from agentic_devtools.cli.pull_request_threads import get_pull_request_threads


def test_github_lists_threads(capsys) -> None:
    thread = type("Thread", (), {"id": "1", "status": "active", "file": "a.py", "line": 2, "comments": ()})()
    with (
        patch("agentic_devtools.cli.pull_request_threads.resolve_thread_provider", return_value="github"),
        patch("agentic_devtools.cli.pull_request_threads.get_value", side_effect=["owner/repo"]),
        patch("agentic_devtools.cli.pull_request_threads.GitHubPullRequestThreadsAdapter.list", return_value=(thread,)),
    ):
        get_pull_request_threads(4)
    assert '"id": "1"' in capsys.readouterr().out


def test_github_ignores_legacy_azure_repository_name(monkeypatch) -> None:
    monkeypatch.delenv("GITHUB_REPOSITORY", raising=False)
    with (
        patch("agentic_devtools.cli.pull_request_threads.resolve_thread_provider", return_value="github"),
        patch(
            "agentic_devtools.cli.pull_request_threads.get_value",
            side_effect=lambda key: {"repository": "repo-name"}.get(key),
        ),
        patch("agentic_devtools.cli.pull_request_threads.resolve_github_repo_safe", return_value="owner/repo"),
        patch("agentic_devtools.cli.pull_request_threads.GitHubPullRequestThreadsAdapter.list", return_value=()),
    ):
        get_pull_request_threads(4)


def test_github_dry_run_validates_request_without_constructing_adapter(capsys) -> None:
    with (
        patch("agentic_devtools.cli.pull_request_threads.resolve_thread_provider", return_value="github"),
        patch("agentic_devtools.cli.pull_request_threads.get_value", return_value="owner/repo"),
        patch("agentic_devtools.cli.pull_request_threads.is_dry_run", return_value=True),
        patch("agentic_devtools.cli.pull_request_threads.GitHubPullRequestThreadsAdapter") as adapter,
    ):
        assert get_pull_request_threads(4) is None

    adapter.assert_not_called()
    output = capsys.readouterr().out
    assert "[DRY RUN] Would get threads for PR 4" in output
    assert "Repository: owner/repo" in output


def test_github_dry_run_rejects_invalid_request_before_preview() -> None:
    with (
        patch("agentic_devtools.cli.pull_request_threads.resolve_thread_provider", return_value="github"),
        patch("agentic_devtools.cli.pull_request_threads.is_dry_run", return_value=True),
        patch("agentic_devtools.cli.pull_request_threads.GitHubPullRequestThreadsAdapter") as adapter,
        pytest.raises(ValueError, match="owner/repo"),
    ):
        get_pull_request_threads(4, repository="invalid")

    adapter.assert_not_called()


def test_azure_delegates_to_existing_command() -> None:
    with (
        patch("agentic_devtools.cli.pull_request_threads.resolve_thread_provider", return_value="azure_devops"),
        patch(
            "agentic_devtools.cli.pull_request_threads._azure_devops_context",
            return_value=("https://dev.azure.com/org", "project", "repo"),
        ),
        patch("agentic_devtools.cli.azure_devops.commands.get_pull_request_threads") as delegate,
    ):
        get_pull_request_threads(4)
    delegate.assert_called_once_with(
        4,
        repository="repo",
        organization="https://dev.azure.com/org",
        project="project",
    )


def test_azure_passes_repository_override() -> None:
    with (
        patch("agentic_devtools.cli.pull_request_threads.resolve_thread_provider", return_value="azure_devops"),
        patch(
            "agentic_devtools.cli.pull_request_threads._azure_devops_context",
            return_value=("https://dev.azure.com/org", "project", "override-repo"),
        ),
        patch("agentic_devtools.cli.azure_devops.commands.get_pull_request_threads") as delegate,
    ):
        get_pull_request_threads(4, repository="override-repo")
    delegate.assert_called_once_with(
        4,
        repository="override-repo",
        organization="https://dev.azure.com/org",
        project="project",
    )


def test_azure_falls_back_when_legacy_context_exists() -> None:
    with (
        patch(
            "agentic_devtools.cli.pull_request_threads.resolve_thread_provider",
            return_value="azure_devops",
        ) as resolve_provider,
        patch(
            "agentic_devtools.cli.pull_request_threads._azure_devops_context",
            return_value=("https://dev.azure.com/org", "project", "repo"),
        ),
        patch("agentic_devtools.cli.azure_devops.commands.get_pull_request_threads") as delegate,
    ):
        get_pull_request_threads(4)
    delegate.assert_called_once_with(
        4,
        repository="repo",
        organization="https://dev.azure.com/org",
        project="project",
    )
    resolve_provider.assert_called_once_with(None, allow_legacy_azure_fallback=True)


def test_azure_uses_remote_when_root_configuration_is_malformed() -> None:
    with (
        patch("agentic_devtools.cli.pull_request_threads.resolve_thread_provider", return_value="azure_devops"),
        patch("agentic_devtools.cli.pull_request_threads.get_value", return_value=None),
        patch("agentic_devtools.cli.pull_request_threads.get_repo_root", return_value="/repo"),
        patch(
            "agentic_devtools.cli.pull_request_threads.load_platform_config",
            return_value={"azure_devops": None},
        ),
        patch(
            "agentic_devtools.cli.pull_request_threads.get_azure_devops_context_from_git_remote",
            return_value=("https://dev.azure.com/org", "project", "repo"),
        ),
        patch("agentic_devtools.cli.azure_devops.commands.get_pull_request_threads") as delegate,
    ):
        get_pull_request_threads(4)

    delegate.assert_called_once_with(
        4,
        repository="repo",
        organization="https://dev.azure.com/org",
        project="project",
    )


@pytest.mark.parametrize("field", ["repository", "organization", "project"])
def test_rejects_empty_explicit_azure_coordinate(field: str) -> None:
    with (
        patch("agentic_devtools.cli.pull_request_threads.resolve_thread_provider", return_value="azure_devops"),
        pytest.raises(ValueError, match=f"{field} must be a non-empty string"),
    ):
        get_pull_request_threads(4, **{field: " "})


def test_rejects_unknown_provider_without_legacy_azure_context() -> None:
    with (
        patch(
            "agentic_devtools.cli.pull_request_threads.resolve_thread_provider", side_effect=ValueError("bad provider")
        ),
        patch(
            "agentic_devtools.cli.pull_request_threads.AzureDevOpsConfig.from_state", side_effect=ValueError("no azure")
        ),
    ):
        with pytest.raises(ValueError, match="bad provider"):
            get_pull_request_threads(4)


def test_rejects_invalid_explicit_provider_without_azure_fallback() -> None:
    with patch(
        "agentic_devtools.cli.pull_request_threads.resolve_thread_provider",
        side_effect=ValueError("bad provider"),
    ):
        with pytest.raises(ValueError, match="bad provider"):
            get_pull_request_threads(4, provider="bitbucket")


def test_rejects_invalid_configured_provider_without_azure_fallback() -> None:
    with (
        patch(
            "agentic_devtools.cli.pull_request_threads.resolve_thread_provider",
            side_effect=ValueError("bad provider"),
        ),
        patch("agentic_devtools.cli.pull_request_threads.get_value", return_value="bitbucket"),
    ):
        with pytest.raises(ValueError, match="bad provider"):
            get_pull_request_threads(4)


def test_rejects_malformed_configured_provider_without_azure_fallback() -> None:
    with (
        patch(
            "agentic_devtools.cli.pull_request_threads.resolve_thread_provider",
            side_effect=ValueError("bad provider"),
        ),
        patch("agentic_devtools.cli.pull_request_threads.get_value", return_value=123),
    ):
        with pytest.raises(ValueError, match="bad provider"):
            get_pull_request_threads(4)


@pytest.mark.parametrize("value", [None, True, "not-a-number", 0, -1])
def test_rejects_invalid_pull_request_id(value) -> None:
    with (
        patch("agentic_devtools.cli.pull_request_threads.resolve_thread_provider", return_value="github"),
        patch("agentic_devtools.cli.pull_request_threads.get_value", return_value=None),
    ):
        with pytest.raises(ValueError, match="pull_request_id"):
            get_pull_request_threads(value)


def test_rejects_missing_repository(monkeypatch) -> None:
    monkeypatch.delenv("GITHUB_REPOSITORY", raising=False)
    with (
        patch("agentic_devtools.cli.pull_request_threads.resolve_thread_provider", return_value="github"),
        patch("agentic_devtools.cli.pull_request_threads.get_value", return_value=None),
        patch("agentic_devtools.cli.pull_request_threads.get_repo_root", return_value=None),
        patch("agentic_devtools.cli.pull_request_threads.resolve_github_repo_safe", return_value=None),
    ):
        with pytest.raises(ValueError, match="repository"):
            get_pull_request_threads(4)
