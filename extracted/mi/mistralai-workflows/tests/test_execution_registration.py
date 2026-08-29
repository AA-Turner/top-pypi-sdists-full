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
    _resolve_search_key_metadata,
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
    CoercedSearchKeyWorkflow,
    ContinueAsNewWorkflow,
    DefaultMultiParamSearchKeyWorkflow,
    DefaultScalarSearchKeyWorkflow,
    DefaultSingleParamSearchKeyWorkflow,
    IterationInput,
    MixedScalarModelSearchKeyWorkflow,
    MultiParamSearchKeyWorkflow,
    MultiScalarSearchKeyWorkflow,
    ParentWorkflow,
    ScalarEnumSearchKeyWorkflow,
    ScalarIntSearchKeyWorkflow,
    ScalarParamSearchKeyWorkflow,
    SearchKeyContext,
    SearchKeyCustomer,
    SearchKeyInput,
    SearchKeyWorkflow,
    SingleActivityWorkflow,
    SingleBaseModelSearchKeyWorkflow,
    Tier,
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


async def _run_and_get_search_key_metadata(workflow_cls: Any, payload: Any = None) -> dict[str, str] | None:
    """Run a workflow with the given payload, return the search_key_metadata sent to /register."""
    tracker = _RegistrationTracker()
    arg = _make_initial_arg() if payload is None else _make_initial_arg_with_payload(payload)
    async with _env_with_converter() as env:
        with tracker.activate():
            async with create_test_worker(
                env,
                workflows=[workflow_cls],
                activities=[capture_token, _register_execution],
                interceptors=_make_interceptors(),
            ):
                wf = get_workflow_definition(workflow_cls)
                handle = await env.client.start_workflow(
                    wf.name, arg, id="test-reg-search-keys", task_queue="test-task-queue"
                )
                await handle.result()
    return tracker.calls[0].get("search_key_metadata")


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
    async def test_registration_method_not_allowed_does_not_fail_workflow(self) -> None:
        tracker = _RegistrationTracker()
        mock_response = AsyncMock()
        mock_response.status_code = 405
        tracker._mock_client.register_execution_async = AsyncMock(
            side_effect=SDKError("Method Not Allowed", mock_response)
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
                        id="test-reg-method-not-allowed",
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

    @pytest.mark.asyncio
    async def test_search_key_metadata_is_extracted_and_sent(self) -> None:
        # `note` is declared but unset (None) → omitted.
        payload = SearchKeyInput(id="pr-402", customer=SearchKeyCustomer(name="acme", tier=2)).model_dump()
        metadata = await _run_and_get_search_key_metadata(SearchKeyWorkflow, payload)
        assert metadata == {"id": "pr-402", "customer.name": "acme", "customer.tier": "2"}

    @pytest.mark.asyncio
    async def test_search_key_metadata_multi_param_roots_at_param_names(self) -> None:
        # Multi-param entrypoints root paths at the parameter name; `context.region`
        # is declared but unset (None) → omitted.
        payload = {
            "payload": SearchKeyInput(id="pr-402", customer=SearchKeyCustomer(name="acme", tier=2)).model_dump(),
            "context": SearchKeyContext(tenant_name="globex").model_dump(),
        }
        metadata = await _run_and_get_search_key_metadata(MultiParamSearchKeyWorkflow, payload)
        assert metadata == {
            "payload.id": "pr-402",
            "payload.customer.name": "acme",
            "context.tenant_name": "globex",
        }

    @pytest.mark.asyncio
    async def test_workflow_without_search_keys_sends_no_metadata(self) -> None:
        metadata = await _run_and_get_search_key_metadata(SingleActivityWorkflow)
        assert metadata is None

    @pytest.mark.asyncio
    async def test_search_key_metadata_scalar_param_is_extracted(self) -> None:
        metadata = await _run_and_get_search_key_metadata(ScalarParamSearchKeyWorkflow, "paris")
        assert metadata == {"city": "paris"}

    @pytest.mark.asyncio
    async def test_search_key_metadata_int_scalar_is_stringified(self) -> None:
        metadata = await _run_and_get_search_key_metadata(ScalarIntSearchKeyWorkflow, 42)
        assert metadata == {"count": "42"}

    @pytest.mark.asyncio
    async def test_search_key_metadata_enum_scalar_uses_value(self) -> None:
        # JSON serializes a str-enum to its value; str() of that is a no-op.
        metadata = await _run_and_get_search_key_metadata(ScalarEnumSearchKeyWorkflow, Tier.paid)
        assert metadata == {"tier": "paid"}

    @pytest.mark.asyncio
    async def test_search_key_metadata_multi_scalar_params(self) -> None:
        metadata = await _run_and_get_search_key_metadata(MultiScalarSearchKeyWorkflow, {"city": "lyon", "count": 7})
        assert metadata == {"city": "lyon", "count": "7"}

    @pytest.mark.asyncio
    async def test_search_key_metadata_mixed_scalar_and_model_params(self) -> None:
        payload = {
            "city": "nice",
            "payload": SearchKeyInput(id="mix-1", customer=SearchKeyCustomer(name="acme", tier=2)).model_dump(),
        }
        metadata = await _run_and_get_search_key_metadata(MixedScalarModelSearchKeyWorkflow, payload)
        assert metadata == {
            "city": "nice",
            "payload.id": "mix-1",
            "payload.customer.name": "acme",
        }

    @pytest.mark.asyncio
    async def test_search_key_metadata_single_basemodel_param_roots_at_fields(self) -> None:
        # A single BaseModel param IS the input model, so paths root at its fields
        # rather than at the parameter name.
        payload = SearchKeyInput(id="sbm-1", customer=SearchKeyCustomer(name="acme", tier=2)).model_dump()
        metadata = await _run_and_get_search_key_metadata(SingleBaseModelSearchKeyWorkflow, payload)
        assert metadata == {"id": "sbm-1", "customer.name": "acme", "customer.tier": "2"}


class TestSearchKeyResolution:
    """Metadata reflects the validated input, not the raw caller JSON.

    The registration interceptor validates against the input model before extracting,
    so omitted defaults are filled in and values are coerced to their declared types —
    matching what the workflow actually runs with.
    """

    @pytest.mark.asyncio
    async def test_multi_param_all_defaults_omitted_yields_defaults(self) -> None:
        # Caller passes {} → id="hi" and payload.id="hey" are resolved from defaults.
        metadata = await _run_and_get_search_key_metadata(DefaultMultiParamSearchKeyWorkflow, {})
        assert metadata == {"id": "hi", "payload.id": "hey"}

    @pytest.mark.asyncio
    async def test_multi_param_partial_default_supplied_overrides_default(self) -> None:
        # Caller supplies payload.id but omits top-level "id" default →
        # payload.id from caller, id from default.
        metadata = await _run_and_get_search_key_metadata(DefaultMultiParamSearchKeyWorkflow, {"payload": {"id": "x"}})
        assert metadata == {"id": "hi", "payload.id": "x"}

    @pytest.mark.asyncio
    async def test_multi_param_all_supplied_extracts_both(self) -> None:
        # Both supplied → both extracted (sanity check that the paths work).
        metadata = await _run_and_get_search_key_metadata(
            DefaultMultiParamSearchKeyWorkflow, {"id": "y", "payload": {"id": "x"}}
        )
        assert metadata == {"id": "y", "payload.id": "x"}

    @pytest.mark.asyncio
    async def test_single_param_default_field_omitted_yields_defaults(self) -> None:
        # Single BaseModel param: paths root at fields. Caller passes {} →
        # the model default resolves id="hey" and note="default-note".
        metadata = await _run_and_get_search_key_metadata(DefaultSingleParamSearchKeyWorkflow, {})
        assert metadata == {"id": "hey", "note": "default-note"}

    @pytest.mark.asyncio
    async def test_single_param_default_field_partially_supplied(self) -> None:
        # Caller supplies id but omits note → id from caller, note from default.
        metadata = await _run_and_get_search_key_metadata(DefaultSingleParamSearchKeyWorkflow, {"id": "z"})
        assert metadata == {"id": "z", "note": "default-note"}

    @pytest.mark.asyncio
    async def test_scalar_param_default_omitted_yields_default(self) -> None:
        # Caller passes {} → city default "paris" is resolved from the input model.
        metadata = await _run_and_get_search_key_metadata(DefaultScalarSearchKeyWorkflow, {})
        assert metadata == {"city": "paris"}

    @pytest.mark.asyncio
    async def test_values_are_coerced_to_declared_types(self) -> None:
        # int 1 → float 1.0, and the timestamp is normalized to ISO 8601 with an offset.
        metadata = await _run_and_get_search_key_metadata(
            CoercedSearchKeyWorkflow, {"ratio": 1, "when": "2024-01-01T00:00:00Z"}
        )
        assert metadata == {"ratio": "1.0", "when": "2024-01-01T00:00:00+00:00"}

    def test_unvalidatable_input_yields_no_metadata(self) -> None:
        # Registration must survive input the model rejects; the run wrapper reports the real error.
        wf = get_workflow_definition(CoercedSearchKeyWorkflow)
        assert _resolve_search_key_metadata(wf.name, [{"ratio": "not-a-number"}]) == {}
