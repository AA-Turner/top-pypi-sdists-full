from unittest.mock import patch

import pytest
from pydantic import BaseModel

import mistralai.workflows as workflows
from mistralai.workflows.core._events.event_context import EventContext


class EmptyModel(BaseModel): ...


@workflows.activity()
async def _simple_activity() -> bool:
    return True


@workflows.activity()
async def _activity_using_event_context() -> bool:
    EventContext.get_singleton()
    return True


@workflows.workflow.define(name="local-execution-workflow")
class LocalExecWorkflow:
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
    async def test_no_warning_out_of_local_workflow_execution(self, mock_logger):
        """Make sure we don't emit any warning when executing a workflow locally"""

        await workflows.execute_workflow(
            LocalExecWorkflow,
            params=EmptyModel(),
        )
        mock_logger.warning.assert_not_called()

    @pytest.mark.asyncio
    @patch("mistralai.workflows.core._events.event_context.logger")
    async def test_warning_when_activity_uses_event_context_without_init(self, mock_logger):
        """Verify that a warning is emitted when an activity calls get_singleton()
        outside a Temporal activity and no EventContext has been initialized."""

        await _activity_using_event_context()
        mock_logger.warning.assert_called_once()
