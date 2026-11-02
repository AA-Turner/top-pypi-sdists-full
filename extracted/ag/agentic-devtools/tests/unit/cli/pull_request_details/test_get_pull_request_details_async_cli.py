import sys
from unittest.mock import call, patch

import pytest

from agentic_devtools.cli.pull_request_details import get_pull_request_details_async_cli


def test_get_pull_request_details_async_cli_persists_overrides() -> None:
    with (
        patch.object(
            sys,
            "argv",
            ["agdt-get-pull-request-details", "--provider", "github", "--pr", "7", "--repo", "o/r"],
        ),
        patch("agentic_devtools.cli.pull_request_details.set_value") as set_value,
        patch("agentic_devtools.cli.pull_request_details.get_pull_request_details_async") as dispatch,
    ):
        get_pull_request_details_async_cli()
    assert set_value.call_count == 2
    set_value.assert_any_call("pull_request_id", 7)
    # The parsed overrides must also be forwarded directly to the dispatcher so they
    # take precedence over a stale persisted top-level `provider` state key.
    dispatch.assert_called_once_with(provider="github", pull_request_id=7, repository="o/r")


def test_get_pull_request_details_async_cli_preserves_inherited_provider_and_repository_for_pr_scope() -> None:
    with (
        patch.object(sys, "argv", ["agdt-get-pull-request-details", "--pr", "43"]),
        patch(
            "agentic_devtools.cli.pull_request_details.load_state_locked",
            return_value={"platform": {"code_hosting": "github"}, "github": {"repo": "owner/repo"}},
        ),
        patch("agentic_devtools.cli.pull_request_details.set_value") as set_value,
        patch("agentic_devtools.cli.pull_request_details.get_pull_request_details_async") as dispatch,
    ):
        get_pull_request_details_async_cli()

    set_value.assert_any_call("pull_request_id", 43)
    dispatch.assert_called_once_with(provider="github", pull_request_id=43, repository="owner/repo")


def test_get_pull_request_details_async_cli_preserves_inherited_azure_repository_for_pr_scope() -> None:
    with (
        patch.object(sys, "argv", ["agdt-get-pull-request-details", "--pr", "43"]),
        patch(
            "agentic_devtools.cli.pull_request_details.load_state_locked",
            return_value={
                "provider": "azure_devops",
                "azure_devops": {"repository": "project/repo"},
            },
        ),
        patch("agentic_devtools.cli.pull_request_details.set_value"),
        patch("agentic_devtools.cli.pull_request_details.get_pull_request_details_async") as dispatch,
    ):
        get_pull_request_details_async_cli()

    dispatch.assert_called_once_with(provider="azure_devops", pull_request_id=43, repository="project/repo")


def test_get_pull_request_details_async_cli_preserves_azure_organization_and_project_for_pr_scope() -> None:
    organization = "https://dev.azure.com/example"
    project = "Example Project"
    with (
        patch.object(sys, "argv", ["agdt-get-pull-request-details", "--pr", "43"]),
        patch(
            "agentic_devtools.cli.pull_request_details.load_state_locked",
            return_value={
                "provider": "azure_devops",
                "organization": organization,
                "project": project,
            },
        ),
        patch("agentic_devtools.cli.pull_request_details.set_value") as set_value,
        patch("agentic_devtools.cli.pull_request_details.get_pull_request_details_async") as dispatch,
    ):
        get_pull_request_details_async_cli()

    assert set_value.call_args_list[-2:] == [
        call("organization", organization),
        call("project", project),
    ]
    dispatch.assert_called_once_with(provider="azure_devops", pull_request_id=43)


def test_get_pull_request_details_async_cli_carries_dry_run_and_nested_azure_config_on_provider_switch() -> None:
    organization = "https://dev.azure.com/selected"
    project = "Selected Project"
    with (
        patch.object(
            sys,
            "argv",
            ["agdt-get-pull-request-details", "--provider", "azure_devops", "--pr", "43"],
        ),
        patch(
            "agentic_devtools.cli.pull_request_details.load_state_locked",
            return_value={
                "provider": "github",
                "organization": "https://dev.azure.com/stale",
                "project": "Stale Project",
                "dry_run": True,
                "azure_devops": {"organization": organization, "project": project},
            },
        ),
        patch("agentic_devtools.cli.pull_request_details.set_value") as set_value,
        patch("agentic_devtools.cli.pull_request_details.get_pull_request_details_async") as dispatch,
    ):
        get_pull_request_details_async_cli()

    assert call("dry_run", True) in set_value.call_args_list
    assert call("organization", organization) in set_value.call_args_list
    assert call("project", project) in set_value.call_args_list
    assert call("organization", "https://dev.azure.com/stale") not in set_value.call_args_list
    assert call("project", "Stale Project") not in set_value.call_args_list
    dispatch.assert_called_once_with(provider="azure_devops", pull_request_id=43)


