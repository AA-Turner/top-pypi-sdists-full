from unittest.mock import patch

import pytest

from agentic_devtools.cli.pull_request_threads import (
    build_thread_resolution_request,
)


@patch("agentic_devtools.cli.pull_request_threads.get_value")
def test_builds_github_snapshot_without_writing_state(mock_get_value) -> None:
    values = {
        "platform.code_hosting": "github",
        "thread_id": 99,
        "repository": "owner/repo",
    }
    mock_get_value.side_effect = lambda key: values.get(key)

    request = build_thread_resolution_request(pull_request_id=7)

    assert request.provider == "github"
    assert request.github_comment_id == 99
    assert request.as_dict()["github_comment_id"] == 99


@patch("agentic_devtools.cli.pull_request_threads.get_value")
def test_builds_github_snapshot_from_state_comment_id(mock_get_value) -> None:
    values = {
        "platform.code_hosting": "github",
        "github.comment_id": 99,
        "repository": "owner/repo",
    }
    mock_get_value.side_effect = lambda key: values.get(key)

    request = build_thread_resolution_request(pull_request_id=7)

    assert request.provider == "github"
    assert request.github_comment_id == 99
    assert request.github_thread_node_id is None


@patch("agentic_devtools.cli.pull_request_threads.get_value")
def test_github_native_identifier_precedes_stale_legacy_thread(mock_get_value) -> None:
    mock_get_value.side_effect = lambda key: {
        "platform.code_hosting": "github",
        "github.repo": "owner/repo",
        "repository": "stale/repo",
        "thread_id": 99,
        "github.thread_node_id": "PRRT_node",
    }.get(key)

    request = build_thread_resolution_request(pull_request_id=7)

    assert request.repository == "owner/repo"
    assert request.github_thread_node_id == "PRRT_node"
    assert request.github_comment_id is None


@patch("agentic_devtools.cli.pull_request_threads.get_value")
def test_github_thread_node_id_precedes_stale_comment_id_from_state(mock_get_value) -> None:
    mock_get_value.side_effect = lambda key: {
        "platform.code_hosting": "github",
        "github.repo": "owner/repo",
        "github.thread_node_id": "PRRT_node",
        "github.comment_id": 99,
    }.get(key)

    request = build_thread_resolution_request(pull_request_id=7)

    assert request.github_thread_node_id == "PRRT_node"
    assert request.github_comment_id is None


@patch("agentic_devtools.cli.pull_request_threads.get_value")
def test_blank_github_thread_node_id_falls_back_to_comment_id(mock_get_value) -> None:
    mock_get_value.side_effect = lambda key: {
        "platform.code_hosting": "github",
        "github.repo": "owner/repo",
        "github.thread_node_id": "",
        "github.comment_id": 99,
    }.get(key)

    request = build_thread_resolution_request(pull_request_id=7)

    assert request.github_thread_node_id is None
    assert request.github_comment_id == 99


@patch("agentic_devtools.cli.pull_request_threads.get_value")
def test_blank_github_native_aliases_fall_back_to_legacy_thread_id(mock_get_value) -> None:
    mock_get_value.side_effect = lambda key: {
        "platform.code_hosting": "github",
        "github.repo": "owner/repo",
        "github.thread_node_id": " ",
        "github.comment_id": "",
        "thread_id": 42,
    }.get(key)

    request = build_thread_resolution_request(pull_request_id=7)

    assert request.github_thread_node_id is None
    assert request.github_comment_id == 42


@patch("agentic_devtools.cli.pull_request_threads.get_value")
def test_azure_ignores_github_repository_state(mock_get_value) -> None:
    mock_get_value.side_effect = lambda key: {
        "platform.code_hosting": "azure_devops",
        "organization": "https://dev.azure.com/org",
        "project": "project",
        "github.repo": "owner/repo",
        "repository": "ado-repo",
        "thread_id": 99,
    }.get(key)

    request = build_thread_resolution_request(pull_request_id=7)

    assert request.repository == "ado-repo"


@patch("agentic_devtools.cli.pull_request_threads.get_azure_devops_context_from_git_remote")
@patch("agentic_devtools.cli.pull_request_threads.get_value")
def test_azure_state_context_does_not_probe_git_remote(mock_get_value, mock_remote_context) -> None:
    mock_get_value.side_effect = lambda key: {
        "platform.code_hosting": "azure_devops",
        "organization": "https://dev.azure.com/org",
        "project": "project",
        "repository": "ado-repo",
        "thread_id": 99,
    }.get(key)

    request = build_thread_resolution_request(pull_request_id=7)

    assert request.repository == "ado-repo"
    mock_remote_context.assert_not_called()


