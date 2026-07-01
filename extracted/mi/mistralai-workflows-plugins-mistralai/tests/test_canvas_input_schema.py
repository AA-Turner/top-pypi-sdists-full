from typing import Any

import pytest
from pydantic import ValidationError
from temporalio.testing import WorkflowEnvironment

from mistralai.workflows import InteractiveWorkflow, workflow
from mistralai.workflows.conversational import (
    CanvasInput,
)
from mistralai.workflows.core._events.event_context import EventContext
from mistralai.workflows.testing import (
    create_capturing_mock_events_client,
    create_test_worker_with_events,
    wait_for_pending_inputs,
)

# --- Schema shape tests ---


def test_canvas_input_schema_without_chat_input() -> None:
    """CanvasInput without prompt produces the expected JSON schema shape."""
    schema = CanvasInput(canvas_uri="file://canvas/draft.md").model_json_schema()

    assert schema["title"] == "Canvas"
    assert schema["type"] == "object"
    assert schema["$metadata"] == {"canvasUri": "file://canvas/draft.md"}
    assert schema["required"] == ["canvas"]
    assert "chatInput" not in schema["properties"]

    # Canvas property (resolved from $defs)
    defs = schema.get("$defs", {})
    canvas_def = defs["CanvasInputData"]
    assert canvas_def["type"] == "object"
    assert canvas_def["properties"]["title"]["type"] == "string"
    assert canvas_def["properties"]["content"]["type"] == "string"
    assert canvas_def["required"] == ["title", "content"]


def test_canvas_input_schema_with_chat_input() -> None:
    """CanvasInput with prompt includes chatInput in the schema."""
    prompt = "Any feedback on the document?"
    schema = CanvasInput(
        canvas_uri="file://canvas/rfc.md",
        prompt=prompt,
    ).model_json_schema()

    assert schema["title"] == "Canvas"
    assert schema["type"] == "object"
    assert schema["$metadata"] == {"canvasUri": "file://canvas/rfc.md"}
    assert schema["required"] == ["canvas"]
    assert "chatInput" in schema["properties"]

    # ChatInput def is present and has the expected shape
    defs = schema.get("$defs", {})
    chat_input_defs = [d for d in defs.values() if d.get("title") == "ChatInput"]
    assert len(chat_input_defs) == 1
    chat_input_def = chat_input_defs[0]
    assert chat_input_def["type"] == "object"
    assert chat_input_def["additionalProperties"] is False
    assert "message" in chat_input_def["properties"]
    # Prompt text must be propagated as description on the message field
    assert chat_input_def["properties"]["message"]["description"] == prompt


def test_canvas_input_schema_metadata_uri_varies() -> None:
    """Different canvas_uri values produce different $metadata."""
    schema1 = CanvasInput(canvas_uri="file://canvas/a.md").model_json_schema()
    schema2 = CanvasInput(canvas_uri="file://canvas/b.md").model_json_schema()

    assert schema1["$metadata"]["canvasUri"] == "file://canvas/a.md"
    assert schema2["$metadata"]["canvasUri"] == "file://canvas/b.md"


# --- Data validation tests ---


def test_canvas_input_validates_canvas_data() -> None:
    """CanvasInput model validates canvas data correctly."""
    Model = CanvasInput(canvas_uri="file://canvas/1.md")
    result = Model.model_validate({"canvas": {"title": "My Doc", "content": "# Hello"}})
    assert result.canvas.title == "My Doc"
    assert result.canvas.content == "# Hello"
    assert result.chatInput is None


def test_canvas_input_validates_with_chat_input() -> None:
    """CanvasInput model validates canvas + chatInput data."""
    Model = CanvasInput(canvas_uri="file://canvas/1.md", prompt="feedback?")
    result = Model.model_validate(
        {
            "canvas": {"title": "My Doc", "content": "# Hello"},
            "chatInput": {"message": [{"type": "text", "text": "Looks good!"}]},
        }
    )
    assert result.canvas.title == "My Doc"
    assert result.chatInput is not None
    assert len(result.chatInput.message) == 1
    assert result.chatInput.message[0].text == "Looks good!"


def test_canvas_input_rejects_missing_canvas() -> None:
    """CanvasInput model rejects data without canvas field."""
    Model = CanvasInput(canvas_uri="file://canvas/1.md")
    with pytest.raises(ValidationError):
        Model.model_validate({})


def test_canvas_input_rejects_incomplete_canvas() -> None:
    """CanvasInput model rejects canvas missing required fields."""
    Model = CanvasInput(canvas_uri="file://canvas/1.md")
    with pytest.raises(ValidationError):
        Model.model_validate({"canvas": {"title": "Only title"}})


