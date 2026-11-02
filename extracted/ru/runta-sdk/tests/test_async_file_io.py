"""Functional concurrency and cancellation tests; no timing benchmarks."""

import asyncio
import io
import json
from pathlib import Path
import threading
from unittest.mock import Mock

import pytest

from runta import AsyncRunta
from runta._internal import async_file_io as file_io
from runta._internal import streaming_transfer as transfer
from runta._internal.async_file_io import _AsyncFileIO
from runta._internal.byte_budget import _ByteBudget, _YIELD_BYTES
from test_streaming_transfer import _FakeSocket, _FakeSocketContext, _data_frame


@pytest.mark.parametrize("value", [0, -1, True, False, 1.5, "4"])
def test_invalid_worker_count(value):
    with pytest.raises(ValueError, match="file_io_workers"):
        AsyncRunta(token="test", file_io_workers=value)


@pytest.mark.parametrize("count, expected", [(1, 5), (4, 8), (100, 32), (None, 5)])
def test_default_workers(monkeypatch, count, expected):
    monkeypatch.setattr(file_io.os, "process_cpu_count", lambda: count, raising=False)
    monkeypatch.delattr(file_io.os, "sched_getaffinity", raising=False)
    monkeypatch.setattr(file_io.os, "cpu_count", lambda: None)
    assert file_io.file_io_worker_count(None) == expected
    assert file_io.file_io_worker_count(64) == 64


def test_cpu_affinity_and_fallback(monkeypatch):
    monkeypatch.delattr(file_io.os, "process_cpu_count", raising=False)
    monkeypatch.setattr(
        file_io.os, "sched_getaffinity", lambda _: {2, 3}, raising=False
    )
    assert file_io.file_io_worker_count(None) == 6

    def unavailable(_):
        raise OSError("unavailable")

    monkeypatch.setattr(file_io.os, "sched_getaffinity", unavailable)
    monkeypatch.setattr(file_io.os, "cpu_count", lambda: 8)
    assert file_io.file_io_worker_count(None) == 12


async def wait_until(predicate):
    async def wait():
        while not predicate():
            await asyncio.sleep(0)

    await asyncio.wait_for(wait(), 5)


@pytest.mark.asyncio
async def test_pool_bounds_submission_and_does_not_block_loop():
    pool = _AsyncFileIO(2, asyncio.get_running_loop)
    release = threading.Event()
    entered = []
    progress = []

    def work(i):
        entered.append((i, threading.current_thread().name))
        release.wait(5)
        return i

    with pool.lease():
        tasks = [asyncio.create_task(pool.run(work, i)) for i in range(5)]
        try:
            await wait_until(lambda: len(entered) == 2)
            asyncio.get_running_loop().call_soon(progress.append, True)
            await asyncio.sleep(0)
            assert progress == [True]
            assert len(entered) == 2
            assert pool._executor._work_queue.qsize() == 0
            assert all(name.startswith("runta-file-io") for _, name in entered)
            # A waiter cancelled before submission must never enter the worker.
            tasks[-1].cancel()
            with pytest.raises(asyncio.CancelledError):
                await tasks[-1]
            release.set()
            assert await asyncio.gather(*tasks[:-1]) == [0, 1, 2, 3]
            assert len(entered) == 4
        finally:
            release.set()
            await asyncio.gather(*tasks, return_exceptions=True)
            pool.close()
    assert pool._executor._shutdown


@pytest.mark.asyncio
async def test_client_close_defers_shutdown_for_existing_lease():
    client = AsyncRunta(token="test", file_io_workers=1)
    pool = client._http._file_io
    assert pool is client.runtimes._client._http._file_io
    assert pool._executor is None
    with pool.lease():
        assert await pool.run(lambda: 1) == 1
        await client.close()
        assert not pool._executor._shutdown
        with pytest.raises(RuntimeError, match="closed"):
            with pool.lease():
                pass
        assert await pool.run(lambda: 2) == 2
    assert pool._executor._shutdown
    await client.close()
    unused = AsyncRunta(token="test")
    await unused.close()
    assert unused._http._file_io._executor is None


