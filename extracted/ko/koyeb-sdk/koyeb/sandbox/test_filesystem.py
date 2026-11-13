"""Pins the executor-reply seam of the filesystem layer: every dict
reply is interpreted once, error strings classify into the SDK taxonomy,
and shell fallbacks escape their arguments."""

import asyncio
import base64
import hashlib
import inspect
import json
import os
import signal
import sys
import tempfile
import threading
import time
import unittest
from contextlib import contextmanager
from unittest.mock import patch

from koyeb.sandbox.errors import (
    SandboxRequestError,
    SandboxServiceError,
    SandboxTimeoutError,
)
from koyeb.sandbox.exec import CommandResult, CommandStatus
from koyeb.sandbox.filesystem import (
    UPLOAD_CONCURRENCY,
    UPLOAD_PART_SIZE,
    AsyncSandboxFilesystem,
    FileInfo,
    SandboxFilesystem,
    SandboxFilesystemError,
    SandboxFileExistsError,
    SandboxFileNotFoundError,
)


class _FakeSyncClient:
    """Executor-reply fake: per-method dict replies or exceptions."""

    def __init__(self, **replies):
        self.replies = replies
        self.calls = []

    def _reply(self, method, *args):
        self.calls.append((method, *args))
        reply = self.replies.get(method, {})
        if isinstance(reply, Exception):
            raise reply
        return reply

    def write_file(self, path, content):
        return self._reply("write_file", path, content)

    def read_file(self, path):
        return self._reply("read_file", path)

    def make_dir(self, path):
        return self._reply("make_dir", path)

    def list_dir(self, path):
        return self._reply("list_dir", path)

    def delete_file(self, path):
        return self._reply("delete_file", path)

    def delete_dir(self, path):
        return self._reply("delete_dir", path)

    # Streamed /files routes (executor v0.0.24+). has_files_routes defaults
    # to False so legacy-behavior tests stay on the JSON routes.
    def has_files_routes(self):
        return self.replies.get("has_files_routes", False)

    def files_put(
        self, path, content, mode=None, parents=False, sha256=None, timeout=None
    ):
        # The real transport consumes the body inside the call; a lazy
        # generator would dangle past the caller's file close.
        if not isinstance(content, (bytes, bytearray)):
            content = b"".join(content)
        self.calls.append(("files_put", path, content, mode, sha256))
        reply = self.replies.get("files_put", {})
        if isinstance(reply, Exception):
            raise reply
        return reply

    def files_read(self, path, chunk_size=65536, timeout=None):
        self.calls.append(("files_read", path))
        reply = self.replies.get("files_read", b"")
        if isinstance(reply, Exception):
            raise reply
        return iter([reply])

    def files_stat(self, path):
        return self._reply("files_stat", path)


class _FakeAsyncClient(_FakeSyncClient):
    async def write_file(self, path, content):
        return _FakeSyncClient.write_file(self, path, content)

    async def read_file(self, path):
        return _FakeSyncClient.read_file(self, path)

    async def make_dir(self, path):
        return _FakeSyncClient.make_dir(self, path)

    async def list_dir(self, path):
        return _FakeSyncClient.list_dir(self, path)

    async def delete_file(self, path):
        return _FakeSyncClient.delete_file(self, path)

    async def delete_dir(self, path):
        return _FakeSyncClient.delete_dir(self, path)

    async def has_files_routes(self):
        return _FakeSyncClient.has_files_routes(self)

    async def files_put(
        self, path, content, mode=None, parents=False, sha256=None, timeout=None
    ):
        return _FakeSyncClient.files_put(
            self, path, content, mode=mode, sha256=sha256, timeout=timeout
        )

    async def files_read(self, path, chunk_size=65536, timeout=None):
        for chunk in _FakeSyncClient.files_read(self, path, timeout=timeout):
            yield chunk

    async def files_stat(self, path):
        return _FakeSyncClient.files_stat(self, path)


@contextmanager
def _fs(client):
    """SandboxFilesystem with its executor client patched for the block."""
    fs = SandboxFilesystem(sandbox=None)
    with patch.object(SandboxFilesystem, "_get_client", return_value=client):
        yield fs


@contextmanager
def _async_fs(client):
    """AsyncSandboxFilesystem with its async client patched for the block."""
    fs = AsyncSandboxFilesystem(sandbox=None)
    with patch.object(AsyncSandboxFilesystem, "_get_async_client", return_value=client):
        yield fs


class TestReplyInterpretation(unittest.TestCase):
    """Dict replies classify once: error strings map to the taxonomy."""

    def test_write_file_error(self):
        with _fs(_FakeSyncClient(write_file={"error": "disk full"})) as fs:
            with self.assertRaises(SandboxFilesystemError) as cm:
                fs.write_file("/a", "x")
        self.assertEqual(str(cm.exception), "Failed to write file: disk full")

    def test_write_file_base64_encodes_bytes(self):
        client = _FakeSyncClient()
        with _fs(client) as fs:
            fs.write_file("/b", b"\x00\x01", encoding="base64")
        method, path, content = client.calls[0]
        self.assertEqual((method, path), ("write_file", "/b"))
        self.assertEqual(content, base64.b64encode(b"\x00\x01").decode("ascii"))

    def test_read_file_returns_file_info(self):
        with _fs(_FakeSyncClient(read_file={"content": "hi"})) as fs:
            self.assertEqual(
                fs.read_file("/a"), FileInfo(content="hi", encoding="utf-8")
            )

    def test_read_file_base64_decodes_bytes(self):
        encoded = base64.b64encode(b"\x00\x01").decode("ascii")
        with _fs(_FakeSyncClient(read_file={"content": encoded})) as fs:
            info = fs.read_file("/a", encoding="base64")
        self.assertEqual(info.content, b"\x00\x01")
        self.assertEqual(info.encoding, "base64")

    def test_read_file_not_found(self):
        with _fs(
            _FakeSyncClient(read_file={"error": "no such file or directory"})
        ) as fs:
            with self.assertRaises(SandboxFileNotFoundError) as cm:
                fs.read_file("/a")
        self.assertEqual(str(cm.exception), "File not found: /a")

    def test_read_file_generic_error(self):
        with _fs(_FakeSyncClient(read_file={"error": "boom"})) as fs:
            with self.assertRaises(SandboxFilesystemError) as cm:
                fs.read_file("/a")
        self.assertEqual(str(cm.exception), "Failed to read file: boom")

    def test_exception_strings_classify_too(self):
        # Transport failures map through the same classifier, chained.
        with _fs(_FakeSyncClient(read_file=RuntimeError("... no such file ..."))) as fs:
            with self.assertRaises(SandboxFileNotFoundError) as cm:
                fs.read_file("/a")
        self.assertIsNotNone(cm.exception.__cause__)

    def test_mkdir_exists_error(self):
        with _fs(_FakeSyncClient(make_dir={"error": "file already exists"})) as fs:
            with self.assertRaises(SandboxFileExistsError) as cm:
                fs.mkdir("/d")
        self.assertEqual(str(cm.exception), "Directory already exists: /d")

    def test_mkdir_generic_error(self):
        with _fs(_FakeSyncClient(make_dir={"error": "boom"})) as fs:
            with self.assertRaises(SandboxFilesystemError) as cm:
                fs.mkdir("/d")
        self.assertEqual(str(cm.exception), "Failed to create directory: boom")

    def test_list_dir_entries_and_not_found(self):
        with _fs(_FakeSyncClient(list_dir={"entries": ["a", "b"]})) as fs:
            self.assertEqual(fs.list_dir("/d"), ["a", "b"])
        with _fs(_FakeSyncClient(list_dir={"error": "no such file"})) as fs:
            with self.assertRaises(SandboxFileNotFoundError) as cm:
                fs.list_dir("/d")
        self.assertEqual(str(cm.exception), "Directory not found: /d")

    def test_delete_file_not_found(self):
        with _fs(_FakeSyncClient(delete_file={"error": "no such file"})) as fs:
            with self.assertRaises(SandboxFileNotFoundError) as cm:
                fs.delete_file("/f")
        self.assertEqual(str(cm.exception), "File not found: /f")

    def test_delete_dir_not_empty(self):
        with _fs(_FakeSyncClient(delete_dir={"error": "directory not empty"})) as fs:
            with self.assertRaises(SandboxFilesystemError) as cm:
                fs.delete_dir("/d")
        self.assertEqual(str(cm.exception), "Directory not empty: /d")


class TestShellFallbacks(unittest.TestCase):
    """mv/test/rm run through the executor with escaped arguments."""

    @staticmethod
    def _result(exit_code=0, stderr=""):
        return CommandResult(
            stdout="",
            stderr=stderr,
            exit_code=exit_code,
            status=CommandStatus.FINISHED if exit_code == 0 else CommandStatus.FAILED,
        )

    @contextmanager
    def _fs(self, results):
        fs = SandboxFilesystem(sandbox=None)
        calls = []
        queue = list(results)

        def executor(cmd):
            calls.append(cmd)
            return queue.pop(0)

        with patch.object(SandboxFilesystem, "_get_executor", return_value=executor):
            yield fs, calls

    def test_rename_escapes_and_reports_not_found(self):
        with self._fs([self._result(), self._result(1, "mv: no such file")]) as (
            fs,
            calls,
        ):
            fs.rename_file("/a b", "/c d")
            self.assertEqual(calls[0], "mv '/a b' '/c d'")
            with self.assertRaises(SandboxFileNotFoundError):
                fs.rename_file("/gone", "/c")

    def test_exists_is_file_is_dir_use_test_builtins(self):
        with self._fs([self._result(), self._result(1), self._result()]) as (fs, calls):
            self.assertTrue(fs.exists("/x"))
            self.assertFalse(fs.is_file("/x"))
            self.assertTrue(fs.is_dir("/x"))
        self.assertEqual(
            [c.split()[:2] for c in calls],
            [["test", "-e"], ["test", "-f"], ["test", "-d"]],
        )

    def test_rm_recursive_flag_and_escaping(self):
        with self._fs([self._result(), self._result()]) as (fs, calls):
            fs.rm("/x")
            fs.rm("/x y", recursive=True)
        # shlex.quote leaves plain paths bare and quotes special ones
        self.assertEqual(calls, ["rm /x", "rm -rf '/x y'"])

    def test_rm_not_found(self):
        with self._fs([self._result(1, "no such file")]) as (fs, _):
            with self.assertRaises(SandboxFileNotFoundError):
                fs.rm("/gone")

    def test_move_file(self):
        with self._fs([self._result()]) as (fs, calls):
            fs.move_file("/a b", "/c")
        self.assertEqual(calls, ["mv '/a b' /c"])


