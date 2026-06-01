from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, Any, Type

from temporalio.testing import WorkflowEnvironment

from mistralai.workflows.core.activity import get_all_temporal_activities
from mistralai.workflows.core.worker_client import get_worker_client
from mistralai.workflows.models import WorkflowContext
from mistralai.workflows.protocol.v1.events import (
    CustomTaskStarted,
    CustomTaskStartedAttributes,
    WorkflowEvent,
)
from mistralai.workflows.testing import (
    create_capturing_mock_events_client,
    create_test_worker,
    create_test_worker_with_events,
    wait_for_pending_inputs,
)
from mistralai.workflows.worker_client.sdk import PrivateWorkerClient

if TYPE_CHECKING:
    import httpx

__all__ = [
    "create_http_test_worker_client",
    "create_test_workflow_context",
    "create_test_workflow_event",
    "create_test_worker",
    "create_test_worker_with_events",
    "execute_workflow_in_test_env",
    "wait_for_pending_inputs",
    "create_capturing_mock_events_client",
]


def create_http_test_worker_client(transport: httpx.AsyncBaseTransport) -> PrivateWorkerClient:
    client = get_worker_client(base_url="http://localhost", api_key="test-key")
    async_client = client.sdk_configuration.async_client
    assert async_client is not None
    setattr(async_client, "_transport", transport)
    return client


def create_test_workflow_context(execution_token: str) -> WorkflowContext:
    return WorkflowContext(
        namespace="test-namespace",
        execution_id="exec-1",
        execution_token=execution_token,
    )


def create_test_workflow_event(
    *,
    event_id: str = "evt-0",
    workflow_exec_id: str = "exec-1",
    workflow_run_id: str = "run-1",
    parent_workflow_exec_id: str | None = None,
) -> WorkflowEvent:
    return CustomTaskStarted(
        event_id=event_id,
        root_workflow_exec_id=workflow_exec_id,
        parent_workflow_exec_id=parent_workflow_exec_id,
        workflow_exec_id=workflow_exec_id,
        workflow_run_id=workflow_run_id,
        workflow_name="test-workflow",
        attributes=CustomTaskStartedAttributes(custom_task_id="task-1", custom_task_type="test-task"),
    )


async def execute_workflow_in_test_env(
    env: WorkflowEnvironment,
    workflow_class: Type,
    workflow_input: Any,
    workflow_id: str | None = None,
    task_queue: str = "test-task-queue",
) -> Any:
    from mistralai.workflows.core.definition.workflow_definition import get_workflow_definition

    workflow_def: Any = get_workflow_definition(workflow_class)
    if not workflow_def:
        raise ValueError(f"Workflow {workflow_class} is not properly decorated")

    handle = await env.client.start_workflow(
        workflow_def.name,
        workflow_input,
        id=workflow_id or f"test-workflow-{asyncio.current_task().get_name()}",  # type: ignore
        task_queue=task_queue,
    )

    return await handle.result()


def get_temporal_activities_by_names(names: list[str]) -> list:
    """Get temporal activities from the registry by name."""
    all_activities = get_all_temporal_activities()
    return [act for act in all_activities if act.__name__ in names]