@pytest.mark.asyncio
@pytest.mark.parametrize("stage", ["open", "write", "close"])
async def test_file_operations_drain_despite_repeated_cancel(
    tmp_path, monkeypatch, stage
):
    pool = _AsyncFileIO(1, asyncio.get_running_loop)
    entered = threading.Event()
    release = threading.Event()
    events = []
    handle = io.BytesIO()

    def record(name):
        events.append((name, threading.current_thread().name))
        if name == stage:
            entered.set()
            release.wait(5)

    class Handle:
        def write(self, data):
            record("write")
            return handle.write(data)

        def flush(self):
            record("flush")

        def close(self):
            record("close")
            handle.close()

    def open_file(*args):
        record("open")
        return Handle()

    monkeypatch.setattr(Path, "open", open_file)

    async def download():
        with pool.lease():
            writer = transfer._AsyncDownloadWriter(pool, tmp_path / "payload.tar")
            try:
                await writer.open()
                await writer.write_frame({"data_base64": "YWJj"})
            finally:
                await writer.close()

    task = asyncio.create_task(download())
    try:
        await wait_until(entered.is_set)
        task.cancel()
        await asyncio.sleep(0)
        task.cancel()
        await asyncio.sleep(0)
        assert not task.done()
        assert not handle.closed
        release.set()
        with pytest.raises(asyncio.CancelledError):
            await task
        assert handle.closed
        assert events[-1][0] == "close"
        assert all(name.startswith("runta-file-io") for _, name in events)
        assert pool._slots._value == 1
    finally:
        release.set()
        await asyncio.gather(task, return_exceptions=True)
        pool.close()


@pytest.mark.asyncio
async def test_cancel_cleanup_can_wait_for_busy_pool(tmp_path, monkeypatch):
    pool = _AsyncFileIO(1, asyncio.get_running_loop)
    writer = transfer._AsyncDownloadWriter(pool, tmp_path / "payload.tar")
    entered = threading.Event()
    release = threading.Event()

    def block():
        entered.set()
        release.wait(5)

    with pool.lease():
        await writer.open()
        task = asyncio.create_task(pool.run(block))
        cleanup = None
        try:
            await wait_until(entered.is_set)
            cleanup = asyncio.create_task(writer.close())
            await asyncio.sleep(0)
            cleanup.cancel()
            await asyncio.sleep(0)
            cleanup.cancel()
            assert not writer._handle.closed
            release.set()
            await task
            with pytest.raises(asyncio.CancelledError):
                await cleanup
            assert writer._handle.closed
        finally:
            release.set()
            if cleanup is not None:
                await asyncio.gather(cleanup, return_exceptions=True)
            await asyncio.gather(task, return_exceptions=True)
            pool.close()


@pytest.mark.asyncio
async def test_download_cancel_waits_for_extraction_before_temp_cleanup(
    tmp_path, monkeypatch
):
    entered = threading.Event()
    release = threading.Event()
    workspace = []

    async def download_archive(*args, **kwargs):
        args[4].write_bytes(b"archive")

    def extract(archive, *args, **kwargs):
        workspace.append(archive.parent)
        entered.set()
        release.wait(5)
        assert archive.exists()
        (archive.parent / "extracted").write_bytes(b"complete")

    monkeypatch.setattr(transfer, "_async_download_archive", download_archive)
    monkeypatch.setattr(transfer, "_extract_and_commit", extract)
    task = asyncio.create_task(
        transfer.async_download_path(
            "https://test",
            "token",
            "runtime",
            "source",
            tmp_path / "result",
            destination_is_directory=False,
            timeout=2,
        )
    )
    try:
        await wait_until(entered.is_set)
        task.cancel()
        await asyncio.sleep(0)
        task.cancel()
        await asyncio.sleep(0)
        assert not task.done()
        assert workspace[0].exists()
        release.set()
        with pytest.raises(asyncio.CancelledError):
            await task
        assert not workspace[0].exists()
    finally:
        release.set()
        await asyncio.gather(task, return_exceptions=True)