class TestBatchAndTransfers(unittest.TestCase):
    def test_write_files_batches(self):
        client = _FakeSyncClient()
        with _fs(client) as fs:
            fs.write_files(
                [
                    {"path": "/a", "content": "1"},
                    {"path": "/b", "content": "2", "encoding": "base64"},
                ]
            )
        self.assertEqual([c[1] for c in client.calls], ["/a", "/b"])

    def test_upload_download_roundtrip(self):
        client = _FakeSyncClient(
            read_file={"content": base64.b64encode(b"payload").decode("ascii")}
        )
        with _fs(client) as fs:
            with tempfile.TemporaryDirectory() as tmp:
                local = os.path.join(tmp, "f.bin")
                with open(local, "wb") as f:
                    f.write(b"payload")
                fs.upload_file(local, "/remote", encoding="base64")
                self.assertEqual(client.calls[0][1], "/remote")
                target = os.path.join(tmp, "out.bin")
                fs.download_file("/remote", target, encoding="base64")
                with open(target, "rb") as f:
                    self.assertEqual(f.read(), b"payload")

    def test_upload_missing_local_file(self):
        with _fs(_FakeSyncClient()) as fs:
            with self.assertRaises(SandboxFileNotFoundError):
                fs.upload_file("/no/such/local", "/remote")


class TestSandboxFileIO(unittest.TestCase):
    def test_read_write_modes(self):
        with _fs(_FakeSyncClient(read_file={"content": "abc"})) as fs:
            with fs.open("/a", "r") as handle:
                self.assertEqual(handle.read(), "abc")
        client = _FakeSyncClient()
        with _fs(client) as fs:
            with fs.open("/b", "w") as handle:
                handle.write("data")
        self.assertEqual(client.calls[0][0], "write_file")

    def test_wrong_mode_raises(self):
        with _fs(_FakeSyncClient()) as fs:
            with self.assertRaises(ValueError):
                fs.open("/a", "r").write("x")
        with _fs(_FakeSyncClient()) as fs:
            with self.assertRaises(ValueError):
                fs.open("/a", "w").read()

    def test_closed_handle_raises(self):
        with _fs(_FakeSyncClient()) as fs:
            handle = fs.open("/a", "r")
            handle.close()
            with self.assertRaises(ValueError):
                handle.read()


class TestAsyncReplyInterpretation(unittest.TestCase):
    """Async twin classifies through the same taxonomy."""

    def test_read_file_not_found(self):
        with _async_fs(_FakeAsyncClient(read_file={"error": "no such file"})) as fs:
            with self.assertRaises(SandboxFileNotFoundError) as cm:
                asyncio.run(fs.read_file("/a"))
        self.assertEqual(str(cm.exception), "File not found: /a")

    def test_mkdir_exists_error(self):
        with _async_fs(_FakeAsyncClient(make_dir={"error": "already exists"})) as fs:
            with self.assertRaises(SandboxFileExistsError) as cm:
                asyncio.run(fs.mkdir("/d"))
        self.assertEqual(str(cm.exception), "Directory already exists: /d")

    def test_list_dir_entries(self):
        with _async_fs(_FakeAsyncClient(list_dir={"entries": ["x"]})) as fs:
            self.assertEqual(asyncio.run(fs.list_dir("/d")), ["x"])

    def test_delete_dir_not_empty(self):
        with _async_fs(
            _FakeAsyncClient(delete_dir={"error": "directory not empty"})
        ) as fs:
            with self.assertRaises(SandboxFilesystemError) as cm:
                asyncio.run(fs.delete_dir("/d"))
        self.assertEqual(str(cm.exception), "Directory not empty: /d")


class TestNewRoutesWriteFile(unittest.TestCase):
    """The streamed /files routes: binary-safe writes, real bytes on disk."""

    def _last_put(self, client):
        for call in reversed(client.calls):
            if call[0] == "files_put":
                return call
        raise AssertionError("no files_put call recorded")

    def test_bytes_go_raw(self):
        client = _FakeSyncClient(has_files_routes=True)
        with _fs(client) as fs:
            fs.write_file("/a.bin", b"\x00\xff\xfe")
        _, path, content, mode, _ = self._last_put(client)
        self.assertEqual(path, "/a.bin")
        self.assertEqual(content, b"\x00\xff\xfe")
        self.assertEqual(mode, None)

    def test_str_encodes_utf8(self):
        client = _FakeSyncClient(has_files_routes=True)
        with _fs(client) as fs:
            fs.write_file("/a.txt", "héllo")
        _, _, content, _, _ = self._last_put(client)
        self.assertEqual(content, "héllo".encode("utf-8"))

    def test_base64_is_transport_only_real_bytes_on_disk(self):
        client = _FakeSyncClient(has_files_routes=True)
        with _fs(client) as fs:
            fs.write_file(
                "/a.bin",
                base64.b64encode(b"\x00\x01").decode("ascii"),
                encoding="base64",
            )
        _, _, content, _, _ = self._last_put(client)
        self.assertEqual(content, b"\x00\x01")

    def test_mode_forwarded(self):
        client = _FakeSyncClient(has_files_routes=True)
        with _fs(client) as fs:
            fs.write_file("/a.sh", "x", mode="0755")
        _, _, _, mode, _ = self._last_put(client)
        self.assertEqual(mode, "0755")

    def test_404_classifies_not_found(self):
        client = _FakeSyncClient(
            has_files_routes=True,
            files_put=SandboxRequestError(
                status_code=404, body='{"error": "file does not exist"}'
            ),
        )
        with _fs(client) as fs:
            with self.assertRaises(SandboxFileNotFoundError) as cm:
                fs.write_file("/missing", b"x")
        self.assertEqual(str(cm.exception), "File not found: /missing")

    def test_409_classifies_exists(self):
        client = _FakeSyncClient(
            has_files_routes=True,
            files_put=SandboxRequestError(
                status_code=409,
                body='{"error": "destination is a directory"}',
            ),
        )
        with _fs(client) as fs:
            with self.assertRaises(SandboxFileExistsError) as cm:
                fs.write_file("/isdir", b"x")
        self.assertEqual(str(cm.exception), "destination is a directory")


class TestAsyncNewRoutesWriteFile(unittest.IsolatedAsyncioTestCase):
    async def test_bytes_go_raw(self):
        client = _FakeAsyncClient(has_files_routes=True)
        with _async_fs(client) as fs:
            await fs.write_file("/a.bin", b"\x00\xff\xfe")
        call = [c for c in client.calls if c[0] == "files_put"][-1]
        self.assertEqual(call[1], "/a.bin")
        self.assertEqual(call[2], b"\x00\xff\xfe")

    async def test_404_classifies_not_found(self):
        client = _FakeAsyncClient(
            has_files_routes=True,
            files_put=SandboxRequestError(
                status_code=404, body='{"error": "file does not exist"}'
            ),
        )
        with _async_fs(client) as fs:
            with self.assertRaises(SandboxFileNotFoundError):
                await fs.write_file("/missing", b"x")


class TestNewRoutesReadFile(unittest.TestCase):
    """Binary-safe reads on the streamed routes: sizes from stat, bytes from GET."""

    def test_encoding_none_returns_raw_bytes(self):
        client = _FakeSyncClient(has_files_routes=True, files_read=b"\x00\xff\xfe")
        with _fs(client) as fs:
            info = fs.read_file("/a.bin", encoding=None)
        self.assertEqual(info.content, b"\x00\xff\xfe")
        self.assertEqual(info.encoding, None)

    def test_utf8_decodes(self):
        client = _FakeSyncClient(has_files_routes=True, files_read="héllo".encode())
        with _fs(client) as fs:
            info = fs.read_file("/a.txt")
        self.assertEqual(info.content, "héllo")
        self.assertEqual(info.encoding, "utf-8")

    def test_base64_encodes_real_bytes(self):
        client = _FakeSyncClient(has_files_routes=True, files_read=b"\x00\x01")
        with _fs(client) as fs:
            info = fs.read_file("/a.bin", encoding="base64")
        self.assertEqual(info.content, base64.b64encode(b"\x00\x01").decode("ascii"))
        self.assertEqual(info.encoding, "base64")

    def test_404_classifies_not_found(self):
        client = _FakeSyncClient(
            has_files_routes=True,
            files_read=SandboxRequestError(
                status_code=404, body='{"error": "file does not exist"}'
            ),
        )
        with _fs(client) as fs:
            with self.assertRaises(SandboxFileNotFoundError) as cm:
                fs.read_file("/missing")
        self.assertEqual(str(cm.exception), "File not found: /missing")

    def test_open_read_yields_chunks(self):
        client = _FakeSyncClient(has_files_routes=True, files_read=b"\x00\xff")
        with _fs(client) as fs:
            chunks = list(fs.open_read("/a.bin"))
        self.assertEqual(b"".join(chunks), b"\x00\xff")


class TestAsyncNewRoutesReadFile(unittest.IsolatedAsyncioTestCase):
    async def test_encoding_none_returns_raw_bytes(self):
        client = _FakeAsyncClient(has_files_routes=True, files_read=b"\x00\xff\xfe")
        with _async_fs(client) as fs:
            info = await fs.read_file("/a.bin", encoding=None)
        self.assertEqual(info.content, b"\x00\xff\xfe")

    async def test_open_read_yields_chunks(self):
        client = _FakeAsyncClient(has_files_routes=True, files_read=b"\x00\xff")
        with _async_fs(client) as fs:
            chunks = []
            async for chunk in fs.open_read("/a.bin"):
                chunks.append(chunk)
        self.assertEqual(b"".join(chunks), b"\x00\xff")


class TestStat(unittest.TestCase):
    def test_returns_file_stat_from_entry(self):
        client = _FakeSyncClient(
            has_files_routes=True,
            files_stat={
                "type": "file",
                "size": 7,
                "mode": "0644",
                "mtime": "2026-10-27T10:00:00.123456789Z",
            },
        )
        with _fs(client) as fs:
            st = fs.stat("/a.txt")
        self.assertEqual(st.type, "file")
        self.assertEqual(st.size, 7)
        self.assertEqual(st.mode, "0644")
        self.assertEqual(st.mtime, "2026-10-27T10:00:00.123456789Z")
        self.assertIsNone(st.sha256)

    def test_404_classifies_not_found(self):
        client = _FakeSyncClient(
            has_files_routes=True,
            files_stat=SandboxRequestError(
                status_code=404, body='{"error": "file does not exist"}'
            ),
        )
        with _fs(client) as fs:
            with self.assertRaises(SandboxFileNotFoundError):
                fs.stat("/missing")

    def test_legacy_executors_raise_clear_error(self):
        client = _FakeSyncClient(has_files_routes=False)
        with _fs(client) as fs:
            with self.assertRaises(SandboxFilesystemError) as cm:
                fs.stat("/a.txt")
        self.assertIn("v0.0.24", str(cm.exception))


