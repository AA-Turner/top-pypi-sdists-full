from __future__ import annotations

import asyncio
import base64
import io
import json
import os
import subprocess
import sys
import tarfile
import threading
from concurrent.futures import ThreadPoolExecutor
from contextlib import asynccontextmanager, contextmanager
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from websockets.asyncio.server import serve

from runta._internal import streaming_transfer as transfer


def test_directory_uploads_with_saturated_default_executor(tmp_path):
    # Isolate the executor: the regression leaves real worker threads blocked,
    # so cancellation inside the pytest process would hang its shutdown too.
    result = subprocess.run(
        [sys.executable, __file__, str(tmp_path), "300"],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0, result.stdout[-4000:] + result.stderr[-4000:]
    assert "300/300 uploads completed and verified" in result.stdout


@pytest.mark.asyncio
async def test_cancelling_upload_stops_backpressured_producer(tmp_path, monkeypatch):
    source = tmp_path / "source"
    source.mkdir()
    (source / "binary").write_bytes(bytes(range(256)) * 8192)
    sending = asyncio.Event()
    finished = threading.Event()
    original_open = tarfile.open

    @contextmanager
    def track_producer(*args, **kwargs):
        try:
            with original_open(*args, **kwargs) as archive:
                yield archive
        finally:
            finished.set()

    async def send(raw):
        if json.loads(raw)["type"] == "stdin":
            sending.set()
            await asyncio.Event().wait()

    @asynccontextmanager
    async def socket(*args, **kwargs):
        yield SimpleNamespace(send=send)

    monkeypatch.setattr(transfer, "_async_socket", socket)
    monkeypatch.setattr(transfer.tarfile, "open", track_producer)
    task = asyncio.create_task(
        transfer._async_upload_directory("test", "test", "runtime", source, "/dst", 2)
    )
    await asyncio.wait_for(sending.wait(), timeout=2)
    # A slow consumer fills the bounded queue and blocks the archive writer.
    await asyncio.sleep(0.15)
    assert not finished.is_set()
    task.cancel()
    with pytest.raises(asyncio.CancelledError):
        await asyncio.wait_for(task, timeout=2)
    assert finished.is_set()


@pytest.mark.asyncio
async def test_directory_producer_error_reaches_consumer(tmp_path, monkeypatch):
    send = AsyncMock()

    @asynccontextmanager
    async def socket(*args, **kwargs):
        yield SimpleNamespace(send=send)

    monkeypatch.setattr(transfer, "_async_socket", socket)
    with pytest.raises(FileNotFoundError):
        await asyncio.wait_for(
            transfer._async_upload_directory(
                "test", "test", "runtime", tmp_path / "missing", "/dst", 2
            ),
            timeout=2,
        )
    assert "close_stdin" not in [
        json.loads(call.args[0])["type"] for call in send.call_args_list
    ]


async def exercise(source_root: Path, concurrency: int):
    source = source_root / "source"
    source.mkdir()
    payload = bytes(range(256)) * 512
    (source / "binary").write_bytes(payload)
    verified = set()

    async def handler(ws):
        start = json.loads(await ws.recv())
        assert start["type"] == "start"
        destination = start["args"][-1]
        contents = bytearray()
        async for raw in ws:
            message = json.loads(raw)
            if message["type"] == "stdin":
                contents.extend(base64.b64decode(message["data_base64"]))
            elif message["type"] == "close_stdin":
                with tarfile.open(fileobj=io.BytesIO(contents)) as archive:
                    assert archive.extractfile("./binary").read() == payload
                verified.add(destination)
                await ws.send(json.dumps({"type": "exit", "code": 0}))
                return

    loop = asyncio.get_running_loop()
    executor = ThreadPoolExecutor(max_workers=1)
    loop.set_default_executor(executor)
    release = threading.Event()
    blocker = loop.run_in_executor(None, release.wait)
    async with serve(handler, "127.0.0.1", 0, backlog=512) as server:
        endpoint = f"http://127.0.0.1:{server.sockets[0].getsockname()[1]}"
        tasks = [
            asyncio.create_task(
                transfer.async_upload_path(
                    endpoint,
                    "test",
                    "runtime",
                    source,
                    f"/upload-{index}",
                    timeout=15,
                    attempts=1,
                )
            )
            for index in range(concurrency)
        ]
        # Force consumers to start while every producer has to wait for a slot.
        await asyncio.sleep(0.5)
        release.set()
        await blocker
        done, pending = await asyncio.wait(tasks, timeout=10)
        if pending:
            print(
                f"Blocked: {len(done)}/{concurrency} completed, {len(pending)} pending",
                flush=True,
            )
            os._exit(1)
        for task in done:
            task.result()
    assert verified == {f"/upload-{index}" for index in range(concurrency)}
    print(f"{concurrency}/{concurrency} uploads completed and verified", flush=True)


if __name__ == "__main__":
    asyncio.run(exercise(Path(sys.argv[1]), int(sys.argv[2])))
