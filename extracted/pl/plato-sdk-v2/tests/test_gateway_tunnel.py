from __future__ import annotations

import asyncio
import contextlib
from unittest.mock import patch

import pytest

from plato.v2.utils.gateway_tunnel import GatewayTunnel


class _SlowServer:
    def __init__(self) -> None:
        self.closed = False

    def close(self) -> None:
        self.closed = True

    async def wait_closed(self) -> None:
        await asyncio.sleep(10)


@pytest.mark.asyncio
async def test_stop_is_bounded_and_cancels_client_tasks():
    tunnel = GatewayTunnel(job_id="test-job", remote_port=5432, local_port=0)
    tunnel._server = _SlowServer()
    worker = asyncio.create_task(asyncio.sleep(10))
    tunnel._client_tasks.add(worker)

    # stop() should not hang even if server.wait_closed() is slow.
    await asyncio.wait_for(tunnel.stop(timeout=0.01), timeout=0.5)
    await asyncio.sleep(0)

    assert tunnel._server is None
    assert worker.cancelled() or worker.done()
    with contextlib.suppress(asyncio.CancelledError):
        await worker


@pytest.mark.asyncio
async def test_stop_is_noop_when_already_stopped():
    tunnel = GatewayTunnel(job_id="test-job", remote_port=5432, local_port=0)
    await tunnel.stop()


@pytest.mark.asyncio
async def test_stop_applies_timeout_as_total_budget():
    tunnel = GatewayTunnel(job_id="test-job", remote_port=5432, local_port=0)
    tunnel._server = _SlowServer()
    worker = asyncio.create_task(asyncio.sleep(10))
    tunnel._client_tasks.add(worker)

    observed_wait_for_timeout: dict[str, float] = {}

    async def _slow_wait(tasks, timeout=None):
        await asyncio.sleep(0.03)
        return set(), set(tasks)

    async def _capture_wait_for(awaitable, timeout=None):
        # Ensure we don't leak an un-awaited coroutine in this test shim.
        if hasattr(awaitable, "close"):
            awaitable.close()
        observed_wait_for_timeout["value"] = float(timeout)
        return None

    with (
        patch("plato.v2.utils.gateway_tunnel.asyncio.wait", side_effect=_slow_wait),
        patch(
            "plato.v2.utils.gateway_tunnel.asyncio.wait_for",
            side_effect=_capture_wait_for,
        ),
    ):
        await tunnel.stop(timeout=0.05)

    assert observed_wait_for_timeout["value"] < 0.049
    with contextlib.suppress(asyncio.CancelledError):
        await worker


@pytest.mark.asyncio
async def test_stop_closes_server_before_waiting_on_tasks():
    tunnel = GatewayTunnel(job_id="test-job", remote_port=5432, local_port=0)
    tunnel._server = _SlowServer()
    worker = asyncio.create_task(asyncio.sleep(10))
    tunnel._client_tasks.add(worker)

    saw_wait = False

    async def _assert_wait(tasks, timeout=None):
        nonlocal saw_wait
        _ = timeout
        saw_wait = True
        assert tunnel._server is not None
        assert tunnel._server.closed is True
        for task in list(tasks):
            tunnel._client_tasks.discard(task)
        return set(tasks), set()

    async def _noop_wait_for(awaitable, timeout=None):
        _ = timeout
        if hasattr(awaitable, "close"):
            awaitable.close()
        return None

    with (
        patch("plato.v2.utils.gateway_tunnel.asyncio.wait", side_effect=_assert_wait),
        patch(
            "plato.v2.utils.gateway_tunnel.asyncio.wait_for",
            side_effect=_noop_wait_for,
        ),
    ):
        await tunnel.stop(timeout=0.1)

    assert saw_wait
    with contextlib.suppress(asyncio.CancelledError):
        await worker


@pytest.mark.asyncio
async def test_stop_cancels_tasks_added_during_teardown():
    tunnel = GatewayTunnel(job_id="test-job", remote_port=5432, local_port=0)
    tunnel._server = _SlowServer()
    initial = asyncio.create_task(asyncio.sleep(10))
    tunnel._client_tasks.add(initial)

    injected: asyncio.Task | None = None
    wait_calls = 0

    async def _wait_with_injected(tasks, timeout=None):
        nonlocal injected, wait_calls
        _ = timeout
        wait_calls += 1

        if wait_calls == 1:
            injected = asyncio.create_task(asyncio.sleep(10))
            tunnel._client_tasks.add(injected)
            for task in list(tasks):
                tunnel._client_tasks.discard(task)
            return set(tasks), set()

        assert injected is not None
        assert injected in tasks
        for task in list(tasks):
            tunnel._client_tasks.discard(task)
        return set(tasks), set()

    async def _noop_wait_for(awaitable, timeout=None):
        _ = timeout
        if hasattr(awaitable, "close"):
            awaitable.close()
        return None

    with (
        patch("plato.v2.utils.gateway_tunnel.asyncio.wait", side_effect=_wait_with_injected),
        patch(
            "plato.v2.utils.gateway_tunnel.asyncio.wait_for",
            side_effect=_noop_wait_for,
        ),
    ):
        await tunnel.stop(timeout=0.2)

    await asyncio.sleep(0)
    assert wait_calls >= 2
    assert injected is not None
    assert injected.cancelled() or injected.done()
    with contextlib.suppress(asyncio.CancelledError):
        await initial
    with contextlib.suppress(asyncio.CancelledError):
        await injected
