"""Each workflow follows its own on_behalf_of declaration, never its parent's."""

from datetime import timedelta
from typing import List
from unittest.mock import AsyncMock, patch

import pytest
import temporalio.activity
import temporalio.workflow
from pydantic import BaseModel
from temporalio.common import RetryPolicy
from temporalio.exceptions import ApplicationError
from temporalio.testing import WorkflowEnvironment
from temporalio.worker import Replayer

import mistralai.workflows as workflows
from mistralai.workflows import get_workflow_definition, workflow
from mistralai.workflows.constants import OBO_PARALLEL_EXECUTION_WORKFLOW_NAME, PARALLEL_EXECUTION_WORKFLOW_NAME
from mistralai.workflows.core._registration.execution_registration_interceptor import ExecutionRegistrationInterceptor
from mistralai.workflows.core._registration.registration_activity import _register_execution
from mistralai.workflows.core.definition.workflow_definition import mount_workflow, set_workflow_definition
from mistralai.workflows.core.execution.concurrency._concurrency_workflow import (
    OnBehalfOfParallelExecutionWorkflow,
    ParallelExecutionWorkflow,
)
from mistralai.workflows.core.execution.concurrency.execute_activities_in_parallel import (
    execute_activities_in_parallel,
)
from mistralai.workflows.core.temporal.context_handler_interceptor import ContextHandlerInterceptor, retrieve_context
from mistralai.workflows.core.utils.contextvars import unwrap_contextual_result
from mistralai.workflows.worker_client.models import RegisterExecutionResponse
from mistralai.workflows.worker_client.sdk import PrivateWorkerClient

from .utils import create_test_worker


class IdentityReport(BaseModel):
    marker: str
    workflow_type: str
    on_behalf_of: bool | None


class ChildParams(BaseModel):
    fail_first_attempt: bool = False


class ParentInput(BaseModel):
    child_on_behalf_of: bool
    retried: bool


@workflows.activity()
async def report_identity(marker: str) -> IdentityReport:
    context = retrieve_context()
    assert context is not None
    return IdentityReport(
        marker=marker,
        workflow_type=temporalio.activity.info().workflow_type,
        on_behalf_of=context.on_behalf_of,
    )


async def _report_identity_directly_and_through_fan_out(params: ChildParams) -> List[IdentityReport]:
    if params.fail_first_attempt and temporalio.workflow.info().attempt == 1:
        raise ApplicationError("fail the first attempt so the child is retried")
    direct = await report_identity("direct")
    return [direct, *await execute_activities_in_parallel(activity=report_identity, items=["fanout"])]


@workflow.define(name="test-identity-child-obo", on_behalf_of=True)
class OboChild:
    @workflow.entrypoint
    async def run(self, params: ChildParams) -> List[IdentityReport]:
        return await _report_identity_directly_and_through_fan_out(params)


@workflow.define(name="test-identity-child-plain")
class PlainChild:
    @workflow.entrypoint
    async def run(self, params: ChildParams) -> List[IdentityReport]:
        return await _report_identity_directly_and_through_fan_out(params)


async def _run_child(input: ParentInput) -> List[IdentityReport]:
    child = OboChild if input.child_on_behalf_of else PlainChild
    if not input.retried:
        return await workflow.execute_workflow(child, params=ChildParams())
    # The SDK's execute_workflow exposes no retry policy, so start the retried child through Temporal directly.
    result = await temporalio.workflow.execute_child_workflow(
        get_workflow_definition(child).name,
        ChildParams(fail_first_attempt=True).model_dump(),
        result_type=dict,
        retry_policy=RetryPolicy(maximum_attempts=2, initial_interval=timedelta(milliseconds=1)),
    )
    _, child_result = unwrap_contextual_result(result)
    return child_result["result"]


@workflow.define(name="test-identity-parent-obo", on_behalf_of=True)
class OboParent:
    @workflow.entrypoint
    async def run(self, input: ParentInput) -> List[IdentityReport]:
        return await _run_child(input)


@workflow.define(name="test-identity-parent-plain")
class PlainParent:
    @workflow.entrypoint
    async def run(self, input: ParentInput) -> List[IdentityReport]:
        return await _run_child(input)


_ALL_WORKFLOWS = [
    OboParent,
    PlainParent,
    OboChild,
    PlainChild,
    ParallelExecutionWorkflow,
    OnBehalfOfParallelExecutionWorkflow,
]


