"""AnyIO AI Watch daemon request dispatch and drain behavior."""

from __future__ import annotations

import json
import math
import os
import socket
import stat
import sys
import tempfile
import threading
from collections.abc import Iterator
from functools import partial
from io import StringIO
from pathlib import Path

import anyio
import pytest

from runlayer_cli import flow_trace
from runlayer_cli.daemon import server
from runlayer_cli.hook import daemon_client, daemon_protocol, dispatch, hook_io
from runlayer_cli.hook.clients import Client
from runlayer_cli.mdm_config import AIWatchMode
from tests.daemon_frame_helpers import read_frame, write_frame

pytestmark = pytest.mark.skipif(
    sys.platform == "win32",
    reason="Unix-socket server tests; Windows named pipe has a separate integration test",
)


@pytest.fixture
def endpoint() -> Iterator[Path]:
    # Darwin limits AF_UNIX paths to 103 bytes; pytest's tmp_path can exceed it.
    with tempfile.TemporaryDirectory(prefix="rl-aiwatch-", dir="/tmp") as directory:
        yield Path(directory) / "daemon.sock"


def _request(
    *,
    version: str | None = None,
    stdin: str = "{}",
    environment: dict[str, str] | None = None,
    cwd: str = "/workspace",
    argv: list[str] | None = None,
) -> daemon_protocol.HookRequest:
    return {
        "version": version or daemon_protocol.protocol_version(),
        "argv": argv or ["aiwatch", "--client", "cursor"],
        "cwd": cwd,
        "env": environment or {},
        "stdin": stdin,
    }


def _run_inline(request: daemon_protocol.HookRequest) -> daemon_protocol.HookResult:
    stdout = StringIO()
    stderr = StringIO()
    exit_code = 0
    with hook_io.scoped(
        hook_io.HookIO(
            stdin_text=request["stdin"],
            stdout=stdout,
            stderr=stderr,
            env=request["env"],
            cwd=request["cwd"],
            argv=request["argv"],
        )
    ):
        try:
            dispatch.run_hook()
        except SystemExit as exc:
            if isinstance(exc.code, int):
                exit_code = exc.code
            elif exc.code is not None:
                stderr.write(f"{exc.code}\n")
                exit_code = 1
    return {
        "stdout": stdout.getvalue(),
        "stderr": stderr.getvalue(),
        "exit_code": exit_code,
    }


