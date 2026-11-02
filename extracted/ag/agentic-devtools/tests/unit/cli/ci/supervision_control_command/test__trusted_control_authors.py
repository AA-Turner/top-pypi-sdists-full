"""Tests for _trusted_control_authors."""

from unittest.mock import patch

import pytest

from agentic_devtools.cli.ci.supervision_control_command import _trusted_control_authors


def test_includes_verified_bookkeeping_identity_in_actions(monkeypatch) -> None:
    monkeypatch.setenv("GITHUB_ACTIONS", "true")
    monkeypatch.setenv("AI_PR_LOOP_BOOKKEEPING_TOKEN", "bookkeeping-token")

    with (
        patch(
            "agentic_devtools.cli.ci.supervision_control_command._run_gh",
            side_effect=[
                {"login": "pat-owner"},
                {"data": {"viewer": {"login": "github-actions[bot]"}}},
            ],
        ),
        patch(
            "agentic_devtools.cli.ci.supervision_control_command.require_ai_pr_loop_bookkeeping_token",
            return_value="bookkeeping-token",
        ),
    ):
        assert _trusted_control_authors() == {"pat-owner", "github-actions[bot]"}


def test_requires_bookkeeping_token_in_actions(monkeypatch) -> None:
    monkeypatch.setenv("GITHUB_ACTIONS", "true")
    monkeypatch.delenv("AI_PR_LOOP_BOOKKEEPING_TOKEN", raising=False)

    with (
        patch(
            "agentic_devtools.cli.ci.supervision_control_command._run_gh",
            return_value={"login": "pat-owner"},
        ),
        pytest.raises(RuntimeError, match="AI_PR_LOOP_BOOKKEEPING_TOKEN is required"),
    ):
        _trusted_control_authors()


def test_requires_verified_bookkeeping_identity_in_actions(monkeypatch) -> None:
    monkeypatch.setenv("GITHUB_ACTIONS", "true")
    monkeypatch.setenv("AI_PR_LOOP_BOOKKEEPING_TOKEN", "bookkeeping-token")

    with (
        patch(
            "agentic_devtools.cli.ci.supervision_control_command._run_gh",
            side_effect=[
                {"login": "pat-owner"},
                {"data": {"viewer": {"login": ""}}},
            ],
        ),
        patch(
            "agentic_devtools.cli.ci.supervision_control_command.require_ai_pr_loop_bookkeeping_token",
            return_value="bookkeeping-token",
        ),
        pytest.raises(RuntimeError, match="AI_PR_LOOP_BOOKKEEPING_TOKEN identity could not be verified"),
    ):
        _trusted_control_authors()


def test_rejects_non_bot_bookkeeping_identity_in_actions(monkeypatch) -> None:
    monkeypatch.setenv("GITHUB_ACTIONS", "true")
    monkeypatch.setenv("AI_PR_LOOP_BOOKKEEPING_TOKEN", "bookkeeping-token")

    with (
        patch(
            "agentic_devtools.cli.ci.supervision_control_command._run_gh",
            side_effect=[
                {"login": "pat-owner"},
                {"data": {"viewer": {"login": "human-owner"}}},
            ],
        ),
        patch(
            "agentic_devtools.cli.ci.supervision_control_command.require_ai_pr_loop_bookkeeping_token",
            return_value="bookkeeping-token",
        ),
        pytest.raises(RuntimeError, match="github-actions\\[bot\\]"),
    ):
        _trusted_control_authors()


def test_uses_only_default_identity_outside_actions(monkeypatch) -> None:
    monkeypatch.delenv("GITHUB_ACTIONS", raising=False)

    with patch(
        "agentic_devtools.cli.ci.supervision_control_command._run_gh",
        return_value={"login": "Pat-Owner"},
    ):
        assert _trusted_control_authors() == {"pat-owner", "github-actions[bot]"}
