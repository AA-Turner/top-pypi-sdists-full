"""Tests for selecting an actual task activity clock."""

from datetime import UTC, datetime, timedelta

import pytest

from agentic_devtools.cli.ci.agent_task_lifecycle_assessment import _parent_lifecycle_clock
from agentic_devtools.cli.ci.models import AgentTaskLifecycle

NOW = datetime(2026, 10, 16, 10, 0, tzinfo=UTC)


@pytest.mark.parametrize(
    ("started_at", "idle_at", "created_at", "expected"),
    [
        (
            (NOW - timedelta(minutes=2)).isoformat(),
            (NOW - timedelta(minutes=1)).isoformat(),
            NOW.isoformat(),
            NOW - timedelta(minutes=1),
        ),
        ("", "", (NOW - timedelta(minutes=3)).isoformat(), None),
        ("", "", "", None),
    ],
)
def test_parent_lifecycle_clock_uses_only_task_activity(
    started_at: str, idle_at: str, created_at: str, expected: datetime | None
) -> None:
    task = AgentTaskLifecycle(
        task_id="task-1",
        repository="owner/repo",
        pr_number=42,
        head_branch="feature",
        state="running",
        created_at=created_at,
        started_at=started_at,
        idle_at=idle_at,
    )

    assert _parent_lifecycle_clock(task) == expected
