"""Provider and snapshot fixtures scoped to failed-session action tests."""

from typing import Any
from unittest.mock import MagicMock

from agentic_devtools.cli.ci.pipeline.snapshot_models import PRStateSnapshot


def _snapshot(**overrides) -> PRStateSnapshot:
    values: dict[str, Any] = {
        "pr_number": 12,
        "head_repo_full_name": "org/repo",
        "base_repo_full_name": "org/repo",
        "head_branch": "copilot/feature",
        "files": [],
        "labels": [],
        "title": "[WIP] Resume work",
    }
    values.update(overrides)
    return PRStateSnapshot(**values)


def _provider() -> MagicMock:
    provider = MagicMock()
    provider.get_dispatch_login.return_value = "workflow-bot"
    provider.list_issue_comments.return_value = []
    provider.list_closing_issues.return_value = []
    provider.get_pr_body.return_value = "Original task description"
    provider.get_agent_task_prompt.return_value = ""
    return provider
