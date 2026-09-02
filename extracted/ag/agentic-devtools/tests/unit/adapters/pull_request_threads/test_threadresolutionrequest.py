from typing import Any

import pytest

from agentic_devtools.adapters.pull_request_threads import ThreadResolutionRequest


def test_github_numeric_thread_id_is_preserved_as_comment_id() -> None:
    request = ThreadResolutionRequest(
        provider="github",
        repository="owner/repo",
        pull_request_id=12,
        thread_id=34,
    )

    assert request.github_comment_id == 34
    assert request.github_thread_node_id is None


def test_bool_thread_id_is_rejected() -> None:
    with pytest.raises(ValueError, match="boolean"):
        ThreadResolutionRequest(
            provider="github",
            repository="owner/repo",
            pull_request_id=12,
            thread_id=True,
        )


def test_github_node_id_must_be_opaque() -> None:
    with pytest.raises(ValueError, match="opaque"):
        ThreadResolutionRequest(
            provider="github",
            repository="owner/repo",
            pull_request_id=12,
            github_thread_node_id="34",
        )


def test_github_opaque_thread_id_is_preserved() -> None:
    request = ThreadResolutionRequest(
        provider="github",
        repository="owner/repo",
        pull_request_id=12,
        thread_id="PRRT_opaque",
    )

    assert request.github_thread_node_id == "PRRT_opaque"


def test_azure_requires_numeric_thread_id() -> None:
    with pytest.raises(ValueError, match="positive integer"):
        ThreadResolutionRequest(
            provider="azure_devops",
            repository="repo",
            pull_request_id=12,
            thread_id="PRRT_opaque",
        )


def test_azure_digit_string_thread_id_is_normalized_to_int() -> None:
    request = ThreadResolutionRequest(
        provider="azure_devops",
        repository="repo",
        pull_request_id=12,
        thread_id="34",
    )

    assert request.azure_devops_thread_id == 34


def test_thread_id_can_be_combined_with_azure_context_fields() -> None:
    request = ThreadResolutionRequest(
        provider="azure_devops",
        repository="repo",
        pull_request_id=12,
        thread_id=7,
        azure_devops_organization="myorg",
        azure_devops_project="myproject",
    )

    assert request.azure_devops_thread_id == 7
    assert request.azure_devops_organization == "myorg"
    assert request.azure_devops_project == "myproject"


@pytest.mark.parametrize(
    ("kwargs", "message"),
    [
        ({"provider": "github", "repository": "owner", "pull_request_id": 1, "thread_id": 1}, "owner/repo"),
        ({"provider": "github", "repository": "owner/repo name", "pull_request_id": 1, "thread_id": 1}, "owner/repo"),
        ({"provider": "github", "repository": "owner/repo", "pull_request_id": True, "thread_id": 1}, "positive"),
        (
            {
                "provider": "github",
                "repository": "owner/repo",
                "pull_request_id": 1,
                "thread_id": 1,
                "github_thread_node_id": "PRRT_node",
            },
            "combined",
        ),
        (
            {
                "provider": "github",
                "repository": "owner/repo",
                "pull_request_id": 1,
                "thread_id": 1,
                "github_comment_id": 2,
            },
            "combined",
        ),
        (
            {
                "provider": "azure_devops",
                "repository": "repo",
                "pull_request_id": 1,
                "azure_devops_thread_id": 1,
                "github_comment_id": 2,
            },
            "GitHub identifiers",
        ),
        (
            {
                "provider": "github",
                "repository": "owner/repo",
                "pull_request_id": 1,
                "azure_devops_thread_id": 1,
                "github_thread_node_id": "PRRT_node",
            },
            "Azure DevOps identifiers",
        ),
        (
            {
                "provider": "github",
                "repository": "owner/repo",
                "pull_request_id": 1,
                "github_comment_id": True,
            },
            "positive integer",
        ),
    ],
)
def test_rejects_provider_and_identifier_mismatches(kwargs: dict[str, Any], message: str) -> None:
    with pytest.raises(ValueError, match=message):
        ThreadResolutionRequest(**kwargs)


def test_request_snapshot_is_credential_free() -> None:
    request = ThreadResolutionRequest(
        provider="github",
        repository="owner/repo",
        pull_request_id=1,
        github_thread_node_id="PRRT_node",
    )

    assert request.as_dict()["github_thread_node_id"] == "PRRT_node"


@pytest.mark.parametrize(
    ("kwargs", "message"),
    [
        ({"provider": "jira", "repository": "repo", "pull_request_id": 1, "thread_id": 1}, "provider"),
        ({"provider": "github", "repository": "", "pull_request_id": 1, "thread_id": 1}, "repository"),
        ({"provider": "github", "repository": "owner/repo", "pull_request_id": 0, "thread_id": 1}, "positive"),
        (
            {
                "provider": "github",
                "repository": "owner/repo",
                "pull_request_id": 1,
                "thread_id": 1,
                "discussion_kind": "comment",
            },
            "discussion_kind",
        ),
        (
            {
                "provider": "github",
                "repository": "owner/repo",
                "pull_request_id": 1,
                "thread_id": 1,
                "requested_operation": "close",
            },
            "requested_operation",
        ),
        ({"provider": "github", "repository": "owner/repo", "pull_request_id": 1}, "required"),
        (
            {
                "provider": "github",
                "repository": "owner/repo",
                "pull_request_id": 1,
                "github_thread_node_id": "PRRT_node",
                "github_comment_id": 2,
            },
            "either",
        ),
        (
            {
                "provider": "github",
                "repository": "owner/repo",
                "pull_request_id": 1,
                "thread_id": 1,
                "dry_run": "false",
            },
            "boolean",
        ),
    ],
)
def test_rejects_invalid_request_values(kwargs: dict[str, Any], message: str) -> None:
    with pytest.raises(ValueError, match=message):
        ThreadResolutionRequest(**kwargs)