class TestAsyncStat(unittest.IsolatedAsyncioTestCase):
    async def test_returns_file_stat_from_entry(self):
        client = _FakeAsyncClient(
            has_files_routes=True,
            files_stat={"type": "dir", "size": 0, "mode": "0755", "mtime": "t"},
        )
        with _async_fs(client) as fs:
            st = await fs.stat("/tmp")
        self.assertEqual(st.type, "dir")
        self.assertEqual(st.mode, "0755")

    async def test_legacy_executors_raise_clear_error(self):
        client = _FakeAsyncClient(has_files_routes=False)
        with _async_fs(client) as fs:
            with self.assertRaises(SandboxFilesystemError) as cm:
                await fs.stat("/a.txt")
        self.assertIn("v0.0.24", str(cm.exception))


class TestNewRoutesTransfers(unittest.TestCase):
    """Streamed file transfers on the /files routes: raw bytes, progress, .part rename."""

    @staticmethod
    def _local(data):
        fd, path = tempfile.mkstemp()
        with os.fdopen(fd, "wb") as f:
            f.write(data)
        return path

    @staticmethod
    def _last_put(client):
        for call in reversed(client.calls):
            if call[0] == "files_put":
                return call
        raise AssertionError("no files_put call recorded")

    def test_upload_streams_binary_raw(self):
        import hashlib

        data = bytes(range(256)) * 1024
        local = self._local(data)
        digest = hashlib.sha256(data).hexdigest()
        client = _FakeSyncClient(
            has_files_routes=True,
            files_put={"size": len(data), "sha256": digest},
        )
        try:
            with _fs(client) as fs:
                fs.upload_file(local, "/remote.bin")
        finally:
            os.unlink(local)
        _, path, content, mode, sent_sha = self._last_put(client)
        self.assertEqual(path, "/remote.bin")
        self.assertEqual(content, data)
        self.assertEqual(sent_sha, digest)

    def test_upload_progress_reports_totals(self):
        import hashlib

        data = bytes(range(256)) * 1024
        local = self._local(data)
        calls = []
        client = _FakeSyncClient(
            has_files_routes=True,
            files_put={"size": len(data), "sha256": hashlib.sha256(data).hexdigest()},
        )
        with _fs(client) as fs:
            fs.upload_file(
                local,
                "/remote.bin",
                progress=lambda done, total: calls.append((done, total)),
            )
        os.unlink(local)
        self.assertEqual(calls[-1], (len(data), len(data)))
        self.assertLessEqual(len(calls), 6)

    def test_download_stats_streams_and_renames(self):
        data = b"\x00\xff" * 100
        client = _FakeSyncClient(
            has_files_routes=True,
            files_read=data,
            files_stat={"type": "file", "size": len(data), "mode": "0644"},
        )
        with tempfile.TemporaryDirectory() as d:
            target = os.path.join(d, "out.bin")
            with _fs(client) as fs:
                fs.download_file("/remote.bin", target)
            with open(target, "rb") as f:
                self.assertEqual(f.read(), data)
            self.assertFalse(os.path.exists(target + ".part"))

    def test_download_404_classifies_and_leaves_no_part(self):
        client = _FakeSyncClient(
            has_files_routes=True,
            files_stat=SandboxRequestError(
                status_code=404, body='{"error": "file does not exist"}'
            ),
        )
        with tempfile.TemporaryDirectory() as d:
            target = os.path.join(d, "out.bin")
            with _fs(client) as fs:
                with self.assertRaises(SandboxFileNotFoundError):
                    fs.download_file("/missing", target)
            self.assertFalse(os.path.exists(target + ".part"))


class TestAsyncNewRoutesTransfers(unittest.IsolatedAsyncioTestCase):
    @staticmethod
    def _local(data):
        fd, path = tempfile.mkstemp()
        with os.fdopen(fd, "wb") as f:
            f.write(data)
        return path

    async def test_upload_streams_binary_raw(self):
        import hashlib

        data = bytes(range(256)) * 1024
        local = self._local(data)
        digest = hashlib.sha256(data).hexdigest()
        client = _FakeAsyncClient(
            has_files_routes=True,
            files_put={"size": len(data), "sha256": digest},
        )
        try:
            with _async_fs(client) as fs:
                await fs.upload_file(local, "/remote.bin")
        finally:
            os.unlink(local)
        call = [c for c in client.calls if c[0] == "files_put"][-1]
        self.assertEqual(call[1], "/remote.bin")
        self.assertEqual(call[2], data)
        self.assertEqual(call[4], digest)

    async def test_download_stats_streams_and_renames(self):
        data = b"\x00\xff" * 100
        client = _FakeAsyncClient(
            has_files_routes=True,
            files_read=data,
            files_stat={"type": "file", "size": len(data), "mode": "0644"},
        )
        with tempfile.TemporaryDirectory() as d:
            target = os.path.join(d, "out.bin")
            with _async_fs(client) as fs:
                await fs.download_file("/remote.bin", target)
            with open(target, "rb") as f:
                self.assertEqual(f.read(), data)
            self.assertFalse(os.path.exists(target + ".part"))

    async def test_mid_transfer_404_leaves_no_part_file(self):
        client = _FakeAsyncClient(
            has_files_routes=True,
            files_read=SandboxRequestError(
                status_code=404, body='{"error": "file does not exist"}'
            ),
            files_stat={"type": "file", "size": 4},
        )
        with tempfile.TemporaryDirectory() as d:
            target = os.path.join(d, "out.bin")
            with _async_fs(client) as fs:
                with self.assertRaises(SandboxFileNotFoundError):
                    await fs.download_file("/gone", target)
            self.assertFalse(os.path.exists(target + ".part"))

    async def test_download_progress_reports_exact_totals(self):
        data = b"\x00" * 300
        client = _FakeAsyncClient(
            has_files_routes=True,
            files_read=data,
            files_stat={"type": "file", "size": len(data)},
        )
        calls = []
        with tempfile.TemporaryDirectory() as d:
            target = os.path.join(d, "out.bin")
            with _async_fs(client) as fs:
                await fs.download_file(
                    "/r.bin",
                    target,
                    progress=lambda done, total: calls.append((done, total)),
                )
        self.assertEqual(calls[-1], (len(data), len(data)))


class TestProgressReporter(unittest.TestCase):
    """progress(done, total): throttled to 100 ms, plus a guaranteed final call."""

    def test_throttle_and_final_call(self):
        from koyeb.sandbox import filesystem as fs_module

        calls = []
        reporter = fs_module._ProgressReporter(
            lambda done, total: calls.append((done, total)), total=100
        )
        clock = iter([0.1, 0.15, 0.26])

        with patch.object(fs_module.time, "monotonic", side_effect=lambda: next(clock)):
            reporter.update(10)  # 0.1 - 0.0 == 0.1: fires on the boundary
            reporter.update(20)  # 0.15 - 0.1 < 0.1: suppressed
            reporter.update(30)  # 0.26 - 0.1 >= 0.1: fires
        reporter.finish(100)  # always fires, whatever the throttle saw

        self.assertEqual(calls, [(10, 100), (30, 100), (100, 100)])

    def test_no_progress_callback_is_a_no_op(self):
        from koyeb.sandbox import filesystem as fs_module

        reporter = fs_module._ProgressReporter(None, total=100)
        reporter.update(10)
        reporter.finish(100)  # must not raise


class TestNewRoutesDownloadFailures(unittest.TestCase):
    def test_mid_transfer_404_leaves_no_part_file(self):
        client = _FakeSyncClient(
            has_files_routes=True,
            files_read=SandboxRequestError(
                status_code=404, body='{"error": "file does not exist"}'
            ),
            files_stat={"type": "file", "size": 4},
        )
        with tempfile.TemporaryDirectory() as d:
            target = os.path.join(d, "out.bin")
            with _fs(client) as fs:
                with self.assertRaises(SandboxFileNotFoundError):
                    fs.download_file("/gone", target)
            self.assertFalse(os.path.exists(target + ".part"))

    def test_download_progress_reports_exact_totals(self):
        data = b"\x00" * 300
        client = _FakeSyncClient(
            has_files_routes=True,
            files_read=data,
            files_stat={"type": "file", "size": len(data)},
        )
        calls = []
        with tempfile.TemporaryDirectory() as d:
            target = os.path.join(d, "out.bin")
            with _fs(client) as fs:
                fs.download_file(
                    "/r.bin",
                    target,
                    progress=lambda done, total: calls.append((done, total)),
                )
        self.assertEqual(calls[-1], (len(data), len(data)))

    def test_write_file_generic_status_carries_executor_message(self):
        client = _FakeSyncClient(
            has_files_routes=True,
            files_put=SandboxRequestError(
                status_code=400, body='{"error": "sha256 mismatch: got a, expected b"}'
            ),
        )
        with _fs(client) as fs:
            with self.assertRaises(SandboxFilesystemError) as cm:
                fs.write_file("/a", b"x")
        self.assertEqual(
            str(cm.exception),
            "Failed to write file: sha256 mismatch: got a, expected b",
        )


class TestLegacyEncodingContract(unittest.TestCase):
    """Legacy executors cannot return raw bytes: encoding=None must say so."""

    def test_none_encoding_raises_on_legacy(self):
        client = _FakeSyncClient(read_file={"content": "hi"})
        with _fs(client) as fs:
            with self.assertRaises(SandboxFilesystemError) as cm:
                fs.read_file("/a", encoding=None)
        self.assertIn("v0.0.24", str(cm.exception))

    def test_base64_keeps_legacy_decode_semantics(self):
        encoded = base64.b64encode(b"\x00\x01").decode("ascii")
        client = _FakeSyncClient(read_file={"content": encoded})
        with _fs(client) as fs:
            info = fs.read_file("/a", encoding="base64")
        self.assertEqual(info.content, b"\x00\x01")
        self.assertEqual(info.encoding, "base64")


class TestAsyncLegacyEncodingContract(unittest.IsolatedAsyncioTestCase):
    async def test_none_encoding_raises_on_legacy(self):
        client = _FakeAsyncClient(read_file={"content": "hi"})
        with _async_fs(client) as fs:
            with self.assertRaises(SandboxFilesystemError) as cm:
                await fs.read_file("/a", encoding=None)
        self.assertIn("v0.0.24", str(cm.exception))

    async def test_base64_keeps_legacy_decode_semantics(self):
        encoded = base64.b64encode(b"\x00\x01").decode("ascii")
        client = _FakeAsyncClient(read_file={"content": encoded})
        with _async_fs(client) as fs:
            info = await fs.read_file("/a", encoding="base64")
        self.assertEqual(info.content, b"\x00\x01")
        self.assertEqual(info.encoding, "base64")

    async def test_unexpected_failure_wraps(self):
        client = _FakeAsyncClient(read_file=ValueError("boom"))
        with _async_fs(client) as fs:
            with self.assertRaises(SandboxFilesystemError) as cm:
                await fs.read_file("/a")
        self.assertIn("boom", str(cm.exception))


