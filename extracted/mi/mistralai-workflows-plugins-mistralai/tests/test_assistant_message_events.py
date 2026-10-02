from typing import Any

import pytest
from temporalio.testing import WorkflowEnvironment

from mistralai.workflows.core._events.event_context import EventContext
from mistralai.workflows.core.activity import activity
from mistralai.workflows.core.workflow import workflow
from mistralai.workflows.plugins.mistralai import (
    CanvasPayload,
    CanvasResource,
    send_assistant_message,
)
from mistralai.workflows.testing import (
    compare_itemwise,
    create_capturing_mock_events_client,
    create_test_worker_with_events,
    custom_task_completed,
    custom_task_started,
)


@activity(name="assistant_message_text_activity")
async def assistant_message_text_activity() -> dict[str, Any]:
    """Activity testing basic text assistant message."""
    await send_assistant_message("Hello, how can I help you today?")
    return {"sent": True}


@activity(name="assistant_message_canvas_activity")
async def assistant_message_canvas_activity() -> dict[str, Any]:
    """Activity testing assistant message with canvas."""
    await send_assistant_message(
        "Here is your document:",
        canvas=CanvasResource(
            canvas=CanvasPayload(
                type="text/markdown",
                title="Test Document",
                content="# Hello World",
            ),
        ),
    )
    return {"sent": True}


@activity(name="assistant_message_multiple_activity")
async def assistant_message_multiple_activity() -> dict[str, Any]:
    """Activity testing multiple sequential assistant messages."""
    await send_assistant_message("First message")
    await send_assistant_message("Second message")
    return {"count": 2}


@workflow.define(name="assistant_message_text_workflow")
class AssistantMessageTextWorkflow:
    @workflow.entrypoint
    async def run(self) -> dict[str, Any]:
        return await assistant_message_text_activity()


@workflow.define(name="assistant_message_canvas_workflow")
class AssistantMessageCanvasWorkflow:
    @workflow.entrypoint
    async def run(self) -> dict[str, Any]:
        return await assistant_message_canvas_activity()


@workflow.define(name="assistant_message_multiple_workflow")
class AssistantMessageMultipleWorkflow:
    @workflow.entrypoint
    async def run(self) -> dict[str, Any]:
        return await assistant_message_multiple_activity()


@pytest.mark.asyncio
async def test_assistant_message_text_emits_events(temporal_env: WorkflowEnvironment) -> None:
    """Test that send_assistant_message with text emits correct custom task events."""
    captured_events: list[Any] = []
    mock_client = create_capturing_mock_events_client(captured_events)

    async with EventContext(mock_client):
        async with create_test_worker_with_events(
            temporal_env,
            workflows=[AssistantMessageTextWorkflow],
            activities=[assistant_message_text_activity],
        ):
            handle = await temporal_env.client.start_workflow(
                "assistant_message_text_workflow",
                id="test-assistant-message-text",
                task_queue="test-task-queue",
            )
            result = await handle.result()

            assert result["result"]["sent"] is True

            custom_task_events = [e for e in captured_events if e.event_type.value.startswith("CUSTOM_TASK_")]

            expected_events = [
                custom_task_started(
                    "assistant_message",
                    {
                        "contentChunks": [
                            {"type": "text", "text": "Hello, how can I help you today?"},
                        ]
                    },
                    workflow_name="assistant_message_text_workflow",
                ),
                custom_task_completed(
                    "assistant_message",
                    {
                        "contentChunks": [
                            {"type": "text", "text": "Hello, how can I help you today?"},
                        ]
                    },
                    workflow_name="assistant_message_text_workflow",
                ),
            ]

            errors = compare_itemwise(
                expected_events,
                custom_task_events,
                exclude_paths={
                    "event_id",
                    "event_timestamp",
                    "root_workflow_exec_id",
                    "parent_workflow_exec_id",
                    "workflow_exec_id",
                    "workflow_run_id",
                    "attributes.task_id",
                    "attributes.custom_task_id",
                    "attributes.input",
                    "attributes.result",
                    "attributes.payload.value",
                },
            )
            assert len(errors) == 0, "Event sequence mismatch:\n" + "\n".join(errors)


@pytest.mark.asyncio
async def test_assistant_message_multiple_emits_events(temporal_env: WorkflowEnvironment) -> None:
    """Test that multiple send_assistant_message calls emit separate events."""
    captured_events: list[Any] = []
    mock_client = create_capturing_mock_events_client(captured_events)

    async with EventContext(mock_client):
        async with create_test_worker_with_events(
            temporal_env,
            workflows=[AssistantMessageMultipleWorkflow],
            activities=[assistant_message_multiple_activity],
        ):
            handle = await temporal_env.client.start_workflow(
                "assistant_message_multiple_workflow",
                id="test-assistant-message-multiple",
                task_queue="test-task-queue",
            )
            result = await handle.result()

            assert result["result"]["count"] == 2

            custom_task_events = [e for e in captured_events if e.event_type.value.startswith("CUSTOM_TASK_")]

            assert len(custom_task_events) == 4

            assert custom_task_events[0].event_type.value == "CUSTOM_TASK_STARTED"
            assert custom_task_events[0].attributes.payload.value["contentChunks"][0]["text"] == "First message"
            assert custom_task_events[1].event_type.value == "CUSTOM_TASK_COMPLETED"

            assert custom_task_events[2].event_type.value == "CUSTOM_TASK_STARTED"
            assert custom_task_events[2].attributes.payload.value["contentChunks"][0]["text"] == "Second message"
            assert custom_task_events[3].event_type.value == "CUSTOM_TASK_COMPLETED"


@pytest.mark.asyncio
async def test_assistant_message_canvas_emits_events(temporal_env: WorkflowEnvironment) -> None:
    """Test that send_assistant_message with canvas emits text and resource chunks."""
    captured_events: list[Any] = []
    mock_client = create_capturing_mock_events_client(captured_events)

    async with EventContext(mock_client):
        async with create_test_worker_with_events(
            temporal_env,
            workflows=[AssistantMessageCanvasWorkflow],
            activities=[assistant_message_canvas_activity],
        ):
            handle = await temporal_env.client.start_workflow(
                "assistant_message_canvas_workflow",
                id="test-assistant-message-canvas",
                task_queue="test-task-queue",
            )
            result = await handle.result()

            assert result["result"]["sent"] is True

            custom_task_events = [e for e in captured_events if e.event_type.value.startswith("CUSTOM_TASK_")]

            assert len(custom_task_events) == 2

            started_event = custom_task_events[0]
            assert started_event.event_type.value == "CUSTOM_TASK_STARTED"

            chunks = started_event.attributes.payload.value["contentChunks"]
            assert len(chunks) == 2

            assert chunks[0] == {"type": "text", "text": "Here is your document:"}
            assert chunks[1]["type"] == "resource"
            assert chunks[1]["resource"]["uri"].startswith("file://canvas/")
            assert chunks[1]["resource"]["mimeType"] == "application/vnd.mistral.canvas"
            assert chunks[1]["resource"]["canvas"]["type"] == "text/markdown"
            assert chunks[1]["resource"]["canvas"]["title"] == "Test Document"
            assert chunks[1]["resource"]["canvas"]["content"] == "# Hello World"

            assert custom_task_events[1].event_type.value == "CUSTOM_TASK_COMPLETED"