@pytest.mark.asyncio
async def test_byte_budget_exact_threshold_and_reset():
    budget = _ByteBudget()
    progress = []
    asyncio.get_running_loop().call_soon(progress.append, "first")
    for _ in range(15):
        await budget.processed(64 * 1024)
        assert not progress
    await budget.processed(64 * 1024)
    assert progress == ["first"]
    asyncio.get_running_loop().call_soon(progress.append, "second")
    await budget.processed(_YIELD_BYTES - 1)
    assert progress == ["first"]
    await budget.processed(1)
    assert progress == ["first", "second"]


@pytest.mark.asyncio
async def test_execute_cached_send_and_receive_yield_without_io(monkeypatch):
    frames = [_data_frame("stdout", b"x" * (256 * 1024)) for _ in range(4)]
    frames.append(json.dumps({"type": "exit", "code": 0}))
    socket = _FakeSocket(frames)
    received = []
    sent = []
    recv = socket.recv
    send = socket.send

    async def observe_send(frame):
        await send(frame)
        if json.loads(frame)["type"] == "stdin" and not sent:
            asyncio.get_running_loop().call_soon(lambda: sent.append(len(socket.sent)))

    async def observe_recv():
        result = await recv()
        if not received:
            asyncio.get_running_loop().call_soon(
                lambda: received.append(len(socket.frames))
            )
        return result

    socket.send, socket.recv = observe_send, observe_recv
    monkeypatch.setattr(
        transfer, "_async_socket", lambda *a, **k: _FakeSocketContext(socket)
    )
    result = await transfer.async_execute(
        "https://test",
        "token",
        "runtime",
        "cat",
        [],
        env=None,
        stdin=b"s" * _YIELD_BYTES,
        timeout=None,
        max_output_bytes=1,
        connect_timeout=2,
    )
    assert sent == [5] * 4  # start + four chunks, before close_stdin.
    assert received == [1] * 4  # Queued callbacks run at the receive threshold.
    assert result.stdout == b"x"
    assert result.stdout_truncated


@pytest.mark.asyncio
async def test_idle_timeout_decodes_each_output_frame_once(monkeypatch):
    socket = _FakeSocket(
        [
            _data_frame("stdout", b"hello"),
            _data_frame("stderr", b"world"),
            json.dumps({"type": "exit", "code": 0}),
        ]
    )
    monkeypatch.setattr(
        transfer, "_async_socket", lambda *a, **k: _FakeSocketContext(socket)
    )
    decode = Mock(wraps=transfer._decode_frame_data)
    monkeypatch.setattr(transfer, "_decode_frame_data", decode)
    result = await transfer.async_execute(
        "https://test",
        "token",
        "runtime",
        "cat",
        [],
        env=None,
        stdin=None,
        timeout=None,
        max_output_bytes=100,
        connect_timeout=2,
        idle_timeout=2,
    )
    assert (result.stdout, result.stderr) == (b"hello", b"world")
    assert decode.call_count == 2


@pytest.mark.asyncio
async def test_download_order_and_content(tmp_path):
    pool = _AsyncFileIO(2, asyncio.get_running_loop)
    path = tmp_path / "payload.tar"
    parts = [b"a" * 200, b"b" * 300, b"c" * 400]
    socket = _FakeSocket(
        [
            *[_data_frame("stdout", p) for p in parts],
            json.dumps({"type": "exit", "code": 0}),
            None,
        ]
    )
    with pool.lease():
        writer = transfer._AsyncDownloadWriter(pool, path)
        try:
            await writer.open()
            await transfer._async_receive_completion(socket.recv, writer)
        finally:
            await writer.close()
            pool.close()
    assert path.read_bytes() == b"".join(parts)