class TestAsyncLegacyWriteFile(unittest.IsolatedAsyncioTestCase):
    async def test_base64_encodes_bytes_on_legacy(self):
        client = _FakeAsyncClient()
        with _async_fs(client) as fs:
            await fs.write_file("/b", b"\x00\x01", encoding="base64")
        method, path, content = client.calls[0]
        self.assertEqual((method, path), ("write_file", "/b"))
        self.assertEqual(content, base64.b64encode(b"\x00\x01").decode("ascii"))

    async def test_utf8_encodes_bytes_on_legacy(self):
        client = _FakeAsyncClient()
        with _async_fs(client) as fs:
            await fs.write_file("/b", b"hi", encoding="utf-8")
        method, path, content = client.calls[0]
        self.assertEqual((method, path), ("write_file", "/b"))
        self.assertEqual(content, "hi")

    async def test_unexpected_failure_wraps(self):
        client = _FakeAsyncClient(write_file=ValueError("boom"))
        with _async_fs(client) as fs:
            with self.assertRaises(SandboxFilesystemError) as cm:
                await fs.write_file("/b", "x")
        self.assertIn("Failed to write file", str(cm.exception))
        self.assertIn("boom", str(cm.exception))


class TestAsyncUploadDownloadRoundtrip(unittest.IsolatedAsyncioTestCase):
    async def test_roundtrip_on_legacy_routes(self):
        client = _FakeAsyncClient(
            read_file={"content": base64.b64encode(b"payload").decode("ascii")}
        )
        with _async_fs(client) as fs:
            with tempfile.TemporaryDirectory() as tmp:
                local = os.path.join(tmp, "f.bin")
                with open(local, "wb") as f:
                    f.write(b"payload")
                await fs.upload_file(local, "/remote", encoding="base64")
                self.assertEqual(client.calls[0][1], "/remote")
                target = os.path.join(tmp, "out.bin")
                await fs.download_file("/remote", target, encoding="base64")
                with open(target, "rb") as f:
                    self.assertEqual(f.read(), b"payload")


class TestNewRoutesUploadIntegrity(unittest.TestCase):
    """upload_file verifies content end to end: X-Content-SHA256 both ways."""

    @staticmethod
    def _local(data):
        import hashlib

        fd, path = tempfile.mkstemp()
        with os.fdopen(fd, "wb") as f:
            f.write(data)
        return path, hashlib.sha256(data).hexdigest()

    def test_upload_sends_content_sha256(self):
        data = bytes(range(256)) * 512
        local, digest = self._local(data)
        client = _FakeSyncClient(
            has_files_routes=True,
            files_put={"size": len(data), "sha256": digest},
        )
        try:
            with _fs(client) as fs:
                fs.upload_file(local, "/r.bin")
        finally:
            os.unlink(local)
        call = [c for c in client.calls if c[0] == "files_put"][-1]
        self.assertEqual(call[4], digest)

    def test_upload_reply_mismatch_raises(self):
        data = b"abc"
        local, digest = self._local(data)
        client = _FakeSyncClient(
            has_files_routes=True,
            files_put={"size": 3, "sha256": "deadbeef"},
        )
        try:
            with _fs(client) as fs:
                with self.assertRaises(SandboxFilesystemError) as cm:
                    fs.upload_file(local, "/r.bin")
        finally:
            os.unlink(local)
        self.assertIn("corrupt", str(cm.exception))


class TestAsyncNewRoutesUploadIntegrity(unittest.IsolatedAsyncioTestCase):
    async def test_upload_sends_content_sha256(self):
        import hashlib

        data = bytes(range(256)) * 512
        fd, local = tempfile.mkstemp()
        with os.fdopen(fd, "wb") as f:
            f.write(data)
        digest = hashlib.sha256(data).hexdigest()
        client = _FakeAsyncClient(
            has_files_routes=True,
            files_put={"size": len(data), "sha256": digest},
        )
        try:
            with _async_fs(client) as fs:
                await fs.upload_file(local, "/r.bin")
        finally:
            os.unlink(local)
        call = [c for c in client.calls if c[0] == "files_put"][-1]
        self.assertEqual(call[4], digest)

    async def test_upload_reply_mismatch_raises(self):
        data = b"abc"
        fd, local = tempfile.mkstemp()
        with os.fdopen(fd, "wb") as f:
            f.write(data)
        client = _FakeAsyncClient(
            has_files_routes=True,
            files_put={"size": 3, "sha256": "deadbeef"},
        )
        try:
            with _async_fs(client) as fs:
                with self.assertRaises(SandboxFilesystemError) as cm:
                    await fs.upload_file(local, "/r.bin")
        finally:
            os.unlink(local)
        self.assertIn("corrupt", str(cm.exception))


class TestWriteFileStreams(unittest.TestCase):
    """write_file accepts streams on the new routes; legacy says so when it can't."""

    def test_iterable_content_streams(self):
        client = _FakeSyncClient(has_files_routes=True)
        with _fs(client) as fs:
            fs.write_file("/a", iter([b"ab", b"cdef"]))
        call = [c for c in client.calls if c[0] == "files_put"][-1]
        self.assertEqual(call[1], "/a")
        self.assertEqual(call[2], b"abcdef")

    def test_stream_content_raises_on_legacy(self):
        client = _FakeSyncClient()
        with _fs(client) as fs:
            with self.assertRaises(SandboxFilesystemError) as cm:
                fs.write_file("/a", iter([b"ab"]))
        self.assertIn("v0.0.24", str(cm.exception))


class TestAsyncWriteFileStreams(unittest.IsolatedAsyncioTestCase):
    async def test_iterable_content_streams(self):
        client = _FakeAsyncClient(has_files_routes=True)
        with _async_fs(client) as fs:
            await fs.write_file("/a", iter([b"ab", b"cdef"]))
        call = [c for c in client.calls if c[0] == "files_put"][-1]
        self.assertEqual(call[1], "/a")
        self.assertEqual(call[2], b"abcdef")

    async def test_stream_content_raises_on_legacy(self):
        client = _FakeAsyncClient()
        with _async_fs(client) as fs:
            with self.assertRaises(SandboxFilesystemError) as cm:
                await fs.write_file("/a", iter([b"ab"]))
        self.assertIn("v0.0.24", str(cm.exception))


class TestOpenReadLegacy(unittest.TestCase):
    """Legacy open_read: the file is read as text and yielded as one chunk."""

    def test_yields_text_bytes_as_one_chunk(self):
        client = _FakeSyncClient(read_file={"content": "hello"})
        with _fs(client) as fs:
            chunks = list(fs.open_read("/a"))
        self.assertEqual(chunks, [b"hello"])


class TestAsyncOpenReadLegacy(unittest.IsolatedAsyncioTestCase):
    async def test_yields_text_bytes_as_one_chunk(self):
        client = _FakeAsyncClient(read_file={"content": "hello"})
        with _async_fs(client) as fs:
            chunks = []
            async for chunk in fs.open_read("/a"):
                chunks.append(chunk)
        self.assertEqual(chunks, [b"hello"])


class TestMalformedStatReplies(unittest.TestCase):
    """Malformed executor replies fail fast — no plausible FileStat fabricated."""

    def test_stat_missing_fields_raises(self):
        client = _FakeSyncClient(has_files_routes=True, files_stat={"size": 5})
        with _fs(client) as fs:
            with self.assertRaises(SandboxFilesystemError) as cm:
                fs.stat("/a")
        self.assertIn("Failed to stat file", str(cm.exception))

    def test_download_missing_size_raises(self):
        client = _FakeSyncClient(
            has_files_routes=True,
            files_stat={"type": "file"},
            files_read=b"x",
        )
        with tempfile.TemporaryDirectory() as d:
            target = os.path.join(d, "out.bin")
            with _fs(client) as fs:
                with self.assertRaises(SandboxFilesystemError) as cm:
                    fs.download_file("/r", target)
        self.assertIn("Failed to download file", str(cm.exception))
        self.assertFalse(os.path.exists(target + ".part"))


class TestAsyncMalformedStatReplies(unittest.IsolatedAsyncioTestCase):
    async def test_stat_missing_fields_raises(self):
        client = _FakeAsyncClient(has_files_routes=True, files_stat={"size": 5})
        with _async_fs(client) as fs:
            with self.assertRaises(SandboxFilesystemError) as cm:
                await fs.stat("/a")
        self.assertIn("Failed to stat file", str(cm.exception))


class TestAsyncWriteFileLegacyErrors(unittest.IsolatedAsyncioTestCase):
    async def test_legacy_error_reply_classifies(self):
        client = _FakeAsyncClient(write_file={"error": "no such file or directory"})
        with _async_fs(client) as fs:
            with self.assertRaises(SandboxFilesystemError) as cm:
                await fs.write_file("/a", "x")
        self.assertIn("Failed to write file", str(cm.exception))


