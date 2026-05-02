from unittest.mock import MagicMock, patch
from uuid import uuid4
from typing import Any

from vellum.workflows.context import ExecutionContext
from vellum.workflows.errors import WorkflowErrorCode
from workflow_server.api.workflow_view import _emit_async_error_events
from workflow_server.core.workflow_executor_context import WorkflowExecutorContext


def _create_test_context(
    workflow_span_id: Any = None,
    execution_context: Any = None,
) -> WorkflowExecutorContext:
    """Helper to create a WorkflowExecutorContext for testing."""
    return WorkflowExecutorContext(
        execution_id=uuid4(),
        files={"__init__.py": "", "workflow.py": ""},
        environment_api_key="test-api-key",
        module="workflow",
        workflow_span_id=workflow_span_id,
        execution_context=execution_context or ExecutionContext(),
    )


def test_emit_async_error_events__happy_path():
    """
    Tests that _emit_async_error_events emits both initiated and rejected events to the Vellum API.
    """
    # GIVEN a workflow context with a workflow_span_id
    workflow_span_id = uuid4()
    context = _create_test_context(workflow_span_id=workflow_span_id)

    # AND a mock vellum client
    mock_events_create = MagicMock()

    # WHEN we call _emit_async_error_events
    with patch.object(context, "vellum_client") as mock_client:
        mock_client.events.create = mock_events_create
        _emit_async_error_events(context, "Test error message")

    # THEN the events.create method should be called once
    mock_events_create.assert_called_once()

    # AND it should be called with a list of two events
    call_args = mock_events_create.call_args
    events = call_args.kwargs["request"]
    assert len(events) == 2

    # AND the first event should be a WorkflowExecutionInitiatedEvent
    initiated_event = events[0]
    assert initiated_event.name == "workflow.execution.initiated"
    assert initiated_event.trace_id == context.trace_id
    assert str(initiated_event.span_id) == str(workflow_span_id)

    # AND the second event should be a WorkflowExecutionRejectedEvent with the error message
    rejected_event = events[1]
    assert rejected_event.name == "workflow.execution.rejected"
    assert rejected_event.trace_id == context.trace_id
    assert str(rejected_event.span_id) == str(workflow_span_id)
    assert rejected_event.body.error.message == "Test error message"
    assert rejected_event.body.error.code == WorkflowErrorCode.INTERNAL_ERROR


def test_emit_async_error_events__logs_exception_on_failure(caplog):
    """
    Tests that _emit_async_error_events logs an exception when the API call fails.
    """
    # GIVEN a workflow context
    context = _create_test_context(workflow_span_id=uuid4())

    # AND a mock vellum client that raises an exception
    mock_events_create = MagicMock(side_effect=Exception("API connection failed"))

    # WHEN we call _emit_async_error_events
    with patch.object(context, "vellum_client") as mock_client:
        mock_client.events.create = mock_events_create
        _emit_async_error_events(context, "Test error message")

    # THEN the function should not raise an exception
    # (implicit - if we get here, no exception was raised)

    # AND the exception should be logged
    assert any("Failed to emit async error events" in record.message for record in caplog.records)
