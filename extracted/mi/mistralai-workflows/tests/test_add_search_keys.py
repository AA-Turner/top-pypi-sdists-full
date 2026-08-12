"""Tests for runtime search key ingestion (RFC-402 V3)."""

from __future__ import annotations

import asyncio
from contextlib import asynccontextmanager, contextmanager
from dataclasses import dataclass
from datetime import date, datetime, timezone
from enum import Enum
from types import MappingProxyType
from typing import Any, AsyncGenerator, Callable, Generator
from unittest.mock import AsyncMock, patch

import httpx
import pytest
from temporalio.client import WorkflowFailureError
from temporalio.converter import DataConverter
from temporalio.exceptions import ActivityError, ApplicationError, CancelledError
from temporalio.exceptions import TimeoutError as TemporalTimeoutError
from temporalio.testing import WorkflowEnvironment

from mistralai.workflows.core._registration.execution_registration_interceptor import (
    ExecutionRegistrationInterceptor,
)
from mistralai.workflows.core._registration.registration_activity import _register_execution
from mistralai.workflows.core._registration.search_key_ingestion import (
    _MAX_UPSERT_ATTEMPTS,
    _is_retryable,
    _must_propagate,
    _upsert_search_keys,
    _validate_and_coerce,
)
from mistralai.workflows.core.config.config import (
    MAX_SEARCH_KEY_CHARS,
    MAX_SEARCH_KEY_VALUE_CHARS,
    MAX_SEARCH_KEYS,
)
from mistralai.workflows.core.definition.workflow_definition import get_workflow_definition
from mistralai.workflows.core.temporal.context_handler_interceptor import ContextHandlerInterceptor
from mistralai.workflows.core.temporal.payload_converter import MistralWorkflowsPayloadConverter
from mistralai.workflows.models import PayloadWithContext, WorkflowContext
from mistralai.workflows.worker_client.errors.no_response_error import NoResponseError
from mistralai.workflows.worker_client.errors.responsevalidationerror import ResponseValidationError
from mistralai.workflows.worker_client.errors.sdkerror import SDKError
from mistralai.workflows.worker_client.models import (
    RegisterExecutionResponse,
    UpsertExecutionMetadataResponse,
)
from mistralai.workflows.worker_client.sdk import PrivateWorkerClient

from .fixtures_add_search_keys import (
    AddInvalidSearchKeysWorkflow,
    AddSearchKeysFromActivityWorkflow,
    AddSearchKeysWorkflow,
    tag_from_activity,
)
from .utils import create_test_worker

_REGISTER_PATCH = "mistralai.workflows.core._registration.registration_activity.get_worker_client"
_INGEST_MODULE = "mistralai.workflows.core._registration.search_key_ingestion"
_INGEST_PATCH = f"{_INGEST_MODULE}.get_worker_client"


class _Tier(str, Enum):
    paid = "paid"


class TestValidateAndCoerce:
    def test_coerces_scalar_values_to_strings(self) -> None:
        assert _validate_and_coerce({"a": 1, "b": True, "c": "x"}) == {"a": "1", "b": "true", "c": "x"}

    def test_enum_value_uses_enum_value_not_repr(self) -> None:
        assert _validate_and_coerce({"tier": _Tier.paid}) == {"tier": "paid"}

    def test_datetime_value_uses_isoformat(self) -> None:
        moment = datetime(2026, 7, 27, 8, 30, tzinfo=timezone.utc)
        assert _validate_and_coerce({"at": moment}) == {"at": "2026-07-27T08:30:00+00:00"}

    def test_date_value_uses_isoformat(self) -> None:
        assert _validate_and_coerce({"on": date(2026, 7, 27)}) == {"on": "2026-07-27"}

    def test_none_value_is_skipped(self) -> None:
        assert _validate_and_coerce({"a": None, "b": "x"}) == {"b": "x"}

    def test_empty_payload_returns_empty(self) -> None:
        assert _validate_and_coerce({}) == {}

    def test_accepts_any_mapping_not_just_dict(self) -> None:
        assert _validate_and_coerce(MappingProxyType({"a": "x"})) == {"a": "x"}

    def test_non_mapping_payload_raises(self) -> None:
        with pytest.raises(ApplicationError):
            _validate_and_coerce([("a", "x")])  # type: ignore[arg-type]

    def test_overlong_value_is_truncated(self) -> None:
        value = "x" * (MAX_SEARCH_KEY_VALUE_CHARS + 10)
        assert _validate_and_coerce({"a": value}) == {"a": "x" * MAX_SEARCH_KEY_VALUE_CHARS}

    def test_overlong_key_is_dropped_but_others_kept(self) -> None:
        long_key = "k" * (MAX_SEARCH_KEY_CHARS + 1)
        assert _validate_and_coerce({long_key: "v", "ok": "v"}) == {"ok": "v"}

    def test_more_than_max_keys_raises(self) -> None:
        payload: dict[str, str] = {f"k{i}": "v" for i in range(MAX_SEARCH_KEYS + 1)}
        with pytest.raises(ApplicationError, match="at most"):
            _validate_and_coerce(payload)

    @pytest.mark.parametrize("key", ["", "  ", " padded", "padded "])
    def test_empty_or_padded_key_raises(self, key: str) -> None:
        with pytest.raises(ApplicationError):
            _validate_and_coerce({key: "v"})

    def test_key_containing_colon_raises(self) -> None:
        with pytest.raises(ApplicationError, match="':'"):
            _validate_and_coerce({"a:b": "v"})

    def test_non_string_key_raises(self) -> None:
        with pytest.raises(ApplicationError):
            _validate_and_coerce({1: "v"})  # type: ignore[dict-item]

    def test_reserved_prefix_raises_for_callers(self) -> None:
        with pytest.raises(ApplicationError, match="reserves"):
            _validate_and_coerce({"internal.execution.state": "v"})

    def test_reserved_prefix_allowed_for_sdk(self) -> None:
        assert _validate_and_coerce({"internal.execution.state": "v"}, allow_reserved=True) == {
            "internal.execution.state": "v"
        }

    @pytest.mark.parametrize("value", [{"a": 1}, [1, 2], (1, 2), {1, 2}])
    def test_container_value_raises(self, value: object) -> None:
        with pytest.raises(ApplicationError):
            _validate_and_coerce({"a": value})