class _UploadFakeExecutor:
    """Stateful fake for the multipart session flow.

    Parts land at offsets into a pre-sized buffer; complete answers 409
    with the true missing ranges until coverage holds, then verifies the
    whole-file digest the way the executor does. fail_parts / forget_parts
    / never_record script the faults the fs layer must recover from;
    omit_complete_sha drops the contract-optional digest from the
    complete reply.
    """

    def __init__(
        self,
        *,
        max_part_size=1 << 30,
        fail_parts=None,
        forget_parts=(),
        never_record=(),
        open_reply=None,
        lie_about_sha=None,
        raw_409_body=None,
        abort_error=False,
        on_part=None,
        omit_complete_sha=False,
    ):
        self.max_part_size = max_part_size
        self.fail_parts = dict(fail_parts or {})
        self.forget_parts = set(forget_parts)
        self.never_record = set(never_record)
        self.open_reply = open_reply
        self.lie_about_sha = lie_about_sha
        self.raw_409_body = raw_409_body
        self.abort_error = abort_error
        self.on_part = on_part
        self.omit_complete_sha = omit_complete_sha
        self.session = None
        self.calls = []
        self.in_flight = 0
        self.max_in_flight = 0
        self._lock = threading.Lock()

    # -- executor semantics ----------------------------------------------

    def _enter_part(self):
        self.in_flight += 1
        self.max_in_flight = max(self.max_in_flight, self.in_flight)

    def _exit_part(self):
        self.in_flight -= 1

    def _live(self):
        if self.session is None:
            raise SandboxRequestError(
                404, json.dumps({"error": "unknown upload session"})
            )
        return self.session

    def _record(self, start, end):
        # The executor's addSpan: merge every overlapping-or-adjacent span
        # into the new one, keep the rest, sort.
        ns, ne = start, end
        out = []
        for sp in self.session["spans"]:
            if sp[1] >= ns and ne >= sp[0]:
                ns, ne = min(ns, sp[0]), max(ne, sp[1])
                continue
            out.append(sp)
        out.append((ns, ne))
        out.sort()
        self.session["spans"] = out

    def _missing(self):
        at, missing = 0, []
        for start, end in self.session["spans"]:
            if start > at:
                missing.append((at, start))
            at = max(at, end)
        if at < self.session["size"]:
            missing.append((at, self.session["size"]))
        return missing

    def _part_core(self, offset, content, sha256, timeout):
        self.calls.append(("part", offset, bytes(content), sha256, timeout))
        key = (offset, len(content))
        if key in self.fail_parts:
            raise self.fail_parts.pop(key)
        with self._lock:
            sess = self._live()
            if sha256 is not None and hashlib.sha256(content).hexdigest() != sha256:
                raise SandboxRequestError(
                    400, json.dumps({"error": "sha256 mismatch on part"})
                )
            if offset + len(content) > sess["size"]:
                raise SandboxRequestError(
                    400, json.dumps({"error": "part writes past the end"})
                )
            if len(content) > self.max_part_size:
                raise SandboxRequestError(
                    413, json.dumps({"error": "part is larger than max_part_size"})
                )
            sess["data"][offset : offset + len(content)] = content
            if offset in self.never_record:
                pass
            elif offset in self.forget_parts:
                self.forget_parts.discard(offset)
            else:
                self._record(offset, offset + len(content))

    # -- transport surface (the fs layer's seam) --------------------------

    def has_files_routes(self):
        return True

    def files_stat(self, path):
        self.calls.append(("files_stat", path))
        return {
            "type": "file",
            "size": 12,
            "mode": "0644",
            "mtime": "2026-01-01T00:00:00Z",
        }

    def files_put(
        self, path, content, mode=None, parents=False, sha256=None, timeout=None
    ):
        content = content if isinstance(content, bytes) else b"".join(content)
        self.calls.append(("files_put", path, content, sha256, timeout))
        return {"size": len(content), "sha256": hashlib.sha256(content).hexdigest()}

    def files_read(self, path, chunk_size=65536, timeout=None):
        self.calls.append(("files_read", path, timeout))
        return iter([b"remote-bytes"])

    def files_upload_open(self, path, size, mode=None, sha256=None, timeout=None):
        self.calls.append(("open", path, size, sha256, timeout))
        if self.open_reply is not None:
            return dict(self.open_reply)
        self.session = {
            "path": path,
            "size": size,
            "want": sha256,
            "data": bytearray(size),
            "spans": [],
        }
        return {"upload_id": "u-1", "max_part_size": self.max_part_size}

    def files_upload_part(self, upload_id, offset, content, sha256=None, timeout=None):
        self._enter_part()
        try:
            if self.on_part is not None:
                self.on_part()
            self._part_core(offset, content, sha256, timeout)
        finally:
            self._exit_part()

    def files_upload_complete(self, upload_id, timeout=None):
        self.calls.append(("complete", timeout))
        sess = self._live()
        missing = self._missing()
        if missing:
            body = (
                self.raw_409_body
                if self.raw_409_body is not None
                else json.dumps(
                    {
                        "error": f"{len(missing)} range(s) still missing",
                        "ranges": [{"start": s, "end": e} for s, e in missing],
                    }
                )
            )
            raise SandboxRequestError(409, body)
        digest = hashlib.sha256(bytes(sess["data"])).hexdigest()
        if sess["want"] is not None and digest != sess["want"]:
            self.session = None
            raise SandboxRequestError(
                400, json.dumps({"error": f"sha256 mismatch: got {digest}"})
            )
        if self.omit_complete_sha:
            return {"size": sess["size"]}
        return {
            "size": sess["size"],
            "sha256": digest if self.lie_about_sha is None else self.lie_about_sha,
        }

    def files_upload_abort(self, upload_id, timeout=None):
        self.calls.append(("abort", timeout))
        if self.abort_error:
            raise SandboxRequestError(
                404, json.dumps({"error": "unknown upload session"})
            )
        self._live()
        self.session = None

    # -- readouts for assertions -----------------------------------------

    def kinds(self):
        return [c[0] for c in self.calls]

    def part_puts(self):
        """(offset, length) of every part PUT, in call order."""
        return [(c[1], len(c[2])) for c in self.calls if c[0] == "part"]

    def landed(self):
        return bytes(self.session["data"]) if self.session else None


class _AsyncUploadFakeExecutor(_UploadFakeExecutor):
    async def has_files_routes(self):
        return True

    async def files_stat(self, path):
        return _UploadFakeExecutor.files_stat(self, path)

    async def files_put(
        self, path, content, mode=None, parents=False, sha256=None, timeout=None
    ):
        return _UploadFakeExecutor.files_put(
            self,
            path,
            content,
            mode=mode,
            parents=parents,
            sha256=sha256,
            timeout=timeout,
        )

    async def files_read(self, path, chunk_size=65536, timeout=None):
        for chunk in _UploadFakeExecutor.files_read(self, path, chunk_size, timeout):
            yield chunk

    async def files_upload_open(self, path, size, mode=None, sha256=None, timeout=None):
        return _UploadFakeExecutor.files_upload_open(
            self, path, size, mode=mode, sha256=sha256, timeout=timeout
        )

    async def files_upload_part(
        self, upload_id, offset, content, sha256=None, timeout=None
    ):
        self._enter_part()
        try:
            if self.on_part is not None:
                maybe = self.on_part()
                if inspect.isawaitable(maybe):
                    await maybe
            self._part_core(offset, content, sha256, timeout)
        finally:
            self._exit_part()

    async def files_upload_complete(self, upload_id, timeout=None):
        return _UploadFakeExecutor.files_upload_complete(
            self, upload_id, timeout=timeout
        )

    async def files_upload_abort(self, upload_id, timeout=None):
        return _UploadFakeExecutor.files_upload_abort(self, upload_id, timeout=timeout)


def _local_file(directory, name, data):
    path = os.path.join(directory, name)
    with open(path, "wb") as f:
        f.write(data)
    return path


class TestUploadDefaults(unittest.TestCase):
    """The documented defaults, pinned where the flow reads them."""

    def test_documented_defaults(self):
        self.assertEqual(UPLOAD_PART_SIZE, 50 * 1024 * 1024)
        self.assertEqual(UPLOAD_CONCURRENCY, 4)


class TestUploadMultipartDispatch(unittest.TestCase):
    """size > part_size opens a session; otherwise the single streamed PUT."""

    DATA = b"abcdefghijkl"

    def test_small_file_takes_the_single_put(self):
        fake = _UploadFakeExecutor()
        with tempfile.TemporaryDirectory() as d:
            local = _local_file(d, "small.bin", b"abc")
            with _fs(fake) as fs:
                fs.upload_file(local, "/r/small.bin")
        self.assertEqual(fake.kinds(), ["files_put"])
        self.assertIsNone(fake.session)

    def test_size_past_part_size_opens_a_session(self):
        fake = _UploadFakeExecutor()
        with tempfile.TemporaryDirectory() as d:
            local = _local_file(d, "big.bin", self.DATA)
            with _fs(fake) as fs:
                fs.upload_file(local, "/r/big.bin", part_size=4, concurrency=1)
        self.assertEqual(fake.kinds()[0], "open")
        self.assertNotIn("files_put", fake.kinds())
        self.assertEqual(fake.kinds()[-1], "complete")
        self.assertEqual(fake.landed(), self.DATA)

    def test_zero_byte_file_takes_the_single_put(self):
        fake = _UploadFakeExecutor()
        with tempfile.TemporaryDirectory() as d:
            local = _local_file(d, "empty.bin", b"")
            with _fs(fake) as fs:
                fs.upload_file(local, "/r/empty.bin", part_size=4)
        self.assertEqual(fake.kinds(), ["files_put"])

    def test_part_size_capped_by_max_part_size(self):
        fake = _UploadFakeExecutor(max_part_size=3)
        with tempfile.TemporaryDirectory() as d:
            local = _local_file(d, "big.bin", self.DATA)
            with _fs(fake) as fs:
                fs.upload_file(local, "/r/big.bin", part_size=4)
        self.assertEqual(sorted(fake.part_puts()), [(0, 3), (3, 3), (6, 3), (9, 3)])
        self.assertEqual(fake.landed(), self.DATA)

    def test_invalid_part_size_raises_before_any_wire_call(self):
        fake = _UploadFakeExecutor()
        with tempfile.TemporaryDirectory() as d:
            local = _local_file(d, "x", b"abc")
            with _fs(fake) as fs:
                with self.assertRaises(SandboxFilesystemError):
                    fs.upload_file(local, "/r/x", part_size=0)
        self.assertEqual(fake.calls, [])

    def test_invalid_concurrency_raises_before_any_wire_call(self):
        fake = _UploadFakeExecutor()
        with tempfile.TemporaryDirectory() as d:
            local = _local_file(d, "x", b"abc")
            with _fs(fake) as fs:
                with self.assertRaises(SandboxFilesystemError):
                    fs.upload_file(local, "/r/x", concurrency=0)
        self.assertEqual(fake.calls, [])


