from typing import Any
from unittest.mock import patch

import pytest

import mistralai.workflows as workflows
from mistralai.workflows import get_workflow_definition
from mistralai.workflows.core._events.event_context import EventContext

from .utils import create_test_worker


@workflows.activity()
async def _simple_activity() -> bool:
    return True


@workflows.activity()
async def _activity_using_event_context() -> bool:
    EventContext.get_singleton()
    return True


@workflows.workflow.define(name="activity-calling-workflow")
class ActivityCallingWorkflow:
    @workflows.workflow.entrypoint
    async def run(self) -> bool:
        return await _simple_activity()


class TestWarnings:
    @pytest.mark.asyncio
    @patch("mistralai.workflows.core._events.event_context.logger")
    async def test_no_warning_out_of_activity_call(self, mock_logger):
        """Make sure we don't emit any warning when calling an activity from outside a workflow"""

        await _simple_activity()
        mock_logger.warning.assert_not_called()

    @pytest.mark.asyncio
    @patch("mistralai.workflows.core._events.event_context.logger")
    async def test_no_warning_when_workflow_calls_activity_without_event_context(
        self, mock_logger: Any, temporal_env: Any
    ) -> None:
        """Make sure we don't emit any warning when a workflow calls an activity on a worker with no EventContext"""

        async with create_test_worker(temporal_env, workflows=[ActivityCallingWorkflow], activities=[_simple_activity]):
            workflow_def = get_workflow_definition(ActivityCallingWorkflow)
            assert workflow_def is not None
            result = await temporal_env.client.execute_workflow(
                workflow_def.name,
                id="test-no-event-context-warning",
                task_queue="test-task-queue",
            )

        assert result == {"result": True}
        mock_logger.warning.assert_not_called()

    @pytest.mark.asyncio
    @patch("mistralai.workflows.core._events.event_context.logger")
    async def test_warning_when_activity_uses_event_context_without_init(self, mock_logger):
        """Verify that a warning is emitted when an activity calls get_singleton()
        outside a Temporal activity and no EventContext has been initialized."""

        await _activity_using_event_context()
        mock_logger.warning.assert_called_once()
