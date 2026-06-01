"""Lifecycle tests for ExecutorCredentialsHook.

Each test runs real Temporal workflows and asserts how many times the JWT mint
endpoint is called, validating the hook's caching behaviour across different scenarios.
"""

from __future__ import annotations

import asyncio
import base64
import json
import time
from contextlib import contextmanager
from typing import Any, Generator
from unittest.mock import patch

import pytest
from temporalio.client import WorkflowFailureError
from temporalio.testing import WorkflowEnvironment

from mistralai.workflows.core.definition.workflow_definition import get_workflow_definition
from mistralai.workflows.models.payload import WorkflowContext
from mistralai.workflows.worker_client.models import ExecutorIdentityTokenResponse
from mistralai.workflows.worker_client.sdk import PrivateWorkerClient

from . import fixtures_executor_credentials_lifecycle as _fixtures
from .fixtures_executor_credentials_lifecycle import (
    ContinueAsNewWorkflow,
    InterleavedWorkflow,
    IterationInput,
    RetryWorkflow,
    SingleActivityWorkflow,
    TwoActivityWorkflow,
    TwoOwnClientWorkflow,
    api_call,
    api_call_fail_once,
    api_call_logged,
    api_call_own_client,
    api_call_sync_point,
)
from .utils import create_test_worker

_PATCH_RETRIEVE = "mistralai.workflows.hooks.executor_credentials_hook.retrieve_context"


@pytest.fixture(autouse=True)
def _reset_executor_credentials_lifecycle_state() -> Generator[None, None, None]:
    _fixtures._interleave_events = None
    _fixtures._activity_log.clear()
    yield
    _fixtures._interleave_events = None
    _fixtures._activity_log.clear()


def _make_jwt(exp: float) -> str:
    header = base64.urlsafe_b64encode(json.dumps({"alg": "HS256"}).encode()).rstrip(b"=").decode()
    payload = base64.urlsafe_b64encode(json.dumps({"exp": exp}).encode()).rstrip(b"=").decode()
    return f"{header}.{payload}.signature"


class _JWTMintingTracker:
    """Patches httpx + retrieve_context in the hook module and tracks JWT minting requests.

    Each call to retrieve_context returns a WorkflowContext whose execution_token
    cycles through the provided token list, simulating different workflow executions.
    """

    def __init__(
        self,
        jwt_expiry: float = 3600.0,
        execution_tokens: list[str] | None = None,
        workflow_token_map: dict[str, str] | None = None,
    ):
        self.call_log: list[dict] = []
        self._jwt_expiry = jwt_expiry
        self._execution_tokens = execution_tokens
        self._workflow_token_map = workflow_token_map
        self._token_index = 0

    def _next_context(self) -> WorkflowContext | None:
        if self._workflow_token_map is not None:
            from temporalio import activity

            workflow_id = activity.info().workflow_id
            token = self._workflow_token_map.get(workflow_id)
            if token is None:
                return None
            return WorkflowContext(namespace="test", execution_id=workflow_id, execution_token=token, on_behalf_of=True)

        if self._execution_tokens is None:
            return None
        token = self._execution_tokens[min(self._token_index, len(self._execution_tokens) - 1)]
        self._token_index += 1
        return WorkflowContext(namespace="test", execution_id="test", execution_token=token, on_behalf_of=True)

    def _mock_executor_identity_token_async(self, **kwargs: Any) -> ExecutorIdentityTokenResponse:
        execution_token = kwargs.get("execution_token", "")
        self.call_log.append({"execution_token": execution_token})
        jwt = _make_jwt(time.time() + self._jwt_expiry)
        return ExecutorIdentityTokenResponse(token=jwt)

    @contextmanager
    def activate(self) -> Generator[None, None, None]:
        with (
            patch(_PATCH_RETRIEVE, side_effect=self._next_context),
            patch.object(
                PrivateWorkerClient,
                "executor_identity_token_async",
                side_effect=self._mock_executor_identity_token_async,
            ),
        ):
            yield