@pytest.mark.parametrize("missing_key", ["organization", "project", "repository"])
@patch("agentic_devtools.cli.pull_request_threads.get_azure_devops_context_from_git_remote")
@patch("agentic_devtools.cli.pull_request_threads.get_value")
def test_azure_partial_state_context_uses_missing_remote_value(
    mock_get_value, mock_remote_context, missing_key
) -> None:
    values = {
        "platform.code_hosting": "azure_devops",
        "organization": "https://dev.azure.com/state-org",
        "project": "state-project",
        "repository": "state-repo",
        "thread_id": 99,
    }
    values[missing_key] = None
    mock_get_value.side_effect = lambda key: values.get(key)
    mock_remote_context.return_value = (
        "https://dev.azure.com/remote-org",
        "remote-project",
        "remote-repo",
    )

    request = build_thread_resolution_request(pull_request_id=7)

    assert request.repository == ("remote-repo" if missing_key == "repository" else "state-repo")
    mock_remote_context.assert_called_once_with()


@patch("agentic_devtools.cli.pull_request_threads.get_value")
def test_rejects_missing_explicit_provider(mock_get_value) -> None:
    mock_get_value.return_value = None

    with patch("agentic_devtools.cli.pull_request_threads.get_repo_root", return_value=None):
        with pytest.raises(ValueError, match="platform.code_hosting"):
            build_thread_resolution_request(
                repository="owner/repo",
                pull_request_id=7,
                thread_node_id="PRRT_node",
            )


@patch("agentic_devtools.cli.pull_request_threads.get_value")
def test_builds_azure_snapshot_from_legacy_aliases(mock_get_value) -> None:
    values = {
        "platform.code_hosting": "azure_devops",
        "organization": "https://dev.azure.com/org",
        "project": "project",
        "repository": "repo",
        "thread_id": 99,
    }
    mock_get_value.side_effect = lambda key: values.get(key)

    request = build_thread_resolution_request(pull_request_id="7")

    assert request.azure_devops_thread_id == 99
    assert request.repository == "repo"


@patch("agentic_devtools.cli.pull_request_threads.get_value")
def test_rejects_numeric_github_target_when_non_positive(mock_get_value) -> None:
    values = {"platform.code_hosting": "github", "repository": "owner/repo"}
    mock_get_value.side_effect = lambda key: values.get(key)

    with pytest.raises(ValueError, match="positive integer"):
        build_thread_resolution_request(pull_request_id=7, comment_id=0)


@pytest.mark.parametrize("value", [object(), "not-a-number", 0, True])
def test_rejects_invalid_numeric_inputs(value: object) -> None:
    with pytest.raises(ValueError, match="positive integer"):
        build_thread_resolution_request(
            provider="github",
            repository="owner/repo",
            pull_request_id=value,  # type: ignore[arg-type]
            thread_node_id="PRRT_node",
        )


def test_requires_pull_request_id() -> None:
    with (
        pytest.raises(ValueError, match="pull_request_id is required"),
        patch(
            "agentic_devtools.cli.pull_request_threads.get_value",
            return_value=None,
        ),
    ):
        build_thread_resolution_request(
            provider="github",
            repository="owner/repo",
            thread_node_id="PRRT_node",
        )


def test_resolves_provider_native_github_node_id() -> None:
    request = build_thread_resolution_request(
        provider="github",
        repository="owner/repo",
        pull_request_id=7,
        thread_id="PRRT_node",
    )

    assert request.github_thread_node_id == "PRRT_node"


def test_rejects_conflicting_github_identifiers() -> None:
    with pytest.raises(ValueError, match="cannot be combined"):
        build_thread_resolution_request(
            provider="github",
            repository="owner/repo",
            pull_request_id=7,
            thread_id="PRRT_node",
            comment_id=4,
        )


def test_rejects_explicit_github_thread_node_id_and_comment_id() -> None:
    with pytest.raises(ValueError, match="provide either github_thread_node_id or github_comment_id"):
        build_thread_resolution_request(
            provider="github",
            repository="owner/repo",
            pull_request_id=7,
            thread_node_id="PRRT_node",
            comment_id=4,
        )