def test_canvas_input_accepts_canvas_without_chat_input() -> None:
    """Even with prompt, chatInput is optional in the data."""
    Model = CanvasInput(canvas_uri="file://canvas/1.md", prompt="feedback?")
    result = Model.model_validate({"canvas": {"title": "Doc", "content": "text"}})
    assert result.chatInput is None


# --- Integration tests ---


@workflow.define(name="canvas_input_workflow")
class CanvasInputWorkflow(InteractiveWorkflow):
    @workflow.entrypoint
    async def run(self) -> dict[str, Any]:
        result = await self.wait_for_input(
            CanvasInput(canvas_uri="file://canvas/draft.md"),
            label="Edit Canvas",
        )
        return {"title": result.canvas.title, "content": result.canvas.content}


@workflow.define(name="canvas_input_with_chat_workflow")
class CanvasInputWithChatWorkflow(InteractiveWorkflow):
    @workflow.entrypoint
    async def run(self) -> dict[str, Any]:
        result = await self.wait_for_input(
            CanvasInput(canvas_uri="file://canvas/draft.md", prompt="Any feedback?"),
            label="Review Canvas",
        )
        chat_text = ""
        if result.chatInput:
            chat_text = " ".join(chunk.text for chunk in result.chatInput.message)
        return {
            "title": result.canvas.title,
            "content": result.canvas.content,
            "feedback": chat_text,
        }


def extract_input_schema_from_events(captured_events: list[Any]) -> dict[str, Any] | None:
    for event in captured_events:
        if (
            hasattr(event, "event_type")
            and event.event_type.value == "CUSTOM_TASK_STARTED"
            and hasattr(event, "attributes")
            and event.attributes.custom_task_type == "wait_for_input"
        ):
            return event.attributes.payload.value.get("input_schema")
    return None


@pytest.mark.asyncio
async def test_canvas_input_schema_in_event(temporal_env: WorkflowEnvironment) -> None:
    """CanvasInput schema is correctly emitted in wait_for_input events."""
    captured_events: list[Any] = []
    mock_client = create_capturing_mock_events_client(captured_events)

    async with EventContext(mock_client):
        async with create_test_worker_with_events(
            temporal_env,
            workflows=[CanvasInputWorkflow],
        ):
            handle = await temporal_env.client.start_workflow(
                "canvas_input_workflow",
                id="test-canvas-input-schema",
                task_queue="test-task-queue",
            )

            pending_inputs = await wait_for_pending_inputs(handle, expected_count=1)
            task_id = pending_inputs[0]["task_id"]

            await handle.execute_update(
                "__submit_input",
                {
                    "task_id": task_id,
                    "input": {"canvas": {"title": "Edited", "content": "New content"}},
                },
            )
            result = await handle.result()

    assert result["result"] == {"title": "Edited", "content": "New content"}

    input_schema = extract_input_schema_from_events(captured_events)
    assert input_schema is not None
    assert input_schema["title"] == "Canvas"
    assert input_schema["$metadata"]["canvasUri"] == "file://canvas/draft.md"


@pytest.mark.asyncio
async def test_canvas_input_with_chat_in_event(temporal_env: WorkflowEnvironment) -> None:
    """CanvasInput with prompt correctly handles both canvas and chat data."""
    captured_events: list[Any] = []
    mock_client = create_capturing_mock_events_client(captured_events)

    async with EventContext(mock_client):
        async with create_test_worker_with_events(
            temporal_env,
            workflows=[CanvasInputWithChatWorkflow],
        ):
            handle = await temporal_env.client.start_workflow(
                "canvas_input_with_chat_workflow",
                id="test-canvas-input-with-chat",
                task_queue="test-task-queue",
            )

            pending_inputs = await wait_for_pending_inputs(handle, expected_count=1)
            task_id = pending_inputs[0]["task_id"]

            await handle.execute_update(
                "__submit_input",
                {
                    "task_id": task_id,
                    "input": {
                        "canvas": {"title": "RFC", "content": "# Updated RFC"},
                        "chatInput": {"message": [{"type": "text", "text": "Looks good!"}]},
                    },
                },
            )
            result = await handle.result()

    assert result["result"] == {
        "title": "RFC",
        "content": "# Updated RFC",
        "feedback": "Looks good!",
    }

    input_schema = extract_input_schema_from_events(captured_events)
    assert input_schema is not None
    assert "chatInput" in input_schema["properties"]
