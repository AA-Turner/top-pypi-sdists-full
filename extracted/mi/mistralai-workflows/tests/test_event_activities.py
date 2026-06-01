"""Unit tests for wait_for_input activity return values (WaitForInputResult).

These tests verify that each activity always returns a WaitForInputResult with
task_id set, regardless of whether event publishing succeeds or fails. The
frontend reads task_id from the MarkerRecorded result in workflow history.

Note: create_base_event_fields() requires a live Temporal context, so all tests
that exercise a non-None EventContext mock it out to isolate the activity logic.
The integration-level happy-path (real Temporal activity context) is covered by
test_interactive_workflow_events.py.
"""

from contextlib import contextmanager
from typing import Generator
from unittest.mock import AsyncMock, patch

import pytest

from mistralai.workflows.core._events.event_activities import (
    WaitForInputResult,
    _emit_waiting_for_input_completed,
    _emit_waiting_for_input_failed,
    _emit_waiting_for_input_started,
)
from mistralai.workflows.core._events.event_context import EventContext

TASK_ID = "task-abc-123"
INPUT_SCHEMA = {"type": "object", "properties": {"approved": {"type": "boolean"}}}
LABEL = "Approval"
INPUT_VALUES = {"approved": True, "reason": "Looks good"}
ERROR_MSG = "Validation failed: required field missing"

_BASE_EVENT_FIELDS = {
    "event_id": "evt-1",
    "root_workflow_exec_id": "root-1",
    "parent_workflow_exec_id": None,
    "workflow_exec_id": "wf-1",
    "workflow_run_id": "run-1",
    "workflow_name": "test_workflow",
}


@contextmanager
def _mock_event_context(*, publish_raises: Exception | None = None) -> Generator[AsyncMock, None, None]:
    """Patch EventContext.get_singleton and create_base_event_fields for unit tests."""
    mock_ctx = AsyncMock()
    if publish_raises is not None:
        mock_ctx.publish_event.side_effect = publish_raises

    with (
        patch.object(EventContext, "has_context", return_value=False),
        patch.object(EventContext, "get_singleton", return_value=mock_ctx),
        patch(
            "mistralai.workflows.core._events.event_activities.create_base_event_fields",
            return_value=_BASE_EVENT_FIELDS,
        ),
    ):
        yield mock_ctx


# ---------------------------------------------------------------------------
# _emit_waiting_for_input_started
# ---------------------------------------------------------------------------


class TestEmitWaitingForInputStarted:
    @pytest.mark.asyncio
    async def test_no_context_returns_task_id(self) -> None:
        result = await _emit_waiting_for_input_started(TASK_ID, INPUT_SCHEMA, LABEL)

        assert isinstance(result, WaitForInputResult)
        assert result.task_id == TASK_ID

    @pytest.mark.asyncio
    async def test_publish_success_returns_task_id(self) -> None:
        with _mock_event_context():
            result = await _emit_waiting_for_input_started(TASK_ID, INPUT_SCHEMA, LABEL)

        assert result.task_id == TASK_ID

    @pytest.mark.asyncio
    async def test_publish_failure_returns_task_id(self) -> None:
        with _mock_event_context(publish_raises=RuntimeError("network error")):
            result = await _emit_waiting_for_input_started(TASK_ID, INPUT_SCHEMA, LABEL)

        assert result.task_id == TASK_ID


# ---------------------------------------------------------------------------
# _emit_waiting_for_input_completed
# ---------------------------------------------------------------------------


class TestEmitWaitingForInputCompleted:
    @pytest.mark.asyncio
    async def test_no_context_returns_task_id(self) -> None:
        result = await _emit_waiting_for_input_completed(TASK_ID, INPUT_SCHEMA, LABEL, INPUT_VALUES)

        assert isinstance(result, WaitForInputResult)
        assert result.task_id == TASK_ID

    @pytest.mark.asyncio
    async def test_publish_success_returns_task_id(self) -> None:
        with _mock_event_context():
            result = await _emit_waiting_for_input_completed(TASK_ID, INPUT_SCHEMA, LABEL, INPUT_VALUES)

        assert result.task_id == TASK_ID

    @pytest.mark.asyncio
    async def test_publish_failure_returns_task_id(self) -> None:
        with _mock_event_context(publish_raises=RuntimeError("network error")):
            result = await _emit_waiting_for_input_completed(TASK_ID, INPUT_SCHEMA, LABEL, INPUT_VALUES)

        assert result.task_id == TASK_ID


# ---------------------------------------------------------------------------
# _emit_waiting_for_input_failed
# ---------------------------------------------------------------------------


class TestEmitWaitingForInputFailed:
    @pytest.mark.asyncio
    async def test_no_context_returns_task_id(self) -> None:
        result = await _emit_waiting_for_input_failed(TASK_ID, INPUT_SCHEMA, LABEL, ERROR_MSG)

        assert isinstance(result, WaitForInputResult)
        assert result.task_id == TASK_ID

    @pytest.mark.asyncio
    async def test_publish_success_returns_task_id(self) -> None:
        with _mock_event_context():
            result = await _emit_waiting_for_input_failed(TASK_ID, INPUT_SCHEMA, LABEL, ERROR_MSG)

        assert result.task_id == TASK_ID

    @pytest.mark.asyncio
    async def test_publish_failure_returns_task_id(self) -> None:
        with _mock_event_context(publish_raises=RuntimeError("network error")):
            result = await _emit_waiting_for_input_failed(TASK_ID, INPUT_SCHEMA, LABEL, ERROR_MSG)

        assert result.task_id == TASK_ID