@pytest.mark.parametrize(
    ("case", "mode", "payload"),
    [
        (
            "allow",
            AIWatchMode.MONITOR,
            {"hook_event_name": "UserPromptSubmit", "session_id": "session"},
        ),
        (
            "deny",
            AIWatchMode.ENFORCE,
            {
                "hook_event_name": "PreToolUse",
                "tool_name": "Bash",
                "tool_input": {"command": "cat .env"},
            },
        ),
        (
            "mask",
            AIWatchMode.PROTECT,
            {
                "hook_event_name": "PostToolUse",
                "tool_name": "Read",
                "tool_input": {"file_path": "data.txt"},
                "tool_response": "SSN 123-45-6789",
            },
        ),
        (
            "fail_closed",
            AIWatchMode.ENFORCE,
            {
                "hook_event_name": "PreToolUse",
                "tool_name": "Write",
                "tool_input": {"file_path": "notes.txt", "content": "text"},
            },
        ),
    ],
)
@pytest.mark.asyncio
async def test_daemon_output_matches_inline_for_hook_decision_paths(
    endpoint,
    monkeypatch,
    case,
    mode,
    payload,
) -> None:
    ready = anyio.Event()
    request = _request(
        stdin=json.dumps(payload),
        environment={"RUNLAYER_HOOK_CLIENT": "claude_code"},
        argv=["aiwatch"],
    )
    monkeypatch.setattr(dispatch, "detect_client", lambda: Client.CLAUDE_CODE)
    monkeypatch.setattr(dispatch, "_resolve_mode", lambda: mode)
    monkeypatch.setattr(dispatch, "silence_hook_logging", lambda: None)
    monkeypatch.setattr(dispatch.flow_spool, "spool_append", lambda *_args: None)
    monkeypatch.setattr(dispatch, "forward_event", lambda *_args, **_kwargs: None)
    monkeypatch.setattr(
        dispatch,
        "forward_tool_lifecycle",
        lambda *_args, **_kwargs: None,
    )
    monkeypatch.setattr(
        dispatch,
        "start_transcript_stream",
        lambda *_args, **_kwargs: True,
    )

    def check_tool_lifecycle(*_args, **_kwargs) -> str:
        if case == "mask":
            return '{"blocked":false,"modified_output":"SSN [REDACTED]"}'
        if case == "fail_closed":
            raise dispatch.RelayError(2, "network error")
        return '{"permission":"allow"}'

    monkeypatch.setattr(dispatch, "check_tool_lifecycle", check_tool_lifecycle)

    inline = _run_inline(request)
    flow_trace.reset_flow()
    async with anyio.create_task_group() as tasks:
        tasks.start_soon(
            partial(
                server.serve_daemon,
                endpoint=str(endpoint),
                gate_check=lambda: True,
                ready=ready.set,
            )
        )
        await ready.wait()
        response = await anyio.to_thread.run_sync(
            daemon_client._send_unix_request,
            str(endpoint),
            request,
        )
        await anyio.to_thread.run_sync(
            daemon_client._send_unix_request,
            str(endpoint),
            _request(version="version-skew"),
        )

    assert daemon_protocol.parse_hook_response(response) == inline


@pytest.mark.asyncio
async def test_daemon_round_trip_captures_io_and_system_exit(endpoint) -> None:
    ready = anyio.Event()

    def run_hook() -> None:
        hook_io.write_stdout(f"stdin={hook_io.read_stdin()}")
        hook_io.write_stderr(f"cwd={hook_io.getcwd()}")
        raise SystemExit(2)

    async with anyio.create_task_group() as tasks:
        tasks.start_soon(
            partial(
                server.serve_daemon,
                endpoint=str(endpoint),
                gate_check=lambda: True,
                ready=ready.set,
                hook_runner=run_hook,
            )
        )
        await ready.wait()
        response = await anyio.to_thread.run_sync(
            daemon_client._send_unix_request,
            str(endpoint),
            _request(stdin="payload", cwd="/request"),
        )
        restarting = await anyio.to_thread.run_sync(
            daemon_client._send_unix_request,
            str(endpoint),
            _request(version="version-skew"),
        )

    assert daemon_protocol.parse_hook_response(response) == {
        "stdout": "stdin=payload",
        "stderr": "cwd=/request",
        "exit_code": 2,
    }
    assert restarting == {"status": "restarting"}
    assert not endpoint.exists()


@pytest.mark.asyncio
async def test_health_probe_is_side_effect_free_and_does_not_version_drain(
    endpoint,
) -> None:
    ready = anyio.Event()
    hook_calls = 0

    def run_hook() -> None:
        nonlocal hook_calls
        hook_calls += 1

    async with anyio.create_task_group() as tasks:
        tasks.start_soon(
            partial(
                server.serve_daemon,
                endpoint=str(endpoint),
                gate_check=lambda: True,
                ready=ready.set,
                hook_runner=run_hook,
            )
        )
        await ready.wait()
        health = await anyio.to_thread.run_sync(
            daemon_client._send_unix_request,
            str(endpoint),
            {"op": "health", "version": "older-client"},
        )
        assert endpoint.exists()
        hook = await anyio.to_thread.run_sync(
            daemon_client._send_unix_request,
            str(endpoint),
            _request(),
        )
        await anyio.to_thread.run_sync(
            daemon_client._send_unix_request,
            str(endpoint),
            _request(version="version-skew"),
        )

    assert health == {
        "status": "ok",
        "version": daemon_protocol.protocol_version(),
    }
    assert daemon_protocol.parse_hook_response(hook)["exit_code"] == 0
    assert hook_calls == 1


