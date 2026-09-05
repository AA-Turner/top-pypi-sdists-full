"""wait / create_and_wait poll to a terminal state and time out client-side.

The services are built without a channel (the stub is never touched): `get`
and `create` are replaced with fakes, and sleeping is patched out, so these
pin the polling logic — terminal detection, the poll cadence, and the
client-side timeout that leaves the run executing server-side.
"""

import asyncio

import pytest

from seltz import SeltzTimeoutError
from seltz.services.agent_service import AgentService, AsyncAgentService
from seltz_public_api.proto.v1 import agent_pb2


def _run(
    status: "agent_pb2.AgentRunStatus", run_id: str = "run_0189"
) -> agent_pb2.AgentRun:
    return agent_pb2.AgentRun(id=run_id, object="agent.run", status=status)


PENDING = agent_pb2.AGENT_RUN_STATUS_PENDING
RUNNING = agent_pb2.AGENT_RUN_STATUS_RUNNING
COMPLETED = agent_pb2.AGENT_RUN_STATUS_COMPLETED
CANCELLED = agent_pb2.AGENT_RUN_STATUS_CANCELLED


def _service_polling(statuses: list) -> "tuple[AgentService, list]":
    """A stub-less service whose get() serves the given statuses in order,
    and a record of the sleeps wait() takes between polls."""
    service = AgentService.__new__(AgentService)
    remaining = list(statuses)
    slept: list = []
    service.get = lambda run_id: _run(remaining.pop(0))  # type: ignore[method-assign]
    return service, slept


def test_wait_polls_until_terminal(monkeypatch: pytest.MonkeyPatch) -> None:
    service, slept = _service_polling([PENDING, RUNNING, COMPLETED])
    monkeypatch.setattr(
        "seltz.services.agent_service.time.sleep", lambda s: slept.append(s)
    )

    run = service.wait("run_0189", poll_interval=5.0)
    assert run.status == COMPLETED
    assert slept == [5.0, 5.0], "one sleep between polls, none after terminal"


def test_wait_treats_every_terminal_status_as_done(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr("seltz.services.agent_service.time.sleep", lambda s: None)
    for terminal in (COMPLETED, agent_pb2.AGENT_RUN_STATUS_FAILED, CANCELLED):
        service, _ = _service_polling([terminal])
        assert service.wait("run_0189").status == terminal


def test_wait_times_out_client_side(monkeypatch: pytest.MonkeyPatch) -> None:
    service, _ = _service_polling([PENDING, PENDING])
    monkeypatch.setattr("seltz.services.agent_service.time.sleep", lambda s: None)

    with pytest.raises(SeltzTimeoutError, match="keeps running"):
        service.wait("run_0189", timeout=0)


def test_create_and_wait_chains_create_into_wait(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    service, _ = _service_polling([RUNNING, COMPLETED])
    created = []

    def fake_create(query, *, output_schema=None):
        created.append((query, output_schema))
        return _run(PENDING, "run_new")

    service.create = fake_create  # type: ignore[method-assign, assignment]
    monkeypatch.setattr("seltz.services.agent_service.time.sleep", lambda s: None)

    run = service.create_and_wait("q", output_schema={"type": "json_object"})
    assert run.status == COMPLETED
    assert created == [("q", {"type": "json_object"})]


async def test_async_wait_polls_until_terminal(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    service = AsyncAgentService.__new__(AsyncAgentService)
    remaining = [PENDING, RUNNING, COMPLETED]
    slept: list = []

    async def fake_get(run_id: str) -> agent_pb2.AgentRun:
        return _run(remaining.pop(0))

    async def fake_sleep(seconds: float) -> None:
        slept.append(seconds)

    service.get = fake_get  # type: ignore[method-assign]
    monkeypatch.setattr(asyncio, "sleep", fake_sleep)

    run = await service.wait("run_0189", poll_interval=5.0)
    assert run.status == COMPLETED
    assert slept == [5.0, 5.0]


async def test_async_wait_times_out_client_side(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    service = AsyncAgentService.__new__(AsyncAgentService)

    async def fake_get(run_id: str) -> agent_pb2.AgentRun:
        return _run(PENDING)

    service.get = fake_get  # type: ignore[method-assign]

    with pytest.raises(SeltzTimeoutError, match="keeps running"):
        await service.wait("run_0189", timeout=0)
