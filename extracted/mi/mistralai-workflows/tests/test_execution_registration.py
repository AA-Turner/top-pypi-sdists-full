"""Tests for eager execution registration via workflow interceptor."""

from __future__ import annotations

from contextlib import asynccontextmanager, contextmanager
from typing import Any, AsyncGenerator, Generator
from unittest.mock import AsyncMock, patch

import pytest
from pydantic_core import to_json
from temporalio.client import WorkflowFailureError
from temporalio.converter import DataConverter
from temporalio.testing import WorkflowEnvironment

from mistralai.workflows.core._registration.execution_registration_interceptor import (
    ExecutionRegistrationInterceptor,
    _hash_token,
)
from mistralai.workflows.core._registration.registration_activity import (
    _register_execution,
)
from mistralai.workflows.core.definition.workflow_definition import get_workflow_definition
from mistralai.workflows.core.temporal.context_handler_interceptor import (
    ContextHandlerInterceptor,
)
from mistralai.workflows.core.temporal.payload_converter import (
    MistralWorkflowsPayloadConverter,
)
from mistralai.workflows.models import PayloadWithContext, WorkflowContext
from mistralai.workflows.worker_client.errors.sdkerror import SDKError
from mistralai.workflows.worker_client.models import RegisterExecutionResponse
from mistralai.workflows.worker_client.sdk import PrivateWorkerClient

from . import fixtures_execution_registration as _fixtures
from .fixtures_execution_registration import (
    ChildWorkflow,
    ContinueAsNewWorkflow,
    IterationInput,
    ParentWorkflow,
    SingleActivityWorkflow,
    TwoActivityWorkflow,
    capture_token,
)
from .utils import create_test_worker

_REGISTER_PATCH = "mistralai.workflows.core._registration.registration_activity.get_worker_client"


@pytest.fixture(autouse=True)
def _reset_observed_tokens() -> Generator[None, None, None]:
    _fixtures._observed_tokens.clear()
    yield
    _fixtures._observed_tokens.clear()


class _RegistrationTracker:
    def __init__(self) -> None:
        self.calls: list[dict[str, Any]] = []
        self._mock_client = AsyncMock(spec=PrivateWorkerClient)
        self._mock_client.register_execution_async = AsyncMock(side_effect=self._capture_call)

    async def _capture_call(self, **kwargs: Any) -> RegisterExecutionResponse:
        self.calls.append(kwargs)
        return RegisterExecutionResponse(execution_id=kwargs["temporal_workflow_id"], created=True)

    @contextmanager
    def activate(self) -> Generator[None, None, None]:
        with patch(_REGISTER_PATCH, return_value=self._mock_client):
            yield


def _make_interceptors() -> list:
    return [ContextHandlerInterceptor(), ExecutionRegistrationInterceptor()]


@asynccontextmanager
async def _env_with_converter() -> AsyncGenerator[WorkflowEnvironment, None]:
    data_converter = DataConverter(payload_converter_class=MistralWorkflowsPayloadConverter)
    async with await WorkflowEnvironment.start_time_skipping(
        data_converter=data_converter,
    ) as env:
        yield env


def _make_initial_arg(
    execution_token: str | None = None,
    **extra: Any,
) -> PayloadWithContext:
    return PayloadWithContext(
        payload=b"null",
        empty=True,
        context=WorkflowContext(
            namespace="test-ns",
            execution_id="placeholder",
            execution_token=execution_token,
            **extra,
        ),
    )


def _make_initial_arg_with_payload(
    payload: Any,
    execution_token: str | None = None,
) -> PayloadWithContext:
    return PayloadWithContext(
        payload=to_json(payload),
        context=WorkflowContext(
            namespace="test-ns",
            execution_id="placeholder",
            execution_token=execution_token,
        ),
    )


