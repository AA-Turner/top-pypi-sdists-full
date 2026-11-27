from __future__ import annotations

import asyncio
import base64
import json
import time
from collections.abc import AsyncIterator, Awaitable, Callable
from contextlib import asynccontextmanager
from typing import Any, NamedTuple
from unittest.mock import AsyncMock, patch

import pytest
from pydantic import BaseModel, Field
from pydantic_core import to_json
from temporalio.client import WorkflowFailureError, WorkflowHandle
from temporalio.converter import DataConverter
from temporalio.testing import WorkflowEnvironment

from mistralai.workflows import activity, workflow
from mistralai.workflows.core._registration.execution_registration_interceptor import (
    ExecutionRegistrationInterceptor,
)
from mistralai.workflows.core._registration.registration_activity import (
    _register_execution,
)
from mistralai.workflows.core.definition.workflow_definition import (
    get_workflow_definition,
    is_workflow_on_behalf_of,
    set_workflow_definition,
)
from mistralai.workflows.core.temporal.context_handler_interceptor import ContextHandlerInterceptor
from mistralai.workflows.core.temporal.payload_converter import MistralWorkflowsPayloadConverter
from mistralai.workflows.exceptions import WorkflowsException
from mistralai.workflows.models import PayloadWithContext, WorkflowContext
from mistralai.workflows.worker_client.models import ExecutorIdentityTokenResponse, RegisterExecutionResponse
from mistralai.workflows.worker_client.sdk import PrivateWorkerClient

from .fixtures_continue_as_new import (
    REREG_NON_OBO_CAN,
    REREG_NON_OBO_TO_OBO,
    REREG_OBO_CAN,
    REREG_OBO_TO_NON_OBO,
    IterationInput,
    JWTPropagationContinueAsNewWorkflow,
    ReregNonOBOContinueAsNewWorkflow,
    ReregNonOBOToOBOWorkflow,
    ReregOBOContinueAsNewWorkflow,
    ReregOBOToNonOBOWorkflow,
    api_call_with_credentials,
    set_obo_flag,
)
from .utils import create_test_worker


class PageParams(BaseModel):
    offset: int = Field(default=0)
    limit: int = Field(default=100)
    total_processed: int = Field(default=0)


class ProcessingResult(BaseModel):
    total_processed: int
    status: str = Field(default="completed")


@activity()
async def fetch_items(offset: int, limit: int) -> list[str]:
    if offset >= 500:
        return []
    items = [f"item_{i}" for i in range(offset, min(offset + limit, 500))]
    return items


@activity()
async def process_items(items: list[str]) -> int:
    return len(items)


@workflow.define(name="test-continue-as-new-basic")
class BasicContinueAsNewWorkflow:
    @workflow.entrypoint
    async def run(self, params: PageParams) -> ProcessingResult:
        items = await fetch_items(params.offset, params.limit)
        if not items:
            return ProcessingResult(total_processed=params.total_processed)
        processed_count = await process_items(items)
        next_params = PageParams(
            offset=params.offset + params.limit,
            limit=params.limit,
            total_processed=params.total_processed + processed_count,
        )
        workflow.continue_as_new(next_params)


@workflow.define(name="test-continue-as-new-small-batches")
class SmallBatchContinueAsNewWorkflow:
    @workflow.entrypoint
    async def run(self, params: PageParams) -> ProcessingResult:
        items = await fetch_items(params.offset, params.limit)
        if not items:
            return ProcessingResult(total_processed=params.total_processed)
        processed_count = await process_items(items)
        next_params = PageParams(
            offset=params.offset + params.limit,
            limit=params.limit,
            total_processed=params.total_processed + processed_count,
        )
        workflow.continue_as_new(next_params)