@pytest.mark.asyncio
async def test_concurrent_connections_do_not_cross_request_contexts(endpoint) -> None:
    ready = anyio.Event()
    rendezvous = threading.Barrier(2)
    responses: list[object | None] = [None, None]

    def run_hook() -> None:
        rendezvous.wait(timeout=5)
        hook_io.write_stdout(
            json.dumps(
                {
                    "stdin": hook_io.read_stdin(),
                    "client": hook_io.getenv("RUNLAYER_HOOK_CLIENT"),
                    "cwd": hook_io.getcwd(),
                    "argv": list(hook_io.argv()),
                },
                sort_keys=True,
            )
        )

    async def send(index: int, request: daemon_protocol.HookRequest) -> None:
        responses[index] = await anyio.to_thread.run_sync(
            daemon_client._send_unix_request,
            str(endpoint),
            request,
        )

    async with anyio.create_task_group() as daemon_tasks:
        daemon_tasks.start_soon(
            partial(
                server.serve_daemon,
                endpoint=str(endpoint),
                gate_check=lambda: True,
                ready=ready.set,
                hook_runner=run_hook,
            )
        )
        await ready.wait()
        async with anyio.create_task_group() as clients:
            clients.start_soon(
                send,
                0,
                _request(
                    stdin="cursor",
                    environment={"RUNLAYER_HOOK_CLIENT": "cursor"},
                    cwd="/cursor",
                    argv=["aiwatch", "--client", "cursor"],
                ),
            )
            clients.start_soon(
                send,
                1,
                _request(
                    stdin="hermes",
                    environment={"RUNLAYER_HOOK_CLIENT": "hermes"},
                    cwd="/hermes",
                    argv=["aiwatch", "--client", "hermes"],
                ),
            )
        await anyio.to_thread.run_sync(
            daemon_client._send_unix_request,
            str(endpoint),
            _request(version="version-skew"),
        )

    parsed = [
        json.loads(daemon_protocol.parse_hook_response(response)["stdout"])
        for response in responses
    ]
    assert parsed == [
        {
            "argv": ["aiwatch", "--client", "cursor"],
            "client": "cursor",
            "cwd": "/cursor",
            "stdin": "cursor",
        },
        {
            "argv": ["aiwatch", "--client", "hermes"],
            "client": "hermes",
            "cwd": "/hermes",
            "stdin": "hermes",
        },
    ]


@pytest.mark.asyncio
async def test_version_skew_drains_after_inflight_hook_finishes(endpoint) -> None:
    ready = anyio.Event()
    server_exited = anyio.Event()
    hook_started = threading.Event()
    release_hook = threading.Event()
    response: object | None = None

    def run_hook() -> None:
        hook_started.set()
        assert release_hook.wait(timeout=5)
        hook_io.write_stdout("finished")

    async def run_server() -> None:
        try:
            await server.serve_daemon(
                endpoint=str(endpoint),
                gate_check=lambda: True,
                ready=ready.set,
                hook_runner=run_hook,
            )
        finally:
            server_exited.set()

    async def send_hook() -> None:
        nonlocal response
        response = await anyio.to_thread.run_sync(
            daemon_client._send_unix_request,
            str(endpoint),
            _request(),
        )

    try:
        async with anyio.create_task_group() as tasks:
            tasks.start_soon(run_server)
            await ready.wait()
            tasks.start_soon(send_hook)
            assert await anyio.to_thread.run_sync(hook_started.wait, 5)
            restarting = await anyio.to_thread.run_sync(
                daemon_client._send_unix_request,
                str(endpoint),
                _request(version="version-skew"),
            )
            await anyio.sleep(0.05)
            assert restarting == {"status": "restarting"}
            assert not server_exited.is_set()
            release_hook.set()
    finally:
        release_hook.set()

    assert daemon_protocol.parse_hook_response(response) == {
        "stdout": "finished",
        "stderr": "",
        "exit_code": 0,
    }
    assert server_exited.is_set()


