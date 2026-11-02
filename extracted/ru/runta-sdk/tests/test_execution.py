from __future__ import annotations

import asyncio
import base64
import json
import os
from pathlib import Path
import signal
import select
import subprocess
import time
from types import SimpleNamespace
import uuid
from contextlib import asynccontextmanager, contextmanager
from unittest.mock import AsyncMock, Mock

import pytest
from websockets.asyncio.server import serve
from websockets.exceptions import ConnectionClosed

from runta import CommandResult, ExecutionError
from runta._internal.execution import AsyncExecution, Execution
from runta._internal import execution
from runta._internal.streaming_transfer import async_execute, execute


def runtime(http):
    return SimpleNamespace(id="runtime-test", _client=SimpleNamespace(_http=http))


@pytest.fixture
def guest_root(tmp_path, monkeypatch):
    root = tmp_path / "tasks"
    monkeypatch.setattr(execution, "_ROOT", str(root))
    yield root
    # Test failures must not leave detached commands on the developer machine.
    for task in root.glob("*"):
        for name in ("command.identity", "supervisor.identity"):
            identity = task / name
            if identity.exists():
                pid = int(identity.read_text().split()[0])
                try:
                    if name == "command.identity":
                        os.killpg(pid, signal.SIGKILL)
                    else:
                        os.kill(pid, signal.SIGTERM)
                except ProcessLookupError:
                    pass


def launch(root, command, *, timeout=None, limit=1024, env=None, stdin=None):
    task = root / str(uuid.uuid4())
    data = stdin.encode() if isinstance(stdin, str) else stdin or b""
    body = execution._bootstrap(
        str(task),
        "sh",
        ["-c", command],
        env=env,
        timeout=timeout,
        limit=limit,
        stdin_size=len(data),
    )
    observer = subprocess.Popen(
        ["sh", "-c", body],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        stdin=subprocess.PIPE,
        start_new_session=True,
    )
    observer.stdin.write(data)
    observer.stdin.close()
    observer.stdin = None
    return task, observer


def wait_result(task, timeout=10):
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if (task / "result").exists():
            return execution._parse_state((task / "result").read_bytes().strip())
        time.sleep(0.02)
    pytest.fail(f"Task did not finish: {task}")


def ready(task):
    deadline = time.monotonic() + 5
    while not (task / "go").exists():
        assert time.monotonic() < deadline
        time.sleep(0.02)


@pytest.mark.parametrize(
    "limit,size,truncated",
    [(0, 1, True), (3, 3, False), (3, 4, True), (7, 100000, True)],
)
def test_guest_output_is_capped_and_drained(guest_root, limit, size, truncated):
    task, observer = launch(
        guest_root,
        f"head -c {size} /dev/zero; head -c {size} /dev/zero >&2; exit 7",
        limit=limit,
    )
    stdout, stderr = observer.communicate(timeout=10)
    assert observer.returncode == 0, stderr
    state = wait_result(task)
    assert state.exit_code == 7
    assert state.stdout_truncated is truncated
    assert state.stderr_truncated is truncated
    assert (task / "stdout").read_bytes() == b"\0" * min(limit, size)
    assert (task / "stderr").read_bytes() == b"\0" * min(limit, size)
    assert not list(task.glob("*.raw"))
    assert b"RUNTA_EXEC_RESULT_V2 completed" in stdout


def test_observer_group_can_die_without_killing_task(guest_root):
    task, observer = launch(guest_root, "sleep 0.5; printf done")
    ready(task)
    os.killpg(observer.pid, signal.SIGKILL)
    observer.communicate(timeout=2)
    state = wait_result(task)
    assert state.exit_code == 0
    assert (task / "stdout").read_bytes() == b"done"
    # Reattach after completion; no command is relaunched.
    reattached = subprocess.run(
        ["sh", str(task / "control.sh"), "watch", str(task)],
        capture_output=True,
        timeout=2,
    )
    assert reattached.returncode == 0
    assert b"completed" in reattached.stdout


def test_guest_timeout_and_cancel_reclaim_descendants(guest_root):
    for timeout in (0.15, None):
        child_path = guest_root.parent / f"child-{timeout}"
        task, observer = launch(
            guest_root,
            f"sleep 60 & printf '%s' $! > '{child_path}'; wait",
            timeout=timeout,
        )
        ready(task)
        if timeout is None:
            result = subprocess.run(
                ["sh", str(task / "control.sh"), "cancel", str(task)],
                capture_output=True,
                timeout=2,
            )
            assert result.returncode == 0
        observer.communicate(timeout=8)
        state = wait_result(task)
        assert state.status == ("timed_out" if timeout else "cancelled")
        assert state.exit_code == (124 if timeout else 143)
        child_stat = Path(f"/proc/{child_path.read_text()}/stat")
        assert not child_stat.exists() or child_stat.read_text().split()[2] == "Z"
        if timeout:
            assert b"Command timed out" in (task / "stderr").read_bytes()


def test_binary_input_and_user_environment_do_not_change_supervisor(guest_root):
    task, observer = launch(
        guest_root,
        "cat; printf '%s' \"$VALUE\"",
        stdin=b"\0\xffabc",
        env={"VALUE": "a ' \n b", "RUNTA_EXEC_V1": "user value"},
    )
    observer.communicate(timeout=5)
    assert wait_result(task).exit_code == 0
    assert (task / "stdout").read_bytes() == b"\0\xffabca ' \n b"
    assert (task.stat().st_mode & 0o777) == 0o700
    assert all((p.stat().st_mode & 0o077) == 0 for p in task.iterdir())