def test_rejects_missing_thread_identifier() -> None:
    with pytest.raises(ValueError, match="thread_id"):
        build_thread_resolution_request(
            provider="github",
            repository="owner/repo",
            pull_request_id=7,
        )


def test_rejects_invalid_github_repository() -> None:
    with pytest.raises(ValueError, match="owner/repo"):
        build_thread_resolution_request(
            provider="github",
            repository="owner",
            pull_request_id=7,
            thread_node_id="PRRT_node",
        )


@patch("agentic_devtools.cli.pull_request_threads.get_value")
def test_explicit_identifier_overrides_stale_state_identifier(mock_get_value) -> None:
    mock_get_value.side_effect = lambda key: {
        "platform.code_hosting": "github",
        "repository": "owner/repo",
        "thread_id": 99,
    }.get(key)

    request = build_thread_resolution_request(
        pull_request_id=7,
        thread_node_id="PRRT_node",
    )

    assert request.github_thread_node_id == "PRRT_node"


def test_uses_azure_repository_from_configuration() -> None:
    with patch(
        "agentic_devtools.cli.pull_request_threads.get_azure_devops_context_from_git_remote",
        return_value=("https://dev.azure.com/org", "project", "configured-repo"),
    ):
        request = build_thread_resolution_request(
            provider="azure_devops",
            pull_request_id=7,
            thread_id=9,
        )

    assert request.repository == "configured-repo"


@patch("agentic_devtools.cli.pull_request_threads.get_azure_devops_context_from_git_remote", return_value=None)
@patch("agentic_devtools.cli.pull_request_threads.get_value")
def test_uses_explicit_azure_devops_state_without_remote_context(mock_get_value, _mock_remote_context) -> None:
    mock_get_value.side_effect = lambda key: {
        "platform.code_hosting": "azure_devops",
        "organization": "https://dev.azure.com/org",
        "project": "project",
        "repository": "repo",
        "thread_id": 99,
    }.get(key)

    request = build_thread_resolution_request(pull_request_id=7)

    assert request.azure_devops_organization == "https://dev.azure.com/org"
    assert request.azure_devops_project == "project"
    assert request.repository == "repo"


@pytest.mark.parametrize(
    ("missing_key", "expected"),
    [
        ("organization", "https://dev.azure.com/remote-org"),
        ("project", "remote-project"),
        ("repository", "remote-repo"),
    ],
)
@patch(
    "agentic_devtools.cli.pull_request_threads.get_azure_devops_context_from_git_remote",
    return_value=("https://dev.azure.com/remote-org", "remote-project", "remote-repo"),
)
@patch("agentic_devtools.cli.pull_request_threads.get_value")
def test_partial_azure_devops_state_uses_remote_fallback(
    mock_get_value, _mock_remote_context, missing_key, expected
) -> None:
    """A partially configured Azure DevOps state fills only its missing coordinate."""
    values = {
        "platform.code_hosting": "azure_devops",
        "organization": "https://dev.azure.com/state-org",
        "project": "state-project",
        "repository": "state-repo",
        "thread_id": 99,
    }
    values[missing_key] = None
    mock_get_value.side_effect = values.get

    request = build_thread_resolution_request(pull_request_id=7)

    actual = {
        "organization": request.azure_devops_organization,
        "project": request.azure_devops_project,
        "repository": request.repository,
    }
    assert actual[missing_key] == expected


@patch("agentic_devtools.cli.pull_request_threads.get_azure_devops_context_from_git_remote", return_value=None)
@patch("agentic_devtools.cli.pull_request_threads.get_value")
def test_rejects_missing_azure_devops_context_without_placeholder_defaults(
    mock_get_value, _mock_remote_context
) -> None:
    mock_get_value.side_effect = lambda key: {
        "platform.code_hosting": "azure_devops",
        "thread_id": 99,
    }.get(key)

    with pytest.raises(ValueError, match="Azure DevOps organization, project, and repository are required"):
        build_thread_resolution_request(pull_request_id=7)


def test_rejects_missing_repository() -> None:
    with pytest.raises(ValueError, match="repository is required"):
        build_thread_resolution_request(
            provider="github",
            pull_request_id=7,
            thread_node_id="PRRT_node",
        )