class TestExecutionRegistration:
    @pytest.mark.asyncio
    async def test_registration_happens_and_hash_matches(self) -> None:
        tracker = _RegistrationTracker()
        async with _env_with_converter() as env:
            with tracker.activate():
                async with create_test_worker(
                    env,
                    workflows=[SingleActivityWorkflow],
                    activities=[capture_token, _register_execution],
                    interceptors=_make_interceptors(),
                ):
                    wf = get_workflow_definition(SingleActivityWorkflow)
                    handle = await env.client.start_workflow(
                        wf.name,
                        _make_initial_arg(),
                        id="test-reg-basic",
                        task_queue="test-task-queue",
                    )
                    await handle.result()

        assert len(tracker.calls) == 1
        call = tracker.calls[0]
        assert call["temporal_workflow_id"] == "test-reg-basic"
        assert call["workflow_name"] == wf.name
        assert call["task_queue"] == "test-task-queue"

        # Activity observed the raw token; registration got its hash
        assert len(_fixtures._observed_tokens) == 1
        raw_token = _fixtures._observed_tokens[0]
        assert raw_token is not None
        assert call["execution_token_hash"] == _hash_token(raw_token)

    @pytest.mark.asyncio
    async def test_incoming_token_is_reused(self) -> None:
        existing_token = "pre-existing-api-token-abc"
        tracker = _RegistrationTracker()
        async with _env_with_converter() as env:
            with tracker.activate():
                async with create_test_worker(
                    env,
                    workflows=[SingleActivityWorkflow],
                    activities=[capture_token, _register_execution],
                    interceptors=_make_interceptors(),
                ):
                    wf = get_workflow_definition(SingleActivityWorkflow)
                    handle = await env.client.start_workflow(
                        wf.name,
                        _make_initial_arg(execution_token=existing_token),
                        id="test-reg-reuse-token",
                        task_queue="test-task-queue",
                    )
                    await handle.result()

        assert _fixtures._observed_tokens == [existing_token]
        assert len(tracker.calls) == 1
        assert tracker.calls[0]["execution_token_hash"] == _hash_token(existing_token)

    @pytest.mark.asyncio
    async def test_same_run_activities_see_token(self) -> None:
        tracker = _RegistrationTracker()
        async with _env_with_converter() as env:
            with tracker.activate():
                async with create_test_worker(
                    env,
                    workflows=[TwoActivityWorkflow],
                    activities=[capture_token, _register_execution],
                    interceptors=_make_interceptors(),
                ):
                    wf = get_workflow_definition(TwoActivityWorkflow)
                    handle = await env.client.start_workflow(
                        wf.name,
                        _make_initial_arg(),
                        id="test-reg-two-activities",
                        task_queue="test-task-queue",
                    )
                    await handle.result()

        assert len(_fixtures._observed_tokens) == 2
        assert _fixtures._observed_tokens[0] is not None
        assert _fixtures._observed_tokens[0] == _fixtures._observed_tokens[1]
        assert len(tracker.calls) == 1

    @pytest.mark.asyncio
    async def test_child_workflow_gets_different_token(self) -> None:
        tracker = _RegistrationTracker()
        async with _env_with_converter() as env:
            with tracker.activate():
                async with create_test_worker(
                    env,
                    workflows=[ParentWorkflow, ChildWorkflow],
                    activities=[capture_token, _register_execution],
                    interceptors=_make_interceptors(),
                ):
                    wf = get_workflow_definition(ParentWorkflow)
                    handle = await env.client.start_workflow(
                        wf.name,
                        _make_initial_arg(),
                        id="test-reg-parent",
                        task_queue="test-task-queue",
                    )
                    await handle.result()

        assert len(_fixtures._observed_tokens) == 2
        parent_token, child_token = _fixtures._observed_tokens
        assert parent_token is not None
        assert child_token is not None
        assert parent_token != child_token
        assert len(tracker.calls) == 2
        hashes = {c["execution_token_hash"] for c in tracker.calls}
        assert len(hashes) == 2

    @pytest.mark.asyncio
    async def test_continue_as_new_gets_new_token(self) -> None:
        tracker = _RegistrationTracker()
        async with _env_with_converter() as env:
            with tracker.activate():
                async with create_test_worker(
                    env,
                    workflows=[ContinueAsNewWorkflow],
                    activities=[capture_token, _register_execution],
                    interceptors=_make_interceptors(),
                ):
                    wf = get_workflow_definition(ContinueAsNewWorkflow)
                    handle = await env.client.start_workflow(
                        wf.name,
                        _make_initial_arg_with_payload(IterationInput(iteration=0).model_dump()),
                        id="test-reg-can",
                        task_queue="test-task-queue",
                    )
                    await handle.result()

        # Two runs: each gets its own token
        assert len(_fixtures._observed_tokens) == 2
        assert _fixtures._observed_tokens[0] != _fixtures._observed_tokens[1]
        assert len(tracker.calls) == 2
        hashes = [c["execution_token_hash"] for c in tracker.calls]
        assert hashes[0] != hashes[1]

    @pytest.mark.asyncio
    async def test_registration_not_found_does_not_fail_workflow(self) -> None:
        tracker = _RegistrationTracker()
        mock_response = AsyncMock()
        mock_response.status_code = 404
        tracker._mock_client.register_execution_async = AsyncMock(side_effect=SDKError("Not Found", mock_response))

        async with _env_with_converter() as env:
            with tracker.activate():
                async with create_test_worker(
                    env,
                    workflows=[SingleActivityWorkflow],
                    activities=[capture_token, _register_execution],
                    interceptors=_make_interceptors(),
                ):
                    wf = get_workflow_definition(SingleActivityWorkflow)
                    handle = await env.client.start_workflow(
                        wf.name,
                        _make_initial_arg(),
                        id="test-reg-not-found",
                        task_queue="test-task-queue",
                    )
                    await handle.result()

        assert len(_fixtures._observed_tokens) == 1
        assert _fixtures._observed_tokens[0] is None

    @pytest.mark.asyncio
    async def test_registration_server_error_fails_workflow(self) -> None:
        tracker = _RegistrationTracker()
        mock_response = AsyncMock()
        mock_response.status_code = 500
        tracker._mock_client.register_execution_async = AsyncMock(
            side_effect=SDKError("Internal Server Error", mock_response)
        )

        async with _env_with_converter() as env:
            with tracker.activate():
                async with create_test_worker(
                    env,
                    workflows=[SingleActivityWorkflow],
                    activities=[capture_token, _register_execution],
                    interceptors=_make_interceptors(),
                ):
                    wf = get_workflow_definition(SingleActivityWorkflow)
                    handle = await env.client.start_workflow(
                        wf.name,
                        _make_initial_arg(),
                        id="test-reg-server-error",
                        task_queue="test-task-queue",
                    )
                    with pytest.raises(WorkflowFailureError):
                        await handle.result()
