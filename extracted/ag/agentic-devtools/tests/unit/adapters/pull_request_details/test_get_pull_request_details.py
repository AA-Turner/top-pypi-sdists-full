from pathlib import Path
from typing import Any
from unittest.mock import patch

import pytest

from agentic_devtools.adapters.pull_request_details import get_pull_request_details


def test_get_pull_request_details_github_collects_provider_data() -> None:
    provider = type(
        "Provider",
        (),
        {
            "get_pr_diff": lambda self, number: "diff",
            "list_reviews": lambda self, number: [{"id": 1}],
            "list_all_review_comments": lambda self, number: [],
            "list_issue_comments": lambda self, number: [],
            "list_review_threads_by_thread_id": lambda self, number: {},
        },
    )()
    with patch("agentic_devtools.adapters.pull_request_details.GitHubActionsProvider", return_value=provider):
        with patch(
            "agentic_devtools.adapters.pull_request_details._github_api_json",
            side_effect=[
                {
                    "number": 3,
                    "title": "Title",
                    "draft": False,
                    "state": "open",
                    "head": {"ref": "feature", "sha": "abc"},
                    "base": {"ref": "main", "sha": "def"},
                },
                [{"sha": "abc"}],
                [{"filename": "x.py", "status": "modified", "additions": 2, "deletions": 1, "patch": "@@"}],
                {"head": {"sha": "abc"}},
            ],
        ):
            result = get_pull_request_details("github", 3, "owner/repo")
    assert result is not None
    assert result["pullRequest"]["pullRequestId"] == 3
    assert result["pullRequest"]["lastMergeSourceCommit"] == {"commitId": "abc"}
    assert result["commits"] == [{"sha": "abc"}]
    assert result["files"][0]["path"] == "x.py"
    assert result["files"][0]["changeType"] == "edit"
    assert result["diff"] == "diff"
    assert result["reviewer"]["reviews"] == [{"id": 1}]


def test_get_pull_request_details_delegates_azure() -> None:
    with patch("agentic_devtools.cli.azure_devops.pull_request_details_commands.get_pull_request_details") as delegated:
        state = {"pull_request_id": 9}
        assert get_pull_request_details("azure_devops", 3, "repo", state=state) is None
    delegated.assert_called_once_with(
        pull_request_id=3,
        repository="repo",
        state={
            "pull_request_id": 9,
            "provider": "azure_devops",
            "platform": {"code_hosting": "azure_devops"},
        },
    )


def test_get_pull_request_details_delegates_azure_overrides_conflicting_provider() -> None:
    """An explicit azure_devops selection wins even if state carries a conflicting provider."""
    with patch("agentic_devtools.cli.azure_devops.pull_request_details_commands.get_pull_request_details") as delegated:
        state = {"provider": "github", "platform": {"code_hosting": "github"}}
        assert get_pull_request_details("azure_devops", 3, "repo", state=state) is None
    delegated.assert_called_once_with(
        pull_request_id=3,
        repository="repo",
        state={"provider": "azure_devops", "platform": {"code_hosting": "azure_devops"}},
    )


def test_get_pull_request_details_drops_stale_repository_aliases_on_azure_switch() -> None:
    state: dict[str, Any] = {
        "provider": "github",
        "platform": {"code_hosting": "github", "other_setting": True},
        "sourceCodeHostingPlatform": {"pullRequest": {"repository": "old-owner/old-repo", "headSha": "abc"}},
        "repository": "old-owner/generic-repo",
        "github": {"repo": "old-owner/old-repo", "pull_request_number": 9},
        "azure_devops": {"repository": "current-azure-repo"},
        "organization": "org",
        "project": "project",
    }
    with patch("agentic_devtools.cli.azure_devops.pull_request_details_commands.get_pull_request_details") as delegated:
        get_pull_request_details("azure_devops", 3, state=state)

    delegated_state = delegated.call_args.kwargs["state"]
    assert "repository" not in delegated_state
    assert "repository" not in delegated_state["sourceCodeHostingPlatform"]["pullRequest"]
    assert delegated_state["sourceCodeHostingPlatform"]["pullRequest"]["headSha"] == "abc"
    assert "repo" not in delegated_state["github"]
    assert delegated_state["github"]["pull_request_number"] == 9
    assert delegated_state["azure_devops"]["repository"] == "current-azure-repo"
    assert delegated_state["organization"] == "org"
    assert delegated_state["project"] == "project"
    assert delegated_state["platform"] == {"code_hosting": "azure_devops", "other_setting": True}
    assert state["sourceCodeHostingPlatform"]["pullRequest"]["repository"] == "old-owner/old-repo"
    assert state["github"]["repo"] == "old-owner/old-repo"

    with patch("agentic_devtools.cli.azure_devops.pull_request_details_commands.get_pull_request_details") as delegated:
        get_pull_request_details(
            "azure_devops",
            3,
            state={"provider": "github", "sourceCodeHostingPlatform": {"pullRequest": None}},
        )
    assert delegated.call_args.kwargs["state"]["sourceCodeHostingPlatform"]["pullRequest"] is None


def test_get_pull_request_details_delegates_azure_without_state() -> None:
    """Delegation still injects the resolved provider when no state is supplied."""
    with patch("agentic_devtools.cli.azure_devops.pull_request_details_commands.get_pull_request_details") as delegated:
        assert get_pull_request_details("azure_devops", 3, "repo") is None
    delegated.assert_called_once_with(
        pull_request_id=3,
        repository="repo",
        state={"provider": "azure_devops", "platform": {"code_hosting": "azure_devops"}},
    )


def test_get_pull_request_details_passes_request_snapshot_options_to_azure() -> None:
    output_file = Path("request.json")
    with patch("agentic_devtools.cli.azure_devops.pull_request_details_commands.get_pull_request_details") as delegated:
        get_pull_request_details(
            "azure_devops",
            3,
            "repo",
            state={"organization": "org", "project": "project"},
            output_file=output_file,
            dry_run=True,
            state_snapshot=True,
        )

    delegated.assert_called_once_with(
        pull_request_id=3,
        repository="repo",
        state={
            "organization": "org",
            "project": "project",
            "provider": "azure_devops",
            "platform": {"code_hosting": "azure_devops"},
        },
        output_file=output_file,
        dry_run=True,
        state_snapshot=True,
    )


def test_get_pull_request_details_validates_github_arguments() -> None:
    with pytest.raises(ValueError, match="positive"):
        get_pull_request_details("github", 0, "owner/repo")
    with pytest.raises(ValueError, match="owner/repo"):
        get_pull_request_details("github", 1, "invalid")
    with pytest.raises(ValueError, match="owner/repo"):
        get_pull_request_details("github", 1, "/repo")
    with pytest.raises(ValueError, match="owner/repo"):
        get_pull_request_details("github", 1, "owner/")
    with pytest.raises(ValueError, match="owner/repo"):
        get_pull_request_details("github", 1, "owner /repo")
