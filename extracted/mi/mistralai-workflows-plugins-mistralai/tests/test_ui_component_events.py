from typing import Any

import pytest
from temporalio.testing import WorkflowEnvironment

from mistralai.workflows.core._events.event_context import EventContext
from mistralai.workflows.core.activity import activity
from mistralai.workflows.core.workflow import workflow
from mistralai.workflows.plugins.mistralai import (
    ResourceOutput,
    TextOutput,
    UIComponentResource,
    send_assistant_message,
)
from mistralai.workflows.plugins.mistralai.conversational_ui_components import LLM_UI_VERSION, Markdown
from mistralai.workflows.testing import (
    compare_itemwise,
    create_capturing_mock_events_client,
    create_test_worker_with_events,
    custom_task_completed,
    custom_task_started,
)


@activity(name="ui_component_activity")
async def ui_component_activity() -> dict[str, Any]:
    await send_assistant_message(
        [
            TextOutput(text="Report:"),
            ResourceOutput(resource=UIComponentResource(component=Markdown(content="**Score:** 0.82"))),
        ]
    )
    return {"sent": True}


@workflow.define(name="ui_component_workflow")
class UIComponentWorkflow:
    @workflow.entrypoint
    async def run(self) -> dict[str, Any]:
        return await ui_component_activity()


@pytest.mark.asyncio
async def test_ui_component_emits_events(temporal_env: WorkflowEnvironment) -> None:
    captured_events: list[Any] = []
    mock_client = create_capturing_mock_events_client(captured_events)

    expected_state = {
        "contentChunks": [
            {"type": "text", "text": "Report:"},
            {
                "type": "resource",
                "resource": {
                    "mimeType": "application/vnd.mistral.ui-component",
                    "component": {"name": "Markdown", "props": {"content": "**Score:** 0.82"}},
                    "version": LLM_UI_VERSION,
                    "display": "block",
                },
            },
        ]
    }

    async with EventContext(mock_client):
        async with create_test_worker_with_events(
            temporal_env,
            workflows=[UIComponentWorkflow],
            activities=[ui_component_activity],
        ):
            handle = await temporal_env.client.start_workflow(
                "ui_component_workflow",
                id="test-ui-component",
                task_queue="test-task-queue",
            )
            result = await handle.result()
            assert result["result"]["sent"] is True

            custom_task_events = [e for e in captured_events if e.event_type.value.startswith("CUSTOM_TASK_")]

            expected_events = [
                custom_task_started("assistant_message", expected_state, workflow_name="ui_component_workflow"),
                custom_task_completed("assistant_message", expected_state, workflow_name="ui_component_workflow"),
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