class TestContinueAsNew:
    @pytest.mark.asyncio
    async def test_completes_with_no_items(self, temporal_env: Any) -> None:
        async with create_test_worker(
            temporal_env,
            workflows=[BasicContinueAsNewWorkflow],
            activities=[fetch_items, process_items],
        ):
            workflow_def = get_workflow_definition(BasicContinueAsNewWorkflow)
            assert workflow_def is not None
            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                PageParams(offset=500, limit=100, total_processed=0).model_dump(),
                id="test-continue-as-new-no-items",
                task_queue="test-task-queue",
            )
            result = await handle.result()
            assert isinstance(result, dict)
            assert result["total_processed"] == 0
            assert result["status"] == "completed"

    @pytest.mark.asyncio
    async def test_processes_multiple_pages(self, temporal_env: Any) -> None:
        async with create_test_worker(
            temporal_env,
            workflows=[SmallBatchContinueAsNewWorkflow],
            activities=[fetch_items, process_items],
        ):
            workflow_def = get_workflow_definition(SmallBatchContinueAsNewWorkflow)
            assert workflow_def is not None
            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                PageParams(offset=0, limit=50, total_processed=0).model_dump(),
                id="test-continue-as-new-multiple-pages",
                task_queue="test-task-queue",
            )
            result = await handle.result()
            assert isinstance(result, dict)
            assert result["total_processed"] == 500
            assert result["status"] == "completed"

    @pytest.mark.asyncio
    async def test_accumulates_state(self, temporal_env: Any) -> None:
        async with create_test_worker(
            temporal_env,
            workflows=[BasicContinueAsNewWorkflow],
            activities=[fetch_items, process_items],
        ):
            workflow_def = get_workflow_definition(BasicContinueAsNewWorkflow)
            assert workflow_def is not None
            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                PageParams(offset=200, limit=100, total_processed=200).model_dump(),
                id="test-continue-as-new-state",
                task_queue="test-task-queue",
            )
            result = await handle.result()
            assert isinstance(result, dict)
            assert result["total_processed"] == 500
            assert result["status"] == "completed"


def _make_jwt(exp: float) -> str:
    header = base64.urlsafe_b64encode(json.dumps({"alg": "HS256"}).encode()).rstrip(b"=").decode()
    payload = base64.urlsafe_b64encode(json.dumps({"exp": exp}).encode()).rstrip(b"=").decode()
    return f"{header}.{payload}.signature"


class _ReregistrationHarness(NamedTuple):
    start: Callable[[str], Awaitable[WorkflowHandle[Any, Any]]]
    assert_ran_as: Callable[[WorkflowHandle[Any, Any], bool], Awaitable[None]]


