"""Tests for runtime search key deletion (RFC-402 V3).

Key validation and the failure taxonomy are shared with the upsert path and covered in
test_add_search_keys.py; this covers what delete does differently.
"""

from __future__ import annotations

from collections.abc import Sequence
from contextlib import asynccontextmanager, contextmanager
from typing import Any, AsyncGenerator, Callable, Generator, Iterator
from unittest.mock import AsyncMock, patch

import httpx
import pytest
from temporalio.client import WorkflowFailureError
from temporalio.converter import DataConverter
from temporalio.exceptions import ActivityError, ApplicationError
from temporalio.testing import WorkflowEnvironment

from mistralai.workflows.core._registration.execution_registration_interceptor import (
    ExecutionRegistrationInterceptor,
)
from mistralai.workflows.core._registration.registration_activity import _register_execution
from mistralai.workflows.core._registration.search_key_ingestion import (
    _MAX_REQUEST_ATTEMPTS,
    _delete_search_keys,
    _validate_keys,
)
from mistralai.workflows.core.config.config import MAX_SEARCH_KEY_CHARS, MAX_SEARCH_KEYS
from mistralai.workflows.core.definition.workflow_definition import get_workflow_definition
from mistralai.workflows.core.temporal.context_handler_interceptor import ContextHandlerInterceptor
from mistralai.workflows.core.temporal.payload_converter import MistralWorkflowsPayloadConverter
from mistralai.workflows.models import PayloadWithContext, WorkflowContext
from mistralai.workflows.worker_client.errors.sdkerror import SDKError
from mistralai.workflows.worker_client.models import (
    DeleteExecutionMetadataResponse,
    RegisterExecutionResponse,
)
from mistralai.workflows.worker_client.sdk import PrivateWorkerClient

from .fixtures_delete_search_keys import (
    DeleteInvalidSearchKeysWorkflow,
    DeleteSearchKeysFromActivityWorkflow,
    DeleteSearchKeysWorkflow,
    untag_from_activity,
)
from .utils import create_test_worker

_REGISTER_PATCH = "mistralai.workflows.core._registration.registration_activity.get_worker_client"
_INGEST_PATCH = "mistralai.workflows.core._registration.search_key_ingestion.get_worker_client"


class TestValidateKeys:
    def test_keeps_requested_keys_in_order(self) -> None:
        assert _validate_keys(["b", "a"]) == ["b", "a"]

    def test_deduplicates_repeated_keys(self) -> None:
        assert _validate_keys(["a", "a", "b"]) == ["a", "b"]

    def test_accepts_a_tuple(self) -> None:
        assert _validate_keys(("a", "b")) == ["a", "b"]

    def test_bare_string_raises_rather_than_deleting_per_character(self) -> None:
        with pytest.raises(ApplicationError, match="list or tuple"):
            _validate_keys("customer.tier")  # type: ignore[arg-type]

    def test_set_raises_because_its_order_is_not_replay_stable(self) -> None:
        with pytest.raises(ApplicationError, match="list or tuple"):
            _validate_keys({"a", "b"})  # type: ignore[arg-type]

    def test_generator_raises_without_being_consumed(self) -> None:
        consumed = 0

        def endless() -> Iterator[str]:
            nonlocal consumed
            while True:
                consumed += 1
                yield "a"

        with pytest.raises(ApplicationError, match="list or tuple"):
            _validate_keys(endless())  # type: ignore[arg-type]
        assert consumed == 0

    def test_sequence_lying_about_its_length_is_still_bounded(self) -> None:
        class Endless(Sequence[str]):
            def __len__(self) -> int:
                return 1

            def __getitem__(self, index: Any) -> str:
                return f"k{index}"

            def __iter__(self) -> Iterator[str]:
                index = 0
                while True:
                    yield f"k{index}"
                    index += 1

        assert _validate_keys(Endless()) == [f"k{i}" for i in range(MAX_SEARCH_KEYS)]

    def test_overlong_key_is_dropped_but_others_kept(self) -> None:
        assert _validate_keys(["k" * (MAX_SEARCH_KEY_CHARS + 1), "ok"]) == ["ok"]

    def test_more_than_max_keys_raises(self) -> None:
        with pytest.raises(ApplicationError, match="at most"):
            _validate_keys([f"k{i}" for i in range(MAX_SEARCH_KEYS + 1)])

    def test_invalid_key_raises(self) -> None:
        with pytest.raises(ApplicationError, match="':'"):
            _validate_keys(["a:b"])

    def test_reserved_prefix_allowed_for_sdk(self) -> None:
        assert _validate_keys(["internal.execution.state"], allow_reserved=True) == ["internal.execution.state"]


