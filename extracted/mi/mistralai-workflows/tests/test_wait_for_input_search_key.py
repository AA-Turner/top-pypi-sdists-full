"""Tests for the internal.execution.state search key set/cleared by wait_for_input."""

from __future__ import annotations

import asyncio
import json
from collections.abc import AsyncGenerator, Generator
from contextlib import asynccontextmanager, contextmanager
from typing import Any
from unittest.mock import AsyncMock, patch

import pytest
import temporalio.exceptions
from temporalio.client import WorkflowFailureError
from temporalio.converter import DataConverter
from temporalio.testing import WorkflowEnvironment

from mistralai.workflows.core._registration.execution_registration_interceptor import (
    ExecutionRegistrationInterceptor,
)
from mistralai.workflows.core._registration.registration_activity import _register_execution
from mistralai.workflows.core._registration.search_key_ingestion import _upsert_search_keys
from mistralai.workflows.core.temporal.context_handler_interceptor import ContextHandlerInterceptor
from mistralai.workflows.core.temporal.payload_converter import MistralWorkflowsPayloadConverter
from mistralai.workflows.models import PayloadWithContext, WorkflowContext
from mistralai.workflows.worker_client.models import (
    RegisterExecutionResponse,
    UpsertExecutionMetadataResponse,
)
from mistralai.workflows.worker_client.sdk import PrivateWorkerClient

from .fixtures_interactive_workflow import (  # noqa: F401
    ParallelApprovalWorkflow,
    SimpleApprovalWorkflow,
    TimeoutTestWorkflow,
    mock_should_publish_event,
)
from .utils import create_test_worker

_REGISTER_PATCH = "mistralai.workflows.core._registration.registration_activity.get_worker_client"
_INGEST_PATCH = "mistralai.workflows.core._registration.search_key_ingestion.get_worker_client"
_WAITING_KEY = "internal.execution.state"
_WAITING = "waiting_for_input"
_RUNNING = "running"


class _UpsertTracker:
    def __init__(self, fail_on_clear: bool = False, fail_first_waiting: bool = False) -> None:
        self.upsert_calls: list[dict[str, Any]] = []
        self._fail_on_clear = fail_on_clear
        self._fail_first_waiting = fail_first_waiting
        self._waiting_failed = False
        register_client = AsyncMock(spec=PrivateWorkerClient)
        register_client.register_execution_async = AsyncMock(
            return_value=RegisterExecutionResponse(execution_id="wf", created=True)
        )
        register_client.aclose = AsyncMock()
        self._upsert_client = AsyncMock(spec=PrivateWorkerClient)
        self._upsert_client.upsert_execution_metadata_async = AsyncMock(side_effect=self._capture_upsert)
        self._upsert_client.__aenter__ = AsyncMock(return_value=self._upsert_client)
        self._upsert_client.__aexit__ = AsyncMock(return_value=None)
        self._upsert_client.aclose = AsyncMock()
        self._patches = (
            patch(_REGISTER_PATCH, return_value=register_client),
            patch(_INGEST_PATCH, return_value=self._upsert_client),
        )

    async def _capture_upsert(self, **kwargs: Any) -> UpsertExecutionMetadataResponse:
        self.upsert_calls.append(kwargs)
        value = kwargs.get("search_key_metadata", {}).get(_WAITING_KEY)
        if self._fail_on_clear and value == _RUNNING:
            raise TypeError("upsert blew up")
        if self._fail_first_waiting and value == _WAITING and not self._waiting_failed:
            self._waiting_failed = True
            raise TypeError("upsert blew up on first waiting set")
        return UpsertExecutionMetadataResponse()

    @property
    def state_values(self) -> list[str]:
        return [
            call["search_key_metadata"][_WAITING_KEY]
            for call in self.upsert_calls
            if _WAITING_KEY in call.get("search_key_metadata", {})
        ]

    @contextmanager
    def activate(self) -> Generator[None, None, None]:
        for p in self._patches:
            p.start()
        try:
            yield
        finally:
            for p in self._patches:
                p.stop()


@asynccontextmanager
async def _env_with_converter() -> AsyncGenerator[WorkflowEnvironment, None]:
    data_converter = DataConverter(payload_converter_class=MistralWorkflowsPayloadConverter)
    async with await WorkflowEnvironment.start_time_skipping(data_converter=data_converter) as env:
        yield env


def _initial_arg(input_args: dict[str, Any] | None = None) -> PayloadWithContext:
    return PayloadWithContext(
        payload=json.dumps(input_args or {}).encode(),
        empty=not input_args,
        context=WorkflowContext(namespace="test-ns", execution_id="placeholder", execution_token=None),
    )


def _unwrap(result: Any) -> Any:
    return result.payload if isinstance(result, PayloadWithContext) else result


async def _await_pending_input(handle: Any, *, timeout: float = 10.0) -> dict[str, Any]:
    deadline = asyncio.get_event_loop().time() + timeout
    while asyncio.get_event_loop().time() < deadline:
        try:
            result = _unwrap(await handle.query("__get_pending_inputs"))
            pending = result["pending_inputs"] if isinstance(result, dict) else []
            if pending:
                return pending[0]
        except Exception:
            pass
        await asyncio.sleep(0.05)
    raise TimeoutError("pending input never appeared")


async def _await_pending_inputs(handle: Any, count: int, *, timeout: float = 10.0) -> list[dict[str, Any]]:
    deadline = asyncio.get_event_loop().time() + timeout
    while asyncio.get_event_loop().time() < deadline:
        try:
            result = _unwrap(await handle.query("__get_pending_inputs"))
            pending = result["pending_inputs"] if isinstance(result, dict) else []
            if len(pending) >= count:
                return [_unwrap(p) for p in pending]
        except Exception:
            pass
        await asyncio.sleep(0.05)
    raise TimeoutError(f"{count} pending inputs never appeared")


