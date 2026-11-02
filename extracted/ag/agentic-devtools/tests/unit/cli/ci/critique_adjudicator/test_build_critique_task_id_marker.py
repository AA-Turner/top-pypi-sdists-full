"""Tests for building trusted Agent Task ID markers."""

from typing import cast

import pytest

from agentic_devtools.cli.ci.critique_adjudicator import build_critique_task_id_marker


def test_builds_a_safe_task_id_marker() -> None:
    assert build_critique_task_id_marker("task-123_a") == "<!-- ai-pr-loop:critique-task-id task=task-123_a -->"


@pytest.mark.parametrize("task_id", ["", "contains spaces", "task/123", cast(str, None)])
def test_rejects_invalid_task_ids(task_id: str) -> None:
    with pytest.raises(ValueError, match="safe identifier"):
        build_critique_task_id_marker(task_id)