@pytest.mark.asyncio
async def test_cached_directory_queue_yields_at_byte_budget(tmp_path, monkeypatch):
    import queue

    chunks = queue.Queue(maxsize=8)
    for _ in range(7):
        chunks.put_nowait(b"x" * (256 * 1024))
    chunks.put_nowait(None)
    monkeypatch.setattr(transfer.queue, "Queue", lambda maxsize: chunks)

    async def no_producer(*args):
        pass  # The bounded queue already contains all producer output.

    monkeypatch.setattr(transfer.asyncio, "to_thread", no_producer)
    socket = _FakeSocket([json.dumps({"type": "exit", "code": 0}), None])
    progress = []
    send = socket.send

    async def observe_send(frame):
        await send(frame)
        if json.loads(frame)["type"] == "stdin" and not progress:
            asyncio.get_running_loop().call_soon(
                lambda: progress.append(len(socket.sent))
            )

    socket.send = observe_send
    monkeypatch.setattr(
        transfer, "_async_socket", lambda *a, **k: _FakeSocketContext(socket)
    )
    await transfer._async_upload_directory(
        "https://test", "token", "runtime", tmp_path, "/remote", 2
    )
    assert progress == [5] * 4
    assert chunks.empty()


@pytest.mark.asyncio
async def test_download_cached_receive_budget(monkeypatch):
    socket = _FakeSocket(
        [
            *[_data_frame("stdout", b"x" * (256 * 1024)) for _ in range(4)],
            json.dumps({"type": "exit", "code": 0}),
            None,
        ]
    )
    progress = []
    recv = socket.recv

    async def observe_recv():
        frame = await recv()
        if not progress:
            asyncio.get_running_loop().call_soon(
                lambda: progress.append(len(socket.frames))
            )
        return frame

    class ImmediateWriter:
        async def write_frame(self, frame):
            return len(transfer._decode_frame_data(frame))

    await transfer._async_receive_completion(observe_recv, ImmediateWriter())
    assert progress == [2] * 4


@pytest.mark.asyncio
async def test_observer_send_and_stderr_budget(monkeypatch):
    from types import SimpleNamespace
    from runta._internal import execution

    http = SimpleNamespace(endpoint="https://test", token="token", timeout=2)
    runtime = SimpleNamespace(_client=SimpleNamespace(_http=http), id="runtime")
    task = execution.AsyncExecution(runtime, "00000000-0000-0000-0000-000000000001")
    task._stdin = b"s" * _YIELD_BYTES
    socket = _FakeSocket(
        [
            *[_data_frame("stderr", b"x" * (256 * 1024)) for _ in range(4)],
            _data_frame("stdout", b"RUNTA_EXEC_V1 completed 0 0 0 1.25\n"),
        ]
    )
    sent, received = [], []
    send, recv = socket.send, socket.recv

    async def observe_send(frame):
        await send(frame)
        if json.loads(frame)["type"] == "stdin" and not sent:
            asyncio.get_running_loop().call_soon(lambda: sent.append(len(socket.sent)))

    async def observe_recv():
        frame = await recv()
        if not received:
            asyncio.get_running_loop().call_soon(
                lambda: received.append(len(socket.frames))
            )
        return frame

    async def immediate_wait(awaitable, **kwargs):
        return await awaitable

    socket.send, socket.recv = observe_send, observe_recv
    monkeypatch.setattr(
        execution, "_async_socket", lambda *a, **k: _FakeSocketContext(socket)
    )
    monkeypatch.setattr(execution.asyncio, "wait_for", immediate_wait)
    state = await task._observe(lambda: None)
    assert state.status == "completed"
    assert sent == [17] * 16
    assert received == [1] * 4
    assert task.id == "00000000-0000-0000-0000-000000000001"