@asynccontextmanager
async def _reregistration_worker(
    workflow_cls: type, workflow_name: str, *, server_returns_flag: bool, continues_as_new: bool = False
) -> AsyncIterator[_ReregistrationHarness]:
    """Registrations answer like abraxas, keeping an execution on the declaration it first registered with;
    with server_returns_flag=False, like a server predating the flag."""
    declared = get_workflow_definition(workflow_cls).on_behalf_of
    minted: list[str] = []
    started_with: dict[str, bool] = {}

    def mock_mint(**kwargs: Any) -> ExecutorIdentityTokenResponse:
        minted.append(kwargs.get("execution_token", ""))
        return ExecutorIdentityTokenResponse(token=_make_jwt(time.time() + 3600))

    async def mock_register(**kwargs: Any) -> RegisterExecutionResponse:
        if not server_returns_flag:
            return RegisterExecutionResponse(execution_id="test-obo-reg", created=True)
        flag = started_with.setdefault(
            kwargs["temporal_workflow_id"], is_workflow_on_behalf_of(kwargs["workflow_name"])
        )
        return RegisterExecutionResponse(execution_id="test-obo-reg", created=True, on_behalf_of=flag)

    mock_worker_client = AsyncMock(spec=PrivateWorkerClient)
    mock_worker_client.register_execution_async = AsyncMock(side_effect=mock_register)
    mock_worker_client.__aenter__ = AsyncMock(return_value=mock_worker_client)
    payload = to_json(IterationInput(iteration=0).model_dump()) if continues_as_new else b"null"

    try:
        async with await WorkflowEnvironment.start_time_skipping(
            data_converter=DataConverter(payload_converter_class=MistralWorkflowsPayloadConverter),
        ) as env:
            with (
                patch.object(PrivateWorkerClient, "executor_identity_token_async", side_effect=mock_mint),
                patch(
                    "mistralai.workflows.core._registration.registration_activity.get_worker_client",
                    return_value=mock_worker_client,
                ),
            ):
                async with create_test_worker(
                    env,
                    workflows=[workflow_cls],
                    activities=[set_obo_flag, api_call_with_credentials, _register_execution],
                    interceptors=[ContextHandlerInterceptor(), ExecutionRegistrationInterceptor()],
                ):

                    async def start(label: str) -> WorkflowHandle[Any, Any]:
                        minted.clear()
                        context = WorkflowContext(
                            namespace="test-ns",
                            execution_id=f"test-obo-{workflow_name}",
                            execution_token=f"token-{label}",
                        )
                        return await env.client.start_workflow(
                            get_workflow_definition(workflow_cls).name,
                            PayloadWithContext(payload=payload, empty=not continues_as_new, context=context),
                            id=f"test-rereg-{workflow_name}-{label}",
                            task_queue="test-task-queue",
                        )

                    async def assert_ran_as(handle: WorkflowHandle[Any, Any], on_behalf_of: bool) -> None:
                        # Only the executor identity can call the API in this setup.
                        if on_behalf_of:
                            await handle.result()
                            assert minted
                        else:
                            with pytest.raises(WorkflowFailureError):
                                await handle.result()
                            assert not minted

                    yield _ReregistrationHarness(start, assert_ran_as)
    finally:
        set_workflow_definition(
            workflow_cls, get_workflow_definition(workflow_cls).model_copy(update={"on_behalf_of": declared})
        )


