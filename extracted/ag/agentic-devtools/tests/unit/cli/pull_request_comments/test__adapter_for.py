"""Tests for provider-neutral pull-request comment command."""

from __future__ import annotations

import pytest

from agentic_devtools.adapters.pull_request_comments import PullRequestCommentRequest
from agentic_devtools.cli import pull_request_comments as commands


def test_adapter_selection(monkeypatch: pytest.MonkeyPatch) -> None:
    request = PullRequestCommentRequest("github", "owner/repo", 7, "comment")
    github = commands._adapter_for(request)
    assert github.capability.provider == "github"

    monkeypatch.setattr(commands, "get_pat", lambda: "pat")
    ado = commands._adapter_for(PullRequestCommentRequest("azure_devops", "repo", 7, "comment"))
    assert ado.capability.provider == "azure_devops"


def test_adapter_uses_snapshotted_ado_target(monkeypatch: pytest.MonkeyPatch) -> None:
    from agentic_devtools.adapters.pull_request_comments import AzureDevOpsPullRequestCommentAdapter

    monkeypatch.setattr(commands, "get_pat", lambda: "pat")
    request = PullRequestCommentRequest(
        "azure_devops", "repo", 7, "comment", organization="https://dev.azure.com/snap", project="snapproj"
    )
    adapter = commands._adapter_for(request)
    assert isinstance(adapter, AzureDevOpsPullRequestCommentAdapter)
    assert adapter._config.organization == "https://dev.azure.com/snap"
    assert adapter._config.project == "snapproj"