class TestChildOnBehalfOfIsOwnDeclaration:
    @pytest.mark.asyncio
    @pytest.mark.timeout(60)
    @pytest.mark.parametrize(
        "parent_on_behalf_of", [True, False], ids=["obo-parent-plain-child", "plain-parent-obo-child"]
    )
    @pytest.mark.parametrize("retried", [False, True], ids=["first-attempt", "retried"])
    async def test_child_follows_own_declaration_not_parent(
        self,
        temporal_env_with_converter: WorkflowEnvironment,
        parent_on_behalf_of: bool,
        retried: bool,
    ) -> None:
        child_on_behalf_of = not parent_on_behalf_of
        parent = OboParent if parent_on_behalf_of else PlainParent
        child = OboChild if child_on_behalf_of else PlainChild
        fanout = OBO_PARALLEL_EXECUTION_WORKFLOW_NAME if child_on_behalf_of else PARALLEL_EXECUTION_WORKFLOW_NAME

        async with create_test_worker(
            temporal_env_with_converter,
            workflows=_ALL_WORKFLOWS,
            activities=[report_identity],
            interceptors=[ContextHandlerInterceptor()],
        ):
            handle = await temporal_env_with_converter.client.start_workflow(
                get_workflow_definition(parent).name,
                ParentInput(child_on_behalf_of=child_on_behalf_of, retried=retried).model_dump(),
                id=f"test-identity-p{int(parent_on_behalf_of)}-r{int(retried)}",
                task_queue="test-task-queue",
            )
            _, result = unwrap_contextual_result(await handle.result())

        child_type = get_workflow_definition(child).name
        expected = [
            IdentityReport(marker="direct", workflow_type=child_type, on_behalf_of=child_on_behalf_of),
            IdentityReport(marker="fanout", workflow_type=fanout, on_behalf_of=child_on_behalf_of),
        ]
        assert result == {"result": [report.model_dump() for report in expected]}


@workflow.define(name="test-obo-parallel-timeout", on_behalf_of=True, execution_timeout=timedelta(hours=4))
class OboParallelTimeoutWorkflow:
    @workflow.entrypoint
    async def run(self) -> List[IdentityReport]:
        return await execute_activities_in_parallel(
            activity=report_identity, items=["fanout"], execution_timeout=timedelta(hours=2)
        )


class TestOnBehalfOfParallelExecutionTimeout:
    @pytest.mark.asyncio
    @pytest.mark.timeout(30)
    async def test_obo_child_uses_requested_timeout(self, temporal_env_with_converter: WorkflowEnvironment) -> None:
        async with create_test_worker(
            temporal_env_with_converter,
            workflows=[OboParallelTimeoutWorkflow, OnBehalfOfParallelExecutionWorkflow],
            activities=[report_identity],
            interceptors=[ContextHandlerInterceptor()],
        ):
            handle = await temporal_env_with_converter.client.start_workflow(
                get_workflow_definition(OboParallelTimeoutWorkflow).name,
                id="test-obo-parallel-timeout",
                task_queue="test-task-queue",
            )
            await handle.result()
            history = await handle.fetch_history()

        child_starts = [
            event.start_child_workflow_execution_initiated_event_attributes
            for event in history.events
            if event.HasField("start_child_workflow_execution_initiated_event_attributes")
        ]
        assert len(child_starts) == 1
        assert child_starts[0].workflow_type.name == OBO_PARALLEL_EXECUTION_WORKFLOW_NAME
        assert child_starts[0].workflow_execution_timeout.ToTimedelta() == timedelta(hours=2)


# enforce_determinism=False keeps the sandbox from re-importing the registry, so the test can flip it.
@workflow.define(name="test-identity-replay-obo", on_behalf_of=True, enforce_determinism=False)
class OboFanOutWorkflow:
    @workflow.entrypoint
    async def run(self) -> List[IdentityReport]:
        return await execute_activities_in_parallel(activity=report_identity, items=["fanout"])


@workflow.define(name="test-identity-replay-plain", enforce_determinism=False)
class PlainFanOutWorkflow:
    @workflow.entrypoint
    async def run(self) -> List[IdentityReport]:
        return await execute_activities_in_parallel(activity=report_identity, items=["fanout"])


class TestOnBehalfOfPinnedForReplay:
    @pytest.mark.asyncio
    @pytest.mark.timeout(60)
    @pytest.mark.parametrize("workflow_cls", [OboFanOutWorkflow, PlainFanOutWorkflow], ids=["obo", "plain"])
    async def test_replay_keeps_declaration_the_run_started_with(
        self, temporal_env_with_converter: WorkflowEnvironment, workflow_cls: type
    ) -> None:
        name = get_workflow_definition(workflow_cls).name
        definition = get_workflow_definition(workflow_cls)
        declared = definition.on_behalf_of
        interceptors = [ContextHandlerInterceptor(), ExecutionRegistrationInterceptor()]
        worker_client = AsyncMock(spec=PrivateWorkerClient)
        worker_client.register_execution_async = AsyncMock(
            return_value=RegisterExecutionResponse(execution_id=name, created=True)
        )
        worker_client.__aenter__ = AsyncMock(return_value=worker_client)

        with patch(
            "mistralai.workflows.core._registration.registration_activity.get_worker_client",
            return_value=worker_client,
        ):
            async with create_test_worker(
                temporal_env_with_converter,
                workflows=[workflow_cls, ParallelExecutionWorkflow, OnBehalfOfParallelExecutionWorkflow],
                activities=[report_identity, _register_execution],
                interceptors=interceptors,
            ):
                handle = await temporal_env_with_converter.client.start_workflow(
                    name, id=f"test-replay-{name}", task_queue="test-task-queue"
                )
                await handle.result()

        history = await handle.fetch_history()
        set_workflow_definition(workflow_cls, definition.model_copy(update={"on_behalf_of": not declared}))
        try:
            with mount_workflow(name, workflow_cls):
                await Replayer(
                    workflows=[workflow_cls],
                    interceptors=interceptors,
                    data_converter=temporal_env_with_converter.client.data_converter,
                ).replay_workflow(history)
        finally:
            set_workflow_definition(workflow_cls, definition)