def _sdk_error(status_code: int, message: str) -> SDKError:
    response = AsyncMock()
    response.status_code = status_code
    return SDKError(message, response)


def _unparseable_response() -> ResponseValidationError:
    return ResponseValidationError("bad body", httpx.Response(200, text="{}"), ValueError("field missing"))


@dataclass(frozen=True)
class _FailureCase:
    """One upsert failure and the behaviour it must produce in *both* dispatch branches."""

    name: str
    error: Callable[[], Exception]
    attempts: int
    fails_execution: bool


# Status-code classification is covered exhaustively by the _is_retryable unit tests; these
# are one representative per class, run end-to-end through both branches.
_FAILURE_CASES = [
    _FailureCase("server_error", lambda: _sdk_error(500, "Internal Server Error"), _MAX_UPSERT_ATTEMPTS, False),
    _FailureCase("rate_limited", lambda: _sdk_error(429, "Too Many Requests"), _MAX_UPSERT_ATTEMPTS, False),
    _FailureCase("connect_error", lambda: httpx.ConnectError("connection refused"), _MAX_UPSERT_ATTEMPTS, False),
    _FailureCase("read_timeout", lambda: httpx.ReadTimeout("read timed out"), _MAX_UPSERT_ATTEMPTS, False),
    _FailureCase("not_found", lambda: _sdk_error(404, "Not Found"), 1, False),
    _FailureCase("unprocessable", lambda: _sdk_error(422, "Unprocessable Entity"), 1, False),
    _FailureCase("unparseable_body", _unparseable_response, 1, False),
    _FailureCase("bug", lambda: TypeError("unsupported operand"), 1, True),
]

_BRANCHES = [
    pytest.param(AddSearchKeysWorkflow, None, id="workflow_body"),
    pytest.param(AddSearchKeysFromActivityWorkflow, [tag_from_activity], id="from_activity"),
]


def _unwrap(exc: BaseException | None) -> BaseException | None:
    """Peel ActivityError wrappers; the activity branch nests one more than the workflow branch."""
    while isinstance(exc, ActivityError) and exc.cause is not None:
        exc = exc.cause
    return exc


class _UpsertTracker:
    def __init__(
        self,
        *,
        upsert_response: UpsertExecutionMetadataResponse | None = None,
        upsert_error: Exception | None = None,
        register_error: Exception | None = None,
        hang_on_upsert: bool = False,
    ) -> None:
        self.register_calls: list[dict[str, Any]] = []
        self.upsert_calls: list[dict[str, Any]] = []
        self._upsert_response = upsert_response or UpsertExecutionMetadataResponse()
        self._upsert_error = upsert_error
        self._hang_on_upsert = hang_on_upsert

        self._register_client = AsyncMock(spec=PrivateWorkerClient)
        self._register_client.register_execution_async = AsyncMock(side_effect=register_error or self._capture_register)
        self._register_client.__aenter__ = AsyncMock(return_value=self._register_client)
        self._upsert_client = AsyncMock(spec=PrivateWorkerClient)
        self._upsert_client.upsert_execution_metadata_async = AsyncMock(side_effect=self._capture_upsert)
        self._upsert_client.__aenter__ = AsyncMock(return_value=self._upsert_client)

    async def _capture_register(self, **kwargs: Any) -> RegisterExecutionResponse:
        self.register_calls.append(kwargs)
        return RegisterExecutionResponse(execution_id=kwargs["temporal_workflow_id"], created=True)

    async def _capture_upsert(self, **kwargs: Any) -> UpsertExecutionMetadataResponse:
        self.upsert_calls.append(kwargs)
        if self._hang_on_upsert:
            await asyncio.Event().wait()  # block until the test cancels the workflow
        if self._upsert_error is not None:
            raise self._upsert_error
        return self._upsert_response

    @contextmanager
    def activate(self) -> Generator[None, None, None]:
        with (
            patch(_REGISTER_PATCH, return_value=self._register_client),
            patch(_INGEST_PATCH, return_value=self._upsert_client),
        ):
            yield


