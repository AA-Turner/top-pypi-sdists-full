"""Tests for provider-neutral pull-request comment command."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock

import pytest

from agentic_devtools.adapters.pull_request_comments import PullRequestCommentRequest
from agentic_devtools.cli import pull_request_comments as commands
from agentic_devtools.cli.azure_devops.config import AzureDevOpsConfig


def test_build_request_resolves_state_and_flags(monkeypatch: pytest.MonkeyPatch) -> None:
    state = {
        "platform.code_hosting": "github",
        "github.pull_request_number": 7,
        "comment": "from state",
        "path": "src/app.py",
        "line": "3",
        "end_line": 4,
        "leave_thread_active": True,
    }
    monkeypatch.setattr(commands, "get_value", lambda key: state.get(key))
    monkeypatch.setattr(commands, "is_dry_run", lambda: True)
    request = commands._build_request(repository="owner/repo", idempotency_marker="m")
    assert request == PullRequestCommentRequest(
        "github", "owner/repo", 7, "from state", "src/app.py", 3, 4, False, True, "m"
    )

    state["path"] = 42
    with pytest.raises(ValueError, match="path"):
        commands._build_request(repository="owner/repo", pull_request_id=7, content="x")
    state["path"] = None
    state["github.pull_request_number"] = None
    with pytest.raises(ValueError, match="pull_request_id"):
        commands._build_request(repository="owner/repo", content="x")
    state["pull_request_id"] = 7
    state["content"] = ""
    state["comment"] = ""
    with pytest.raises(ValueError, match="content"):
        commands._build_request(repository="owner/repo")
    state["content"] = "x"
    state["comment_marker"] = 42
    with pytest.raises(ValueError, match="idempotency_marker"):
        commands._build_request(repository="owner/repo", pull_request_id=7)


def test_build_request_snapshots_ado_org_and_project(monkeypatch: pytest.MonkeyPatch) -> None:
    state: dict[str, object] = {
        "platform.code_hosting": "azure_devops",
        "pull_request_id": 5,
        "content": "hello",
    }
    monkeypatch.setattr(commands, "get_value", lambda key: state.get(key))
    monkeypatch.setattr(commands, "is_dry_run", lambda: False)
    fake_cfg = MagicMock(spec=AzureDevOpsConfig)
    fake_cfg.organization = "https://dev.azure.com/myorg"
    fake_cfg.project = "myproj"
    monkeypatch.setattr(commands, "AzureDevOpsConfig", MagicMock(from_state=lambda: fake_cfg))
    monkeypatch.setattr(commands, "_resolve_repository", lambda provider, repo, state_lookup=None: "myrepo")
    request = commands._build_request(repository="myrepo")
    assert request.organization == "https://dev.azure.com/myorg"
    assert request.project == "myproj"


def test_build_request_generates_stable_idempotency_marker(monkeypatch: pytest.MonkeyPatch) -> None:
    state = {
        "platform.code_hosting": "github",
        "pull_request_id": 7,
        "content": "comment",
    }
    monkeypatch.setattr(commands, "get_value", lambda key: state.get(key))
    monkeypatch.setattr(commands, "is_dry_run", lambda: False)

    first = commands._build_request(repository="owner/repo")
    second = commands._build_request(repository="owner/repo")

    assert first.idempotency_marker == second.idempotency_marker
    assert first.idempotency_marker is not None


def test_build_request_without_state_defaults_ignores_state_for_provider_and_repository(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    state = {
        "platform.code_hosting": "azure_devops",
        "github.repo": "state/should-not-be-used",
        "pull_request_id": 7,
        "content": "state content",
    }
    monkeypatch.setattr(commands, "get_value", lambda key: state.get(key))
    monkeypatch.setattr(commands, "get_repo_root", lambda: tmp_path)
    monkeypatch.setattr(commands, "load_platform_config", lambda root: {"code_hosting": "github"})
    monkeypatch.setattr(commands, "is_dry_run", lambda: False)
    monkeypatch.setenv("GITHUB_REPOSITORY", "owner/from-env")

    request = commands._build_request(
        pull_request_id=9,
        content="explicit body",
        resolve_after_posting=False,
        dry_run=False,
        use_state_defaults=False,
    )

    assert request.provider == "github"
    assert request.repository == "owner/from-env"
    assert request.pull_request_id == 9
    assert request.content == "explicit body"