class TestContinueAsNewContextPropagation:
    @pytest.mark.asyncio
    async def test_jwt_minting_works_after_continue_as_new(self) -> None:
        mint_calls: list[dict] = []

        def mock_mint(**kwargs: Any) -> ExecutorIdentityTokenResponse:
            mint_calls.append({"execution_token": kwargs.get("execution_token", "")})
            return ExecutorIdentityTokenResponse(token=_make_jwt(time.time() + 3600))

        mock_worker_client = AsyncMock(spec=PrivateWorkerClient)
        mock_worker_client.register_execution_async = AsyncMock(
            return_value=RegisterExecutionResponse(execution_id="test-can-jwt", created=True)
        )
        mock_worker_client.__aenter__ = AsyncMock(return_value=mock_worker_client)

        interceptors = [ContextHandlerInterceptor(), ExecutionRegistrationInterceptor()]
        data_converter = DataConverter(payload_converter_class=MistralWorkflowsPayloadConverter)

        async with await WorkflowEnvironment.start_time_skipping(
            data_converter=data_converter,
        ) as env:
            with (
                patch.object(
                    PrivateWorkerClient,
                    "executor_identity_token_async",
                    side_effect=mock_mint,
                ),
                patch(
                    "mistralai.workflows.core._registration.registration_activity.get_worker_client",
                    return_value=mock_worker_client,
                ),
            ):
                async with create_test_worker(
                    env,
                    workflows=[JWTPropagationContinueAsNewWorkflow],
                    activities=[api_call_with_credentials, _register_execution],
                    interceptors=interceptors,
                ):
                    wf = get_workflow_definition(JWTPropagationContinueAsNewWorkflow)
                    assert wf is not None

                    context = WorkflowContext(
                        namespace="test-ns",
                        execution_id="test-can-jwt",
                        execution_token="test-token-abc",
                    )
                    initial_arg = PayloadWithContext(
                        payload=to_json(IterationInput(iteration=0).model_dump()),
                        context=context,
                    )

                    handle = await env.client.start_workflow(
                        wf.name,
                        initial_arg,
                        id="test-can-jwt-propagation",
                        task_queue="test-task-queue",
                    )
                    await handle.result()

        # First run reuses the incoming token; continued run gets a new one.
        # Both runs must complete (proving each had a valid token for the hook).
        assert len(mint_calls) >= 1
        assert mint_calls[0]["execution_token"] == "test-token-abc"

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "workflow_cls, workflow_name, initial_obo",
        [
            pytest.param(ReregOBOToNonOBOWorkflow, REREG_OBO_TO_NON_OBO, True, id="obo"),
            pytest.param(ReregNonOBOToOBOWorkflow, REREG_NON_OBO_TO_OBO, False, id="non-obo"),
        ],
    )
    async def test_obo_reregistration_applies_from_next_execution(
        self, workflow_cls: type, workflow_name: str, initial_obo: bool
    ) -> None:
        """Re-registering a workflow's OBO flag mid-run must not change that run's context; the next execution
        follows the flipped declaration."""
        async with _reregistration_worker(workflow_cls, workflow_name, server_returns_flag=True) as harness:
            await harness.assert_ran_as(await harness.start("exec-1"), initial_obo)
            await harness.assert_ran_as(await harness.start("exec-2"), not initial_obo)

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "workflow_cls, workflow_name, initial_obo",
        [
            pytest.param(ReregOBOContinueAsNewWorkflow, REREG_OBO_CAN, True, id="obo"),
            pytest.param(ReregNonOBOContinueAsNewWorkflow, REREG_NON_OBO_CAN, False, id="non-obo"),
        ],
    )
    @pytest.mark.parametrize("server_returns_flag", [True, False], ids=["server-returns-flag", "older-server"])
    async def test_continue_as_new_keeps_the_flag_its_execution_started_with(
        self, workflow_cls: type, workflow_name: str, initial_obo: bool, server_returns_flag: bool
    ) -> None:
        """The flag is flipped before continuing as new, and only the continued run calls the API. An older server
        reports no flag, so the continued run then follows the flipped declaration."""
        async with _reregistration_worker(
            workflow_cls, workflow_name, server_returns_flag=server_returns_flag, continues_as_new=True
        ) as harness:
            await harness.assert_ran_as(
                await harness.start("exec-1"), initial_obo if server_returns_flag else not initial_obo
            )


class HandlerCounter(BaseModel):
    count: int = 0
    continued: bool = False


@activity()
async def slow_increment(value: int) -> int:
    await asyncio.sleep(0.5)
    return value + 1


@workflow.define(name="test-continue-as-new-waits-for-handlers")
class WaitForHandlersContinueAsNewWorkflow:
    def __init__(self) -> None:
        self.count = 0
        self.handler_started = False

    @workflow.signal(name="increment")
    async def increment(self) -> None:
        self.handler_started = True
        self.count = await slow_increment(self.count)

    @workflow.entrypoint
    async def run(self, state: HandlerCounter) -> HandlerCounter:
        if state.continued:
            return state
        await workflow.wait_condition(lambda: self.handler_started)
        await workflow.wait_for_handlers()
        workflow.continue_as_new(HandlerCounter(count=state.count + self.count, continued=True))


class TestWaitForHandlers:
    @pytest.mark.asyncio
    async def test_continue_as_new_keeps_work_of_running_handlers(self, temporal_env: Any) -> None:
        async with create_test_worker(
            temporal_env,
            workflows=[WaitForHandlersContinueAsNewWorkflow],
            activities=[slow_increment],
        ):
            workflow_def = get_workflow_definition(WaitForHandlersContinueAsNewWorkflow)
            assert workflow_def is not None
            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                HandlerCounter().model_dump(),
                id="test-continue-as-new-waits-for-handlers",
                task_queue="test-task-queue",
            )
            await handle.signal("increment")

            result = await handle.result()

            assert result == {"count": 1, "continued": True}

    @pytest.mark.asyncio
    async def test_raises_outside_workflow(self) -> None:
        with pytest.raises(WorkflowsException):
            await workflow.wait_for_handlers()