@asynccontextmanager
async def _env_with_converter() -> AsyncGenerator[WorkflowEnvironment, None]:
    data_converter = DataConverter(payload_converter_class=MistralWorkflowsPayloadConverter)
    async with await WorkflowEnvironment.start_time_skipping(data_converter=data_converter) as env:
        yield env


def _initial_arg() -> PayloadWithContext:
    return PayloadWithContext(
        payload=b"null",
        empty=True,
        context=WorkflowContext(namespace="test-ns", execution_id="placeholder", execution_token=None),
    )


async def _run(
    workflow_cls: Any,
    tracker: _UpsertTracker,
    *,
    workflow_id: str,
    extra_activities: list[Callable] | None = None,
) -> Any:
    activities: list[Callable] = [_register_execution, _upsert_search_keys, *(extra_activities or [])]
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
                    wf.name, _initial_arg(), id=workflow_id, task_queue="test-task-queue"
                )
                return await handle.result()


async def _wait_for_upsert(tracker: _UpsertTracker, *, count: int) -> None:
    """Poll until the tracker has recorded ``count`` in-flight upsert calls."""
    while len(tracker.upsert_calls) < count:
        await asyncio.sleep(0.01)


class TestDispatch:
    @pytest.mark.asyncio
    async def test_workflow_body_upserts_search_keys(self) -> None:
        tracker = _UpsertTracker()

        await _run(AddSearchKeysWorkflow, tracker, workflow_id="wf-search-keys-body")

        assert len(tracker.upsert_calls) == 1
        call = tracker.upsert_calls[0]
        assert call["temporal_workflow_id"] == "wf-search-keys-body"
        assert call["search_key_metadata"] == {"customer.tier": "gold"}

    @pytest.mark.asyncio
    async def test_upsert_token_hash_matches_registration(self) -> None:
        tracker = _UpsertTracker()

        await _run(AddSearchKeysWorkflow, tracker, workflow_id="wf-search-keys-hash")

        assert tracker.upsert_calls[0]["execution_token_hash"] == tracker.register_calls[0]["execution_token_hash"]

    @pytest.mark.asyncio
    async def test_activity_can_upsert_search_keys(self) -> None:
        tracker = _UpsertTracker()

        await _run(
            AddSearchKeysFromActivityWorkflow,
            tracker,
            workflow_id="wf-search-keys-activity",
            extra_activities=[tag_from_activity],
        )

        assert len(tracker.upsert_calls) == 1
        call = tracker.upsert_calls[0]
        assert call["temporal_workflow_id"] == "wf-search-keys-activity"
        assert call["search_key_metadata"] == {"activity.key": "from-activity"}

    @pytest.mark.asyncio
    async def test_missing_execution_token_skips_upsert(self) -> None:
        tracker = _UpsertTracker(register_error=_sdk_error(404, "Not Found"))

        await _run(AddSearchKeysWorkflow, tracker, workflow_id="wf-search-keys-no-token")

        assert tracker.upsert_calls == []

    @pytest.mark.asyncio
    async def test_upsert_timeout_does_not_fail_workflow(self) -> None:
        # A local activity surfaces a timeout as ActivityError, not the bare TimeoutError
        # the other transient paths raise.
        tracker = _UpsertTracker(hang_on_upsert=True)

        with patch(f"{_INGEST_MODULE}._UPSERT_TIMEOUT_SECONDS", 0.2):
            await _run(AddSearchKeysWorkflow, tracker, workflow_id="wf-search-keys-timeout")

        assert len(tracker.upsert_calls) == _MAX_UPSERT_ATTEMPTS

    @pytest.mark.asyncio
    async def test_partial_response_does_not_fail_workflow(self) -> None:
        tracker = _UpsertTracker(
            upsert_response=UpsertExecutionMetadataResponse(metadata_status="partial", dropped_keys=["customer.tier"])
        )

        await _run(AddSearchKeysWorkflow, tracker, workflow_id="wf-search-keys-partial")

        assert len(tracker.upsert_calls) == 1

    @pytest.mark.asyncio
    async def test_invalid_key_from_workflow_fails_execution(self) -> None:
        tracker = _UpsertTracker()

        with pytest.raises(WorkflowFailureError) as exc_info:
            await _run(AddInvalidSearchKeysWorkflow, tracker, workflow_id="wf-search-keys-invalid")

        assert isinstance(exc_info.value.cause, ApplicationError)
        assert not tracker.upsert_calls

    @pytest.mark.asyncio
    async def test_cancellation_during_upsert_propagates(self) -> None:
        tracker = _UpsertTracker(hang_on_upsert=True)

        activities: list[Callable] = [_register_execution, _upsert_search_keys]
        async with _env_with_converter() as env:
            with tracker.activate():
                async with create_test_worker(
                    env,
                    workflows=[AddSearchKeysWorkflow],
                    activities=activities,
                    interceptors=[ContextHandlerInterceptor(), ExecutionRegistrationInterceptor()],
                ):
                    wf = get_workflow_definition(AddSearchKeysWorkflow)
                    handle = await env.client.start_workflow(
                        wf.name, _initial_arg(), id="wf-search-keys-cancel", task_queue="test-task-queue"
                    )
                    # Wait until the upsert is in-flight, then cancel.
                    await _wait_for_upsert(tracker, count=1)
                    await handle.cancel()

                    with pytest.raises(WorkflowFailureError) as exc_info:
                        await handle.result()

                    assert isinstance(exc_info.value.cause, CancelledError)