@pytest.mark.asyncio
async def test_version_skew_drain_flushes_deferred_event_queue(
    endpoint, monkeypatch
) -> None:
    """Deferred event POSTs queued by hooks are delivered by the bounded
    ``runtime.close()`` flush after the version-skew drain — not dropped with
    the daemon exit."""
    import httpx

    from runlayer_cli.daemon import runtime as daemon_runtime
    from runlayer_cli.hook import relay

    ready = anyio.Event()
    release_send = threading.Event()
    event_requests: list[httpx.Request] = []

    def respond(request: httpx.Request) -> httpx.Response:
        assert release_send.wait(timeout=10)
        event_requests.append(request)
        return httpx.Response(200, text="{}")

    monkeypatch.setattr(
        relay,
        "_load_credentials",
        lambda: ("https://api.example.com", "rl_org_test"),
    )
    monkeypatch.setattr(relay, "_maybe_attach_device", lambda payload: payload)
    monkeypatch.setattr(
        relay, "_maybe_attach_client_flows", lambda payload, target: payload
    )

    runtime = daemon_runtime.DaemonRuntime(
        client=httpx.Client(transport=httpx.MockTransport(respond))
    )
    runtime.install()

    def run_hook() -> None:
        relay.forward_event("cursor", "PreToolUse", {"tool_name": "shell"})

    try:
        async with anyio.create_task_group() as tasks:
            tasks.start_soon(
                partial(
                    server.serve_daemon,
                    endpoint=str(endpoint),
                    gate_check=lambda: True,
                    ready=ready.set,
                    hook_runner=run_hook,
                )
            )
            await ready.wait()
            response = await anyio.to_thread.run_sync(
                daemon_client._send_unix_request,
                str(endpoint),
                _request(),
            )
            assert daemon_protocol.parse_hook_response(response)["exit_code"] == 0
            restarting = await anyio.to_thread.run_sync(
                daemon_client._send_unix_request,
                str(endpoint),
                _request(version="version-skew"),
            )
            assert restarting == {"status": "restarting"}

        # Server drained; the queued event send is still parked on the wire
        # gate, so nothing has been delivered yet.
        assert event_requests == []

        close_done = threading.Event()

        def close_runtime() -> None:
            runtime.close()
            close_done.set()

        closer = threading.Thread(target=close_runtime)
        closer.start()
        # close() blocks on the bounded flush while the send is gated ...
        assert not await anyio.to_thread.run_sync(close_done.wait, 0.2)
        release_send.set()
        # ... and completes once the queued send lands.
        assert await anyio.to_thread.run_sync(close_done.wait, 5)
        closer.join(timeout=5)
        assert not closer.is_alive()
    finally:
        release_send.set()
        runtime.close()

    assert len(event_requests) == 1
    assert event_requests[0].url.path == "/api/v1/hooks/events"
    body = json.loads(event_requests[0].content)
    assert body["event_name"] == "PreToolUse"


@pytest.mark.asyncio
async def test_hook_does_not_dispatch_without_client_accept_ack(endpoint) -> None:
    ready = anyio.Event()
    hook_calls = 0

    def run_hook() -> None:
        nonlocal hook_calls
        hook_calls += 1

    def disconnect_after_accept() -> None:
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as client:
            client.connect(str(endpoint))
            with client.makefile("rwb", buffering=0) as stream:
                write_frame(stream, _request())
                assert read_frame(stream) == {"status": "accepted"}

    async with anyio.create_task_group() as tasks:
        tasks.start_soon(
            partial(
                server.serve_daemon,
                endpoint=str(endpoint),
                gate_check=lambda: True,
                ready=ready.set,
                hook_runner=run_hook,
            )
        )
        await ready.wait()
        await anyio.to_thread.run_sync(disconnect_after_accept)
        await anyio.sleep(0.05)
        assert hook_calls == 0
        assert await anyio.to_thread.run_sync(
            daemon_client._send_unix_request,
            str(endpoint),
            _request(version="version-skew"),
        ) == {"status": "restarting"}


