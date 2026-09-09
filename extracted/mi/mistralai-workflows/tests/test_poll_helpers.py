import asyncio
from typing import Any, Callable

import httpx
import pytest

from mistralai.workflows.testing.workflow_helpers import (
    execute_workflow_and_wait,
    poll_pending_inputs,
    poll_workflow_status,
)

EXECUTION_ID = "exec-1"

Responder = Callable[[httpx.Request], httpx.Response]


@pytest.fixture(autouse=True)
def no_sleep(monkeypatch: pytest.MonkeyPatch) -> None:
    async def instant_sleep(_delay: float) -> None:
        return None

    monkeypatch.setattr(asyncio, "sleep", instant_sleep)


def _client(poll_responses: list[Responder]) -> httpx.AsyncClient:
    remaining = list(poll_responses)

    def handle(request: httpx.Request) -> httpx.Response:
        if request.url.path.endswith("/execute"):
            return httpx.Response(200, json={"execution_id": EXECUTION_ID})
        if not remaining:
            raise AssertionError("polled more times than expected")
        return remaining.pop(0)(request)

    return httpx.AsyncClient(base_url="http://test", transport=httpx.MockTransport(handle))


def _status(status: str) -> Responder:
    return lambda _request: httpx.Response(200, json={"status": status})


def _pending_inputs(count: int) -> Responder:
    pending = [{"task_id": f"task-{i}"} for i in range(count)]
    return lambda _request: httpx.Response(200, json={"result": {"pending_inputs": pending}})


def _server_error() -> Responder:
    return lambda _request: httpx.Response(503)


def _client_error() -> Responder:
    return lambda _request: httpx.Response(404)


def _read_error() -> Responder:
    def raise_read_error(_request: httpx.Request) -> httpx.Response:
        raise httpx.ReadError("connection dropped")

    return raise_read_error


BLIPS = pytest.mark.parametrize("blip", [_server_error, _read_error], ids=["503", "read-error"])


class TestExecuteWorkflowAndWait:
    async def _run(self, client: httpx.AsyncClient, timeout_seconds: int = 20) -> dict[str, Any]:
        async with client:
            return await execute_workflow_and_wait(client, "wf", {}, timeout_seconds=timeout_seconds)

    @BLIPS
    async def test_transient_poll_error_is_tolerated(self, blip: Callable[[], Responder]) -> None:
        client = _client([_status("RUNNING"), blip(), _status("COMPLETED")])

        result = await self._run(client)

        assert result["status"] == "COMPLETED"

    async def test_persistent_server_errors_propagate(self) -> None:
        client = _client([_server_error() for _ in range(20)])

        with pytest.raises(httpx.HTTPStatusError):
            await self._run(client)

    async def test_client_error_propagates_immediately(self) -> None:
        client = _client([_client_error()])

        with pytest.raises(httpx.HTTPStatusError):
            await self._run(client)

    async def test_terminal_status_fails_fast(self) -> None:
        client = _client([_status("FAILED")])

        with pytest.raises(RuntimeError, match="ended with status: FAILED"):
            await self._run(client)

    async def test_timeout_reports_last_known_status(self) -> None:
        client = _client([_status("RUNNING") for _ in range(3)])

        with pytest.raises(TimeoutError, match="last known status: RUNNING"):
            await self._run(client, timeout_seconds=3)


class TestPollWorkflowStatus:
    async def _run(self, client: httpx.AsyncClient, expected: str = "COMPLETED", timeout_seconds: int = 20) -> Any:
        async with client:
            return await poll_workflow_status(client, EXECUTION_ID, expected, timeout_seconds=timeout_seconds)

    @BLIPS
    async def test_transient_poll_error_is_tolerated(self, blip: Callable[[], Responder]) -> None:
        client = _client([_status("RUNNING"), blip(), _status("COMPLETED")])

        result = await self._run(client)

        assert result["status"] == "COMPLETED"

    async def test_persistent_server_errors_propagate(self) -> None:
        client = _client([_server_error() for _ in range(20)])

        with pytest.raises(httpx.HTTPStatusError):
            await self._run(client)

    async def test_client_error_propagates_immediately(self) -> None:
        client = _client([_client_error()])

        with pytest.raises(httpx.HTTPStatusError):
            await self._run(client)

    async def test_unexpected_terminal_status_fails_fast(self) -> None:
        client = _client([_status("COMPLETED")])

        with pytest.raises(RuntimeError, match="expected: RUNNING"):
            await self._run(client, expected="RUNNING")


class TestPollPendingInputs:
    async def _run(self, client: httpx.AsyncClient, timeout_seconds: int = 1) -> list[dict[str, Any]]:
        async with client:
            return await poll_pending_inputs(client, EXECUTION_ID, timeout_seconds=timeout_seconds)

    async def test_returns_once_inputs_are_pending(self) -> None:
        client = _client([_pending_inputs(0), _pending_inputs(1)])

        assert await self._run(client) == [{"task_id": "task-0"}]

    async def test_client_errors_are_tolerated_until_the_workflow_starts(self) -> None:
        # The query 4xxs while the worker has not picked up the execution yet.
        client = _client([_client_error() for _ in range(8)] + [_pending_inputs(1)])

        assert await self._run(client) == [{"task_id": "task-0"}]

    async def test_timeout_reports_the_last_swallowed_error(self) -> None:
        client = _client([_server_error() for _ in range(10)])

        with pytest.raises(TimeoutError, match="last poll error"):
            await self._run(client)