def _sdk_error(status_code: int, message: str) -> SDKError:
    response = AsyncMock()
    response.status_code = status_code
    return SDKError(message, response)


class _DeleteTracker:
    def __init__(self, *, delete_error: Exception | None = None) -> None:
        self.register_calls: list[dict[str, Any]] = []
        self.delete_calls: list[dict[str, Any]] = []
        self._delete_error = delete_error

        self._register_client = AsyncMock(spec=PrivateWorkerClient)
        self._register_client.register_execution_async = AsyncMock(side_effect=self._capture_register)
        self._register_client.__aenter__ = AsyncMock(return_value=self._register_client)
        self._delete_client = AsyncMock(spec=PrivateWorkerClient)
        self._delete_client.delete_execution_metadata_async = AsyncMock(side_effect=self._capture_delete)
        self._delete_client.__aenter__ = AsyncMock(return_value=self._delete_client)

    async def _capture_register(self, **kwargs: Any) -> RegisterExecutionResponse:
        self.register_calls.append(kwargs)
        return RegisterExecutionResponse(execution_id=kwargs["temporal_workflow_id"], created=True)

    async def _capture_delete(self, **kwargs: Any) -> DeleteExecutionMetadataResponse:
        self.delete_calls.append(kwargs)
        if self._delete_error is not None:
            raise self._delete_error
        return DeleteExecutionMetadataResponse(deleted_keys=list(kwargs.get("keys") or []))

    @contextmanager
    def activate(self) -> Generator[None, None, None]:
        with (
            patch(_REGISTER_PATCH, return_value=self._register_client),
            patch(_INGEST_PATCH, return_value=self._delete_client),
        ):
            yield


@asynccontextmanager
async def _env_with_converter() -> AsyncGenerator[WorkflowEnvironment, None]:
    data_converter = DataConverter(payload_converter_class=MistralWorkflowsPayloadConverter)
    async with await WorkflowEnvironment.start_time_skipping(data_converter=data_converter) as env:
        yield env


async def _run(
    workflow_cls: Any,
    tracker: _DeleteTracker,
    *,
    workflow_id: str,
    extra_activities: list[Callable] | None = None,
) -> Any:
    initial_arg = PayloadWithContext(
        payload=b"null",
        empty=True,
        context=WorkflowContext(namespace="test-ns", execution_id="placeholder", execution_token=None),
    )
    activities: list[Callable] = [_register_execution, _delete_search_keys, *(extra_activities or [])]
    async with _env_with_converter() as env:
        with tracker.activate():
            async with create_test_worker(
                env,
                workflows=[workflow_cls],
                activities=activities,
                interceptors=[ContextHandlerInterceptor(), ExecutionRegistrationInterceptor()],
            ):
                wf = get_workflow_definition(workflow_cls)
                handle = await env.client.start_workflow(
                    wf.name, initial_arg, id=workflow_id, task_queue="test-task-queue"
                )
                return await handle.result()


def _unwrap(exc: BaseException | None) -> BaseException | None:
    """Peel ActivityError wrappers; the activity branch nests one more than the workflow branch."""
    while isinstance(exc, ActivityError) and exc.cause is not None:
        exc = exc.cause
    return exc