@pytest.mark.asyncio
async def test_connection_limit_queues_hook_until_slot_is_available(
    endpoint, monkeypatch
) -> None:
    ready = anyio.Event()
    hook_started = threading.Event()
    release_hook = threading.Event()
    hook_calls = 0
    first_response: object | None = None
    second_response: object | None = None
    monkeypatch.setattr(server, "_MAX_CONCURRENT_CONNECTIONS", 1)

    def run_hook() -> None:
        nonlocal hook_calls
        hook_calls += 1
        hook_started.set()
        if hook_calls == 1:
            assert release_hook.wait(timeout=5)

    async def send_first() -> None:
        nonlocal first_response
        first_response = await anyio.to_thread.run_sync(
            daemon_client._send_unix_request,
            str(endpoint),
            _request(),
        )

    async def send_second() -> None:
        nonlocal second_response
        second_response = await anyio.to_thread.run_sync(
            daemon_client._send_unix_request,
            str(endpoint),
            _request(),
        )

    try:
        async with anyio.create_task_group() as tasks:
            tasks.start_soon(
                partial(
                    server.serve_daemon,
                    endpoint=str(endpoint),
                    gate_check=lambda: True,
                    ready=ready.set,
                    hook_runner=run_hook,
                )
            )
            await ready.wait()
            tasks.start_soon(send_first)
            assert await anyio.to_thread.run_sync(hook_started.wait, 5)
            tasks.start_soon(send_second)
            await anyio.sleep(0.05)
            assert second_response is None
            release_hook.set()
            with anyio.fail_after(2):
                while first_response is None or second_response is None:
                    await anyio.sleep(0)
            assert hook_calls == 2
            with anyio.fail_after(2):
                while True:
                    try:
                        await anyio.to_thread.run_sync(
                            daemon_client._send_unix_request,
                            str(endpoint),
                            _request(version="version-skew"),
                        )
                    except (daemon_protocol.FrameError, OSError):
                        await anyio.sleep(0.01)
                    else:
                        break
    finally:
        release_hook.set()

    assert hook_calls == 2


@pytest.mark.asyncio
async def test_connection_queue_timeout_closes_waiting_hook(
    endpoint, monkeypatch
) -> None:
    ready = anyio.Event()
    hook_started = threading.Event()
    release_hook = threading.Event()
    first_done = anyio.Event()
    second_done = anyio.Event()
    gate_open = True
    hook_calls = 0
    first_response: daemon_protocol.HookResult | None = None
    second_response: daemon_protocol.HookResult | None = None
    monkeypatch.setattr(server, "_MAX_CONCURRENT_CONNECTIONS", 1)
    monkeypatch.setattr(server, "_CONNECTION_QUEUE_TIMEOUT_SECONDS", 0.05)
    monkeypatch.setattr(daemon_client, "daemon_endpoint", lambda: str(endpoint))
    monkeypatch.setattr(daemon_client, "daemon_is_enabled", lambda: True)

    def run_hook() -> None:
        nonlocal hook_calls
        hook_calls += 1
        if hook_io.read_stdin() == "first":
            hook_started.set()
            assert release_hook.wait(timeout=5)

    async def send_first() -> None:
        nonlocal first_response
        first_response = await anyio.to_thread.run_sync(
            daemon_client.try_daemon_hook,
            "first",
        )
        first_done.set()

    async def send_second() -> None:
        nonlocal second_response
        second_response = await anyio.to_thread.run_sync(
            daemon_client.try_daemon_hook,
            "second",
        )
        second_done.set()

    async with anyio.create_task_group() as tasks:
        try:
            tasks.start_soon(
                partial(
                    server.serve_daemon,
                    endpoint=str(endpoint),
                    gate_check=lambda: gate_open,
                    gate_check_interval=0.01,
                    ready=ready.set,
                    hook_runner=run_hook,
                )
            )
            await ready.wait()
            tasks.start_soon(send_first)
            assert await anyio.to_thread.run_sync(hook_started.wait, 5)
            tasks.start_soon(send_second)
            with anyio.fail_after(1):
                await second_done.wait()
            assert second_response is None
            assert hook_calls == 1
            release_hook.set()
            with anyio.fail_after(1):
                await first_done.wait()
            gate_open = False
        finally:
            release_hook.set()
            gate_open = False

    assert first_response == {"stdout": "", "stderr": "", "exit_code": 0}
    assert hook_calls == 1