class TestUploadSessionWire(unittest.TestCase):
    """The session flow's wire contract: open payload, parts, complete."""

    DATA = b"abcdefghijkl"

    def test_open_sends_path_size_and_whole_file_digest(self):
        fake = _UploadFakeExecutor()
        with tempfile.TemporaryDirectory() as d:
            local = _local_file(d, "big.bin", self.DATA)
            with _fs(fake) as fs:
                fs.upload_file(local, "/r/big.bin", part_size=4, concurrency=1)
        open_call = fake.calls[0]
        self.assertEqual(open_call[0], "open")
        self.assertEqual(open_call[1], "/r/big.bin")
        self.assertEqual(open_call[2], 12)
        self.assertEqual(open_call[3], hashlib.sha256(self.DATA).hexdigest())

    def test_parts_carry_their_bytes_at_offsets_with_per_part_digests(self):
        fake = _UploadFakeExecutor()
        with tempfile.TemporaryDirectory() as d:
            local = _local_file(d, "big.bin", self.DATA)
            with _fs(fake) as fs:
                fs.upload_file(local, "/r/big.bin", part_size=4, concurrency=1)
        self.assertEqual(fake.part_puts(), [(0, 4), (4, 4), (8, 4)])
        for call in fake.calls:
            if call[0] == "part":
                self.assertEqual(call[3], hashlib.sha256(call[2]).hexdigest())
        self.assertEqual(fake.landed(), self.DATA)

    def test_reply_digest_mismatch_raises_corrupted(self):
        fake = _UploadFakeExecutor(lie_about_sha="ff" * 32)
        with tempfile.TemporaryDirectory() as d:
            local = _local_file(d, "big.bin", self.DATA)
            with _fs(fake) as fs:
                with self.assertRaises(SandboxFilesystemError) as cm:
                    fs.upload_file(local, "/r/big.bin", part_size=4)
        self.assertIn("corrupted in transit", str(cm.exception))
        self.assertIn("abort", fake.kinds())

    def test_complete_reply_without_sha256_still_succeeds(self):
        # The wire contract marks complete's sha256 optional: a 200 has
        # already matched the open-payload digest at the executor.
        fake = _UploadFakeExecutor(omit_complete_sha=True)
        with tempfile.TemporaryDirectory() as d:
            local = _local_file(d, "big.bin", self.DATA)
            with _fs(fake) as fs:
                fs.upload_file(local, "/r/big.bin", part_size=4, concurrency=1)
        self.assertEqual(fake.landed(), self.DATA)
        self.assertNotIn("abort", fake.kinds())

    def test_open_reply_without_max_part_size_aborts_the_live_session(self):
        # A valid upload_id means the session exists at the executor;
        # failing on the cap must abort it, not strand its temp file.
        fake = _UploadFakeExecutor(open_reply={"upload_id": "u-1"})
        with tempfile.TemporaryDirectory() as d:
            local = _local_file(d, "big.bin", self.DATA)
            with _fs(fake) as fs:
                with self.assertRaises(SandboxFilesystemError) as cm:
                    fs.upload_file(local, "/r/big.bin", part_size=4, concurrency=1)
        self.assertIn("max_part_size", str(cm.exception))
        self.assertEqual(fake.kinds().count("abort"), 1)
        self.assertNotIn("part", fake.kinds())

    def test_malformed_open_reply_raises_without_aborting(self):
        fake = _UploadFakeExecutor(open_reply={"max_part_size": 4})
        with tempfile.TemporaryDirectory() as d:
            local = _local_file(d, "big.bin", self.DATA)
            with _fs(fake) as fs:
                with self.assertRaises(SandboxFilesystemError) as cm:
                    fs.upload_file(local, "/r/big.bin", part_size=4)
        self.assertIn("upload_id", str(cm.exception))
        self.assertNotIn("abort", fake.kinds())
        self.assertNotIn("part", fake.kinds())


class TestUploadConcurrency(unittest.TestCase):
    """concurrency=4 parts in flight, each read from disk at its offset."""

    DATA = bytes(range(32))

    def test_four_parts_in_flight(self):
        # The barrier only passes when four parts are truly simultaneous;
        # a smaller pool breaks it and the upload fails.
        barrier = threading.Barrier(4, timeout=10)
        fake = _UploadFakeExecutor(on_part=barrier.wait)
        with tempfile.TemporaryDirectory() as d:
            local = _local_file(d, "big.bin", self.DATA)
            with _fs(fake) as fs:
                fs.upload_file(local, "/r/big.bin", part_size=4)
        self.assertEqual(fake.max_in_flight, 4)
        self.assertEqual(fake.landed(), self.DATA)

    def test_concurrency_one_runs_serially(self):
        fake = _UploadFakeExecutor()
        with tempfile.TemporaryDirectory() as d:
            local = _local_file(d, "big.bin", self.DATA)
            with _fs(fake) as fs:
                fs.upload_file(local, "/r/big.bin", part_size=4, concurrency=1)
        self.assertEqual(fake.max_in_flight, 1)
        self.assertEqual(
            fake.part_puts(),
            [(0, 4), (4, 4), (8, 4), (12, 4), (16, 4), (20, 4), (24, 4), (28, 4)],
        )


class TestUploadTimeoutSplit(unittest.TestCase):
    """A part that times out is split: the fs layer's own retry."""

    DATA = b"abcdefghijkl"

    def test_timed_out_part_is_split_into_halves(self):
        fake = _UploadFakeExecutor(
            fail_parts={(0, 8): SandboxTimeoutError("Request timed out after 60s")}
        )
        with tempfile.TemporaryDirectory() as d:
            local = _local_file(d, "big.bin", self.DATA)
            with _fs(fake) as fs:
                with patch("koyeb.sandbox.filesystem._MIN_SPLIT_SIZE", 2):
                    fs.upload_file(local, "/r/big.bin", part_size=8, concurrency=1)
        # The failed (0, 8) attempt is part of the wire history; the
        # landed coverage is the two halves plus the untouched tail.
        self.assertEqual(sorted(fake.part_puts()), [(0, 4), (0, 8), (4, 4), (8, 4)])
        self.assertEqual(fake.landed(), self.DATA)

    def test_cloudflare_524_is_split_too(self):
        fake = _UploadFakeExecutor(
            fail_parts={(0, 8): SandboxServiceError(524, "origin timeout")}
        )
        with tempfile.TemporaryDirectory() as d:
            local = _local_file(d, "big.bin", self.DATA)
            with _fs(fake) as fs:
                with patch("koyeb.sandbox.filesystem._MIN_SPLIT_SIZE", 2):
                    fs.upload_file(local, "/r/big.bin", part_size=8, concurrency=1)
        self.assertEqual(sorted(fake.part_puts()), [(0, 4), (0, 8), (4, 4), (8, 4)])
        self.assertEqual(fake.landed(), self.DATA)

    def test_split_recurves_until_a_part_lands(self):
        fake = _UploadFakeExecutor(
            fail_parts={
                (0, 8): SandboxTimeoutError("Request timed out after 60s"),
                (0, 4): SandboxTimeoutError("Request timed out after 60s"),
            }
        )
        with tempfile.TemporaryDirectory() as d:
            local = _local_file(d, "big.bin", self.DATA)
            with _fs(fake) as fs:
                with patch("koyeb.sandbox.filesystem._MIN_SPLIT_SIZE", 2):
                    fs.upload_file(local, "/r/big.bin", part_size=8, concurrency=1)
        self.assertEqual(
            sorted(fake.part_puts()),
            [(0, 2), (0, 4), (0, 8), (2, 2), (4, 4), (8, 4)],
        )
        self.assertEqual(fake.landed(), self.DATA)

    def test_part_below_split_floor_fails_the_upload(self):
        fake = _UploadFakeExecutor(
            fail_parts={(0, 4): SandboxTimeoutError("Request timed out after 60s")}
        )
        with tempfile.TemporaryDirectory() as d:
            local = _local_file(d, "big.bin", self.DATA)
            with _fs(fake) as fs:
                with patch("koyeb.sandbox.filesystem._MIN_SPLIT_SIZE", 4):
                    with self.assertRaises(SandboxFilesystemError) as cm:
                        fs.upload_file(local, "/r/big.bin", part_size=4, concurrency=1)
        self.assertIn("timed out", str(cm.exception))
        self.assertIn("abort", fake.kinds())


class TestUploadAbortOnFailure(unittest.TestCase):
    """A hard failure aborts the session; abort never masks the cause."""

    DATA = b"abcdefghijkl"

    @unittest.skipIf(sys.platform == "win32", "^C replay is POSIX-only")
    def test_interrupt_aborts_without_draining_the_queue(self):
        # A ^C mid-upload must surface promptly: the workers finish
        # their in-flight part and stop instead of draining the plan.
        first_in_flight = threading.Event()
        release = threading.Event()
        signalled = [0.0]

        def on_part():
            if not first_in_flight.is_set():
                first_in_flight.set()
                release.wait(timeout=10)
            else:
                time.sleep(0.2)

        def interrupter():
            first_in_flight.wait(timeout=10)
            signalled[0] = time.monotonic()
            os.kill(os.getpid(), signal.SIGINT)
            time.sleep(0.1)
            release.set()

        fake = _UploadFakeExecutor(on_part=on_part)
        with tempfile.TemporaryDirectory() as d:
            local = _local_file(d, "big.bin", bytes(80))
            with _fs(fake) as fs:
                thread = threading.Thread(target=interrupter)
                thread.start()
                try:
                    with self.assertRaises(KeyboardInterrupt):
                        fs.upload_file(local, "/r/big.bin", part_size=4, concurrency=2)
                finally:
                    thread.join(timeout=5)
        self.assertIn("abort", fake.kinds())
        self.assertLess(time.monotonic() - signalled[0], 1.0)

    def test_hard_part_failure_aborts_and_raises(self):
        fake = _UploadFakeExecutor(
            fail_parts={
                (4, 4): SandboxRequestError(
                    400, json.dumps({"error": "sha256 mismatch on part"})
                )
            }
        )
        with tempfile.TemporaryDirectory() as d:
            local = _local_file(d, "big.bin", self.DATA)
            with _fs(fake) as fs:
                with self.assertRaises(SandboxFilesystemError) as cm:
                    fs.upload_file(local, "/r/big.bin", part_size=4, concurrency=1)
        self.assertIn("Failed to upload file", str(cm.exception))
        self.assertIn("abort", fake.kinds())
        self.assertIsNone(fake.session)

    def test_abort_failure_does_not_mask_the_original(self):
        fake = _UploadFakeExecutor(
            fail_parts={
                (0, 4): SandboxRequestError(
                    400, json.dumps({"error": "sha256 mismatch on part"})
                )
            },
            abort_error=True,
        )
        with tempfile.TemporaryDirectory() as d:
            local = _local_file(d, "big.bin", self.DATA)
            with _fs(fake) as fs:
                with self.assertRaises(SandboxFilesystemError) as cm:
                    fs.upload_file(local, "/r/big.bin", part_size=4, concurrency=1)
        self.assertIn("sha256 mismatch on part", str(cm.exception))
        self.assertIn("abort", fake.kinds())

    def test_lost_session_names_the_restart(self):
        fake = _UploadFakeExecutor(
            fail_parts={
                (0, 4): SandboxRequestError(
                    404, json.dumps({"error": "unknown upload session"})
                )
            }
        )
        with tempfile.TemporaryDirectory() as d:
            local = _local_file(d, "big.bin", self.DATA)
            with _fs(fake) as fs:
                with self.assertRaises(SandboxFilesystemError) as cm:
                    fs.upload_file(local, "/r/big.bin", part_size=4, concurrency=1)
        self.assertIn("session was lost", str(cm.exception))
        self.assertIn("abort", fake.kinds())