class TestDispatch:
    @pytest.mark.asyncio
    async def test_workflow_body_deletes_by_run_id(self) -> None:
        tracker = _DeleteTracker()

        await _run(DeleteSearchKeysWorkflow, tracker, workflow_id="wf-delete-search-keys-body")

        assert len(tracker.delete_calls) == 1
        call = tracker.delete_calls[0]
        assert call["temporal_workflow_id"] == "wf-delete-search-keys-body"
        assert call["temporal_run_id"] == tracker.register_calls[0]["temporal_run_id"]
        assert call["keys"] == ["customer.tier"]

    @pytest.mark.asyncio
    async def test_activity_deletes_by_the_calling_workflows_run_id(self) -> None:
        tracker = _DeleteTracker()

        await _run(
            DeleteSearchKeysFromActivityWorkflow,
            tracker,
            workflow_id="wf-delete-search-keys-activity",
            extra_activities=[untag_from_activity],
        )

        assert len(tracker.delete_calls) == 1
        call = tracker.delete_calls[0]
        assert call["temporal_run_id"] == tracker.register_calls[0]["temporal_run_id"]
        assert call["keys"] == ["activity.key"]

    @pytest.mark.asyncio
    async def test_invalid_key_from_workflow_fails_execution(self) -> None:
        tracker = _DeleteTracker()

        with pytest.raises(WorkflowFailureError) as exc_info:
            await _run(DeleteInvalidSearchKeysWorkflow, tracker, workflow_id="wf-delete-search-keys-invalid")

        assert isinstance(exc_info.value.cause, ApplicationError)
        assert not tracker.delete_calls


class TestFailures:
    """One case per failure class, through both dispatch branches.

    Delete does not share the upsert path's dispatch, and the two branches retry through
    different machinery (Temporal's RetryPolicy for the local activity, tenacity for the
    direct call), so neither branch is covered by the other's tests.
    """

    _BRANCHES = [
        pytest.param(DeleteSearchKeysWorkflow, None, id="workflow_body"),
        pytest.param(DeleteSearchKeysFromActivityWorkflow, [untag_from_activity], id="from_activity"),
    ]

    _CASES = [
        pytest.param(lambda: _sdk_error(500, "Internal Server Error"), _MAX_REQUEST_ATTEMPTS, False, id="transient"),
        pytest.param(lambda: httpx.ConnectError("connection refused"), _MAX_REQUEST_ATTEMPTS, False, id="no_response"),
        pytest.param(lambda: _sdk_error(404, "Not Found"), 1, False, id="permanent"),
        pytest.param(lambda: TypeError("unsupported operand"), 1, True, id="bug"),
    ]

    @pytest.mark.parametrize(("workflow_cls", "extra_activities"), _BRANCHES)
    @pytest.mark.parametrize(("error", "attempts", "fails_execution"), _CASES)
    @pytest.mark.asyncio
    async def test_failure_behaviour_is_identical_in_both_branches(
        self,
        error: Callable[[], Exception],
        attempts: int,
        fails_execution: bool,
        workflow_cls: type,
        extra_activities: list[Callable] | None,
        request: pytest.FixtureRequest,
    ) -> None:
        tracker = _DeleteTracker(delete_error=error())
        workflow_id = f"wf-delete-failure-{abs(hash(request.node.callspec.id)):x}"

        async def run() -> Any:
            return await _run(workflow_cls, tracker, workflow_id=workflow_id, extra_activities=extra_activities)

        if fails_execution:
            with pytest.raises(WorkflowFailureError) as exc_info:
                await run()
            inner = _unwrap(exc_info.value.cause)
            assert isinstance(inner, ApplicationError)
            assert inner.non_retryable
        else:
            result = await run()
            assert result.payload["result"] == "ok"

        assert len(tracker.delete_calls) == attempts