class TestFailureMatrix:
    """Every upsert failure, through both dispatch branches.

    The two branches retry through different machinery (Temporal's RetryPolicy for the local
    activity, tenacity for the direct call), so each case is asserted against both to pin the
    symmetry the module promises.
    """

    @pytest.mark.parametrize(("workflow_cls", "extra_activities"), _BRANCHES)
    @pytest.mark.parametrize("case", _FAILURE_CASES, ids=lambda c: c.name)
    @pytest.mark.asyncio
    async def test_failure_behaviour_is_identical_in_both_branches(
        self,
        case: _FailureCase,
        workflow_cls: type,
        extra_activities: list[Callable] | None,
        request: pytest.FixtureRequest,
    ) -> None:
        tracker = _UpsertTracker(upsert_error=case.error())
        workflow_id = f"wf-matrix-{abs(hash(request.node.callspec.id)):x}"

        async def run() -> Any:
            return await _run(workflow_cls, tracker, workflow_id=workflow_id, extra_activities=extra_activities)

        if case.fails_execution:
            with pytest.raises(WorkflowFailureError) as exc_info:
                await run()
            inner = _unwrap(exc_info.value.cause)
            assert isinstance(inner, ApplicationError)
            assert inner.non_retryable
        else:
            result = await run()
            assert result.payload["result"] == "ok"

        assert len(tracker.upsert_calls) == case.attempts


def _activity_error(cause: BaseException) -> ActivityError:
    err = ActivityError(
        "activity failed",
        scheduled_event_id=1,
        started_event_id=2,
        identity="test",
        activity_type="upsert",
        activity_id="1",
        retry_state=None,
    )
    err.__cause__ = cause
    return err


class TestErrorClassification:
    @pytest.mark.parametrize("status_code", [408, 429, 500, 502, 503])
    def test_transient_statuses_are_retryable(self, status_code: int) -> None:
        assert _is_retryable(_sdk_error(status_code, "transient"))

    @pytest.mark.parametrize("status_code", [400, 401, 403, 404, 405, 409, 422])
    def test_permanent_statuses_are_not_retryable(self, status_code: int) -> None:
        assert not _is_retryable(_sdk_error(status_code, "permanent"))

    def test_no_response_is_retryable(self) -> None:
        assert _is_retryable(NoResponseError("connection refused"))

    @pytest.mark.parametrize("exc", [TypeError("bug"), AttributeError("bug"), _unparseable_response()])
    def test_bugs_and_unparseable_responses_are_not_retryable(self, exc: Exception) -> None:
        assert not _is_retryable(exc)

    @pytest.mark.parametrize(
        ("exc", "expected"),
        [
            (ApplicationError("bug", non_retryable=True), True),
            (ApplicationError("transient"), False),
            (_activity_error(TemporalTimeoutError("timed out", type=None, last_heartbeat_details=[])), False),
            (_activity_error(CancelledError("cancelled")), True),
            (_activity_error(ApplicationError("bug", non_retryable=True)), True),
            (_activity_error(ApplicationError("transient")), False),
        ],
    )
    def test_only_bugs_and_cancellation_propagate(self, exc: BaseException, expected: bool) -> None:
        assert _must_propagate(exc) is expected