@pytest.mark.usefixtures("mock_should_publish_event")
class TestWaitForInputSearchKeyState:
    @pytest.mark.asyncio
    async def test_sets_waiting_then_clears_on_input(self) -> None:
        tracker = _UpsertTracker()

        async with _env_with_converter() as env:
            with tracker.activate():
                async with create_test_worker(
                    env,
                    workflows=[SimpleApprovalWorkflow],
                    activities=[_register_execution, _upsert_search_keys],
                    interceptors=[ContextHandlerInterceptor(), ExecutionRegistrationInterceptor()],
                ):
                    handle = await env.client.start_workflow(
                        "simple_approval_workflow",
                        _initial_arg({"request_id": "req-1", "description": "test"}),
                        id="wf-wfi-state",
                        task_queue="test-task-queue",
                    )

                    await _await_pending_input(handle)
                    assert tracker.state_values == [_WAITING]

                    pending = _unwrap(await handle.query("__get_pending_inputs"))["pending_inputs"][0]
                    task_id = _unwrap(pending)["task_id"]
                    await handle.execute_update(
                        "__submit_input",
                        {"task_id": task_id, "input": {"approved": True, "reason": "LGTM"}},
                    )
                    await handle.result()

        assert tracker.state_values == [_WAITING, _RUNNING]

    @pytest.mark.asyncio
    async def test_key_stays_set_while_concurrent_input_remains_pending(self) -> None:
        tracker = _UpsertTracker()

        async with _env_with_converter() as env:
            with tracker.activate():
                async with create_test_worker(
                    env,
                    workflows=[ParallelApprovalWorkflow],
                    activities=[_register_execution, _upsert_search_keys],
                    interceptors=[ContextHandlerInterceptor(), ExecutionRegistrationInterceptor()],
                ):
                    handle = await env.client.start_workflow(
                        "parallel_approval_workflow",
                        _initial_arg({"request_id": "req-parallel"}),
                        id="wf-wfi-state-parallel",
                        task_queue="test-task-queue",
                    )

                    pending = await _await_pending_inputs(handle, count=2)
                    assert tracker.state_values == [_WAITING, _WAITING]

                    first, second = pending
                    await handle.execute_update(
                        "__submit_input",
                        {"task_id": first["task_id"], "input": {"approved": True, "reason": "LGTM"}},
                    )

                    await _await_pending_inputs(handle, count=1)
                    assert _RUNNING not in tracker.state_values[2:]

                    await handle.execute_update(
                        "__submit_input",
                        {"task_id": second["task_id"], "input": {"approved": False, "reason": "nope"}},
                    )
                    await handle.result()

        assert tracker.state_values[-1] == _RUNNING
        assert tracker.state_values[:2] == [_WAITING, _WAITING]

    @pytest.mark.asyncio
    async def test_failing_clear_does_not_mask_the_wait_timeout(self) -> None:
        tracker = _UpsertTracker(fail_on_clear=True)

        async with _env_with_converter() as env:
            with tracker.activate():
                async with create_test_worker(
                    env,
                    workflows=[TimeoutTestWorkflow],
                    activities=[_register_execution, _upsert_search_keys],
                    interceptors=[ContextHandlerInterceptor(), ExecutionRegistrationInterceptor()],
                ):
                    handle = await env.client.start_workflow(
                        "simple_approval_workflow_with_timeout",
                        _initial_arg(),
                        id="wf-wfi-state-clear-fails",
                        task_queue="test-task-queue",
                    )

                    with pytest.raises(WorkflowFailureError) as exc_info:
                        await handle.result()

        assert "TimeoutError" in str(exc_info.value.cause)

    @pytest.mark.asyncio
    async def test_failing_set_does_not_fail_the_wait(self) -> None:
        tracker = _UpsertTracker(fail_first_waiting=True)

        async with _env_with_converter() as env:
            with tracker.activate():
                async with create_test_worker(
                    env,
                    workflows=[SimpleApprovalWorkflow],
                    activities=[_register_execution, _upsert_search_keys],
                    interceptors=[ContextHandlerInterceptor(), ExecutionRegistrationInterceptor()],
                ):
                    handle = await env.client.start_workflow(
                        "simple_approval_workflow",
                        _initial_arg({"request_id": "req-set-fails"}),
                        id="wf-wfi-state-set-fails",
                        task_queue="test-task-queue",
                    )

                    pending = await _await_pending_input(handle)
                    await handle.execute_update(
                        "__submit_input",
                        {"task_id": _unwrap(pending)["task_id"], "input": {"approved": True, "reason": "LGTM"}},
                    )
                    result = _unwrap(await handle.result())

        assert result["status"] == "approved"
        assert tracker.state_values[-1] == _RUNNING

    @pytest.mark.asyncio
    async def test_cancelling_a_waiting_execution_cancels_the_workflow(self) -> None:
        tracker = _UpsertTracker()

        async with _env_with_converter() as env:
            with tracker.activate():
                async with create_test_worker(
                    env,
                    workflows=[SimpleApprovalWorkflow],
                    activities=[_register_execution, _upsert_search_keys],
                    interceptors=[ContextHandlerInterceptor(), ExecutionRegistrationInterceptor()],
                ):
                    handle = await env.client.start_workflow(
                        "simple_approval_workflow",
                        _initial_arg({"request_id": "req-cancelled"}),
                        id="wf-wfi-state-cancelled",
                        task_queue="test-task-queue",
                    )

                    await _await_pending_input(handle)
                    await handle.cancel()

                    with pytest.raises(WorkflowFailureError) as exc_info:
                        await handle.result()

        assert isinstance(exc_info.value.cause, temporalio.exceptions.CancelledError)
