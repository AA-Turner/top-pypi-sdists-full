from __future__ import annotations

import pytest

from agentic_devtools.adapters.pull_request_approval import PullRequestApprovalRequest


def test_accepts_a_well_formed_github_request() -> None:
    request = PullRequestApprovalRequest("github", "owner/repo", 1, "LGTM", "a" * 40)
    assert request.provider == "github"
    assert request.repository == "owner/repo"
    assert request.expected_head == "a" * 40


def test_accepts_a_well_formed_azure_devops_request() -> None:
    request = PullRequestApprovalRequest(
        "azure_devops",
        " repo ",
        1,
        "LGTM",
        organization=" https://dev.azure.com/example ",
        project=" project ",
    )
    assert request.repository == "repo"
    assert request.organization == "https://dev.azure.com/example"
    assert request.project == "project"


def test_rejects_invalid_provider() -> None:
    with pytest.raises(ValueError, match="provider must be"):
        PullRequestApprovalRequest("bitbucket", "owner/repo", 1, "LGTM")  # type: ignore[arg-type]


def test_rejects_blank_repository() -> None:
    with pytest.raises(ValueError, match="repository is required"):
        PullRequestApprovalRequest("github", "   ", 1, "LGTM")


def test_rejects_github_repository_without_owner_form() -> None:
    with pytest.raises(ValueError, match="owner/repo form"):
        PullRequestApprovalRequest("github", "repo-without-owner", 1, "LGTM", "a" * 40)


def test_rejects_github_repository_with_whitespace_in_a_part() -> None:
    with pytest.raises(ValueError, match="owner/repo form"):
        PullRequestApprovalRequest("github", "owner/re po", 1, "LGTM", "a" * 40)


def test_rejects_non_positive_pull_request_id() -> None:
    with pytest.raises(ValueError, match="positive integer"):
        PullRequestApprovalRequest("github", "owner/repo", 0, "LGTM", "a" * 40)


def test_rejects_boolean_pull_request_id() -> None:
    with pytest.raises(ValueError, match="positive integer"):
        PullRequestApprovalRequest("github", "owner/repo", True, "LGTM", "a" * 40)


def test_rejects_blank_content() -> None:
    with pytest.raises(ValueError, match="content is required"):
        PullRequestApprovalRequest("github", "owner/repo", 1, "   ", "a" * 40)


def test_rejects_github_request_missing_expected_head() -> None:
    with pytest.raises(ValueError, match="40-character lowercase hexadecimal SHA"):
        PullRequestApprovalRequest("github", "owner/repo", 1, "LGTM")


def test_rejects_github_request_with_malformed_expected_head() -> None:
    with pytest.raises(ValueError, match="40-character lowercase hexadecimal SHA"):
        PullRequestApprovalRequest("github", "owner/repo", 1, "LGTM", "not-a-sha")


def test_rejects_azure_expected_head_even_when_well_formed() -> None:
    with pytest.raises(ValueError, match="expected_head is not supported for provider 'azure_devops'"):
        PullRequestApprovalRequest("azure_devops", "repo", 1, "LGTM", "a" * 40)


def test_rejects_blank_organization() -> None:
    with pytest.raises(ValueError, match="organization must be a non-empty string or None"):
        PullRequestApprovalRequest("azure_devops", "repo", 1, "LGTM", organization="   ")


def test_rejects_blank_project() -> None:
    with pytest.raises(ValueError, match="project must be a non-empty string or None"):
        PullRequestApprovalRequest("azure_devops", "repo", 1, "LGTM", project="   ")


def test_rejects_non_boolean_dry_run() -> None:
    with pytest.raises(ValueError, match="dry_run must be a boolean"):
        PullRequestApprovalRequest("github", "owner/repo", 1, "LGTM", "a" * 40, dry_run="yes")  # type: ignore[arg-type]
