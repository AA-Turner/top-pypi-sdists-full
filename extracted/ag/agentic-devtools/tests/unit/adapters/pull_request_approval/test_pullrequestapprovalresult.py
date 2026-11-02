from __future__ import annotations

from agentic_devtools.adapters.pull_request_approval import (
    PullRequestApprovalRequest,
    PullRequestApprovalResult,
)


def test_result_serializes() -> None:
    result = PullRequestApprovalResult(True, "github", "approved")
    payload = result.as_dict()
    assert payload["success"] is True
    assert payload["repository"] == ""
    assert payload["pull_request_id"] == 0
    assert payload["expected_head"] is None
    assert payload["operation_kind"] is None


def test_for_request_carries_target_identity() -> None:
    """The result must identify which PR/head it describes for concurrent callers."""
    request = PullRequestApprovalRequest("github", "owner/repo", 42, "LGTM", "a" * 40)
    result = PullRequestApprovalResult.for_request(request, True, "approved", verified=True, external_id=7)
    assert result.as_dict() == {
        "success": True,
        "provider": "github",
        "status": "approved",
        "error": "",
        "verified": True,
        "external_id": 7,
        "repository": "owner/repo",
        "pull_request_id": 42,
        "expected_head": "a" * 40,
        "operation_kind": None,
        "organization": None,
        "project": None,
    }


def test_for_request_serializes_operation_kind() -> None:
    """Results expose the operation kind without requiring consumers to infer it from external_id."""
    request = PullRequestApprovalRequest("azure_devops", "repo", 42, "LGTM")
    result = PullRequestApprovalResult.for_request(
        request,
        True,
        "approved",
        operation_kind="narrative_update",
    )

    assert result.as_dict()["operation_kind"] == "narrative_update"


def test_for_request_serializes_azure_namespace() -> None:
    """Azure result identity includes organization and project namespaces."""
    first_request = PullRequestApprovalRequest(
        "azure_devops",
        "repo",
        42,
        "LGTM",
        organization="https://dev.azure.com/org-one",
        project="project",
    )
    second_request = PullRequestApprovalRequest(
        "azure_devops",
        "repo",
        42,
        "LGTM",
        organization="https://dev.azure.com/org-two",
        project="project",
    )

    first_result = PullRequestApprovalResult.for_request(first_request, True, "approved").as_dict()
    second_result = PullRequestApprovalResult.for_request(second_request, True, "approved").as_dict()

    assert first_result["organization"] == "https://dev.azure.com/org-one"
    assert first_result["project"] == "project"
    assert second_result["organization"] == "https://dev.azure.com/org-two"
    assert second_result["project"] == "project"
    assert first_result != second_result
