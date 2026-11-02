"""Tests for require_ai_pr_loop_bookkeeping_token()."""

import pytest

from agentic_devtools.cli.ci.credential_roles import require_ai_pr_loop_bookkeeping_token


def test_returns_stripped_bookkeeping_token(monkeypatch) -> None:
    monkeypatch.setenv("AI_PR_LOOP_BOOKKEEPING_TOKEN", "  bot-token  ")

    assert require_ai_pr_loop_bookkeeping_token("post review replies") == "bot-token"


@pytest.mark.parametrize(
    "environment",
    [
        {},
        {"AI_PR_LOOP_BOOKKEEPING_TOKEN": "   "},
        {
            "GH_TOKEN": "human-token",
            "DEFAULT_CLASSIC_REPO_WORKFLOW_PAT": "human-token",
            "COPILOT_GITHUB_TOKEN": "copilot-token",
            "AGDT_PR_APPROVER_PAT": "approver-token",
        },
    ],
)
def test_does_not_fall_back_to_another_credential(monkeypatch, environment: dict[str, str]) -> None:
    for name in (
        "AI_PR_LOOP_BOOKKEEPING_TOKEN",
        "GH_TOKEN",
        "DEFAULT_CLASSIC_REPO_WORKFLOW_PAT",
        "COPILOT_GITHUB_TOKEN",
        "AGDT_PR_APPROVER_PAT",
    ):
        monkeypatch.delenv(name, raising=False)
    for name, value in environment.items():
        monkeypatch.setenv(name, value)

    with pytest.raises(RuntimeError, match="AI_PR_LOOP_BOOKKEEPING_TOKEN"):
        require_ai_pr_loop_bookkeeping_token("post review replies")
