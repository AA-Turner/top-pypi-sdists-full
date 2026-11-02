from __future__ import annotations

from agentic_devtools.adapters.pull_request_approval import PullRequestApprovalRequest
from agentic_devtools.cli import pull_request_approval as commands


def test_approval_lock_path_is_stable_and_target_scoped(monkeypatch, tmp_path) -> None:
    monkeypatch.setattr(commands.Path, "home", lambda: tmp_path)
    request = PullRequestApprovalRequest("github", "owner/repo", 7, "LGTM", "a" * 40)
    same_target = PullRequestApprovalRequest("github", "owner/repo", 7, "Different content", "b" * 40)
    git_suffix_variant = PullRequestApprovalRequest("github", "owner/repo.git", 7, "LGTM", "a" * 40)
    case_variant = PullRequestApprovalRequest("github", "Owner/Repo", 7, "LGTM", "a" * 40)
    other_target = PullRequestApprovalRequest("github", "owner/repo", 8, "LGTM", "a" * 40)
    azure_org = PullRequestApprovalRequest(
        "azure_devops", "repo", 7, "LGTM", organization="https://dev.azure.com/org", project="project"
    )
    azure_org_with_trailing_slash = PullRequestApprovalRequest(
        "azure_devops", "repo", 7, "LGTM", organization="https://dev.azure.com/org/", project="project"
    )
    azure_encoded_name = PullRequestApprovalRequest(
        "azure_devops", "My%20Repo", 7, "LGTM", organization="https://dev.azure.com/org", project="My%20Project"
    )
    azure_decoded_name = PullRequestApprovalRequest(
        "azure_devops", "My Repo", 7, "LGTM", organization="https://dev.azure.com/org", project="My Project"
    )
    azure_case_variant = PullRequestApprovalRequest(
        "azure_devops",
        "my repo",
        7,
        "LGTM",
        organization="https://dev.azure.com/ORG/",
        project="my project",
    )

    lock_path = commands._approval_lock_path(request)

    assert lock_path == commands._approval_lock_path(same_target)
    assert lock_path == commands._approval_lock_path(git_suffix_variant)
    assert lock_path == commands._approval_lock_path(case_variant)
    assert lock_path != commands._approval_lock_path(other_target)
    assert commands._approval_lock_path(azure_org) == commands._approval_lock_path(azure_org_with_trailing_slash)
    assert commands._approval_lock_path(azure_encoded_name) == commands._approval_lock_path(azure_decoded_name)
    assert commands._approval_lock_path(azure_encoded_name) == commands._approval_lock_path(azure_case_variant)
    assert lock_path.parent == tmp_path / ".agdt" / "locks" / "pull-request-approval"