def test_timeout_kills_children_that_ignore_term(guest_root):
    child_path = guest_root.parent / "stubborn-child"
    task, observer = launch(
        guest_root,
        f"trap '' TERM; sleep 60 & printf '%s' $! > '{child_path}'; wait",
        timeout=0.2,
    )
    observer.communicate(timeout=9)
    state = wait_result(task)
    assert state.exit_code == 124
    assert state.duration >= 5
    child_stat = Path(f"/proc/{child_path.read_text()}/stat")
    assert not child_stat.exists() or child_stat.read_text().split()[2] == "Z"


def test_pid_identity_mismatch_reports_lost_and_does_not_signal(guest_root):
    task, observer = launch(guest_root, "sleep 1")
    ready(task)
    original = (task / "supervisor.identity").read_text()
    fields = original.split()
    fields[1] = str(int(fields[1]) + 1)
    (task / "supervisor.identity").write_text(" ".join(fields) + "\n")
    status = subprocess.run(
        ["sh", str(task / "control.sh"), "status", str(task)],
        capture_output=True,
        timeout=2,
    )
    assert status.stdout == b"RUNTA_EXEC_V1 lost\n"
    cancel = subprocess.run(
        ["sh", str(task / "control.sh"), "cancel", str(task)],
        capture_output=True,
        timeout=2,
    )
    assert cancel.returncode == 1
    (task / "supervisor.identity").write_text(original)
    observer.communicate(timeout=5)
    assert wait_result(task).exit_code == 0


@pytest.mark.parametrize(
    "line",
    [
        b"wrong running",
        b"RUNTA_EXEC_V1 completed 0 2 0 1",
        b"RUNTA_EXEC_V1 completed 0 0 0 nan",
        b"RUNTA_EXEC_V1 cancelled",
        b"RUNTA_EXEC_V1 running extra",
    ],
)
def test_invalid_state_is_rejected(line):
    with pytest.raises(execution._public.ApiError):
        execution._parse_state(line)


def test_observation_handles_split_frames():
    parser = execution._Observation()
    assert parser.feed(b"RUNTA_EXEC_") == []
    states = parser.feed(b"V1 running\nRUNTA_EXEC_V1 completed 0 0 0 1.25\n")
    assert [s.status for s in states] == ["running", "completed"]


@pytest.mark.asyncio
@pytest.mark.parametrize("sync", [False, True])
async def test_output_snapshots_show_small_writes_before_completion(guest_root, sync):
    release = guest_root.parent / "release"
    next_write = guest_root.parent / "next-write"
    task, observer = launch(
        guest_root,
        f"printf ready; printf error >&2; while test ! -f '{next_write}'; do sleep 0.1; done; "
        f"printf later; printf later >&2; while test ! -f '{release}'; do sleep 0.1; done",
    )
    ready(task)

    def read_file(runtime_id, path):
        try:
            return Path(path).read_bytes()
        except FileNotFoundError as exc:
            raise execution._public.ApiError("not found", status_code=404) from exc

    def short(runtime_id, command, args, **kwargs):
        result = subprocess.run([command, *args], capture_output=True, timeout=2)
        return CommandResult(result.returncode, result.stdout, result.stderr, 0)

    http = SimpleNamespace(retry_max_attempts=1)
    http.read_file = read_file if sync else AsyncMock(side_effect=read_file)
    http.execute = short if sync else AsyncMock(side_effect=short)
    handle = (Execution if sync else AsyncExecution)(runtime(http), task.name)
    try:
        deadline = time.monotonic() + 2
        snapshot = (b"", b"")
        while snapshot != (b"ready", b"error") and time.monotonic() < deadline:
            snapshot = handle.output() if sync else await handle.output()
            await asyncio.sleep(0.02)
        assert not (task / "result").exists()
        assert snapshot == (b"ready", b"error")
        next_write.touch()
        deadline = time.monotonic() + 2
        while (
            snapshot != (b"readylater", b"errorlater") and time.monotonic() < deadline
        ):
            snapshot = handle.output() if sync else await handle.output()
            await asyncio.sleep(0.02)
        assert not (task / "result").exists()
        assert snapshot == (b"readylater", b"errorlater")
    finally:
        next_write.touch()
        release.touch()
        observer.communicate(timeout=5)


@pytest.mark.asyncio
@pytest.mark.parametrize("sync", [False, True])
@pytest.mark.parametrize("finalized", [False, True])
async def test_output_snapshot_handles_completion_between_status_and_read(
    sync, finalized
):
    state = (
        execution.ExecutionState("completed", 0)
        if finalized
        else execution.ExecutionState("running")
    )
    states = [execution.ExecutionState("running"), state]
    paths = []

    def read(runtime_id, path):
        paths.append(path)
        if path.endswith("/limit"):
            return b"1024"
        if path.endswith(".raw"):
            raise execution._public.ApiError("not found", status_code=404)
        return b"ready" if path.endswith("/stdout") else b"error"

    http = SimpleNamespace(
        retry_max_attempts=1, read_file=read if sync else AsyncMock(side_effect=read)
    )
    handle = (Execution if sync else AsyncExecution)(runtime(http), str(uuid.uuid4()))
    handle.status = (
        Mock(side_effect=[*states, state])
        if sync
        else AsyncMock(side_effect=[*states, state])
    )
    result = handle.output() if sync else await handle.output()
    assert result == (b"ready", b"error")
    assert any(path.endswith("/stdout") for path in paths)
    assert any(path.endswith("/stderr") for path in paths)


def test_script_content_cannot_close_its_literal_boundary(tmp_path, monkeypatch):
    output = tmp_path / "script"
    injected = tmp_path / "injected"
    marker = "RUNTA_" + "0" * 32
    content = f"before\n{marker}\nprintf injected > '{injected}'\ncat >/dev/null <<'{marker}'\nafter"
    monkeypatch.setattr(execution.uuid, "uuid4", lambda: SimpleNamespace(hex="0" * 32))
    result = subprocess.run(
        ["sh", "-c", execution._write_script(str(output), content)],
        capture_output=True,
        timeout=2,
    )
    assert result.returncode == 0
    assert not injected.exists()
    assert output.read_text() == content + "\n"


