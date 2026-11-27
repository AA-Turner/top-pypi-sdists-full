from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from datetime import timedelta
from typing import Any

import pytest
import temporalio.client
import temporalio.workflow
from pydantic import BaseModel
from temporalio.testing import WorkflowEnvironment

import mistralai.workflows as workflows
from mistralai.workflows import workflow
from mistralai.workflows.core.temporal.call_context_client_interceptor import (
    CallContextClientInterceptor,
    sending_call_context,
)
from mistralai.workflows.core.temporal.context_handler_interceptor import ContextHandlerInterceptor
from mistralai.workflows.core.utils.contextvars import unwrap_contextual_result
from mistralai.workflows.testing import create_test_worker

TASK_QUEUE = "test-task-queue"


@asynccontextmanager
async def client_with_worker(
    env: WorkflowEnvironment, workflow_classes: list[type], activities: list[Any] | None = None
) -> AsyncIterator[temporalio.client.Client]:
    async with create_test_worker(
        env,
        workflows=workflow_classes,
        activities=activities or [],
        interceptors=[ContextHandlerInterceptor()],
    ):
        yield temporalio.client.Client(
            env.client.service_client,
            namespace=env.client.namespace,
            data_converter=env.client.data_converter,
            interceptors=[CallContextClientInterceptor()],
        )


async def workflow_result(handle: temporalio.client.WorkflowHandle[Any, Any]) -> Any:
    _, wrapped_result = unwrap_contextual_result(await handle.result())
    return wrapped_result["result"]


def current_call_context() -> dict[str, Any]:
    return dict(workflows.get_call_context())


@workflow.define(name="call-context-handlers")
class CallContextHandlersWorkflow:
    def __init__(self) -> None:
        self.signal_contexts: list[dict[str, Any]] = []
        self.labelled_contexts: list[list[Any]] = []
        self.validator_context: dict[str, Any] | None = None
        self.update_context: dict[str, Any] | None = None

    @workflow.entrypoint
    async def run(self) -> dict[str, Any]:
        await temporalio.workflow.wait_condition(
            lambda: self.update_context is not None and temporalio.workflow.all_handlers_finished()
        )
        return {
            "signal_contexts": self.signal_contexts,
            "labelled_contexts": self.labelled_contexts,
            "validator_context": self.validator_context,
            "update_context": self.update_context,
            "body_context": current_call_context(),
        }

    @workflow.signal(name="record")
    async def record(self) -> None:
        self.signal_contexts.append(current_call_context())

    @workflow.signal(name="record_labelled")
    async def record_labelled(self, label: str) -> None:
        self.labelled_contexts.append([label, current_call_context()])

    @workflow.update(name="finish")
    async def finish(self) -> bool:
        self.update_context = current_call_context()
        return True

    @finish.validator
    def validate_finish(self) -> None:
        self.validator_context = current_call_context()


class StartParams(BaseModel):
    first_run: dict[str, Any] | None = None


class ChildParams(BaseModel):
    pass


@workflow.define(name="call-context-child")
class CallContextChildWorkflow:
    @workflow.entrypoint
    async def run(self, params: ChildParams) -> dict[str, Any]:
        return current_call_context()


@workflow.define(name="call-context-start")
class CallContextStartWorkflow:
    def __init__(self) -> None:
        self.signal_context: dict[str, Any] | None = None

    @workflow.entrypoint
    async def run(self, params: StartParams) -> dict[str, Any]:
        if params.first_run is not None:
            return {**params.first_run, "continued_run": current_call_context()}
        body_at_start = current_call_context()
        child_context = await workflows.execute_workflow(CallContextChildWorkflow, params=ChildParams())
        await temporalio.workflow.wait_condition(lambda: self.signal_context is not None)
        workflow.continue_as_new(
            StartParams(
                first_run={
                    "body_at_start": body_at_start,
                    "child": child_context,
                    "body_at_end": current_call_context(),
                    "signal_without_context": self.signal_context,
                }
            )
        )
        return {}

    @workflow.signal(name="poke")
    async def poke(self) -> None:
        self.signal_context = current_call_context()


class TestCallContext:
    @pytest.mark.asyncio
    async def test_each_handler_call_sees_its_own_call_context(
        self, temporal_env_with_converter: WorkflowEnvironment
    ) -> None:
        async with client_with_worker(temporal_env_with_converter, [CallContextHandlersWorkflow]) as client:
            handle = await client.start_workflow(
                "call-context-handlers",
                id="call-context-handlers",
                task_queue=TASK_QUEUE,
                execution_timeout=timedelta(seconds=30),
            )
            with sending_call_context({"command_id": "cmd-1", "tracing": True}):
                await handle.signal("record")
            with sending_call_context({}):
                await handle.signal("record")
            with sending_call_context({"command_id": "cmd-2"}):
                await handle.signal("record_labelled", {"label": "a"})
            with sending_call_context({"turn_id": "turn-7"}):
                await handle.execute_update("finish")
            result = await workflow_result(handle)

        assert result == {
            "signal_contexts": [{"command_id": "cmd-1", "tracing": True}, {}],
            "labelled_contexts": [["a", {"command_id": "cmd-2"}]],
            "validator_context": {"turn_id": "turn-7"},
            "update_context": {"turn_id": "turn-7"},
            "body_context": {},
        }

    @pytest.mark.asyncio
    async def test_start_call_context_is_scoped_to_the_workflow_body(
        self, temporal_env_with_converter: WorkflowEnvironment
    ) -> None:
        async with client_with_worker(
            temporal_env_with_converter, [CallContextStartWorkflow, CallContextChildWorkflow]
        ) as client:
            with sending_call_context({"session_id": "sess-1"}):
                handle = await client.start_workflow(
                    "call-context-start",
                    {},
                    id="call-context-start",
                    task_queue=TASK_QUEUE,
                    execution_timeout=timedelta(seconds=30),
                )
            await handle.signal("poke")
            result = await workflow_result(handle)

        assert result == {
            "body_at_start": {"session_id": "sess-1"},
            "child": {},
            "body_at_end": {"session_id": "sess-1"},
            "signal_without_context": {},
            "continued_run": {},
        }

    @pytest.mark.asyncio
    async def test_invalid_call_context_header_is_ignored(
        self, temporal_env_with_converter: WorkflowEnvironment
    ) -> None:
        async with client_with_worker(temporal_env_with_converter, [CallContextHandlersWorkflow]) as client:
            handle = await client.start_workflow(
                "call-context-handlers",
                id="call-context-invalid",
                task_queue=TASK_QUEUE,
                execution_timeout=timedelta(seconds=30),
            )
            # Only a client that bypasses the API validation can send this.
            with sending_call_context({"Not-An-Id": "free text here"}):
                await handle.signal("record_labelled", {"label": "a"})
            await handle.execute_update("finish")
            result = await workflow_result(handle)

        assert result["labelled_contexts"] == [["a", {}]]

    def test_get_call_context_is_empty_outside_a_workflow_call(self) -> None:
        assert workflows.get_call_context() == {}
