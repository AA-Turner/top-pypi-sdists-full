"""Windows named-pipe daemon integration."""

from __future__ import annotations

import sys
from functools import partial
from uuid import uuid4

import anyio
import pytest

from runlayer_cli.daemon import server
from runlayer_cli.daemon.windows_pipe import PipeAlreadyRunning, WindowsPipeListener
from runlayer_cli.hook import daemon_client, daemon_protocol, hook_io

pytestmark = pytest.mark.skipif(
    sys.platform != "win32",
    reason="Windows named-pipe integration",
)


@pytest.mark.asyncio
async def test_idle_listener_reserves_first_pipe_and_closes_promptly() -> None:
    endpoint = rf"\\.\pipe\runlayer-aiwatch-test-{uuid4().hex}"
    listener = WindowsPipeListener(endpoint)
    try:
        with pytest.raises(PipeAlreadyRunning):
            WindowsPipeListener(endpoint)
    finally:
        with anyio.fail_after(1):
            await listener.aclose()


@pytest.mark.asyncio
async def test_owner_pipe_round_trip_and_version_drain() -> None:
    endpoint = rf"\\.\pipe\runlayer-aiwatch-test-{uuid4().hex}"
    ready = anyio.Event()

    def run_hook() -> None:
        hook_io.write_stdout(hook_io.read_stdin())

    request: daemon_protocol.HookRequest = {
        "version": daemon_protocol.protocol_version(),
        "argv": ["aiwatch"],
        "cwd": r"C:\workspace",
        "env": {},
        "stdin": "request",
    }
    skewed = {**request, "version": "version-skew"}

    async with anyio.create_task_group() as tasks:
        tasks.start_soon(
            partial(
                server.serve_daemon,
                endpoint=endpoint,
                gate_check=lambda: True,
                ready=ready.set,
                hook_runner=run_hook,
            )
        )
        await ready.wait()
        response = await anyio.to_thread.run_sync(
            daemon_client._send_windows_request,
            endpoint,
            request,
        )
        restarting = await anyio.to_thread.run_sync(
            daemon_client._send_windows_request,
            endpoint,
            skewed,
        )

    assert response == {"stdout": "request", "stderr": "", "exit_code": 0}
    assert restarting == {"status": "restarting"}