@pytest.mark.parametrize("repository", ["project/repo", ""])
def test_get_pull_request_details_async_cli_uses_generic_azure_repository_fallback(repository: str) -> None:
    with (
        patch.object(sys, "argv", ["agdt-get-pull-request-details", "--pr", "43"]),
        patch(
            "agentic_devtools.cli.pull_request_details.load_state_locked",
            return_value={"provider": "azure_devops", "repository": repository},
        ),
        patch("agentic_devtools.cli.pull_request_details.set_value"),
        patch("agentic_devtools.cli.pull_request_details.get_pull_request_details_async") as dispatch,
    ):
        get_pull_request_details_async_cli()

    expected = {"provider": "azure_devops", "pull_request_id": 43}
    if repository:
        expected["repository"] = repository
    dispatch.assert_called_once_with(**expected)


def test_get_pull_request_details_async_cli_preserves_canonical_repository_for_pr_scope() -> None:
    with (
        patch.object(sys, "argv", ["agdt-get-pull-request-details", "--pr", "43"]),
        patch(
            "agentic_devtools.cli.pull_request_details.load_state_locked",
            return_value={
                "provider": "azure_devops",
                "sourceCodeHostingPlatform": {"pullRequest": {"repository": "project/repo"}},
            },
        ),
        patch("agentic_devtools.cli.pull_request_details.set_value"),
        patch("agentic_devtools.cli.pull_request_details.get_pull_request_details_async") as dispatch,
    ):
        get_pull_request_details_async_cli()

    dispatch.assert_called_once_with(provider="azure_devops", pull_request_id=43, repository="project/repo")


def test_get_pull_request_details_async_cli_preserves_canonical_github_repository_for_pr_scope() -> None:
    with (
        patch.object(sys, "argv", ["agdt-get-pull-request-details", "--pr", "43"]),
        patch(
            "agentic_devtools.cli.pull_request_details.load_state_locked",
            return_value={
                "provider": "github",
                "sourceCodeHostingPlatform": {"pullRequest": {"repository": "owner/repo"}},
            },
        ),
        patch("agentic_devtools.cli.pull_request_details.set_value"),
        patch("agentic_devtools.cli.pull_request_details.get_pull_request_details_async") as dispatch,
    ):
        get_pull_request_details_async_cli()

    dispatch.assert_called_once_with(provider="github", pull_request_id=43, repository="owner/repo")


def test_get_pull_request_details_async_cli_does_not_reuse_canonical_repository_after_provider_switch() -> None:
    with (
        patch.object(
            sys,
            "argv",
            ["agdt-get-pull-request-details", "--provider", "github", "--pr", "43"],
        ),
        patch(
            "agentic_devtools.cli.pull_request_details.load_state_locked",
            return_value={
                "provider": "azure_devops",
                "sourceCodeHostingPlatform": {"pullRequest": {"repository": "project/repo"}},
            },
        ),
        patch("agentic_devtools.cli.pull_request_details.set_value"),
        patch("agentic_devtools.cli.pull_request_details.get_pull_request_details_async") as dispatch,
    ):
        get_pull_request_details_async_cli()

    dispatch.assert_called_once_with(provider="github", pull_request_id=43)


def test_get_pull_request_details_async_cli_does_not_reuse_generic_azure_repository_after_provider_switch() -> None:
    with (
        patch.object(
            sys,
            "argv",
            ["agdt-get-pull-request-details", "--provider", "azure_devops", "--pr", "43"],
        ),
        patch(
            "agentic_devtools.cli.pull_request_details.load_state_locked",
            return_value={"provider": "github", "repository": "owner/old-repo"},
        ),
        patch("agentic_devtools.cli.pull_request_details.set_value"),
        patch("agentic_devtools.cli.pull_request_details.get_pull_request_details_async") as dispatch,
    ):
        get_pull_request_details_async_cli()

    dispatch.assert_called_once_with(provider="azure_devops", pull_request_id=43)


def test_get_pull_request_details_async_cli_persists_azure_repository_under_provider_key() -> None:
    with (
        patch.object(
            sys,
            "argv",
            ["agdt-get-pull-request-details", "--provider", "azure_devops", "--repo", "project/repo"],
        ),
        patch("agentic_devtools.cli.pull_request_details.set_value") as set_value,
        patch("agentic_devtools.cli.pull_request_details.get_pull_request_details_async") as dispatch,
    ):
        get_pull_request_details_async_cli()
    assert not any(call.args == ("repository", "project/repo") for call in set_value.call_args_list)
    dispatch.assert_called_once_with(provider="azure_devops", repository="project/repo")


def test_get_pull_request_details_async_cli_repo_without_provider_uses_persisted_provider() -> None:
    with (
        patch.object(sys, "argv", ["agdt-get-pull-request-details", "--repo", "o/r"]),
        patch(
            "agentic_devtools.cli.pull_request_details.load_state_locked",
            return_value={"provider": "github"},
        ),
        patch("agentic_devtools.cli.pull_request_details.set_value"),
        patch("agentic_devtools.cli.pull_request_details.get_pull_request_details_async") as dispatch,
    ):
        get_pull_request_details_async_cli()
    dispatch.assert_called_once_with(provider="github", repository="o/r")


