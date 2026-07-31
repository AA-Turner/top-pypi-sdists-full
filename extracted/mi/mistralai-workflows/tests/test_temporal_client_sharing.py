from typing import Any
from unittest.mock import MagicMock

import pytest

from mistralai.workflows import activity, workflow
from mistralai.workflows.core.temporal import temporal_client
from mistralai.workflows.core.temporal.temporal_client import (
    get_worker_service_client,
    set_worker_service_client,
)

from .utils import create_test_worker


@pytest.fixture(autouse=True)
def _reset_worker_service_client():
    set_worker_service_client(None)
    yield
    set_worker_service_client(None)


def test_worker_service_client_holder_roundtrip():
    assert get_worker_service_client() is None
    sentinel = MagicMock()
    set_worker_service_client(sentinel)
    assert get_worker_service_client() is sentinel


async def test_create_temporal_client_reuses_provided_service_client(monkeypatch):
    """A provided service client is reused; no new connection is opened."""
    provided = MagicMock(name="service_client")
    monkeypatch.setattr(temporal_client, "TemporalClient", MagicMock(return_value=MagicMock()))
    monkeypatch.setattr(temporal_client, "get_temporal_tracing_interceptors", lambda: [])

    connect_calls: list[int] = []

    async def _fail_connect(runtime: object | None = None) -> MagicMock:
        connect_calls.append(1)
        return MagicMock()

    monkeypatch.setattr(temporal_client, "create_temporal_service_client", _fail_connect)

    await temporal_client.create_temporal_client(temporal_service_client=provided)

    assert connect_calls == []
    assert temporal_client.TemporalClient.call_args.args[0] is provided


async def test_create_temporal_client_connects_when_no_service_client(monkeypatch):
    """With no service client, the worker's connect path is used."""
    connected = MagicMock(name="connected_service_client")
    monkeypatch.setattr(temporal_client, "TemporalClient", MagicMock(return_value=MagicMock()))
    monkeypatch.setattr(temporal_client, "get_temporal_tracing_interceptors", lambda: [])

    async def _connect(runtime: object | None = None) -> MagicMock:
        return connected

    monkeypatch.setattr(temporal_client, "create_temporal_service_client", _connect)

    await temporal_client.create_temporal_client()

    assert temporal_client.TemporalClient.call_args.args[0] is connected


@activity()
async def _probe_worker_service_client() -> bool:
    return get_worker_service_client() is not None


@workflow.define(name="probe_worker_service_client_workflow")
class _ProbeWorkerServiceClientWorkflow:
    @workflow.entrypoint
    async def run(self) -> bool:
        return await _probe_worker_service_client()


@pytest.mark.asyncio
async def test_worker_service_client_visible_inside_activity(temporal_env: Any) -> None:
    """The client published at worker startup must be readable inside an activity context.

    Regression guard for the webhook plugin's DI-provided client: the value is set in the worker's
    context but read inside a Temporal activity execution context. If it does not cross that
    boundary, get_temporal_client falls back to an unauthenticated fresh connection (observed as a
    401 on list_workflows against a rotating-credential deployment).
    """
    set_worker_service_client(MagicMock(name="worker_service_client"))
    async with create_test_worker(
        temporal_env,
        workflows=[_ProbeWorkerServiceClientWorkflow],
        activities=[_probe_worker_service_client],
    ):
        handle = await temporal_env.client.start_workflow(
            "probe_worker_service_client_workflow",
            id="test-probe-worker-service-client",
            task_queue="test-task-queue",
        )
        result = await handle.result()

    assert result["result"] is True, (
        "get_worker_service_client() returned None inside the activity context: the value set at "
        "worker startup did not propagate into Temporal activity execution"
    )


@pytest.mark.asyncio
async def test_worker_service_client_absent_reads_none_inside_activity(temporal_env: Any) -> None:
    """Control: when nothing publishes a client, the activity reads None (the probe discriminates)."""
    async with create_test_worker(
        temporal_env,
        workflows=[_ProbeWorkerServiceClientWorkflow],
        activities=[_probe_worker_service_client],
    ):
        handle = await temporal_env.client.start_workflow(
            "probe_worker_service_client_workflow",
            id="test-probe-worker-service-client-absent",
            task_queue="test-task-queue",
        )
        result = await handle.result()

    assert result["result"] is False
