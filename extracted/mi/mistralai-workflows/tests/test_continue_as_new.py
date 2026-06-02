from __future__ import annotations

import base64
import json
import time
from typing import Any
from unittest.mock import AsyncMock, patch

import pytest
from pydantic import BaseModel, Field
from pydantic_core import to_json
from temporalio.client import WorkflowFailureError
from temporalio.converter import DataConverter
from temporalio.testing import WorkflowEnvironment

from mistralai.workflows import activity, workflow
from mistralai.workflows.core._registration.execution_registration_interceptor import (
    ExecutionRegistrationInterceptor,
)
from mistralai.workflows.core._registration.registration_activity import (
    _register_execution,
)
from mistralai.workflows.core.definition.workflow_definition import _on_behalf_of_by_name, get_workflow_definition
from mistralai.workflows.core.temporal.context_handler_interceptor import ContextHandlerInterceptor
from mistralai.workflows.core.temporal.payload_converter import MistralWorkflowsPayloadConverter
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
        "workflow_cls, workflow_name, initial_obo, uses_continue_as_new",
        [
            pytest.param(ReregOBOToNonOBOWorkflow, REREG_OBO_TO_NON_OBO, True, False, id="obo-frozen-single-exec"),
            pytest.param(ReregNonOBOToOBOWorkflow, REREG_NON_OBO_TO_OBO, False, False, id="non-obo-frozen-single-exec"),
            pytest.param(ReregOBOContinueAsNewWorkflow, REREG_OBO_CAN, True, True, id="obo-preserved-continue-as-new"),
            pytest.param(
                ReregNonOBOContinueAsNewWorkflow, REREG_NON_OBO_CAN, False, True, id="non-obo-preserved-continue-as-new"
            ),
        ],
    )
    async def test_obo_flag_frozen_on_reregistration(
        self, workflow_cls: type, workflow_name: str, initial_obo: bool, uses_continue_as_new: bool
    ) -> None:
        """Re-registering a workflow's OBO flag mid-execution must not change
        the in-flight context — whether the flip happens within a single run
        or across a continue-as-new boundary.

        Single-exec variants also verify that a *new* execution sees the
        flipped registry value.
        """
        mint_calls: list[dict] = []

        def mock_mint(**kwargs: Any) -> ExecutorIdentityTokenResponse:
            mint_calls.append({"execution_token": kwargs.get("execution_token", "")})
            return ExecutorIdentityTokenResponse(token=_make_jwt(time.time() + 3600))

        mock_worker_client = AsyncMock(spec=PrivateWorkerClient)
        mock_worker_client.register_execution_async = AsyncMock(
            return_value=RegisterExecutionResponse(execution_id="test-obo-reg", created=True)
        )

        interceptors = [ContextHandlerInterceptor(), ExecutionRegistrationInterceptor()]
        data_converter = DataConverter(payload_converter_class=MistralWorkflowsPayloadConverter)

        def _make_arg(token: str) -> PayloadWithContext:
            if uses_continue_as_new:
                payload = to_json(IterationInput(iteration=0).model_dump())
                empty = False
            else:
                payload = b"null"
                empty = True
            return PayloadWithContext(
                payload=payload,
                empty=empty,
                context=WorkflowContext(
                    namespace="test-ns",
                    execution_id=f"test-obo-{workflow_name}",
                    execution_token=token,
                ),
            )

        try:
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
                        workflows=[workflow_cls],
                        activities=[set_obo_flag, api_call_with_credentials, _register_execution],
                        interceptors=interceptors,
                    ):
                        wf = get_workflow_definition(workflow_cls)

                        # --- Execution 1: activity (or CAN) flips the flag ---
                        handle1 = await env.client.start_workflow(
                            wf.name,
                            _make_arg("token-exec-1"),
                            id=f"test-rereg-{workflow_name}-exec-1",
                            task_queue="test-task-queue",
                        )
                        if initial_obo:
                            await handle1.result()
                            assert len(mint_calls) >= 1
                        else:
                            with pytest.raises(WorkflowFailureError):
                                await handle1.result()
                            assert len(mint_calls) == 0

                        assert _on_behalf_of_by_name[workflow_name] is not initial_obo

                        if not uses_continue_as_new:
                            # --- Execution 2: new run sees the flipped flag ---
                            mint_calls.clear()
                            handle2 = await env.client.start_workflow(
                                wf.name,
                                _make_arg("token-exec-2"),
                                id=f"test-rereg-{workflow_name}-exec-2",
                                task_queue="test-task-queue",
                            )
                            if initial_obo:
                                with pytest.raises(WorkflowFailureError):
                                    await handle2.result()
                                assert len(mint_calls) == 0
                            else:
                                await handle2.result()
                                assert len(mint_calls) >= 1
        finally:
            _on_behalf_of_by_name[workflow_name] = initial_obo