class TestExecutorCredentialsLifecycle:
    @pytest.mark.asyncio
    async def test_single_activity_one_mint_call(self, temporal_env: Any) -> None:
        tracker = _JWTMintingTracker(execution_tokens=["tok-A"])
        with tracker.activate():
            async with create_test_worker(
                temporal_env,
                workflows=[SingleActivityWorkflow],
                activities=[api_call],
            ):
                wf = get_workflow_definition(SingleActivityWorkflow)
                assert wf is not None
                handle = await temporal_env.client.start_workflow(
                    wf.name, id="test-lifecycle-single-1", task_queue="test-task-queue"
                )
                await handle.result()

        assert len(tracker.call_log) == 1

    @pytest.mark.asyncio
    async def test_two_activities_same_workflow_cache_hit(self, temporal_env: Any) -> None:
        tracker = _JWTMintingTracker(execution_tokens=["tok-A"])
        with tracker.activate():
            async with create_test_worker(
                temporal_env,
                workflows=[TwoActivityWorkflow],
                activities=[api_call],
            ):
                wf = get_workflow_definition(TwoActivityWorkflow)
                assert wf is not None
                handle = await temporal_env.client.start_workflow(
                    wf.name, id="test-lifecycle-two-act-1", task_queue="test-task-queue"
                )
                await handle.result()

        assert len(tracker.call_log) == 1

    @pytest.mark.asyncio
    async def test_own_client_per_activity_mints_twice(self, temporal_env: Any) -> None:
        tracker = _JWTMintingTracker(execution_tokens=["tok-A"])
        with tracker.activate():
            async with create_test_worker(
                temporal_env,
                workflows=[TwoOwnClientWorkflow],
                activities=[api_call_own_client],
            ):
                wf = get_workflow_definition(TwoOwnClientWorkflow)
                assert wf is not None
                handle = await temporal_env.client.start_workflow(
                    wf.name, id="test-lifecycle-own-client-1", task_queue="test-task-queue"
                )
                await handle.result()

        assert len(tracker.call_log) == 2

    @pytest.mark.asyncio
    async def test_different_token_triggers_remint(self, temporal_env: Any) -> None:
        tracker = _JWTMintingTracker(execution_tokens=["tok-A", "tok-B"])
        with tracker.activate():
            async with create_test_worker(
                temporal_env,
                workflows=[SingleActivityWorkflow],
                activities=[api_call],
            ):
                wf = get_workflow_definition(SingleActivityWorkflow)
                assert wf is not None

                h1 = await temporal_env.client.start_workflow(
                    wf.name, id="test-lifecycle-diff-1", task_queue="test-task-queue"
                )
                await h1.result()

                h2 = await temporal_env.client.start_workflow(
                    wf.name, id="test-lifecycle-diff-2", task_queue="test-task-queue"
                )
                await h2.result()

        assert len(tracker.call_log) == 2
        assert tracker.call_log[0]["execution_token"] == "tok-A"
        assert tracker.call_log[1]["execution_token"] == "tok-B"

    @pytest.mark.asyncio
    async def test_expired_jwt_triggers_remint(self, temporal_env: Any) -> None:
        tracker = _JWTMintingTracker(jwt_expiry=5.0, execution_tokens=["tok-A"])
        with tracker.activate():
            async with create_test_worker(
                temporal_env,
                workflows=[TwoActivityWorkflow],
                activities=[api_call],
            ):
                wf = get_workflow_definition(TwoActivityWorkflow)
                assert wf is not None
                handle = await temporal_env.client.start_workflow(
                    wf.name, id="test-lifecycle-expired-1", task_queue="test-task-queue"
                )
                await handle.result()

        assert len(tracker.call_log) == 2

    @pytest.mark.asyncio
    async def test_continue_as_new_cache_persists(self, temporal_env: Any) -> None:
        tracker = _JWTMintingTracker(execution_tokens=["tok-A"])
        with tracker.activate():
            async with create_test_worker(
                temporal_env,
                workflows=[ContinueAsNewWorkflow],
                activities=[api_call],
            ):
                wf = get_workflow_definition(ContinueAsNewWorkflow)
                assert wf is not None
                handle = await temporal_env.client.start_workflow(
                    wf.name,
                    IterationInput(iteration=0).model_dump(),
                    id="test-lifecycle-can-1",
                    task_queue="test-task-queue",
                )
                await handle.result()

        assert len(tracker.call_log) == 1

    @pytest.mark.asyncio
    async def test_cache_survives_activity_retry(self, temporal_env: Any) -> None:
        tracker = _JWTMintingTracker(execution_tokens=["tok-A"])
        with tracker.activate():
            async with create_test_worker(
                temporal_env,
                workflows=[RetryWorkflow],
                activities=[api_call_fail_once],
            ):
                wf = get_workflow_definition(RetryWorkflow)
                assert wf is not None
                handle = await temporal_env.client.start_workflow(
                    wf.name, id="test-lifecycle-retry-1", task_queue="test-task-queue"
                )
                await handle.result()

        assert len(tracker.call_log) == 1

    @pytest.mark.asyncio
    async def test_interleaved_executions_mint_twice(self) -> None:
        wf_id_a = "test-lifecycle-interleaved-A"
        wf_id_b = "test-lifecycle-interleaved-B"
        tracker = _JWTMintingTracker(
            workflow_token_map={wf_id_a: "tok-A", wf_id_b: "tok-B"},
        )
        _fixtures._interleave_events = {wf_id_a: asyncio.Event(), wf_id_b: asyncio.Event()}
        try:
            # Use start_local (no time-skipping) so concurrent activities can
            # block on asyncio.Event without the server fast-forwarding time.
            async with await WorkflowEnvironment.start_local() as env:
                with tracker.activate():
                    async with create_test_worker(
                        env,
                        workflows=[InterleavedWorkflow],
                        activities=[api_call_sync_point, api_call_logged],
                    ):
                        wf = get_workflow_definition(InterleavedWorkflow)
                        assert wf is not None

                        h_a = await env.client.start_workflow(wf.name, id=wf_id_a, task_queue="test-task-queue")
                        h_b = await env.client.start_workflow(wf.name, id=wf_id_b, task_queue="test-task-queue")
                        await asyncio.gather(h_a.result(), h_b.result())
        finally:
            _fixtures._interleave_events = None

        # Verify interleaving: both sync-point activities ran before either logged activity
        activity_names = [name for _, name in _fixtures._activity_log]
        sync_indices = [i for i, n in enumerate(activity_names) if n == "api_call_sync_point"]
        logged_indices = [i for i, n in enumerate(activity_names) if n == "api_call_logged"]
        assert len(sync_indices) == 2
        assert len(logged_indices) == 2
        assert max(sync_indices) < min(logged_indices)

        assert len(tracker.call_log) == 2
        minted_tokens = {entry["execution_token"] for entry in tracker.call_log}
        assert minted_tokens == {"tok-A", "tok-B"}

    @pytest.mark.asyncio
    async def test_missing_context_raises(self, temporal_env: Any) -> None:
        tracker = _JWTMintingTracker(execution_tokens=None)
        with tracker.activate():
            async with create_test_worker(
                temporal_env,
                workflows=[SingleActivityWorkflow],
                activities=[api_call],
            ):
                wf = get_workflow_definition(SingleActivityWorkflow)
                assert wf is not None
                handle = await temporal_env.client.start_workflow(
                    wf.name, id="test-lifecycle-nocontext-1", task_queue="test-task-queue"
                )
                with pytest.raises(WorkflowFailureError):
                    await handle.result()

        assert len(tracker.call_log) == 0
