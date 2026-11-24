from __future__ import annotations

import asyncio
import contextvars
import hashlib
import os
import threading
from pathlib import Path
from types import SimpleNamespace

import pytest

from matrx_files import external_objects
from matrx_files.backends.router import BackendRouter
from matrx_files.backends.s3_backend import S3Backend
from matrx_files.backends.server_backend import ServerBackend


class BlockingClient:
    def __init__(self, *, fail: bool = False) -> None:
        self.started = threading.Event()
        self.release = threading.Event()
        self.finished = threading.Event()
        self.calls = 0
        self.fail = fail
        self.destination: Path | None = None

    def download_file(self, bucket: str, key: str, local_path: str) -> None:
        self.calls += 1
        self.destination = Path(local_path)
        temporary = self.destination.with_suffix(".provider-part")
        try:
            temporary.write_bytes(b"payload")
            self.started.set()
            if not self.release.wait(5):
                raise TimeoutError("test worker was not released")
            if self.fail:
                raise RuntimeError("transfer failed")
            os.replace(temporary, self.destination)
        finally:
            temporary.unlink(missing_ok=True)
            self.finished.set()


def make_engine(monkeypatch: pytest.MonkeyPatch, client: BlockingClient):
    backend = S3Backend()
    monkeypatch.setattr(backend, "_require_configured", lambda: None)
    monkeypatch.setattr(backend, "_get_client", lambda: client)
    router = BackendRouter()
    router._s3 = backend
    return SimpleNamespace(router=router), backend


@pytest.mark.parametrize("cancels,fail", [(1, False), (3, False), (3, True)])
async def test_cancel_drains_worker_before_external_object_cleanup(
    tmp_path, monkeypatch, cancels, fail
):
    client = BlockingClient(fail=fail)
    engine, _ = make_engine(monkeypatch, client)
    original_mkstemp = external_objects.tempfile.mkstemp
    monkeypatch.setattr(
        external_objects.tempfile,
        "mkstemp",
        lambda **kwargs: original_mkstemp(dir=tmp_path, **kwargs),
    )
    task = asyncio.create_task(external_objects._stream_and_hash(engine, "s3://bucket/key"))
    try:
        assert await asyncio.to_thread(client.started.wait, 2)
        for index in range(cancels):
            task.cancel("original cancellation" if index == 0 else "later cancellation")
            await asyncio.sleep(0.02)
        assert not task.done(), "cancellation returned while transfer still owned the path"
        assert not client.finished.is_set()
    finally:
        client.release.set()
        with pytest.raises(asyncio.CancelledError, match="original cancellation"):
            await task
    assert task.cancelled()
    assert client.finished.is_set()
    assert client.calls == 1
    assert list(tmp_path.iterdir()) == []


async def test_default_backend_drains_its_read_before_cancellation(tmp_path, monkeypatch):
    backend = ServerBackend()
    started, release, finished = threading.Event(), threading.Event(), threading.Event()

    def read(_path):
        started.set()
        try:
            assert release.wait(5)
            return b"fallback"
        finally:
            finished.set()

    monkeypatch.setattr(backend, "read", read)
    destination = tmp_path / "download"
    task = asyncio.create_task(backend.download_to_path_async("key", str(destination)))
    try:
        assert await asyncio.to_thread(started.wait, 2)
        task.cancel("fallback cancellation")
        await asyncio.sleep(0.02)
        assert not task.done()
    finally:
        release.set()
        with pytest.raises(asyncio.CancelledError, match="fallback cancellation"):
            await task
    assert finished.is_set()
    assert destination.read_bytes() == b"fallback"


@pytest.mark.parametrize("fail", [False, True])
async def test_download_normal_result_or_failure(tmp_path, monkeypatch, fail):
    client = BlockingClient(fail=fail)
    client.release.set()
    engine, _ = make_engine(monkeypatch, client)
    original_mkstemp = external_objects.tempfile.mkstemp
    monkeypatch.setattr(
        external_objects.tempfile,
        "mkstemp",
        lambda **kwargs: original_mkstemp(dir=tmp_path, **kwargs),
    )
    if fail:
        with pytest.raises(RuntimeError, match="transfer failed"):
            await external_objects._stream_and_hash(engine, "s3://bucket/key")
    else:
        size, digest = await external_objects._stream_and_hash(engine, "s3://bucket/key")
        assert (size, digest) == (7, hashlib.sha256(b"payload").hexdigest())
    assert client.calls == 1
    assert client.finished.is_set()
    assert list(tmp_path.iterdir()) == []


@pytest.mark.parametrize("fail", [False, True])
async def test_shutdown_cancellation_drains_s3_before_cleanup(tmp_path, monkeypatch, fail):
    """Cancelling every task must not cancel the thread's completion signal."""
    request_id = contextvars.ContextVar("download_request_id", default="missing")
    seen_context = []
    client = BlockingClient(fail=fail)
    original_download = client.download_file

    def download_with_context(bucket, key, local_path):
        seen_context.append(request_id.get())
        original_download(bucket, key, local_path)

    monkeypatch.setattr(client, "download_file", download_with_context)
    engine, _ = make_engine(monkeypatch, client)
    original_mkstemp = external_objects.tempfile.mkstemp
    monkeypatch.setattr(
        external_objects.tempfile,
        "mkstemp",
        lambda **kwargs: original_mkstemp(dir=tmp_path, **kwargs),
    )
    baseline = asyncio.all_tasks()
    token = request_id.set("request-collection-archive")
    try:
        caller = asyncio.create_task(external_objects._stream_and_hash(engine, "s3://bucket/key"))
    finally:
        request_id.reset(token)
    try:
        assert await asyncio.to_thread(client.started.wait, 2)
        # Model shutdown's all_tasks() sweep, including any internal transfer task.
        for task in asyncio.all_tasks() - baseline:
            task.cancel("shutdown cancellation")
        for _ in range(5):
            await asyncio.sleep(0)
        caller.cancel("repeated cancellation")
        for _ in range(5):
            await asyncio.sleep(0)
        assert not caller.done(), "shutdown returned before the transfer finished"
        assert not client.finished.is_set()
    finally:
        client.release.set()
        with pytest.raises(asyncio.CancelledError, match="shutdown cancellation"):
            await caller
        assert await asyncio.to_thread(client.finished.wait, 2)
    assert seen_context == ["request-collection-archive"]
    assert client.calls == 1
    assert list(tmp_path.iterdir()) == []