@pytest.mark.asyncio
@pytest.mark.parametrize("sync", [False, True])
@pytest.mark.parametrize("lose_completion", [False, "header", "body"])
async def test_real_websocket_disconnect_reconnect_and_finish(
    guest_root, monkeypatch, sync, lose_completion
):
    bodies = []
    disconnected = 0
    completion_dropped = False

    async def handler(ws):
        nonlocal disconnected
        proc = None
        workers = []
        try:
            start = json.loads(await ws.recv())
            bodies.append(start["args"][1])
            proc = await asyncio.create_subprocess_exec(
                start["command"],
                *start["args"],
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                start_new_session=True,
            )

            async def forward(reader, kind):
                nonlocal disconnected, completion_dropped
                while data := await reader.read(4096):
                    if (
                        lose_completion
                        and not completion_dropped
                        and b"RUNTA_EXEC_RESULT_V2 completed" in data
                    ):
                        completion_dropped = True
                        if lose_completion == "body":
                            end = (
                                data.index(b"\n", data.index(b"RUNTA_EXEC_RESULT_V2"))
                                + 1
                            )
                            # The header and cat output may arrive in different
                            # pipe reads. Drop after one actual payload byte.
                            partial = data[:end] + (
                                data[end : end + 1] or await reader.read(1)
                            )
                            assert len(partial) == end + 1
                            await ws.send(
                                json.dumps(
                                    {
                                        "type": kind,
                                        "data_base64": base64.b64encode(
                                            partial
                                        ).decode(),
                                    }
                                )
                            )
                        await ws.close(code=1011, reason="lost completion message")
                        return
                    await ws.send(
                        json.dumps(
                            {
                                "type": kind,
                                "data_base64": base64.b64encode(data).decode(),
                            }
                        )
                    )
                    if (
                        kind == "stdout"
                        and b"RUNTA_EXEC_V1 running" in data
                        and disconnected < 3
                    ):
                        disconnected += 1
                        await ws.close(code=1011, reason="injected disconnect")
                        return

            async def input_frames():
                async for raw in ws:
                    frame = json.loads(raw)
                    if frame["type"] == "close_stdin":
                        proc.stdin.close()
                    elif frame["type"] == "stdin":
                        proc.stdin.write(base64.b64decode(frame["data_base64"]))
                        await proc.stdin.drain()
                    elif frame["type"] == "heartbeat":
                        await ws.send('{"type":"heartbeat"}')

            workers = [
                asyncio.create_task(forward(proc.stdout, "stdout")),
                asyncio.create_task(forward(proc.stderr, "stderr")),
                asyncio.create_task(input_frames()),
            ]
            done, _ = await asyncio.wait(
                [*workers, asyncio.create_task(proc.wait())],
                return_when=asyncio.FIRST_COMPLETED,
            )
            if workers[2] in done or disconnected and not ws.state.name == "OPEN":
                return
            await proc.wait()
            await asyncio.gather(*workers[:2])
            await ws.send(json.dumps({"type": "exit", "code": proc.returncode}))
        except ConnectionClosed:
            pass
        finally:
            if proc:
                try:
                    os.killpg(proc.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
                await proc.wait()
            for worker in workers:
                worker.cancel()
            await asyncio.gather(*workers, return_exceptions=True)

    async with serve(handler, "127.0.0.1", 0) as server:
        port = server.sockets[0].getsockname()[1]
        endpoint = f"http://127.0.0.1:{port}"
        http = SimpleNamespace(
            endpoint=endpoint, token="test", timeout=2, retry_max_attempts=3
        )
        if sync:
            http.read_file = Mock(
                side_effect=lambda runtime_id, path: Path(path).read_bytes()
            )
            http.execute = lambda runtime_id, cmd, args, **kw: execute(
                endpoint,
                "test",
                runtime_id,
                cmd,
                args,
                env=None,
                stdin=None,
                timeout=kw.get("timeout"),
                max_output_bytes=None,
                connect_timeout=2,
            )
            task_cls = Execution
        else:
            http.read_file = AsyncMock(
                side_effect=lambda runtime_id, path: Path(path).read_bytes()
            )
            http.execute = lambda runtime_id, cmd, args, **kw: async_execute(
                endpoint,
                "test",
                runtime_id,
                cmd,
                args,
                env=None,
                stdin=None,
                timeout=kw.get("timeout"),
                max_output_bytes=None,
                connect_timeout=2,
            )
            task_cls = AsyncExecution
        monkeypatch.setattr(execution, "_delay", lambda *args: 0)
        marker = guest_root.parent / "invocations"
        task = task_cls._new(
            runtime(http),
            f"printf x >> '{marker}'; sleep 2.5; cat >/dev/null; printf answer; printf error >&2; exit 9",
            timeout=None,
            env=None,
            stdin=b"\0\xff" * 100000,
            cwd=None,
            max_output_bytes=4,
        )
        result = await asyncio.to_thread(task.wait) if sync else await task.wait()
        assert result.exit_code == 9
        assert result.stdout == b"answ"
        assert result.stderr == b"erro"
        assert result.stdout_truncated and result.stderr_truncated
        assert disconnected == 3
        assert completion_dropped is bool(lose_completion)
        http.read_file.assert_not_called()
        assert marker.read_text() == "x"
        assert sum("mkdir -m 700" in body for body in bodies) == 1
        assert any("control.sh watch" in body for body in bodies[1:])
        assert not Path(task._directory).exists()


@pytest.mark.asyncio
async def test_async_cancellation_requests_guest_cancellation():
    http = SimpleNamespace(
        execute=AsyncMock(return_value=CommandResult(0, b"", b"", 0)),
        retry_max_attempts=2,
    )
    task = AsyncExecution(runtime(http), str(uuid.uuid4()))
    entered = asyncio.Event()

    async def observe(healthy):
        entered.set()
        await asyncio.Event().wait()

    task._observe = observe
    waiter = asyncio.create_task(task.wait())
    await entered.wait()
    waiter.cancel()
    with pytest.raises(asyncio.CancelledError):
        await waiter
    assert " cancel " in http.execute.await_args.args[2][1]


@pytest.mark.asyncio
@pytest.mark.parametrize("sync", [False, True])
async def test_idle_socket_reconnects_only_to_observe(sync, monkeypatch):
    bodies = []
    http = SimpleNamespace(
        endpoint="http://test", token="test", timeout=1, retry_max_attempts=2
    )
    task = (Execution if sync else AsyncExecution)(runtime(http), str(uuid.uuid4()))
    task._launch = "initial launch"
    monkeypatch.setattr(execution, "_IDLE_TIMEOUT", 0.01)
    monkeypatch.setattr(execution, "_delay", lambda *args: 0)

    if sync:

        class IdleSocket:
            def send(self, raw):
                frame = json.loads(raw)
                if frame["type"] == "start":
                    bodies.append(frame["args"][1])

            def recv(self, *, timeout):
                assert 0 <= timeout <= 0.01
                raise TimeoutError("idle connection")

        @contextmanager
        def socket_context(*args, **kwargs):
            yield IdleSocket()

        monkeypatch.setattr(execution, "_sync_socket", socket_context)
    else:

        class IdleSocket:
            async def send(self, raw):
                frame = json.loads(raw)
                if frame["type"] == "start":
                    bodies.append(frame["args"][1])

            async def recv(self):
                await asyncio.Event().wait()

        @asynccontextmanager
        async def socket_context(*args, **kwargs):
            yield IdleSocket()

        monkeypatch.setattr(execution, "_async_socket", socket_context)

    with pytest.raises(ExecutionError):
        if sync:
            task.wait()
        else:
            await task.wait()
    assert bodies[0] == "initial launch"
    assert len(bodies) == 2
    assert "control.sh watch" in bodies[1]


@pytest.mark.parametrize("sync", [False, True])
@pytest.mark.asyncio
async def test_reconnect_exhaustion_keeps_recovery_id(sync, monkeypatch):
    http = SimpleNamespace(retry_max_attempts=2)
    task = (Execution if sync else AsyncExecution)(runtime(http), str(uuid.uuid4()))
    task._observe = (
        Mock(side_effect=ConnectionError("offline"))
        if sync
        else AsyncMock(side_effect=ConnectionError("offline"))
    )
    monkeypatch.setattr(execution, "_delay", lambda *args: 0)
    with pytest.raises(ExecutionError) as exc:
        if sync:
            task.wait()
        else:
            await task.wait()
    assert exc.value.execution_id == task.id
    assert task._observe.call_count == 2


def test_bootstrap_dependency_failure_is_explicit(guest_root, tmp_path):
    task = guest_root / str(uuid.uuid4())
    bootstrap = execution._bootstrap(
        str(task), "true", [], env=None, timeout=None, limit=1
    )
    result = subprocess.run(
        ["/bin/sh", "-c", bootstrap],
        env={"PATH": str(tmp_path)},
        capture_output=True,
        timeout=2,
    )
    assert result.returncode == 127
    assert b"Missing execution dependency: setsid" in result.stderr
    assert not task.exists()


@pytest.mark.asyncio
@pytest.mark.parametrize("sync", [False, True])
@pytest.mark.parametrize("running", [False, True])
async def test_output_above_rest_file_limit_uses_streaming_snapshot(sync, running):
    limit = 4 * 1024 * 1024
    payload = bytes(range(256)) * (limit // 256)
    downloaded_paths = []

    def read(runtime_id, path):
        if path.endswith("/limit"):
            return str(limit).encode()
        raise execution._public.ApiError(
            "file is too large to return through the API; maximum is 1048576 bytes",
            status_code=422,
            code="invalid_argument",
        )

    def snapshot(runtime_id, command, args, **kwargs):
        assert command == "sh" and args[1] == execution._SNAPSHOT_SCRIPT
        downloaded_paths.append(args[3])
        assert kwargs["max_output_bytes"] == limit
        assert kwargs["timeout"] is None
        assert kwargs["idle_timeout"] == 30
        return CommandResult(0, payload, b"", 0)

    http = SimpleNamespace(
        retry_max_attempts=1,
        read_file=read if sync else AsyncMock(side_effect=read),
        execute=snapshot if sync else AsyncMock(side_effect=snapshot),
    )
    handle = (Execution if sync else AsyncExecution)(runtime(http), str(uuid.uuid4()))
    state = execution.ExecutionState("running" if running else "completed", 0)
    output = handle._output(state) if sync else await handle._output(state)
    assert output == (payload, payload)
    assert len(downloaded_paths) == 2
    assert all(path.endswith(".raw") == running for path in downloaded_paths)


@pytest.mark.asyncio
@pytest.mark.parametrize("sync", [False, True])
async def test_output_does_not_hide_unrelated_file_errors(sync):
    error = execution._public.ApiError("invalid file path", status_code=422)
    http = SimpleNamespace(
        retry_max_attempts=1,
        read_file=Mock(side_effect=error) if sync else AsyncMock(side_effect=error),
        execute=Mock() if sync else AsyncMock(),
    )
    handle = (Execution if sync else AsyncExecution)(runtime(http), str(uuid.uuid4()))
    with pytest.raises(ExecutionError, match="invalid file path"):
        if sync:
            handle._output(execution.ExecutionState("completed", 0))
        else:
            await handle._output(execution.ExecutionState("completed", 0))
    http.execute.assert_not_called()


@pytest.mark.asyncio
@pytest.mark.parametrize("sync", [False, True])
@pytest.mark.parametrize(
    "race",
    [
        "append",
        "remove_before_open",
        "remove_after_open",
        "disconnect",
        "stall",
        "slow",
    ],
)
async def test_streaming_snapshot_survives_collector_changes(
    tmp_path, sync, race, monkeypatch
):
    monkeypatch.setattr(execution, "_delay", lambda *args: 0)
    monkeypatch.setattr(execution, "_IDLE_TIMEOUT", 0.1)
    task_directory = tmp_path / str(uuid.uuid4())
    task_directory.mkdir()
    payload = bytes(range(256)) * 8192
    raw = task_directory / "stdout.raw"
    raw.write_bytes(payload)
    (task_directory / "stderr.raw").write_bytes(b"")
    (task_directory / "stderr").write_bytes(b"")
    changed = False
    commands = []

    async def handler(ws):
        nonlocal changed
        frame = json.loads(await ws.recv())
        assert frame["type"] == "start"
        commands.append(frame["args"])
        assert json.loads(await ws.recv())["type"] == "close_stdin"
        if race == "remove_before_open" and not changed:
            raw.rename(task_directory / "stdout")
            changed = True
        process = await asyncio.create_subprocess_exec(
            frame["command"],
            *frame["args"],
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            start_new_session=True,
        )
        try:
            while chunk := await process.stdout.read(65536):
                if not changed:
                    if race == "append":
                        with raw.open("ab") as output:
                            output.write(b"later" * 65536)
                    elif race == "remove_after_open":
                        raw.unlink()
                    changed = True
                await ws.send(
                    json.dumps(
                        {
                            "type": "stdout",
                            "data_base64": base64.b64encode(chunk).decode(),
                        }
                    )
                )
                if len(commands) == 1 and race == "disconnect":
                    await ws.close(code=1011, reason="injected snapshot disconnect")
                    return
                if len(commands) == 1 and race == "stall":
                    # Heartbeats must not keep a snapshot with no data alive.
                    for _ in range(4):
                        await ws.send('{"type":"heartbeat"}')
                        await asyncio.sleep(0.04)
                    return
                if race == "slow":
                    await asyncio.sleep(0.02)
            errors = await process.stderr.read()
            await ws.send(
                json.dumps(
                    {
                        "type": "stderr",
                        "data_base64": base64.b64encode(errors).decode(),
                    }
                )
            )
            await ws.send(json.dumps({"type": "exit", "code": await process.wait()}))
        finally:
            if process.returncode is None:
                os.killpg(process.pid, signal.SIGKILL)
            await process.communicate()

    def read(runtime_id, path):
        if path.endswith("/limit"):
            return b"4194304"
        try:
            data = Path(path).read_bytes()
        except FileNotFoundError as exc:
            raise execution._public.ApiError("not found", status_code=404) from exc
        if len(data) > 1024 * 1024:
            raise execution._public.ApiError("file is too large", status_code=422)
        return data

    async with serve(handler, "127.0.0.1", 0) as server:
        endpoint = f"http://127.0.0.1:{server.sockets[0].getsockname()[1]}"
        http = SimpleNamespace(
            retry_max_attempts=2,
            read_file=read if sync else AsyncMock(side_effect=read),
        )
        if sync:
            http.execute = lambda rid, command, args, **kw: execute(
                endpoint,
                "test",
                rid,
                command,
                args,
                env=None,
                stdin=None,
                connect_timeout=2,
                **kw,
            )
        else:
            http.execute = lambda rid, command, args, **kw: async_execute(
                endpoint,
                "test",
                rid,
                command,
                args,
                env=None,
                stdin=None,
                connect_timeout=2,
                **kw,
            )
        task = (Execution if sync else AsyncExecution)(
            runtime(http), task_directory.name
        )
        task._directory = str(task_directory)
        task.status = (
            Mock(return_value=execution.ExecutionState("completed", 0))
            if sync
            else AsyncMock(return_value=execution.ExecutionState("completed", 0))
        )
        output = (
            await asyncio.to_thread(task._output, execution.ExecutionState("running"))
            if sync
            else await task._output(execution.ExecutionState("running"))
        )
    assert changed
    assert output == (payload, b"")
    assert task.status.called == (race == "remove_before_open")
    assert len(commands) == (
        2 if race in {"remove_before_open", "disconnect", "stall"} else 1
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("sync", [False, True])
@pytest.mark.parametrize("shell_failure", [False, True])
async def test_snapshot_failure_keeps_results_and_respects_retry_budget(
    sync, shell_failure, monkeypatch
):
    from runta._internal.streaming_transfer import _TransferInterrupted

    monkeypatch.setattr(execution, "_delay", lambda *args: 0)

    def read(runtime_id, path):
        if path.endswith("/limit"):
            return b"4194304"
        raise execution._public.ApiError("file is too large", status_code=422)

    failed_result = CommandResult(7, b"partial", b"head failed", 0)
    snapshot = (Mock if sync else AsyncMock)(
        return_value=failed_result,
        side_effect=None if shell_failure else _TransferInterrupted("offline"),
    )
    http = SimpleNamespace(
        retry_max_attempts=2,
        execute=snapshot,
        read_file=read if sync else AsyncMock(side_effect=read),
    )
    task = (Execution if sync else AsyncExecution)(runtime(http), str(uuid.uuid4()))
    terminal = execution.ExecutionState("completed", 0)
    task._observe = (Mock if sync else AsyncMock)(return_value=terminal)
    task.cleanup = (Mock if sync else AsyncMock)()
    with pytest.raises(ExecutionError) as exc:
        if sync:
            task.wait()
        else:
            await task.wait()
    assert exc.value.execution_id == task.id
    assert snapshot.call_count == (1 if shell_failure else 2)
    task.cleanup.assert_not_called()


@pytest.mark.parametrize("code,retryable", [(1005, True), (1008, False)])
def test_snapshot_transport_distinguishes_empty_close_from_policy_rejection(
    code, retryable, monkeypatch
):
    from websockets.exceptions import ConnectionClosedError, ConnectionClosedOK
    from websockets.frames import Close
    from runta._internal import streaming_transfer

    closed = (ConnectionClosedOK if code == 1005 else ConnectionClosedError)(
        Close(code, ""), Close(code, ""), True
    )

    def recv(**kwargs):
        raise closed

    @contextmanager
    def socket(*args, **kwargs):
        yield SimpleNamespace(send=lambda frame: None, recv=recv)

    monkeypatch.setattr(streaming_transfer, "_sync_socket", socket)
    with pytest.raises(execution._public.ApiError) as exc:
        execute(
            "http://test",
            "token",
            "id",
            "head",
            [],
            env=None,
            stdin=None,
            timeout=None,
            max_output_bytes=1024,
            connect_timeout=2,
        )
    assert isinstance(exc.value, streaming_transfer._TransferInterrupted) == retryable
    assert streaming_transfer._retryable_transfer_error(closed) == retryable


@pytest.mark.parametrize("ending", ["exit", "timeout", "cancel"])
@pytest.mark.parametrize("limit", [3, 1024])
def test_escaped_fifo_writers_do_not_block_results(guest_root, tmp_path, ending, limit):
    child_pid = tmp_path / "escaped.pid"
    command = (
        f"setsid sh -c 'echo $$ > {child_pid}; exec sleep 60' & "
        f"while [ ! -f {child_pid} ]; do sleep 0.01; done; "
        "printf captured-stdout; printf captured-stderr >&2; "
        + ("sleep 60" if ending != "exit" else ":")
    )
    task, observer = launch(
        guest_root, command, timeout=0.2 if ending == "timeout" else None, limit=limit
    )
    try:
        ready(task)
        if ending == "cancel":
            deadline = time.monotonic() + 3
            while not child_pid.exists() or (task / "stdout.raw").stat().st_size == 0:
                assert time.monotonic() < deadline
                time.sleep(0.01)
            subprocess.run(
                ["sh", str(task / "control.sh"), "cancel", str(task)], check=True
            )
        state = wait_result(task, timeout=8)
        assert (
            state.status
            == {"exit": "completed", "timeout": "timed_out", "cancel": "cancelled"}[
                ending
            ]
        )
        assert (task / "stdout").read_bytes() == b"captured-stdout"[:limit]
        assert (task / "stderr").read_bytes().startswith(b"captured-stderr"[:limit])
        assert state.stdout_truncated == (limit == 3)
        os.kill(int(child_pid.read_text()), 0)  # It still owns the inherited writers.
        observer.communicate(timeout=3)
        for stream in ("stdout", "stderr"):
            assert not (task / f"{stream}.fifo").exists()
            assert not (task / f"{stream}.raw").exists()
    finally:
        if child_pid.exists():
            try:
                os.killpg(int(child_pid.read_text()), signal.SIGKILL)
            except ProcessLookupError:
                pass
        if observer.poll() is None:
            observer.kill()
            observer.communicate()


@pytest.mark.parametrize("received", [0, 65536, 204799, 204801])
def test_incomplete_stdin_never_launches_command(guest_root, tmp_path, received):
    marker = tmp_path / "command-ran"
    http = SimpleNamespace()
    task = Execution._new(
        runtime(http),
        ["sh", "-c", f"printf x >> {marker}; cat"],
        timeout=1,
        env=None,
        stdin=b"x" * 204800,
        cwd=None,
        max_output_bytes=204800,
    )
    process = subprocess.run(
        ["sh", "-c", task._launch],
        input=b"x" * received,
        capture_output=True,
        timeout=4,
    )
    directory = Path(task._directory)
    assert process.returncode == 125
    assert b"Incomplete execution stdin" in process.stderr
    assert not marker.exists()
    assert not (directory / "stdin.complete").exists()
    assert not (directory / "supervisor.identity").exists()
    assert (directory / "stdin.incomplete").read_text().split() == [
        "204800",
        str(received),
    ]
    result = subprocess.run(
        ["sh", "-c", task._control("watch")], capture_output=True, timeout=2
    )
    with pytest.raises(ExecutionError) as raised:
        task._accept(execution._parse_state(result.stdout.strip()), Mock())
    assert raised.value.execution_id == task.id
    assert not (directory / "stdin.tmp").exists()
    cleanup = subprocess.run(
        ["sh", "-c", task._control("cleanup")], capture_output=True, timeout=2
    )
    assert cleanup.returncode == 0, cleanup.stderr
    assert not directory.exists()


@pytest.mark.parametrize(
    "data", [b"", b"\0\xff" * 100000, "你好" * 100], ids=["empty", "binary", "unicode"]
)
def test_complete_stdin_is_committed_before_launch(guest_root, tmp_path, data):
    marker = tmp_path / "command-ran"
    task = Execution._new(
        runtime(SimpleNamespace()),
        ["sh", "-c", f"printf x >> {marker}; cat"],
        timeout=1,
        env=None,
        stdin=data,
        cwd=None,
        max_output_bytes=262144,
    )
    expected = data.encode() if isinstance(data, str) else data
    process = subprocess.run(
        ["sh", "-c", task._launch], input=expected, capture_output=True, timeout=5
    )
    directory = Path(task._directory)
    assert process.returncode == 0, process.stderr
    assert marker.read_bytes() == b"x"
    assert (directory / "stdin.complete").read_text().strip() == str(len(expected))
    assert (directory / "stdout").read_bytes() == expected
    assert not (directory / "stdin.tmp").exists()
    assert not (directory / "stdin.incomplete").exists()


@pytest.mark.asyncio
@pytest.mark.parametrize("sync", [False, True])
@pytest.mark.parametrize("chunks", [0, 1, 4])
async def test_stdin_disconnect_never_runs_partial_input(
    guest_root, tmp_path, monkeypatch, sync, chunks
):
    bodies = []
    marker = tmp_path / "invocations"
    data = b"\0\xff" * 102400
    monkeypatch.setattr(execution, "_delay", lambda *args: 0)

    async def handler(ws):
        start = json.loads(await ws.recv())
        bodies.append(start["args"][1])
        proc = await asyncio.create_subprocess_exec(
            start["command"],
            *start["args"],
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            start_new_session=True,
        )
        if len(bodies) == 1:
            for _ in range(chunks):
                frame = json.loads(await ws.recv())
                assert frame["type"] == "stdin"
                proc.stdin.write(base64.b64decode(frame["data_base64"]))
                await proc.stdin.drain()
            proc.stdin.close()  # Guest sees EOF caused by the broken connection.
            await proc.communicate()
            await ws.close(code=1011, reason="interrupted stdin delivery")
            return
        proc.stdin.close()
        stdout, stderr = await proc.communicate()
        for kind, output in [("stdout", stdout), ("stderr", stderr)]:
            if output:
                await ws.send(
                    json.dumps(
                        {"type": kind, "data_base64": base64.b64encode(output).decode()}
                    )
                )
        await ws.send(json.dumps({"type": "exit", "code": proc.returncode}))

    async with serve(handler, "127.0.0.1", 0, max_size=None) as server:
        endpoint = f"http://127.0.0.1:{server.sockets[0].getsockname()[1]}"
        http = SimpleNamespace(
            endpoint=endpoint, token="test", timeout=2, retry_max_attempts=4
        )
        if sync:
            http.execute = lambda runtime_id, cmd, args, **kw: execute(
                endpoint,
                "test",
                runtime_id,
                cmd,
                args,
                env=None,
                stdin=None,
                timeout=kw.get("timeout"),
                max_output_bytes=4096,
                connect_timeout=2,
            )
        else:

            async def control(runtime_id, cmd, args, **kw):
                return await async_execute(
                    endpoint,
                    "test",
                    runtime_id,
                    cmd,
                    args,
                    env=None,
                    stdin=None,
                    timeout=kw.get("timeout"),
                    max_output_bytes=4096,
                    connect_timeout=2,
                )

            http.execute = control
        task_cls = Execution if sync else AsyncExecution
        task = task_cls._new(
            runtime(http),
            ["sh", "-c", f"printf x >> {marker}; cat"],
            timeout=2,
            env=None,
            stdin=data,
            cwd=None,
            max_output_bytes=len(data),
        )
        if chunks == 4:
            result = await asyncio.to_thread(task.wait) if sync else await task.wait()
            assert result.stdout == data
            assert result.exit_code == 0
            assert marker.read_bytes() == b"x"
        else:
            with pytest.raises(ExecutionError) as raised:
                if sync:
                    await asyncio.to_thread(task.wait)
                else:
                    await task.wait()
            assert raised.value.execution_id == task.id
            assert not marker.exists()
            assert not Path(task._directory).exists()
            assert "Incomplete execution stdin: expected 204800 bytes" in str(
                raised.value
            )
            assert f"received {chunks * 65536}" in str(raised.value)
        assert sum("mkdir -m 700" in body for body in bodies) == 1
        assert all(
            task.id in body
            and ("control.sh watch" in body or "control.sh cleanup" in body)
            for body in bodies[1:]
        )
        assert len(bodies) >= 2


@pytest.mark.parametrize("active", ["bootstrap", "supervisor", "command"])
def test_incomplete_cleanup_waits_for_owned_processes(guest_root, active):
    task = guest_root / str(uuid.uuid4())
    task.mkdir(parents=True)
    control = task / "control.sh"
    control.write_text(execution._SCRIPT)
    (task / "stdin.incomplete").write_text("1024 512\n")
    (task / "stdin.tmp").write_bytes(b"x" * 512)
    held = subprocess.Popen(["sleep", "60"], start_new_session=True)
    try:
        subprocess.run(
            ["sh", str(control), "bootstrap_identity", str(task), str(held.pid)],
            check=True,
        )
        if active != "bootstrap":
            (task / "bootstrap.identity").rename(task / f"{active}.identity")
            (task / "bootstrap.identity").write_text("99999999 0 previous-boot\n")
        for mode in ["cleanup", "cleanup_incomplete"]:
            result = subprocess.run(
                ["sh", str(control), mode, str(task)], capture_output=True, timeout=2
            )
            assert result.returncode == 1
            assert (task / "stdin.tmp").read_bytes() == b"x" * 512
        held.terminate()
        held.wait(timeout=3)
        result = subprocess.run(
            ["sh", str(control), "cleanup_incomplete", str(task)],
            capture_output=True,
            timeout=2,
        )
        assert result.returncode == 0, result.stderr
        assert not task.exists()
        assert b"expected 1024 bytes, received 512" in result.stdout
    finally:
        if held.poll() is None:
            held.kill()
            held.wait()


def test_incomplete_cleanup_rejects_unverified_state_and_reused_pid(guest_root):
    task = guest_root / str(uuid.uuid4())
    task.mkdir(parents=True)
    control = task / "control.sh"
    control.write_text(execution._SCRIPT)
    (task / "stdin.tmp").write_bytes(b"input")
    for mode in ["cleanup", "cleanup_incomplete"]:
        result = subprocess.run(
            ["sh", str(control), mode, str(task)], capture_output=True, timeout=2
        )
        assert result.returncode == (1 if mode == "cleanup" else 0)
        assert (task / "stdin.tmp").exists()
    (task / "stdin.incomplete").write_text("10 5\n")
    result = subprocess.run(
        ["sh", str(control), "cleanup_incomplete", str(task)],
        capture_output=True,
        timeout=2,
    )
    assert result.returncode == 1  # No bootstrap identity means no proof it has exited.
    subprocess.run(
        ["sh", str(control), "bootstrap_identity", str(task), str(os.getpid())],
        check=True,
    )
    identity = task / "bootstrap.identity"
    fields = identity.read_text().split()
    fields[1] = str(int(fields[1]) - 1)  # Same PID, different process start time.
    identity.write_text(" ".join(fields) + "\n")
    result = subprocess.run(
        ["sh", str(control), "cleanup_incomplete", str(task)],
        capture_output=True,
        timeout=2,
    )
    assert result.returncode == 0
    assert not task.exists()


@pytest.mark.asyncio
@pytest.mark.parametrize("sync", [False, True])
async def test_failed_cleanup_preserves_original_execution_error(monkeypatch, sync):
    task_cls = Execution if sync else AsyncExecution
    original = ExecutionError("Execution is lost", str(uuid.uuid4()))
    task = task_cls(
        runtime(SimpleNamespace(retry_max_attempts=1)), original.execution_id
    )
    observe = Mock(side_effect=original) if sync else AsyncMock(side_effect=original)
    cleanup = (
        Mock(side_effect=RuntimeError("cleanup unavailable"))
        if sync
        else AsyncMock(side_effect=RuntimeError("cleanup unavailable"))
    )
    monkeypatch.setattr(task, "_observe", observe)
    monkeypatch.setattr(task, "_short", cleanup)
    with pytest.raises(ExecutionError) as raised:
        if sync:
            await asyncio.to_thread(task.wait)
        else:
            await task.wait()
    assert raised.value is original
    assert raised.value.execution_id == task.id
    cleanup.assert_called_once_with("cleanup_incomplete")


@pytest.mark.asyncio
@pytest.mark.parametrize("sync", [False, True])
async def test_incomplete_observation_waits_for_bootstrap_exit(
    guest_root, tmp_path, monkeypatch, sync
):
    task_cls = Execution if sync else AsyncExecution
    task = task_cls(runtime(SimpleNamespace(retry_max_attempts=1)), str(uuid.uuid4()))
    marker = tmp_path / "command-ran"
    body = execution._bootstrap(
        task._directory,
        "sh",
        ["-c", f"touch {marker}"],
        env=None,
        timeout=None,
        limit=1024,
        stdin_size=100,
    )
    # Stop after publishing failure to hold the exact cleanup race open.
    lines = body.splitlines()
    published = next(
        i
        for i, line in enumerate(lines)
        if line.strip().startswith("mv ") and "/stdin.incomplete.tmp " in line
    )
    lines.insert(published + 1, '  kill -STOP "$$"')
    bootstrap = subprocess.Popen(
        ["sh", "-c", "\n".join(lines)],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    bootstrap.stdin.write(b"short")
    bootstrap.stdin.close()
    bootstrap.stdin = None
    directory = Path(task._directory)
    watch = None
    try:
        deadline = time.monotonic() + 5
        while time.monotonic() < deadline:
            if (directory / "stdin.incomplete").exists() and "State:\tT" in Path(
                f"/proc/{bootstrap.pid}/status"
            ).read_text():
                break
            await asyncio.sleep(0.01)
        else:
            pytest.fail("Bootstrap did not stop after publishing incomplete input")
        assert not (directory / "stdin.tmp").exists()
        watch = subprocess.Popen(
            ["sh", "-c", task._control("watch")],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        def observe(healthy):
            assert select.select([watch.stdout], [], [], 3)[0]
            starting = execution._parse_state(watch.stdout.readline().strip())
            assert starting.status == "starting"
            assert task._accept(starting, healthy) is None
            # Cleanup must still refuse an active bootstrap.
            refused = subprocess.run(
                ["sh", "-c", task._control("cleanup_incomplete")],
                capture_output=True,
                timeout=2,
            )
            assert refused.returncode == 1
            assert directory.exists()
            os.kill(bootstrap.pid, signal.SIGCONT)
            remaining, errors = watch.communicate(timeout=5)
            assert watch.returncode == 0, errors
            state = execution._parse_state(remaining.strip())
            assert state.status == "lost"
            return task._accept(state, healthy)

        def short(mode):
            result = subprocess.run(
                ["sh", "-c", task._control(mode)], capture_output=True, timeout=3
            )
            assert result.returncode == 0, result.stderr
            return CommandResult(result.returncode, result.stdout, result.stderr, 0)

        async def async_observe(healthy):
            return await asyncio.to_thread(observe, healthy)

        async def async_short(mode):
            return await asyncio.to_thread(short, mode)

        monkeypatch.setattr(task, "_observe", observe if sync else async_observe)
        monkeypatch.setattr(task, "_short", short if sync else async_short)
        with pytest.raises(ExecutionError) as raised:
            if sync:
                await asyncio.to_thread(task.wait)
            else:
                await task.wait()
        assert raised.value.execution_id == task.id
        assert "expected 100 bytes, received 5" in str(raised.value)
        assert not directory.exists()
        assert not marker.exists()
        bootstrap.communicate(timeout=3)
        assert bootstrap.returncode == 125
    finally:
        if bootstrap.poll() is None:
            os.kill(bootstrap.pid, signal.SIGCONT)
            bootstrap.kill()
            bootstrap.wait()
        if watch is not None and watch.poll() is None:
            watch.kill()
            watch.wait()
