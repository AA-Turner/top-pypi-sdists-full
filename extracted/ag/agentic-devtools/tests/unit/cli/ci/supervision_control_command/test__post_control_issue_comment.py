"""Tests for the _post_control_issue_comment symbol."""

from __future__ import annotations

import os

import pytest

from agentic_devtools.cli.ci.supervision_control_command import _post_control_issue_comment


def test_local_comment_write_keeps_the_configured_pat(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("GITHUB_ACTIONS", raising=False)
    monkeypatch.setenv("GH_TOKEN", "workflow-pat")
    calls: list[tuple[list[str], dict[str, str] | None]] = []

    def run_gh_text(arguments: list[str], *, env: dict[str, str] | None = None) -> str:
        calls.append((arguments, env))
        return ""

    monkeypatch.setattr("agentic_devtools.cli.ci.supervision_control_command._run_gh_text", run_gh_text)

    _post_control_issue_comment("owner/repo", 42, "checkpoint")

    assert calls == [
        (
            [
                "issue",
                "comment",
                "42",
                "--repo",
                "owner/repo",
                "--body",
                "checkpoint\n\n🤖 AI PR Loop ·",
            ],
            None,
        )
    ]
    assert os.environ["GH_TOKEN"] == "workflow-pat"


def test_actions_comment_write_scopes_the_bookkeeping_token_to_gh_child(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("GITHUB_ACTIONS", "true")
    monkeypatch.setenv("GH_TOKEN", "workflow-pat")
    monkeypatch.setenv("AI_PR_LOOP_BOOKKEEPING_TOKEN", "bookkeeping-token")
    identity_calls: list[tuple[list[str], dict[str, str] | None]] = []
    write_calls: list[tuple[list[str], dict[str, str] | None]] = []

    def run_gh(arguments: list[str], *, env: dict[str, str] | None = None) -> dict[str, object]:
        identity_calls.append((arguments, env))
        return {"data": {"viewer": {"login": "github-actions[bot]"}}}

    def run_gh_text(arguments: list[str], *, env: dict[str, str] | None = None) -> str:
        write_calls.append((arguments, env))
        return ""

    monkeypatch.setattr("agentic_devtools.cli.ci.supervision_control_command._run_gh", run_gh)
    monkeypatch.setattr("agentic_devtools.cli.ci.supervision_control_command._run_gh_text", run_gh_text)

    _post_control_issue_comment("owner/repo", 42, "checkpoint")

    assert identity_calls == [
        (
            ["api", "graphql", "-f", "query=query { viewer { login } }"],
            {**os.environ, "GH_TOKEN": "bookkeeping-token"},
        )
    ]
    assert len(write_calls) == 1
    assert write_calls[0][0][-1] == "checkpoint\n\n🤖 AI PR Loop ·"
    assert write_calls[0][1] is not None
    assert write_calls[0][1]["GH_TOKEN"] == "bookkeeping-token"
    assert os.environ["GH_TOKEN"] == "workflow-pat"


def test_actions_comment_write_fails_visibly_without_bookkeeping_token(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("GITHUB_ACTIONS", "true")
    monkeypatch.delenv("AI_PR_LOOP_BOOKKEEPING_TOKEN", raising=False)

    with pytest.raises(RuntimeError, match="AI_PR_LOOP_BOOKKEEPING_TOKEN"):
        _post_control_issue_comment("owner/repo", 42, "checkpoint")