class TestUpload409Resume(unittest.TestCase):
    """complete's 409 body carries the missing spans — fill and complete again."""

    DATA = b"abcdefghijkl"

    def test_missing_ranges_from_409_are_filled(self):
        fake = _UploadFakeExecutor(forget_parts={4})
        with tempfile.TemporaryDirectory() as d:
            local = _local_file(d, "big.bin", self.DATA)
            with _fs(fake) as fs:
                fs.upload_file(local, "/r/big.bin", part_size=4, concurrency=1)
        self.assertEqual(fake.kinds().count("complete"), 2)
        self.assertEqual(len(fake.part_puts()), 4)  # 3 parts + the one fill
        self.assertEqual(fake.part_puts()[-1], (4, 4))
        self.assertEqual(fake.landed(), self.DATA)

    def test_two_missing_ranges_are_both_filled(self):
        fake = _UploadFakeExecutor(forget_parts={4, 8})
        with tempfile.TemporaryDirectory() as d:
            local = _local_file(d, "big.bin", self.DATA)
            with _fs(fake) as fs:
                fs.upload_file(local, "/r/big.bin", part_size=4, concurrency=1)
        self.assertEqual(fake.kinds().count("complete"), 2)
        self.assertEqual(len(fake.part_puts()), 5)
        self.assertEqual(fake.landed(), self.DATA)

    def test_no_progress_raises_instead_of_looping(self):
        fake = _UploadFakeExecutor(never_record={4})
        with tempfile.TemporaryDirectory() as d:
            local = _local_file(d, "big.bin", self.DATA)
            with _fs(fake) as fs:
                with self.assertRaises(SandboxFilesystemError) as cm:
                    fs.upload_file(local, "/r/big.bin", part_size=4, concurrency=1)
        self.assertIn("no progress", str(cm.exception))
        self.assertEqual(fake.kinds().count("complete"), 2)
        self.assertIn("abort", fake.kinds())

    def test_unparseable_409_raises(self):
        fake = _UploadFakeExecutor(never_record={4}, raw_409_body="not json")
        with tempfile.TemporaryDirectory() as d:
            local = _local_file(d, "big.bin", self.DATA)
            with _fs(fake) as fs:
                with self.assertRaises(SandboxFilesystemError) as cm:
                    fs.upload_file(local, "/r/big.bin", part_size=4, concurrency=1)
        self.assertIn("missing-ranges reply was unusable", str(cm.exception))
        self.assertNotIsInstance(cm.exception, SandboxFileExistsError)


class TestUploadProgress(unittest.TestCase):
    DATA = b"abcdefghijkl"

    def test_progress_never_passes_the_file_size_across_a_fill(self):
        # A 409-fill re-sends bytes the counter already counted; the
        # callback contract caps done at the file size.
        seen = []
        fake = _UploadFakeExecutor(forget_parts={4})
        with tempfile.TemporaryDirectory() as d:
            local = _local_file(d, "big.bin", self.DATA)
            with _fs(fake) as fs:
                fs.upload_file(
                    local,
                    "/r/big.bin",
                    part_size=4,
                    concurrency=1,
                    progress=lambda done, total: seen.append((done, total)),
                )
        self.assertTrue(seen)
        self.assertEqual(seen[-1], (12, 12))
        self.assertTrue(all(done <= total for done, total in seen))

    def test_progress_reaches_the_full_size(self):
        seen = []
        fake = _UploadFakeExecutor()
        with tempfile.TemporaryDirectory() as d:
            local = _local_file(d, "big.bin", self.DATA)
            with _fs(fake) as fs:
                fs.upload_file(
                    local,
                    "/r/big.bin",
                    part_size=4,
                    concurrency=1,
                    progress=lambda done, total: seen.append((done, total)),
                )
        self.assertTrue(seen)
        self.assertEqual(seen[-1], (12, 12))
        dones = [d for d, _ in seen]
        self.assertEqual(dones, sorted(dones))


class TestUploadTimeoutWiring(unittest.TestCase):
    """The per-call timeout override reaches every call of the transfer."""

    DATA = b"abcdefghijkl"

    def test_multipart_calls_carry_the_override(self):
        fake = _UploadFakeExecutor()
        with tempfile.TemporaryDirectory() as d:
            local = _local_file(d, "big.bin", self.DATA)
            with _fs(fake) as fs:
                fs.upload_file(local, "/r/big.bin", part_size=4, timeout=90)
        for call in fake.calls:
            if call[0] in ("open", "part", "complete"):
                self.assertEqual(call[-1], 90, f"{call[0]} did not carry the override")

    def test_single_put_carries_the_override(self):
        fake = _UploadFakeExecutor()
        with tempfile.TemporaryDirectory() as d:
            local = _local_file(d, "small.bin", b"abc")
            with _fs(fake) as fs:
                fs.upload_file(local, "/r/small.bin", timeout=90)
        self.assertEqual(fake.calls[0][0], "files_put")
        self.assertEqual(fake.calls[0][-1], 90)

    def test_download_carries_the_override(self):
        fake = _UploadFakeExecutor()
        with tempfile.TemporaryDirectory() as d:
            target = os.path.join(d, "out.bin")
            with _fs(fake) as fs:
                fs.download_file("/r", target, timeout=90)
            reads = [c for c in fake.calls if c[0] == "files_read"]
            self.assertEqual(reads[0][-1], 90)
            with open(target, "rb") as f:
                self.assertEqual(f.read(), b"remote-bytes")


class TestAsyncUploadMultipart(unittest.IsolatedAsyncioTestCase):
    """The async twin: same contract through asyncio tasks."""

    DATA = b"abcdefghijkl"

    async def test_small_file_takes_the_single_put(self):
        fake = _AsyncUploadFakeExecutor()
        with tempfile.TemporaryDirectory() as d:
            local = _local_file(d, "small.bin", b"abc")
            with _async_fs(fake) as fs:
                await fs.upload_file(local, "/r/small.bin")
        self.assertEqual(fake.kinds(), ["files_put"])

    async def test_size_past_part_size_opens_a_session(self):
        fake = _AsyncUploadFakeExecutor()
        with tempfile.TemporaryDirectory() as d:
            local = _local_file(d, "big.bin", self.DATA)
            with _async_fs(fake) as fs:
                await fs.upload_file(local, "/r/big.bin", part_size=4, concurrency=1)
        self.assertEqual(fake.kinds()[0], "open")
        self.assertEqual(fake.kinds()[-1], "complete")
        self.assertEqual(fake.part_puts(), [(0, 4), (4, 4), (8, 4)])
        self.assertEqual(fake.landed(), self.DATA)

    async def test_four_parts_in_flight(self):
        # The gate only opens once four parts are truly in flight; a
        # smaller pool times the wait out and the test fails.
        fake = _AsyncUploadFakeExecutor()
        gate = asyncio.Event()

        async def on_part():
            if fake.in_flight == 4:
                gate.set()
            else:
                try:
                    await asyncio.wait_for(gate.wait(), timeout=10)
                except asyncio.TimeoutError:
                    raise AssertionError("never reached 4 parts in flight")

        fake.on_part = on_part
        with tempfile.TemporaryDirectory() as d:
            local = _local_file(d, "big.bin", bytes(range(32)))
            with _async_fs(fake) as fs:
                await fs.upload_file(local, "/r/big.bin", part_size=4)
        self.assertEqual(fake.max_in_flight, 4)
        self.assertEqual(fake.landed(), bytes(range(32)))

    async def test_timed_out_part_is_split_into_halves(self):
        fake = _AsyncUploadFakeExecutor(
            fail_parts={(0, 8): SandboxTimeoutError("Request timed out after 60s")}
        )
        with tempfile.TemporaryDirectory() as d:
            local = _local_file(d, "big.bin", self.DATA)
            with _async_fs(fake) as fs:
                with patch("koyeb.sandbox.filesystem._MIN_SPLIT_SIZE", 2):
                    await fs.upload_file(
                        local, "/r/big.bin", part_size=8, concurrency=1
                    )
        self.assertEqual(sorted(fake.part_puts()), [(0, 4), (0, 8), (4, 4), (8, 4)])
        self.assertEqual(fake.landed(), self.DATA)

    async def test_lost_session_names_the_restart(self):
        fake = _AsyncUploadFakeExecutor(
            fail_parts={
                (0, 4): SandboxRequestError(
                    404, json.dumps({"error": "unknown upload session"})
                )
            }
        )
        with tempfile.TemporaryDirectory() as d:
            local = _local_file(d, "big.bin", self.DATA)
            with _async_fs(fake) as fs:
                with self.assertRaises(SandboxFilesystemError) as cm:
                    await fs.upload_file(
                        local, "/r/big.bin", part_size=4, concurrency=1
                    )
        self.assertIn("session was lost", str(cm.exception))
        self.assertIn("abort", fake.kinds())

    async def test_complete_reply_without_sha256_still_succeeds(self):
        # The wire contract marks complete's sha256 optional: a 200 has
        # already matched the open-payload digest at the executor.
        fake = _AsyncUploadFakeExecutor(omit_complete_sha=True)
        with tempfile.TemporaryDirectory() as d:
            local = _local_file(d, "big.bin", self.DATA)
            with _async_fs(fake) as fs:
                await fs.upload_file(local, "/r/big.bin", part_size=4, concurrency=1)
        self.assertEqual(fake.landed(), self.DATA)
        self.assertNotIn("abort", fake.kinds())

    async def test_open_reply_without_max_part_size_aborts_the_live_session(self):
        # A valid upload_id means the session exists at the executor;
        # failing on the cap must abort it, not strand its temp file.
        fake = _AsyncUploadFakeExecutor(open_reply={"upload_id": "u-1"})
        with tempfile.TemporaryDirectory() as d:
            local = _local_file(d, "big.bin", self.DATA)
            with _async_fs(fake) as fs:
                with self.assertRaises(SandboxFilesystemError) as cm:
                    await fs.upload_file(
                        local, "/r/big.bin", part_size=4, concurrency=1
                    )
        self.assertIn("max_part_size", str(cm.exception))
        self.assertEqual(fake.kinds().count("abort"), 1)
        self.assertNotIn("part", fake.kinds())

    async def test_the_event_loop_stays_responsive_during_the_digest(self):
        # The whole-file hash is disk-and-CPU bound; running it inline
        # would freeze every other task on the loop for its duration.
        ticks = []

        async def ticker():
            while True:
                ticks.append(1)
                await asyncio.sleep(0.005)

        def slow_digest(path):
            time.sleep(0.25)
            with open(path, "rb") as f:
                return hashlib.sha256(f.read()).hexdigest()

        task = asyncio.get_running_loop().create_task(ticker())
        try:
            with patch("koyeb.sandbox.filesystem._file_sha256", slow_digest):
                with tempfile.TemporaryDirectory() as d:
                    local = _local_file(d, "small.bin", b"abc")
                    with _async_fs(_AsyncUploadFakeExecutor()) as fs:
                        await fs.upload_file(local, "/r/small.bin")
        finally:
            task.cancel()
        self.assertGreaterEqual(len(ticks), 20)

    async def test_the_event_loop_stays_responsive_during_multipart_digest(self):
        ticks = []

        async def ticker():
            while True:
                ticks.append(1)
                await asyncio.sleep(0.005)

        def slow_digest(path):
            time.sleep(0.25)
            with open(path, "rb") as f:
                return hashlib.sha256(f.read()).hexdigest()

        task = asyncio.get_running_loop().create_task(ticker())
        try:
            with patch("koyeb.sandbox.filesystem._file_sha256", slow_digest):
                with tempfile.TemporaryDirectory() as d:
                    local = _local_file(d, "big.bin", self.DATA)
                    with _async_fs(_AsyncUploadFakeExecutor()) as fs:
                        await fs.upload_file(
                            local, "/r/big.bin", part_size=4, concurrency=1
                        )
        finally:
            task.cancel()
        self.assertGreaterEqual(len(ticks), 20)

    async def test_malformed_open_reply_raises_without_aborting(self):
        fake = _AsyncUploadFakeExecutor(open_reply={"max_part_size": 4})
        with tempfile.TemporaryDirectory() as d:
            local = _local_file(d, "big.bin", self.DATA)
            with _async_fs(fake) as fs:
                with self.assertRaises(SandboxFilesystemError) as cm:
                    await fs.upload_file(local, "/r/big.bin", part_size=4)
        self.assertIn("upload_id", str(cm.exception))
        self.assertNotIn("abort", fake.kinds())

    async def test_no_progress_raises_instead_of_looping(self):
        fake = _AsyncUploadFakeExecutor(never_record={4})
        with tempfile.TemporaryDirectory() as d:
            local = _local_file(d, "big.bin", self.DATA)
            with _async_fs(fake) as fs:
                with self.assertRaises(SandboxFilesystemError) as cm:
                    await fs.upload_file(
                        local, "/r/big.bin", part_size=4, concurrency=1
                    )
        self.assertIn("no progress", str(cm.exception))
        self.assertEqual(fake.kinds().count("complete"), 2)
        self.assertIn("abort", fake.kinds())

    async def test_hard_part_failure_aborts_and_raises(self):
        fake = _AsyncUploadFakeExecutor(
            fail_parts={
                (0, 4): SandboxRequestError(
                    400, json.dumps({"error": "sha256 mismatch on part"})
                )
            }
        )
        with tempfile.TemporaryDirectory() as d:
            local = _local_file(d, "big.bin", self.DATA)
            with _async_fs(fake) as fs:
                with self.assertRaises(SandboxFilesystemError):
                    await fs.upload_file(
                        local, "/r/big.bin", part_size=4, concurrency=1
                    )
        self.assertIn("abort", fake.kinds())

    async def test_missing_ranges_from_409_are_filled(self):
        fake = _AsyncUploadFakeExecutor(forget_parts={4})
        with tempfile.TemporaryDirectory() as d:
            local = _local_file(d, "big.bin", self.DATA)
            with _async_fs(fake) as fs:
                await fs.upload_file(local, "/r/big.bin", part_size=4, concurrency=1)
        self.assertEqual(fake.kinds().count("complete"), 2)
        self.assertEqual(len(fake.part_puts()), 4)
        self.assertEqual(fake.landed(), self.DATA)

    async def test_progress_reaches_the_full_size(self):
        seen = []
        fake = _AsyncUploadFakeExecutor()
        with tempfile.TemporaryDirectory() as d:
            local = _local_file(d, "big.bin", self.DATA)
            with _async_fs(fake) as fs:
                await fs.upload_file(
                    local,
                    "/r/big.bin",
                    part_size=4,
                    concurrency=1,
                    progress=lambda done, total: seen.append((done, total)),
                )
        self.assertTrue(seen)
        self.assertEqual(seen[-1], (12, 12))

    async def test_multipart_calls_carry_the_timeout_override(self):
        fake = _AsyncUploadFakeExecutor()
        with tempfile.TemporaryDirectory() as d:
            local = _local_file(d, "big.bin", self.DATA)
            with _async_fs(fake) as fs:
                await fs.upload_file(local, "/r/big.bin", part_size=4, timeout=90)
        for call in fake.calls:
            if call[0] in ("open", "part", "complete"):
                self.assertEqual(call[-1], 90, f"{call[0]} did not carry the override")

    async def test_download_carries_the_timeout_override(self):
        fake = _AsyncUploadFakeExecutor()
        with tempfile.TemporaryDirectory() as d:
            target = os.path.join(d, "out.bin")
            with _async_fs(fake) as fs:
                await fs.download_file("/r", target, timeout=90)
        reads = [c for c in fake.calls if c[0] == "files_read"]
        self.assertEqual(reads[0][-1], 90)