@pytest.mark.asyncio
async def test_cancel_write_closes_archive_before_temp_cleanup(tmp_path, monkeypatch):
    entered, release = threading.Event(), threading.Event()
    archive_paths = []
    write = transfer._AsyncDownloadWriter._write

    def blocked_write(self, frame):
        archive_paths.append(self._path)
        entered.set()
        release.wait(5)
        assert self._path.exists()
        return write(self, frame)

    monkeypatch.setattr(transfer._AsyncDownloadWriter, "_write", blocked_write)
    socket = _FakeSocket([_data_frame("stdout", b"payload")])
    monkeypatch.setattr(
        transfer, "_async_socket", lambda *a, **k: _FakeSocketContext(socket)
    )
    client = AsyncRunta(token="token", file_io_workers=1)
    pool = client._http._file_io
    task = asyncio.create_task(
        transfer.async_download_path(
            "https://test",
            "token",
            "runtime",
            "source",
            tmp_path / "result",
            destination_is_directory=False,
            timeout=2,
            _file_io=pool,
        )
    )
    try:
        await wait_until(entered.is_set)
        task.cancel()
        await asyncio.sleep(0)
        task.cancel()
        await asyncio.sleep(0)
        await client.close()
        assert not task.done()
        assert archive_paths[0].exists()
        assert not pool._executor._shutdown
        release.set()
        with pytest.raises(asyncio.CancelledError):
            await task
        assert not archive_paths[0].parent.exists()
        assert pool._executor._shutdown
    finally:
        release.set()
        await asyncio.gather(task, return_exceptions=True)
        await client.close()


@pytest.mark.asyncio
@pytest.mark.parametrize("stage", ["create", "cleanup"])
async def test_workspace_operations_run_in_file_pool_and_drain_cancel(
    monkeypatch, stage
):
    client = AsyncRunta(token="test", file_io_workers=1)
    pool = client._http._file_io
    entered, release = threading.Event(), threading.Event()
    paths = []
    operations = []
    temporary_directory = transfer.tempfile.TemporaryDirectory
    cleanup = temporary_directory.cleanup

    def record(name):
        operations.append((name, threading.current_thread().name))
        if name == stage:
            entered.set()
            release.wait(5)

    def create_workspace(*args, **kwargs):
        workspace = temporary_directory(*args, **kwargs)
        paths.append(Path(workspace.name))
        record("create")
        return workspace

    def cleanup_workspace(self):
        record("cleanup")
        assert Path(self.name).exists()
        cleanup(self)

    monkeypatch.setattr(temporary_directory, "cleanup", cleanup_workspace)
    monkeypatch.setattr(transfer.tempfile, "TemporaryDirectory", create_workspace)

    def populate(path):
        nested = path / "nested" / "deeper"
        nested.mkdir(parents=True)
        (nested / "file").write_bytes(b"contents")

    async def download():
        with pool.lease():
            async with transfer._async_download_workspace(pool) as path:
                await pool.run(populate, path)

    task = asyncio.create_task(download())
    try:
        await wait_until(entered.is_set)
        progress = []
        asyncio.get_running_loop().call_soon(progress.append, True)
        await asyncio.sleep(0)
        assert progress == [True]
        task.cancel()
        await asyncio.sleep(0)
        task.cancel()
        await asyncio.sleep(0)
        await client.close()
        assert not task.done()
        assert paths[0].exists()
        assert not pool._executor._shutdown
        release.set()
        with pytest.raises(asyncio.CancelledError):
            await task
        assert not paths[0].exists()
        assert pool._executor._shutdown
        assert [name for name, _ in operations] == ["create", "cleanup"]
        assert all(name.startswith("runta-file-io") for _, name in operations)
    finally:
        release.set()
        await asyncio.gather(task, return_exceptions=True)
        await client.close()
