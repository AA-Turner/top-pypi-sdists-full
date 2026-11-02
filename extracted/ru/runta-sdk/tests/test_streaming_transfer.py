from __future__ import annotations

import asyncio
import io
import json
import socket
import tarfile
import tempfile
import unittest
from base64 import b64encode
from pathlib import Path
from unittest.mock import patch

from websockets.exceptions import WebSocketException

from runta import ApiError, CommandError
from runta._internal.streaming_transfer import (
    _extract_and_commit,
    _retry_async,
    _retry_sync,
    _remote_parent_and_name,
    _stream_url,
    async_download_path,
    async_upload_path,
    async_execute,
    download_path,
    execute,
    upload_path,
)


class StreamingTransferTests(unittest.TestCase):
    def test_download_interruption_restarts_archive_and_commits_once(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            original = root / "source.txt"
            original.write_text("complete")
            with io.BytesIO() as output:
                with tarfile.open(fileobj=output, mode="w") as tar:
                    tar.add(original, arcname="source.txt")
                archive = output.getvalue()
            first = _FakeSyncSocket([_data_frame("stdout", b"partial"), None])
            second = _FakeSyncSocket(
                [
                    _data_frame("stdout", archive),
                    json.dumps({"type": "exit", "code": 0}),
                    None,
                ]
            )
            target = root / "new" / "result.txt"
            sizes: list[int] = []
            real_commit = _extract_and_commit

            def commit(archive_path: Path, *args: object, **kwargs: object) -> None:
                sizes.append(archive_path.stat().st_size)
                self.assertFalse(target.exists())
                real_commit(archive_path, *args, **kwargs)

            with (
                patch(
                    "runta._internal.streaming_transfer._sync_socket",
                    side_effect=[
                        _FakeSyncSocketContext(first),
                        _FakeSyncSocketContext(second),
                    ],
                ),
                patch(
                    "runta._internal.streaming_transfer._extract_and_commit",
                    side_effect=commit,
                ),
                patch("runta._internal.retry.random.uniform", return_value=0),
            ):
                download_path(
                    "https://api.test",
                    "token",
                    "runtime",
                    "/remote/source.txt",
                    target,
                    destination_is_directory=False,
                    timeout=30,
                    attempts=2,
                )
            self.assertEqual(sizes, [len(archive)])
            self.assertEqual(target.read_text(), "complete")

    def test_failed_file_commit_cleans_temp_file_and_new_directories(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "source.txt"
            source.write_text("payload")
            archive = root / "payload.tar"
            with tarfile.open(archive, "w") as tar:
                tar.add(source, arcname="source.txt")
            target = root / "new" / "nested" / "result.txt"
            with patch(
                "runta._internal.streaming_transfer.shutil.copyfileobj",
                side_effect=OSError("copy failed"),
            ):
                with self.assertRaisesRegex(OSError, "copy failed"):
                    _extract_and_commit(
                        archive,
                        "/remote/source.txt",
                        target,
                        destination_is_directory=False,
                        workspace=root,
                    )
            self.assertFalse((root / "new").exists())
            self.assertEqual(list(root.rglob(".result.txt.runta-*")), [])

    def test_upload_interruption_restarts_file(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / "source.txt"
            source.write_bytes(b"payload")
            first = _FakeSyncSocket([])
            second = _FakeSyncSocket([json.dumps({"type": "exit", "code": 0}), None])
            original_send = first.send

            def interrupted_send(frame: str) -> None:
                original_send(frame)
                if json.loads(frame)["type"] == "stdin":
                    raise ConnectionResetError("lost")

            first.send = interrupted_send
            with (
                patch(
                    "runta._internal.streaming_transfer._sync_socket",
                    side_effect=[
                        _FakeSyncSocketContext(first),
                        _FakeSyncSocketContext(second),
                    ],
                ),
                patch("runta._internal.retry.random.uniform", return_value=0),
            ):
                upload_path(
                    "https://api.test",
                    "token",
                    "runtime",
                    source,
                    "/dst",
                    timeout=30,
                    attempts=2,
                )
            chunks = [
                json.loads(frame)["data_base64"]
                for frame in second.sent
                if json.loads(frame)["type"] == "stdin"
            ]
            self.assertEqual([b64encode(b"payload").decode("ascii")], chunks)

    def test_nontransient_errors_do_not_retry(self) -> None:
        calls = 0

        def fail() -> None:
            nonlocal calls
            calls += 1
            raise ApiError("invalid streaming transfer frame")

        with self.assertRaisesRegex(ApiError, "invalid"):
            _retry_sync(fail, attempts=16)
        self.assertEqual(calls, 1)

    def test_temporary_dns_failure_retries_but_permanent_failure_does_not(self) -> None:
        calls = 0

        def reconnect() -> None:
            nonlocal calls
            calls += 1
            if calls == 1:
                raise socket.gaierror(socket.EAI_AGAIN, "temporary DNS failure")

        with patch("runta._internal.retry.random.uniform", return_value=0):
            _retry_sync(reconnect, attempts=2)
        self.assertEqual(calls, 2)

        def permanent_failure() -> None:
            nonlocal calls
            calls += 1
            raise socket.gaierror(socket.EAI_NONAME, "name not found")

        with self.assertRaises(socket.gaierror):
            _retry_sync(permanent_failure, attempts=2)
        self.assertEqual(calls, 3)

    def test_stream_url_encodes_runtime_reference(self) -> None:
        self.assertEqual(
            _stream_url("https://api.example.test/base/", "runtime/name"),
            "wss://api.example.test/base/v2/runtimes/runtime%2Fname/exec/stream",
        )

    def test_remote_parent_and_name(self) -> None:
        self.assertEqual(
            _remote_parent_and_name("/workspace/tree/"), ("/workspace", "tree")
        )
        with self.assertRaisesRegex(ValueError, "root"):
            _remote_parent_and_name("/")

    def test_extract_and_commit_file_replaces_atomically(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            archive_path = root / "payload.tar"
            source = root / "source.txt"
            source.write_text("new value")
            with tarfile.open(archive_path, "w") as archive:
                archive.add(source, arcname="source.txt")
            target = root / "target.txt"
            target.write_text("old value")

            _extract_and_commit(
                archive_path,
                "/remote/source.txt",
                target,
                destination_is_directory=False,
                workspace=root,
            )

            self.assertEqual(target.read_text(), "new value")
            self.assertEqual(list(root.glob(".target.txt.runta-*")), [])

    def test_extract_and_commit_directory(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            archive_path = root / "payload.tar"
            source = root / "tree"
            (source / "nested").mkdir(parents=True)
            (source / "nested/data.txt").write_text("payload")
            with tarfile.open(archive_path, "w") as archive:
                archive.add(source, arcname="tree")
            target = root / "target"
            target.mkdir()
            (target / "old.txt").write_text("old")

            _extract_and_commit(
                archive_path,
                "/remote/tree",
                target,
                destination_is_directory=False,
                workspace=root,
            )

            self.assertEqual((target / "nested/data.txt").read_text(), "payload")
            self.assertFalse((target / "old.txt").exists())

    def test_extract_rejects_path_traversal(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            archive_path = root / "payload.tar"
            with tarfile.open(archive_path, "w") as archive:
                member = tarfile.TarInfo("../escape.txt")
                member.size = 4
                archive.addfile(member, io.BytesIO(b"nope"))

            with self.assertRaisesRegex(ApiError, "unsafe path"):
                _extract_and_commit(
                    archive_path,
                    "/remote/escape.txt",
                    root / "target.txt",
                    destination_is_directory=False,
                    workspace=root,
                )

    def test_extract_preserves_safe_relative_symlink(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            archive_path = root / "payload.tar"
            with tarfile.open(archive_path, "w") as archive:
                directory = tarfile.TarInfo("tree")
                directory.type = tarfile.DIRTYPE
                directory.mode = 0o755
                archive.addfile(directory)
                target = tarfile.TarInfo("tree/target.txt")
                target.size = 7
                archive.addfile(target, io.BytesIO(b"payload"))
                link = tarfile.TarInfo("tree/link.txt")
                link.type = tarfile.SYMTYPE
                link.linkname = "target.txt"
                archive.addfile(link)

            output = root / "output"
            _extract_and_commit(
                archive_path,
                "/remote/tree",
                output,
                destination_is_directory=False,
                workspace=root,
            )

            self.assertTrue((output / "link.txt").is_symlink())
            self.assertEqual((output / "link.txt").read_text(), "payload")


class AsyncExecuteTests(unittest.IsolatedAsyncioTestCase):
    async def test_execute_uses_stream_frames(self) -> None:
        socket = _FakeSocket(
            [
                json.dumps({"type": "heartbeat"}),
                _data_frame("stdout", b"hello"),
                _data_frame("stderr", b"error"),
                json.dumps({"type": "exit", "code": 7}),
            ]
        )

        with patch(
            "runta._internal.streaming_transfer._async_socket",
            return_value=_FakeSocketContext(socket),
        ):
            result = await async_execute(
                "https://api.example.test",
                "rt_test",
                "runtime-1",
                "sh",
                ["-lc", "command"],
                env={"A": "B"},
                stdin=b"input",
                timeout=10,
                max_output_bytes=3,
                connect_timeout=5,
            )

        self.assertEqual(result.exit_code, 7)
        self.assertEqual(result.stdout, b"hel")
        self.assertEqual(result.stderr, b"err")
        self.assertTrue(result.stdout_truncated)
        self.assertTrue(result.stderr_truncated)
        self.assertEqual(
            json.loads(socket.sent[0]),
            {
                "type": "start",
                "command": "sh",
                "args": ["-lc", "command"],
                "env": {"A": "B"},
                "tty": False,
            },
        )
        self.assertEqual(json.loads(socket.sent[1])["type"], "stdin")
        self.assertEqual(json.loads(socket.sent[2]), {"type": "close_stdin"})
        self.assertEqual(json.loads(socket.sent[3]), {"type": "heartbeat"})

    async def test_execute_timeout_sends_term(self) -> None:
        socket = _FakeSocket([])

        with patch(
            "runta._internal.streaming_transfer._async_socket",
            return_value=_FakeSocketContext(socket),
        ):
            result = await async_execute(
                "https://api.example.test",
                "rt_test",
                "runtime-1",
                "sleep",
                ["60"],
                env=None,
                stdin=None,
                timeout=0.01,
                max_output_bytes=None,
                connect_timeout=5,
            )

        self.assertEqual(result.exit_code, 124)
        self.assertTrue(socket.signal_attempted)


class SyncExecuteTests(unittest.TestCase):
    def test_execute_uses_stream_frames(self) -> None:
        socket = _FakeSyncSocket(
            [
                json.dumps({"type": "heartbeat"}),
                _data_frame("stdout", b"hello"),
                _data_frame("stderr", b"error"),
                json.dumps({"type": "exit", "code": 7}),
            ]
        )

        with patch(
            "runta._internal.streaming_transfer._sync_socket",
            return_value=_FakeSyncSocketContext(socket),
        ):
            result = execute(
                "https://api.example.test",
                "rt_test",
                "runtime-1",
                "sh",
                ["-lc", "command"],
                env={"A": "B"},
                stdin=b"input",
                timeout=10,
                max_output_bytes=3,
                connect_timeout=5,
            )

        self.assertEqual(result.exit_code, 7)
        self.assertEqual(result.stdout, b"hel")
        self.assertEqual(result.stderr, b"err")
        self.assertTrue(result.stdout_truncated)
        self.assertTrue(result.stderr_truncated)
        self.assertEqual(json.loads(socket.sent[0])["env"], {"A": "B"})
        self.assertEqual(json.loads(socket.sent[1])["type"], "stdin")
        self.assertEqual(json.loads(socket.sent[2]), {"type": "close_stdin"})
        self.assertEqual(json.loads(socket.sent[3]), {"type": "heartbeat"})

    def test_execute_timeout_sends_term(self) -> None:
        socket = _FakeSyncSocket([])

        with patch(
            "runta._internal.streaming_transfer._sync_socket",
            return_value=_FakeSyncSocketContext(socket),
        ):
            result = execute(
                "https://api.example.test",
                "rt_test",
                "runtime-1",
                "sleep",
                ["60"],
                env=None,
                stdin=None,
                timeout=0.01,
                max_output_bytes=None,
                connect_timeout=5,
            )

        self.assertEqual(result.exit_code, 124)
        self.assertEqual(
            json.loads(socket.sent[-1]), {"type": "signal", "signal": "TERM"}
        )


class AsyncExecuteFailureTests(unittest.IsolatedAsyncioTestCase):
    async def test_temporary_dns_failure_retries(self) -> None:
        calls = 0

        async def reconnect() -> None:
            nonlocal calls
            calls += 1
            if calls == 1:
                raise socket.gaierror(socket.EAI_AGAIN, "temporary DNS failure")

        with patch("runta._internal.retry.random.uniform", return_value=0):
            await _retry_async(reconnect, attempts=2)
        self.assertEqual(calls, 2)

    async def test_download_interruption_restarts_archive(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "source.txt"
            source.write_text("complete")
            with io.BytesIO() as output:
                with tarfile.open(fileobj=output, mode="w") as tar:
                    tar.add(source, arcname="source.txt")
                archive = output.getvalue()
            first = _FakeSocket([_data_frame("stdout", b"partial"), None])
            second = _FakeSocket(
                [
                    _data_frame("stdout", archive),
                    json.dumps({"type": "exit", "code": 0}),
                    None,
                ]
            )
            target = root / "new" / "result.txt"
            with (
                patch(
                    "runta._internal.streaming_transfer._async_socket",
                    side_effect=[_FakeSocketContext(first), _FakeSocketContext(second)],
                ),
                patch("runta._internal.retry.random.uniform", return_value=0),
            ):
                await async_download_path(
                    "https://api.test",
                    "token",
                    "runtime",
                    "/remote/source.txt",
                    target,
                    destination_is_directory=False,
                    timeout=30,
                    attempts=2,
                )
            self.assertEqual(target.read_text(), "complete")

    async def test_upload_interruption_restarts_file(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / "source.txt"
            source.write_bytes(b"payload")
            first = _FakeSocket([])
            second = _FakeSocket([json.dumps({"type": "exit", "code": 0}), None])
            original_send = first.send

            async def interrupted_send(frame: str) -> None:
                await original_send(frame)
                if json.loads(frame)["type"] == "stdin":
                    raise ConnectionResetError("lost")

            first.send = interrupted_send
            with (
                patch(
                    "runta._internal.streaming_transfer._async_socket",
                    side_effect=[_FakeSocketContext(first), _FakeSocketContext(second)],
                ),
                patch("runta._internal.retry.random.uniform", return_value=0),
            ):
                await async_upload_path(
                    "https://api.test",
                    "token",
                    "runtime",
                    source,
                    "/dst",
                    timeout=30,
                    attempts=2,
                )
            chunks = [
                json.loads(frame)["data_base64"]
                for frame in second.sent
                if json.loads(frame)["type"] == "stdin"
            ]
            self.assertEqual([b64encode(b"payload").decode("ascii")], chunks)

    async def test_command_failure_does_not_retry(self) -> None:
        calls = 0

        async def fail() -> None:
            nonlocal calls
            calls += 1
            raise CommandError("failed", exit_code=2)

        with self.assertRaises(CommandError):
            await _retry_async(fail, attempts=16)
        self.assertEqual(calls, 1)

    async def test_execute_timeout_survives_closed_socket_during_term(self) -> None:
        socket = _FakeSocket([], fail_signal=True)

        with patch(
            "runta._internal.streaming_transfer._async_socket",
            return_value=_FakeSocketContext(socket),
        ):
            result = await async_execute(
                "https://api.example.test",
                "rt_test",
                "runtime-1",
                "sleep",
                ["60"],
                env=None,
                stdin=None,
                timeout=0.01,
                max_output_bytes=None,
                connect_timeout=5,
            )

        self.assertEqual(result.exit_code, 124)

    async def test_execute_cancellation_survives_closed_socket_during_term(
        self,
    ) -> None:
        socket = _FakeSocket([], fail_signal=True)

        with patch(
            "runta._internal.streaming_transfer._async_socket",
            return_value=_FakeSocketContext(socket),
        ):
            task = asyncio.create_task(
                async_execute(
                    "https://api.example.test",
                    "rt_test",
                    "runtime-1",
                    "sleep",
                    ["60"],
                    env=None,
                    stdin=None,
                    timeout=None,
                    max_output_bytes=None,
                    connect_timeout=5,
                )
            )
            await asyncio.sleep(0)
            task.cancel()
            with self.assertRaises(asyncio.CancelledError):
                await task
        self.assertTrue(socket.signal_attempted)


class _FakeSocket:
    def __init__(self, frames: list[str], *, fail_signal: bool = False) -> None:
        self.frames = frames
        self.fail_signal = fail_signal
        self.signal_attempted = False
        self.sent: list[str] = []

    async def send(self, frame: str) -> None:
        if json.loads(frame).get("type") == "signal":
            self.signal_attempted = True
            if self.fail_signal:
                raise WebSocketException("socket already closed")
        self.sent.append(frame)

    async def recv(self) -> str:
        if self.frames:
            return self.frames.pop(0)
        await asyncio.Future()
        raise AssertionError


class _FakeSocketContext:
    def __init__(self, socket: _FakeSocket) -> None:
        self.socket = socket

    async def __aenter__(self) -> _FakeSocket:
        return self.socket

    async def __aexit__(self, *_exc: object) -> None:
        return None


class _FakeSyncSocket:
    def __init__(self, frames: list[str]) -> None:
        self.frames = frames
        self.sent: list[str] = []

    def send(self, frame: str) -> None:
        self.sent.append(frame)

    def recv(self, timeout: float | None = None) -> str:
        if self.frames:
            return self.frames.pop(0)
        if timeout is not None:
            raise TimeoutError
        raise AssertionError("no frame available")


class _FakeSyncSocketContext:
    def __init__(self, socket: _FakeSyncSocket) -> None:
        self.socket = socket

    def __enter__(self) -> _FakeSyncSocket:
        return self.socket

    def __exit__(self, *_exc: object) -> None:
        return None


def _data_frame(kind: str, data: bytes) -> str:
    return json.dumps({"type": kind, "data_base64": b64encode(data).decode("ascii")})