@pytest.mark.asyncio
async def test_connection_queue_sheds_hooks_beyond_bounded_waiters(
    endpoint, monkeypatch
) -> None:
    ready = anyio.Event()
    hook_started = threading.Event()
    release_hook = threading.Event()
    gate_open = True
    hook_calls: list[str] = []
    responses: dict[str, daemon_protocol.HookResult | None] = {}
    done = {label: anyio.Event() for label in ("first", "second", "third")}
    monkeypatch.setattr(server, "_MAX_CONCURRENT_CONNECTIONS", 1)
    monkeypatch.setattr(server, "_MAX_QUEUED_CONNECTIONS", 1, raising=False)
    monkeypatch.setattr(daemon_client, "daemon_endpoint", lambda: str(endpoint))
    monkeypatch.setattr(daemon_client, "daemon_is_enabled", lambda: True)

    def run_hook() -> None:
        label = hook_io.read_stdin()
        hook_calls.append(label)
        if label == "first":
            hook_started.set()
            assert release_hook.wait(timeout=5)

    async def send(label: str) -> None:
        responses[label] = await anyio.to_thread.run_sync(
            daemon_client.try_daemon_hook,
            label,
        )
        done[label].set()

    async with anyio.create_task_group() as tasks:
        try:
            tasks.start_soon(
                partial(
                    server.serve_daemon,
                    endpoint=str(endpoint),
                    gate_check=lambda: gate_open,
                    gate_check_interval=0.01,
                    ready=ready.set,
                    hook_runner=run_hook,
                )
            )
            await ready.wait()
            tasks.start_soon(send, "first")
            assert await anyio.to_thread.run_sync(hook_started.wait, 5)
            tasks.start_soon(send, "second")
            await anyio.sleep(0.05)
            tasks.start_soon(send, "third")
            with anyio.fail_after(1):
                await done["third"].wait()
            assert responses["third"] is None
            assert hook_calls == ["first"]
            assert not done["second"].is_set()

            release_hook.set()
            with anyio.fail_after(2):
                await done["first"].wait()
                await done["second"].wait()
            gate_open = False
        finally:
            release_hook.set()
            gate_open = False

    assert responses["first"] == {"stdout": "", "stderr": "", "exit_code": 0}
    assert responses["second"] == {"stdout": "", "stderr": "", "exit_code": 0}
    assert hook_calls == ["first", "second"]


@pytest.mark.asyncio
async def test_second_unix_daemon_is_rejected(endpoint) -> None:
    ready = anyio.Event()

    async with anyio.create_task_group() as tasks:
        tasks.start_soon(
            partial(
                server.serve_daemon,
                endpoint=str(endpoint),
                gate_check=lambda: True,
                ready=ready.set,
                hook_runner=lambda: None,
            )
        )
        await ready.wait()
        with pytest.raises(server.DaemonAlreadyRunning):
            await server.serve_daemon(
                endpoint=str(endpoint),
                gate_check=lambda: True,
                hook_runner=lambda: None,
            )
        await anyio.to_thread.run_sync(
            daemon_client._send_unix_request,
            str(endpoint),
            _request(version="version-skew"),
        )


