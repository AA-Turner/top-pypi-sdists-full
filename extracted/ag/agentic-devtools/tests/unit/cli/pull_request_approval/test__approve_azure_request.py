from __future__ import annotations

import pytest

from agentic_devtools.adapters.pull_request_approval import PullRequestApprovalRequest
from agentic_devtools.cli import pull_request_approval as commands


def test_uses_snapshotted_azure_values(monkeypatch) -> None:
    captured: dict[str, object] = {}

    class FakeConfig:
        def __init__(self, *, organization, project, repository):
            captured["organization"] = organization
            captured["project"] = project
            captured["repository"] = repository

    monkeypatch.setattr(commands, "AzureDevOpsConfig", FakeConfig)
    monkeypatch.setattr(commands, "approve_azure_pull_request", lambda **kwargs: captured.update(kwargs))

    commands._approve_azure_request(
        PullRequestApprovalRequest(
            "azure_devops",
            "snapshot-repo",
            7,
            "LGTM",
            dry_run=True,
            organization="https://dev.azure.com/example-org",
            project="ExampleProject",
        )
    )

    assert captured["organization"] == "https://dev.azure.com/example-org"
    assert captured["project"] == "ExampleProject"
    assert captured["repository"] == "snapshot-repo"
    assert captured["pull_request_id"] == 7
    assert captured["content"] == "LGTM"
    assert captured["dry_run"] is True
    assert isinstance(captured["config"], FakeConfig)


def test_requires_snapshotted_organization_and_project(monkeypatch) -> None:
    monkeypatch.setattr(commands, "approve_azure_pull_request", lambda **kwargs: None)

    with pytest.raises(ValueError, match="organization and project"):
        commands._approve_azure_request(PullRequestApprovalRequest("azure_devops", "snapshot-repo", 7, "LGTM"))
