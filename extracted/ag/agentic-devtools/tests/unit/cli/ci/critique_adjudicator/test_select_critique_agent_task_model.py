"""Tests for select_critique_agent_task_model."""

import json
from types import SimpleNamespace
from unittest.mock import patch

import pytest

from agentic_devtools.cli.ci.critique_adjudicator import select_critique_agent_task_model
from agentic_devtools.cli.ci.github_provider import GitHubActionsProvider
from agentic_devtools.cli.ci.provider import RepairDispatchNotAttemptedError


def test_critique_task_uses_fixed_model() -> None:
    assert select_critique_agent_task_model("critique prompt", "custom-model") == "gpt-6-luna"


def test_other_agent_task_uses_configured_model() -> None:
    assert select_critique_agent_task_model(None, "  custom-model  ") == "custom-model"


def test_other_agent_task_defaults_when_model_is_blank() -> None:
    assert select_critique_agent_task_model(None, "  ") == "gpt-6-luna"


def test_agent_task_critique_prompt_is_preserved_exactly(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("AGDT_USE_AGENT_TASKS_API", "1")
    monkeypatch.setenv("DEFAULT_CLASSIC_REPO_WORKFLOW_PAT", "test-token")
    prompt = "@copilot please address the following critique of this pr:\n\nA concern remains."
    provider = GitHubActionsProvider(repo="owner/repo")

    with (
        patch.object(
            provider, "get_pr_metadata", return_value=SimpleNamespace(base_branch="main", head_branch="feature")
        ),
        patch("agentic_devtools.cli.ci.github_provider._build_repair_comment") as build_comment,
        patch(
            "agentic_devtools.cli.ci.github_provider._gh_api",
            return_value=json.dumps({"id": 77, "html_url": "https://example.test/task/77"}),
        ) as api,
        patch("agentic_devtools.cli.ci.pipeline.summary._find_active_summary_comment", return_value=None),
        patch.object(provider, "get_pr_token_login", return_value=""),
    ):
        result = provider.dispatch_repair(
            pr_number=42,
            head_sha="head-sha",
            repair_type="review",
            failed_checks=[],
            review_comments=[],
            review_id=100,
            agent_task_prompt=prompt,
        )

    assert result == "task:owner/repo:77"
    task_prompt = api.call_args.kwargs["body"]["prompt"]
    assert task_prompt == prompt
    assert api.call_args.kwargs["body"]["model"] == "gpt-6-luna"
    build_comment.assert_not_called()


def test_agent_task_critique_prompt_does_not_fall_back_when_api_is_disabled(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("AGDT_USE_AGENT_TASKS_API", raising=False)
    monkeypatch.setenv("DEFAULT_CLASSIC_REPO_WORKFLOW_PAT", "test-token")
    provider = GitHubActionsProvider(repo="owner/repo")

    with (
        patch("agentic_devtools.cli.ci.github_provider._gh_api") as api,
        patch.object(provider, "_post_repair_comment") as post_comment,
        pytest.raises(RepairDispatchNotAttemptedError, match="requires the Agent Tasks API"),
    ):
        provider.dispatch_repair(
            pr_number=42,
            head_sha="head-sha",
            repair_type="review",
            failed_checks=[],
            review_comments=[],
            review_id=100,
            agent_task_prompt="@copilot please address the following critique of this pr:\n\nA concern remains.",
        )

    api.assert_not_called()
    post_comment.assert_not_called()