def test_unix_daemon_lock_serializes_stale_socket_replacement(endpoint) -> None:
    server._prepare_unix_parent(endpoint)
    first = server._acquire_unix_lock(endpoint)
    try:
        with pytest.raises(BlockingIOError):
            server._acquire_unix_lock(endpoint)
    finally:
        os.close(first)

    replacement = server._acquire_unix_lock(endpoint)
    os.close(replacement)


@pytest.mark.asyncio
async def test_gate_off_drains_listener(endpoint) -> None:
    ready = anyio.Event()

    await server.serve_daemon(
        endpoint=str(endpoint),
        gate_check=lambda: False,
        gate_check_interval=0.01,
        ready=ready.set,
        hook_runner=lambda: None,
    )

    assert ready.is_set()
    assert not endpoint.exists()


def test_run_daemon_is_noop_when_platform_has_no_endpoint(monkeypatch) -> None:
    """Gate open on Linux must exit cleanly, like gate-off/already-running."""
    from runlayer_cli.daemon import runtime as daemon_runtime

    class FakeRuntime:
        def __init__(self) -> None:
            self.closed = False

        def install(self) -> None:
            pass

        def daemon_is_enabled(self) -> bool:
            return True

        def before_hook(self) -> None:
            pass

        def prewarm_background(self, *, force: bool = False) -> None:
            pass

        def close(self) -> None:
            self.closed = True

    fake = FakeRuntime()
    monkeypatch.setattr(daemon_runtime, "DaemonRuntime", lambda: fake)

    def unsupported() -> str:
        raise daemon_protocol.UnsupportedDaemonPlatform("no daemon endpoint")

    monkeypatch.setattr(server, "daemon_endpoint", unsupported)

    server.run_daemon()

    assert fake.closed


@pytest.mark.asyncio
async def test_unix_socket_permissions_are_owner_only(endpoint) -> None:
    ready = anyio.Event()
    socket_modes: list[int] = []

    def capture_modes() -> None:
        socket_modes.extend(
            [
                stat.S_IMODE(endpoint.parent.stat().st_mode),
                stat.S_IMODE(endpoint.stat().st_mode),
            ]
        )
        ready.set()

    async with anyio.create_task_group() as tasks:
        tasks.start_soon(
            partial(
                server.serve_daemon,
                endpoint=str(endpoint),
                gate_check=lambda: False,
                gate_check_interval=0.01,
                ready=capture_modes,
                hook_runner=lambda: None,
            )
        )
        await ready.wait()

    assert socket_modes == [0o700, 0o600]


@pytest.mark.asyncio
async def test_windows_response_ack_wait_is_bounded_by_client_read_timeout(
    monkeypatch,
) -> None:
    monkeypatch.setattr(server.sys, "platform", "win32")
    monkeypatch.setattr(server, "_REQUEST_READ_TIMEOUT_SECONDS", 0.05)
    sent: list[bytes] = []

    class SilentClient:
        async def send(self, item: bytes) -> None:
            sent.append(item)

        async def wait_for_client_ack(self, expected: bytes) -> None:
            await anyio.sleep(math.inf)

    result: daemon_protocol.HookResult = {
        "stdout": "out",
        "stderr": "",
        "exit_code": 0,
    }
    with anyio.fail_after(1):
        await server._send_response(SilentClient(), result)

    assert sent == [daemon_protocol.encode_frame(result)]


def test_system_exit_string_matches_python_stderr_semantics() -> None:
    result = server._run_hook_request(
        _request(),
        lambda: (_ for _ in ()).throw(SystemExit("fatal")),
    )

    assert result == {"stdout": "", "stderr": "fatal\n", "exit_code": 1}


def test_daemon_request_marks_only_its_hook_context_as_daemon_served() -> None:
    observed: list[bool] = []

    server._run_hook_request(
        _request(),
        lambda: observed.append(hook_io.is_daemon_served()),
    )

    assert observed == [True]
    assert not hook_io.is_daemon_served()
