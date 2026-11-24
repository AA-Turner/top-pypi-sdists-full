"""A name or role in a task id field is the model's mistake to correct, never a database crash.

Regression (2026-11-19, voice agent): task create with assignee_id='staff' reached INSERT INTO projects.tasks,
Postgres raised "invalid input syntax for type uuid", and the call came back as an execution failure filed as a
platform system_error. The tool now refuses it before any database work, naming the field.
"""

from __future__ import annotations

import asyncio

import pytest

from matrx_ai.tools.implementations.tasks import task_create, task_update
from matrx_ai.tools.models import ToolContext

_ID = "8d1f7a52-0c3e-4b9a-9f61-2a7c4e8b1d03"


def _ctx() -> ToolContext:
    return ToolContext(call_id="call_test", tool_name="task")


@pytest.mark.parametrize("field", ["assignee_id", "project_id", "parent_task_id"])
def test_create_refuses_a_name_in_an_id_field(field: str) -> None:
    result = asyncio.run(task_create.__wrapped__({"title": "Pick up dry cleaning", field: "staff"}, _ctx()))
    assert not result.success
    assert result.error.refusal is True
    assert result.error.error_type == "validation"
    assert field in result.error.message and "staff" in result.error.message


def test_update_refuses_a_name_in_an_id_field() -> None:
    result = asyncio.run(task_update.__wrapped__({"task_id": _ID, "assignee_id": "me"}, _ctx()))
    assert not result.success
    assert result.error.refusal is True
    assert "assignee_id" in result.error.message
