"""The observer carries arbitrary binary output without REST reads."""

from __future__ import annotations

import pytest

from runta import ApiError
from runta._internal.execution import _Observation


def result_header(out, err):
    return (
        f"RUNTA_EXEC_RESULT_V2 completed 7 1 0 0.125 {len(out)} {len(err)}\n".encode()
    )


@pytest.mark.parametrize("chunk_size", [1, 2, 17, 65536])
@pytest.mark.parametrize(
    "out,err",
    [
        (b"", b""),
        (b"\x00\xff\nRUNTA_EXEC_V1 running\n", b"\xff\x00"),
        (b"x" * 10000, b"e" * 9000),
    ],
)
def test_result_is_length_delimited_across_any_frame_boundary(chunk_size, out, err):
    parser = _Observation(limit=10000)
    data = b"RUNTA_EXEC_V1 running\n" + result_header(out, err) + out + err
    states = []
    for offset in range(0, len(data), chunk_size):
        states.extend(parser.feed(data[offset : offset + chunk_size]))
    assert [state.status for state in states] == ["running", "completed"]
    assert states[-1].exit_code == 7
    assert states[-1].stdout_truncated
    assert parser.output == (out, err)


def test_incomplete_result_never_publishes_terminal_state():
    parser = _Observation()
    assert parser.feed(result_header(b"abc", b"err") + b"ab") == []
    assert parser.output is None
    assert parser.feed(b"cerr")[0].status == "completed"
    assert parser.output == (b"abc", b"err")


@pytest.mark.parametrize(
    "header",
    [
        b"RUNTA_EXEC_RESULT_V2 completed 0 0 0 1 -1 0\n",
        b"RUNTA_EXEC_RESULT_V2 completed 0 0 0 1 4 0\n",
        b"RUNTA_EXEC_RESULT_V2 running 0 0 0 1 0 0\n",
        b"RUNTA_EXEC_RESULT_V2 completed 0 0 0 nan 0 0\n",
        b"RUNTA_EXEC_RESULT_V2 completed 0 0 0 1 0\n",
        b"RUNTA_EXEC_RESULT_V2 completed 0 0 0 1 0 0\nextra",
        b"x" * 8193,
    ],
)
def test_invalid_result_is_rejected(header):
    with pytest.raises(ApiError):
        _Observation(limit=3).feed(header)


@pytest.mark.asyncio
@pytest.mark.parametrize("sync", [False, True])
async def test_inline_result_survives_independent_cleanup_failure(sync):
    import asyncio
    import uuid
    from types import SimpleNamespace
    from unittest.mock import Mock, AsyncMock
    from runta._internal.execution import Execution, AsyncExecution, ExecutionState

    http = SimpleNamespace(retry_max_attempts=2)
    runtime = SimpleNamespace(_client=SimpleNamespace(_http=http))
    task = (Execution if sync else AsyncExecution)(runtime, str(uuid.uuid4()))
    state = ExecutionState("completed", 0)

    def observe(healthy):
        task._inline_output = (b"answer", b"error")
        return state

    async def async_observe(healthy):
        return observe(healthy)

    task._observe = observe if sync else async_observe
    task._output = (Mock if sync else AsyncMock)(
        side_effect=AssertionError("extra file read")
    )
    task.cleanup = (Mock if sync else AsyncMock)(
        side_effect=ConnectionError("cleanup failed")
    )
    result = await asyncio.to_thread(task.wait) if sync else await task.wait()
    assert result.stdout == b"answer" and result.stderr == b"error"
    task._output.assert_not_called()
    task.cleanup.assert_called_once()


@pytest.mark.asyncio
@pytest.mark.parametrize("sync", [False, True])
@pytest.mark.parametrize("partial", [b"", b"x"])
@pytest.mark.parametrize("running_reset", [False, True])
async def test_incomplete_result_exhausts_budget_without_cleaning_files(
    monkeypatch, tmp_path, sync, partial, running_reset
):
    import asyncio
    import base64
    from collections import deque
    from contextlib import contextmanager, asynccontextmanager
    import json
    from types import SimpleNamespace
    from unittest.mock import Mock, AsyncMock
    import uuid

    from runta import ExecutionError
    from runta._internal import execution

    http = SimpleNamespace(
        endpoint="http://test", token="test", timeout=1, retry_max_attempts=3
    )
    runtime = SimpleNamespace(id="runtime-test", _client=SimpleNamespace(_http=http))
    task = (execution.Execution if sync else execution.AsyncExecution)(
        runtime, str(uuid.uuid4())
    )
    task._launch = "initial launch"
    task._directory = str(tmp_path / task.id)
    directory = tmp_path / task.id
    directory.mkdir()
    (directory / "stdout").write_bytes(b"x" * 100)
    task.cleanup = (Mock if sync else AsyncMock)()
    connections = []
    starts = []
    expected = 5 if running_reset else 3

    def frames():
        connections.append(1)
        if len(connections) > expected:
            # Bound the pre-fix reproduction instead of hanging the test suite.
            raise RuntimeError("incomplete results bypassed retry budget")
        if running_reset and len(connections) < 3:
            return deque([json.dumps({"type": "exit", "code": 0})])
        data = result_header(b"x" * 100, b"") + partial
        if running_reset and len(connections) == 3:
            data = b"RUNTA_EXEC_V1 running\n" + data
        return deque(
            [
                json.dumps(
                    {"type": "stdout", "data_base64": base64.b64encode(data).decode()}
                ),
                json.dumps({"type": "exit", "code": 0}),
            ]
        )

    def record(raw):
        frame = json.loads(raw)
        if frame["type"] == "start":
            starts.append(frame["args"][1])

    @contextmanager
    def sync_socket(*args, **kwargs):
        pending = frames()
        yield SimpleNamespace(send=record, recv=lambda **kwargs: pending.popleft())

    @asynccontextmanager
    async def async_socket(*args, **kwargs):
        pending = frames()

        async def send(raw):
            record(raw)

        async def recv():
            return pending.popleft()

        yield SimpleNamespace(send=send, recv=recv)

    monkeypatch.setattr(
        execution,
        "_sync_socket" if sync else "_async_socket",
        sync_socket if sync else async_socket,
    )
    monkeypatch.setattr(execution, "_delay", lambda *args: 0)
    with pytest.raises(
        ExecutionError, match="Observer exited without a result"
    ) as error:
        if sync:
            await asyncio.to_thread(task.wait)
        else:
            await task.wait()
    assert error.value.execution_id == task.id
    assert len(connections) == expected
    assert starts[0] == "initial launch"
    assert all("control.sh watch" in body for body in starts[1:])
    task.cleanup.assert_not_called()
    assert (directory / "stdout").read_bytes() == b"x" * 100