def test_get_pull_request_details_async_cli_repo_without_provider_detects_remote_provider() -> None:
    with (
        patch.object(sys, "argv", ["agdt-get-pull-request-details", "--repo", "o/r"]),
        patch("agentic_devtools.cli.pull_request_details.load_state_locked", return_value={}),
        patch("agentic_devtools.cli.pull_request_details.detect_provider", return_value="github") as detect,
        patch("agentic_devtools.cli.pull_request_details.set_value"),
        patch("agentic_devtools.cli.pull_request_details.get_pull_request_details_async") as dispatch,
    ):
        get_pull_request_details_async_cli()
    detect.assert_called_once_with(None, {}, "o/r")
    dispatch.assert_called_once_with(provider="github", repository="o/r")


def test_get_pull_request_details_async_cli_rejects_invalid_github_repo() -> None:
    with (
        patch.object(
            sys,
            "argv",
            ["agdt-get-pull-request-details", "--provider", "github", "--repo", "invalid"],
        ),
        patch("agentic_devtools.cli.pull_request_details.set_value") as set_value,
        patch("agentic_devtools.cli.pull_request_details.get_pull_request_details_async") as dispatch,
    ):
        with pytest.raises(SystemExit):
            get_pull_request_details_async_cli()
    assert not any(
        call.args == ("sourceCodeHostingPlatform.pullRequest.repository", "invalid")
        for call in set_value.call_args_list
    )
    dispatch.assert_not_called()


def test_get_pull_request_details_async_cli_rejects_blank_repo() -> None:
    with (
        patch.object(sys, "argv", ["agdt-get-pull-request-details", "--provider", "github", "--repo", "  "]),
        patch("agentic_devtools.cli.pull_request_details.set_value") as set_value,
        patch("agentic_devtools.cli.pull_request_details.get_pull_request_details_async") as dispatch,
    ):
        with pytest.raises(SystemExit):
            get_pull_request_details_async_cli()
    set_value.assert_not_called()
    dispatch.assert_not_called()


def test_get_pull_request_details_async_cli_reports_provider_detection_error(capsys) -> None:
    with (
        patch.object(sys, "argv", ["agdt-get-pull-request-details", "--repo", "o/r"]),
        patch("agentic_devtools.cli.pull_request_details.load_state_locked", return_value={}),
        patch(
            "agentic_devtools.cli.pull_request_details.detect_provider",
            side_effect=ValueError("Unable to detect provider"),
        ),
        patch("agentic_devtools.cli.pull_request_details.set_value") as set_value,
        patch("agentic_devtools.cli.pull_request_details.get_pull_request_details_async") as dispatch,
    ):
        with pytest.raises(SystemExit):
            get_pull_request_details_async_cli()
    assert "Unable to detect provider" in capsys.readouterr().err
    set_value.assert_not_called()
    dispatch.assert_not_called()


def test_get_pull_request_details_async_cli_without_overrides_dispatches() -> None:
    with (
        patch.object(sys, "argv", ["agdt-get-pull-request-details"]),
        patch("agentic_devtools.cli.pull_request_details.set_value") as set_value,
        patch("agentic_devtools.cli.pull_request_details.get_pull_request_details_async") as dispatch,
    ):
        get_pull_request_details_async_cli()
    set_value.assert_not_called()
    dispatch.assert_called_once_with()


def test_get_pull_request_details_async_cli_help_documents_state_fallback(capsys) -> None:
    with (
        patch.object(sys, "argv", ["agdt-get-pull-request-details", "--help"]),
        patch("agentic_devtools.cli.pull_request_details.set_value") as set_value,
        patch("agentic_devtools.cli.pull_request_details.get_pull_request_details_async") as dispatch,
        pytest.raises(SystemExit) as exc_info,
    ):
        get_pull_request_details_async_cli()

    assert exc_info.value.code == 0
    help_text = " ".join(capsys.readouterr().out.split())
    assert "pull_request_id" in help_text
    assert "persists the response and logs its output path" in help_text
    set_value.assert_not_called()
    dispatch.assert_not_called()


def test_get_pull_request_details_async_cli_rejects_zero_pr() -> None:
    with (
        patch.object(sys, "argv", ["agdt-get-pull-request-details", "--pr", "0"]),
        patch("agentic_devtools.cli.pull_request_details.set_value") as set_value,
        patch("agentic_devtools.cli.pull_request_details.get_pull_request_details_async") as dispatch,
    ):
        with pytest.raises(SystemExit):
            get_pull_request_details_async_cli()
    set_value.assert_not_called()
    dispatch.assert_not_called()


def test_get_pull_request_details_async_cli_rejects_negative_pr() -> None:
    with (
        patch.object(sys, "argv", ["agdt-get-pull-request-details", "--pr", "-3"]),
        patch("agentic_devtools.cli.pull_request_details.set_value") as set_value,
        patch("agentic_devtools.cli.pull_request_details.get_pull_request_details_async") as dispatch,
    ):
        with pytest.raises(SystemExit):
            get_pull_request_details_async_cli()
    set_value.assert_not_called()
    dispatch.assert_not_called()