class TestMainGuardIsLast(unittest.TestCase):
    """The direct-run entry point must sit after every test class.

    Appending classes at EOF after the guard is a recurring mistake;
    this pins the convention structurally.
    """

    def test_no_class_follows_the_guard(self):
        src = open(__file__).read()
        # The column-0 guard at the end of the file — not this test's own
        # string literal, which is indented and preceded by src.rindex(.
        guard_at = src.rindex('\nif __name__ == "__main__":')
        after = src[guard_at:]
        self.assertNotIn(
            "\nclass ",
            after,
            "a test class sits after the __main__ guard and is silently "
            "skipped on a direct run",
        )


class TestNewRoutesErrorArms(unittest.TestCase):
    """The translating seam's every arm: wrap, pass-through, cleanup, transport detail."""

    def test_generic_failure_wraps(self):
        client = _FakeSyncClient(has_files_routes=True)

        def blow(*args, **kwargs):
            raise RuntimeError("boom")

        client.files_put = blow
        with _fs(client) as fs:
            with self.assertRaises(SandboxFilesystemError) as cm:
                fs.write_file("/a", b"x")
        self.assertEqual(str(cm.exception), "Failed to write file: boom")

    def test_filesystem_errors_pass_through_unwrapped(self):
        client = _FakeSyncClient(has_files_routes=True)
        original = SandboxFilesystemError("inner")

        def blow(*args, **kwargs):
            raise original

        client.files_put = blow
        with _fs(client) as fs:
            with self.assertRaises(SandboxFilesystemError) as cm:
                fs.write_file("/a", b"x")
        self.assertIs(cm.exception, original)

    def test_download_mid_transfer_failure_cleans_part(self):
        client = _FakeSyncClient(
            has_files_routes=True, files_stat={"type": "file", "size": 4}
        )

        def blow(path, chunk_size=65536, timeout=None):
            raise RuntimeError("wire cut")
            yield b""

        client.files_read = blow
        with tempfile.TemporaryDirectory() as d:
            target = os.path.join(d, "out.bin")
            with _fs(client) as fs:
                with self.assertRaises(SandboxFilesystemError) as cm:
                    fs.download_file("/r", target)
            self.assertIn("wire cut", str(cm.exception))
            self.assertFalse(os.path.exists(target + ".part"))

    def test_bytes_base64_content_decodes(self):
        client = _FakeSyncClient(has_files_routes=True)
        with _fs(client) as fs:
            fs.write_file("/a", base64.b64encode(b"\x00\x01"), encoding="base64")
        call = [c for c in client.calls if c[0] == "files_put"][-1]
        self.assertEqual(call[2], b"\x00\x01")

    def test_non_json_error_body_carries_text(self):
        client = _FakeSyncClient(
            has_files_routes=True,
            files_put=SandboxRequestError(status_code=400, body="plain failure"),
        )
        with _fs(client) as fs:
            with self.assertRaises(SandboxFilesystemError) as cm:
                fs.write_file("/a", b"x")
        self.assertEqual(str(cm.exception), "Failed to write file: plain failure")

    def test_legacy_write_generic_wraps(self):
        client = _FakeSyncClient()

        def blow(path, content):
            raise RuntimeError("boom")

        client.write_file = blow
        with _fs(client) as fs:
            with self.assertRaises(SandboxFilesystemError) as cm:
                fs.write_file("/a", "x")
        self.assertEqual(str(cm.exception), "Failed to write file: boom")


class TestAsyncNewRoutesErrorArms(unittest.IsolatedAsyncioTestCase):
    async def test_generic_failure_wraps_write(self):
        client = _FakeAsyncClient(has_files_routes=True)

        async def blow(*args, **kwargs):
            raise RuntimeError("boom")

        client.files_put = blow
        with _async_fs(client) as fs:
            with self.assertRaises(SandboxFilesystemError) as cm:
                await fs.write_file("/a", b"x")
        self.assertEqual(str(cm.exception), "Failed to write file: boom")

    async def test_generic_failure_wraps_read(self):
        client = _FakeAsyncClient(has_files_routes=True)

        async def blow(path, chunk_size=65536):
            raise RuntimeError("boom")
            yield b""

        client.files_read = blow
        with _async_fs(client) as fs:
            with self.assertRaises(SandboxFilesystemError) as cm:
                await fs.read_file("/a")
        self.assertEqual(str(cm.exception), "Failed to read file: boom")

    async def test_generic_failure_wraps_stat(self):
        client = _FakeAsyncClient(has_files_routes=True)

        async def blow(path):
            raise RuntimeError("boom")

        client.files_stat = blow
        with _async_fs(client) as fs:
            with self.assertRaises(SandboxFilesystemError) as cm:
                await fs.stat("/a")
        self.assertEqual(str(cm.exception), "Failed to stat file: boom")

    async def test_upload_digest_mismatch_raises(self):
        fd, local = tempfile.mkstemp()
        with os.fdopen(fd, "wb") as f:
            f.write(b"abc")
        client = _FakeAsyncClient(
            has_files_routes=True,
            files_put={"size": 3, "sha256": "deadbeef"},
        )
        try:
            with _async_fs(client) as fs:
                with self.assertRaises(SandboxFilesystemError) as cm:
                    await fs.upload_file(local, "/r.bin")
        finally:
            os.unlink(local)
        self.assertIn("corrupt", str(cm.exception))

    async def test_download_mid_transfer_failure_cleans_part(self):
        client = _FakeAsyncClient(
            has_files_routes=True, files_stat={"type": "file", "size": 4}
        )

        async def blow(path, chunk_size=65536, timeout=None):
            raise RuntimeError("wire cut")
            yield b""

        client.files_read = blow
        with tempfile.TemporaryDirectory() as d:
            target = os.path.join(d, "out.bin")
            with _async_fs(client) as fs:
                with self.assertRaises(SandboxFilesystemError) as cm:
                    await fs.download_file("/r", target)
            self.assertIn("wire cut", str(cm.exception))
            self.assertFalse(os.path.exists(target + ".part"))


if __name__ == "__main__":
    unittest.main()