def test_rejects_non_string_thread_node_id() -> None:
    with pytest.raises(ValueError, match="thread_node_id must be a string"):
        build_thread_resolution_request(
            provider="github",
            repository="owner/repo",
            pull_request_id=7,
            thread_node_id=12,  # type: ignore[arg-type]
        )


def test_rejects_missing_azure_thread_id() -> None:
    with pytest.raises(ValueError, match="thread_id is required"):
        build_thread_resolution_request(
            provider="azure_devops",
            repository="repo",
            pull_request_id=7,
        )


@patch("agentic_devtools.cli.pull_request_threads.get_azure_devops_context_from_git_remote", return_value=None)
@patch("agentic_devtools.cli.pull_request_threads.get_value")
def test_rejects_attacker_controlled_organization_url(mock_get_value, _mock_remote_context) -> None:
    mock_get_value.side_effect = lambda key: {
        "platform.code_hosting": "azure_devops",
        "organization": "https://evil.example.com/steal-creds",
        "project": "project",
        "repository": "repo",
        "thread_id": 99,
    }.get(key)

    with pytest.raises(ValueError, match="organization must be"):
        build_thread_resolution_request(pull_request_id=7)


@patch("agentic_devtools.cli.pull_request_threads.get_azure_devops_context_from_git_remote", return_value=None)
@patch("agentic_devtools.cli.pull_request_threads.get_value")
def test_accepts_legacy_visualstudio_organization_url(mock_get_value, _mock_remote_context) -> None:
    mock_get_value.side_effect = lambda key: {
        "platform.code_hosting": "azure_devops",
        "organization": "https://myorg.visualstudio.com",
        "project": "project",
        "repository": "repo",
        "thread_id": 99,
    }.get(key)

    request = build_thread_resolution_request(pull_request_id=7)

    assert request.azure_devops_organization == "https://myorg.visualstudio.com"


@patch("agentic_devtools.cli.pull_request_threads.get_azure_devops_context_from_git_remote", return_value=None)
@patch("agentic_devtools.cli.pull_request_threads.get_value")
def test_accepts_canonical_dev_azure_com_organization_url(mock_get_value, _mock_remote_context) -> None:
    mock_get_value.side_effect = lambda key: {
        "platform.code_hosting": "azure_devops",
        "organization": "https://dev.azure.com/myorg",
        "project": "project",
        "repository": "repo",
        "thread_id": 99,
    }.get(key)

    request = build_thread_resolution_request(pull_request_id=7)

    assert request.azure_devops_organization == "https://dev.azure.com/myorg"


@patch("agentic_devtools.cli.pull_request_threads.get_azure_devops_context_from_git_remote", return_value=None)
@patch("agentic_devtools.cli.pull_request_threads.get_value")
def test_normalizes_plain_organization_name_to_https_url(mock_get_value, _mock_remote_context) -> None:
    mock_get_value.side_effect = lambda key: {
        "platform.code_hosting": "azure_devops",
        "organization": "myorg",
        "project": "project",
        "repository": "repo",
        "thread_id": 99,
    }.get(key)

    request = build_thread_resolution_request(pull_request_id=7)

    assert request.azure_devops_organization == "https://dev.azure.com/myorg"


@patch("agentic_devtools.cli.pull_request_threads.get_azure_devops_context_from_git_remote", return_value=None)
@patch("agentic_devtools.cli.pull_request_threads.get_value")
def test_rejects_invalid_plain_organization_name(mock_get_value, _mock_remote_context) -> None:
    mock_get_value.side_effect = lambda key: {
        "platform.code_hosting": "azure_devops",
        "organization": "my org/path",
        "project": "project",
        "repository": "repo",
        "thread_id": 99,
    }.get(key)

    with pytest.raises(ValueError, match="organization must be"):
        build_thread_resolution_request(pull_request_id=7)


@patch("agentic_devtools.cli.pull_request_threads.get_value")
def test_rejects_non_boolean_dry_run_override(mock_get_value) -> None:
    mock_get_value.side_effect = lambda key: {
        "platform.code_hosting": "github",
        "github.repo": "owner/repo",
        "pull_request_id": 1,
        "github.thread_node_id": "PRRT_opaque",
    }.get(key)

    with pytest.raises(ValueError, match="boolean"):
        build_thread_resolution_request(dry_run="false")  # type: ignore[arg-type]
