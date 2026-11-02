from __future__ import annotations

import asyncio
import os
import sys
import tempfile
import time
import unittest
import uuid
import base64
import json
from collections.abc import Awaitable, Callable, Sequence
from dataclasses import replace
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any
from types import SimpleNamespace
from urllib.parse import urlparse
from unittest.mock import AsyncMock, patch

from websockets.datastructures import Headers
from websockets.exceptions import InvalidStatus
from websockets.http11 import Response

from runta import (
    ApiError,
    AsyncRunta,
    CommandResult,
    EgressMode,
    EgressPolicy,
    RuntimeInfo,
    RuntimeResourceLimits,
    RuntimeResourceRequests,
    RuntimeResources,
    RuntimeStatus,
)

from runta._internal.execution import AsyncExecution, ExecutionState


LIVE_ENABLED = os.getenv("RUNTA_PYTEST_LIVE") == "1" or "--live" in sys.argv
if "--live" in sys.argv:
    sys.argv.remove("--live")

LIVE_SKIP_REASON = (
    "pass --live with RUNTA_ENDPOINT and RUNTA_TOKEN to run real runtime tests"
)


def _live_ready() -> bool:
    return (
        LIVE_ENABLED
        and bool(os.getenv("RUNTA_ENDPOINT"))
        and bool(os.getenv("RUNTA_TOKEN"))
    )


class MockRuntimeTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.client = AsyncRunta(endpoint="http://mock-runta-api", token="rt_mock")
        self.fake_http = FakeHttp()
        await self.client._http.close()
        self.client._http = self.fake_http
        self.fake_http.retry_max_attempts = 2

    async def asyncTearDown(self) -> None:
        await self.client.close()

    async def test_mock_runtime_lifecycle(self) -> None:
        runtime = await self.client.runtimes.create(
            "mock-lifecycle",
            vcpus=1,
            memory_mib=1024,
        )
        self.assertEqual(await runtime.status(), RuntimeStatus.RUNNING)

        self.assertIsNone(await runtime.boot())
        self.assertEqual(runtime.cached_info.status, RuntimeStatus.RUNNING)
        self.assertEqual(await runtime.status(), RuntimeStatus.RUNNING)

        self.assertIsNone(await runtime.pause())
        self.assertEqual(runtime.cached_info.status, RuntimeStatus.PAUSED)
        self.assertEqual(await runtime.status(), RuntimeStatus.PAUSED)

        self.assertIsNone(await runtime.resume())
        self.assertEqual(runtime.cached_info.status, RuntimeStatus.RUNNING)
        self.assertEqual(await runtime.status(), RuntimeStatus.RUNNING)

        self.assertIsNone(await runtime.shutdown())
        self.assertEqual(runtime.cached_info.status, RuntimeStatus.SHUTDOWN)
        self.assertEqual(await runtime.status(), RuntimeStatus.SHUTDOWN)

        await runtime.delete()
        with self.assertRaises(ApiError):
            await self.client.runtimes.get(runtime.id)

    async def test_mock_exec_retries_transient_route_miss(self) -> None:
        runtime = await self.client.runtimes.create("mock-transient-exec")
        await runtime.boot()
        route_miss = InvalidStatus(Response(404, "Not Found", Headers()))
        with (
            patch.object(
                AsyncExecution,
                "_observe",
                AsyncMock(side_effect=[route_miss, ExecutionState("completed", 0)]),
            ) as observe,
            patch.object(
                AsyncExecution, "_output", AsyncMock(return_value=(b"hello", b""))
            ),
            patch.object(AsyncExecution, "cleanup", AsyncMock()),
            patch("runta._internal.execution._delay", return_value=0),
        ):
            result = await runtime.exec("echo hello")

        self.assertEqual(result.exit_code, 0)
        self.assertEqual(observe.await_count, 2)

    async def test_mock_egress_allowlist_and_deny(self) -> None:
        runtime = await self.client.runtimes.create("mock-egress")
        await runtime.boot()

        # This fixture models policy responses, not a guest task filesystem.
        # Exercise the policy via its existing fake command implementation.
        async def fake_exec(_runtime, command, **kwargs):
            return await self.fake_http.execute(
                runtime.id, "sh", ["-c", command], **kwargs
            )

        patcher = patch.object(type(runtime), "exec", fake_exec)
        patcher.start()
        self.addCleanup(patcher.stop)

        await runtime.egress.set_policy(EgressPolicy(mode=EgressMode.ALLOWLIST))
        denied_status = await _curl_http_status(runtime, "http://example.com")
        self.assertEqual(denied_status, "403")

        with self.assertRaisesRegex(ApiError, "invalid egress host"):
            await runtime.egress.set_policy(
                EgressPolicy(
                    mode=EgressMode.ALLOWLIST,
                    allowed_hosts=["https://example.com"],
                )
            )

        await runtime.egress.set_policy(
            EgressPolicy(
                mode=EgressMode.ALLOWLIST,
                allowed_hosts=["example.com"],
            )
        )
        self.assertEqual((await runtime.egress.get()).allowed_hosts, ["example.com"])
        allowed_status = await _curl_http_status(runtime, "http://example.com")
        self.assertEqual(allowed_status, "200")
        await runtime.egress.set_policy(EgressPolicy(mode=EgressMode.ALLOWLIST))
        self.assertEqual((await runtime.egress.get()).allowed_hosts, [])

    async def test_mock_file_read_write_upload_download(self) -> None:
        runtime = await self.client.runtimes.create("mock-files")

        await runtime.files.write("/workspace/output.txt", "hello")
        self.assertEqual(await runtime.files.read("/workspace/output.txt"), b"hello")
        self.assertEqual(
            await runtime.files.read("/workspace/output.txt", max_bytes=2), b"he"
        )

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            local_src = tmp_path / "input.bin"
            local_src.write_bytes(b"\x00runta\xff")

            await runtime.files.upload(str(local_src), "/workspace/uploaded.bin")
            self.assertEqual(
                await runtime.files.read("/workspace/uploaded.bin"),
                b"\x00runta\xff",
            )

            local_dst = tmp_path / "downloads"
            await runtime.files.download(
                "/workspace/uploaded.bin", str(local_dst) + "/"
            )
            self.assertEqual(
                (local_dst / "uploaded.bin").read_bytes(), b"\x00runta\xff"
            )


@unittest.skipUnless(_live_ready(), LIVE_SKIP_REASON)
class LiveRuntimeTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.client = AsyncRunta(timeout=60)
        self.created_runtimes = []
        self.created_checkpoints: list[str] = []
        self.created_secrets: list[str] = []
        await self._assert_rest_runtime_api_ready()

    async def asyncTearDown(self) -> None:
        for runtime in reversed(self.created_runtimes):
            try:
                await runtime.delete()
            except Exception:
                pass

        for checkpoint_id in reversed(self.created_checkpoints):
            try:
                await self.client.checkpoints.delete(checkpoint_id)
            except Exception:
                pass

        for secret_name in reversed(self.created_secrets):
            try:
                await self.client.secrets.delete(secret_name)
            except Exception:
                pass

        await self.client.close()

    async def test_exec_reconnects_without_repeating_command(self) -> None:
        from runta._internal import execution as task_transport

        runtime = await self._create_runtime("exec-reconnect")
        marker = f"/tmp/sdk-exec-once-{uuid.uuid4().hex}"
        factory = task_transport._async_socket
        dropped = False

        @asynccontextmanager
        async def disconnect_once(*args, **kwargs):
            async with factory(*args, **kwargs) as socket:

                async def recv():
                    nonlocal dropped
                    raw = await socket.recv()
                    frame = json.loads(raw)
                    if frame.get("type") == "stdout":
                        data = base64.b64decode(frame["data_base64"])
                        if not dropped and b"RUNTA_EXEC_V1 running" in data:
                            dropped = True
                            await socket.close()
                            raise ConnectionError("injected observer disconnect")
                    return raw

                yield SimpleNamespace(send=socket.send, recv=recv)

        with patch.object(task_transport, "_async_socket", disconnect_once):
            result = await runtime.exec(
                f"printf x >> {marker}; sleep 35; cat; printf done",
                stdin=b"\0\xff",
                timeout=60,
            )
        self.assertTrue(dropped)
        self.assertEqual(result.exit_code, 0, result.stderr_text)
        self.assertEqual(result.stdout, b"\0\xffdone")
        self.assertEqual(await runtime.files.read(marker), b"x")
        timed_out = await runtime.exec("sleep 30", timeout=0.5)
        self.assertEqual(timed_out.exit_code, 124)

    async def test_runtime_lifecycle(self) -> None:
        runtime = await self._create_runtime("lifecycle")

        if runtime.cached_info.status != RuntimeStatus.RUNNING:
            await runtime.boot()
        await _wait_for_status(
            self, runtime, {RuntimeStatus.RUNNING}, timeout=240, verbose=True
        )

        await runtime.pause()
        await _wait_for_status(
            self, runtime, {RuntimeStatus.PAUSED}, timeout=180, verbose=True
        )

        await runtime.resume()
        await _wait_for_status(
            self, runtime, {RuntimeStatus.RUNNING}, timeout=240, verbose=True
        )

        await runtime.shutdown()
        await _wait_for_status(
            self, runtime, {RuntimeStatus.SHUTDOWN}, timeout=180, verbose=True
        )

        await runtime.boot()
        await _wait_for_status(
            self, runtime, {RuntimeStatus.RUNNING}, timeout=240, verbose=True
        )

        await runtime.delete()
        self.created_runtimes.remove(runtime)
        await self._wait_for_deleted(runtime.id, timeout=120)

    async def test_egress_allowlist_and_deny(self) -> None:
        runtime = await self._create_runtime("egress")
        await self._ensure_running(runtime)

        await runtime.egress.set_policy(EgressPolicy(mode=EgressMode.ALLOWLIST))
        denied_status = await _eventually(
            self,
            lambda: _curl_http_status(runtime, "http://example.com"),
            lambda status: status == "403",
            timeout=90,
            detail="example.com should be denied before it is allowlisted",
            label="egress deny example.com",
            verbose=True,
        )
        self.assertEqual(denied_status, "403")

        await runtime.egress.set_policy(
            EgressPolicy(
                mode=EgressMode.ALLOWLIST,
                allowed_hosts=["example.com"],
            )
        )
        allowlist = (await runtime.egress.get()).allowed_hosts
        self.assertIn("example.com", allowlist)

        allowed_status = await _eventually(
            self,
            lambda: _curl_http_status(runtime, "http://example.com"),
            lambda status: status == "200",
            timeout=90,
            detail="example.com should be allowed after it is allowlisted",
            label="egress allow example.com",
            verbose=True,
        )
        self.assertEqual(allowed_status, "200")

    async def test_file_read_write_upload_download(self) -> None:
        runtime = await self._create_runtime("files")
        await self._ensure_running(runtime)

        remote_written = f"/tmp/runta-sdk-written-{uuid.uuid4().hex}.txt"
        await runtime.files.write(remote_written, b"hello from live files")
        self.assertEqual(
            await runtime.files.read(remote_written), b"hello from live files"
        )
        self.assertEqual(
            await runtime.files.read(remote_written, max_bytes=5), b"hello"
        )

        cat_result = await runtime.exec(["cat", remote_written], timeout=30)
        self.assertEqual(cat_result.exit_code, 0)
        self.assertEqual(cat_result.stdout, b"hello from live files")

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            local_src = tmp_path / "upload.bin"
            payload = os.urandom(2 * 1024 * 1024 + 73)
            local_src.write_bytes(payload)

            remote_uploaded = f"/tmp/runta-sdk-uploaded-{uuid.uuid4().hex}.bin"
            await runtime.files.upload(str(local_src), remote_uploaded)

            local_dst = tmp_path / "downloaded.bin"
            await runtime.files.download(remote_uploaded, str(local_dst))
            self.assertEqual(local_dst.read_bytes(), payload)

            local_tree = tmp_path / "tree"
            (local_tree / "nested").mkdir(parents=True)
            (local_tree / "nested" / "result.txt").write_text(
                "directory-stream-ok", encoding="utf-8"
            )
            remote_tree = f"/tmp/runta-sdk-tree-{uuid.uuid4().hex}"
            await runtime.files.upload(str(local_tree), remote_tree)
            downloaded_tree = tmp_path / "downloaded-tree"
            await runtime.files.download(remote_tree, str(downloaded_tree))
            self.assertEqual(
                (downloaded_tree / "nested" / "result.txt").read_text(encoding="utf-8"),
                "directory-stream-ok",
            )

    async def test_stored_secret_crud(self) -> None:
        name = f"sdk-live-secret-{uuid.uuid4().hex}"
        self.created_secrets.append(name)

        created = await self.client.secrets.set(name, "live-secret-value")
        self.assertEqual(created.display_name, name)
        self.assertEqual((await self.client.secrets.get(name)).id, created.id)
        self.assertIn(
            created.id, {item.id for item in await self.client.secrets.list()}
        )

        await self.client.secrets.delete(name)
        self.created_secrets.remove(name)

    async def test_checkpoint_restore_and_exec_options(self) -> None:
        runtime = await self._create_runtime("checkpoint")
        await self._ensure_running(runtime)
        marker = f"checkpoint-{uuid.uuid4().hex}"
        remote_path = f"/tmp/{marker}.txt"

        result = await runtime.exec(
            [
                "sh",
                "-c",
                'printf "%s:%s:%s" "$LIVE_ENV" "$PWD" "$(cat)" > "$1"',
                "sh",
                remote_path,
            ],
            env={"LIVE_ENV": marker},
            stdin="stdin-ok",
            cwd="/tmp",
            timeout=30,
        )
        self.assertEqual(result.exit_code, 0, result.stderr_text)

        checkpoint = await runtime.checkpoints.create(
            name=f"{runtime.name}-restore",
            timeout=600,
            poll_interval=2,
        )
        self.created_checkpoints.append(checkpoint.id)
        self.assertIn(
            checkpoint.id, {item.id for item in await self.client.checkpoints.list()}
        )

        restored = await self.client.runtimes.create(
            f"sdk-live-restored-{int(time.time())}", checkpoint_id=checkpoint.id
        )
        self.created_runtimes.append(restored)
        await self._ensure_running(restored)
        restored_result = await restored.exec(["cat", remote_path], timeout=30)
        self.assertEqual(restored_result.exit_code, 0, restored_result.stderr_text)
        self.assertEqual(restored_result.stdout_text, f"{marker}:/tmp:stdin-ok")

    async def _create_runtime(self, suffix: str):
        name = f"sdk-live-{suffix}-{int(time.time())}"
        runtime = await self.client.runtimes.create(
            name,
            vcpus=1,
            memory_mib=1024,
        )
        self.created_runtimes.append(runtime)
        return runtime

    async def _assert_rest_runtime_api_ready(self) -> None:
        endpoint = self.client._http.endpoint
        parsed = urlparse(endpoint)
        if parsed.port == 50072:
            self.fail(
                "RUNTA_ENDPOINT points at the runta-control gRPC listener "
                f"({endpoint}); live Python SDK tests must use the runta-api "
                "REST listener, for example http://127.0.0.1:8080"
            )
        try:
            await self.client.runtimes.list()
        except ApiError as exc:
            if exc.status_code == 404:
                self.fail(
                    "RUNTA_ENDPOINT does not expose the runtime REST API "
                    f"({endpoint} returned 404 for /v2/runtimes). Rebuild and "
                    "restart runta-api from this branch, then use its REST "
                    "listener, for example http://127.0.0.1:8080"
                )
            raise

    async def _ensure_running(self, runtime) -> None:
        if runtime.cached_info.status != RuntimeStatus.RUNNING:
            await runtime.boot()
        await _wait_for_status(
            self, runtime, {RuntimeStatus.RUNNING}, timeout=240, verbose=True
        )

    async def _wait_for_deleted(self, runtime_id: str, *, timeout: float) -> None:
        deadline = time.monotonic() + timeout
        last_error = None
        attempt = 0
        while time.monotonic() < deadline:
            attempt += 1
            try:
                await self.client.runtimes.get(runtime_id)
                print(
                    f"[live] runtime {runtime_id} deleted: poll {attempt}: still present",
                    flush=True,
                )
            except ApiError:
                print(f"[live] runtime {runtime_id} deleted: success", flush=True)
                return
            except Exception as exc:
                last_error = exc
                print(
                    f"[live] runtime {runtime_id} deleted: poll {attempt}: error={exc!r}",
                    flush=True,
                )
            await asyncio.sleep(2)
        self.fail(
            f"runtime {runtime_id} was not deleted within {timeout}s; last_error={last_error!r}"
        )


class FakeHttp:
    def __init__(self) -> None:
        self.runtimes: dict[str, RuntimeInfo] = {}
        self.files: dict[tuple[str, str], bytes] = {}

    async def close(self) -> None:
        return None

    async def create_runtime(
        self,
        name: str | None = None,
        *,
        vcpus: int = 1,
        memory_mib: int = 1024,
        **_ignored: Any,
    ) -> RuntimeInfo:
        info = RuntimeInfo(
            id=str(uuid.uuid4()),
            display_name=name or f"mock-{uuid.uuid4().hex[:8]}",
            resources=RuntimeResources(
                requests=RuntimeResourceRequests(memory_mib=memory_mib, vcpus=vcpus),
                limits=RuntimeResourceLimits(memory_mib=memory_mib),
            ),
            ingress_specs=[],
            status=RuntimeStatus.RUNNING,
            egress_policy=EgressPolicy(),
        )
        self.runtimes[info.id] = info
        return info

    async def list_runtimes(self, status: str | None = None) -> list[RuntimeInfo]:
        items = list(self.runtimes.values())
        if not status:
            return items
        allowed = {RuntimeStatus.from_user(item.strip()) for item in status.split(",")}
        return [item for item in items if item.status in allowed]

    async def get_runtime(self, runtime_id: str) -> RuntimeInfo:
        for info in self.runtimes.values():
            if info.id == runtime_id or info.display_name == runtime_id:
                return info
        raise ApiError(
            f"runtime not found: {runtime_id}", status_code=404, code="not_found"
        )

    async def delete_runtime(self, runtime_id: str) -> None:
        info = await self.get_runtime(runtime_id)
        del self.runtimes[info.id]
        self.files = {
            key: content for key, content in self.files.items() if key[0] != info.id
        }

    async def read_file(self, runtime_id: str, path: str) -> bytes:
        info = await self.get_runtime(runtime_id)
        try:
            return self.files[(info.id, path)]
        except KeyError as exc:
            raise ApiError(
                f"file not found: {path}", status_code=404, code="not_found"
            ) from exc

    async def write_file(
        self, runtime_id: str, path: str, content: bytes | str
    ) -> None:
        info = await self.get_runtime(runtime_id)
        if isinstance(content, str):
            content = content.encode()
        self.files[(info.id, path)] = content

    async def upload_path(self, runtime_id: str, src: Path, dst: str) -> None:
        target = f"{dst.rstrip('/')}/{src.name}" if dst.endswith("/") else dst
        await self.write_file(runtime_id, target, src.read_bytes())

    async def download_path(
        self,
        runtime_id: str,
        src: str,
        dst: Path,
        *,
        destination_is_directory: bool,
    ) -> None:
        target = dst / Path(src).name if destination_is_directory else dst
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(await self.read_file(runtime_id, src))

    async def update_runtime_status(self, runtime_id: str, action: str) -> RuntimeInfo:
        info = await self.get_runtime(runtime_id)
        status = {
            "boot": RuntimeStatus.RUNNING,
            "resume": RuntimeStatus.RUNNING,
            "pause": RuntimeStatus.PAUSED,
            "shutdown": RuntimeStatus.SHUTDOWN,
        }[action]
        info = replace(info, status=status)
        self.runtimes[info.id] = info
        return info

    async def patch_runtime(
        self,
        runtime_id: str,
        *,
        resources: object | None = None,
        egress_policy: EgressPolicy | None = None,
    ) -> RuntimeInfo:
        info = await self.get_runtime(runtime_id)
        if egress_policy is not None:
            for host in [*egress_policy.allowed_hosts, *egress_policy.denied_hosts]:
                _validate_egress_host(host)
            info = replace(info, egress_policy=egress_policy)
        if resources is not None:
            info = replace(info, resources=resources)
        self.runtimes[info.id] = info
        return info

    async def execute(
        self,
        runtime_id: str,
        command: str,
        args: Sequence[str] = (),
        **_kwargs: Any,
    ) -> CommandResult:
        info = await self.get_runtime(runtime_id)
        command_text = " ".join([command, *args])
        if "example.com" in command_text:
            status = "200" if self._host_allowed(info, "example.com") else "403"
            return CommandResult(0, status.encode(), b"", 0.01)
        return CommandResult(0, b"", b"", 0.01)

    def _host_allowed(self, info: RuntimeInfo, host: str) -> bool:
        if info.egress_policy.mode == EgressMode.ALLOWLIST:
            return host in info.egress_policy.allowed_hosts
        return host not in info.egress_policy.denied_hosts


async def _wait_for_status(
    test: unittest.TestCase,
    runtime,
    expected: set[RuntimeStatus],
    *,
    timeout: float,
    verbose: bool = False,
) -> RuntimeStatus:
    async def get_status() -> RuntimeStatus:
        return await runtime.status()

    return await _eventually(
        test,
        get_status,
        lambda status: status in expected,
        timeout=timeout,
        detail=f"runtime {runtime.id} did not reach one of {sorted(item.value for item in expected)}",
        label=f"runtime {runtime.id} status",
        verbose=verbose,
    )


async def _curl_http_status(runtime, url: str) -> str:
    command = (
        "curl -sS -o /tmp/runta-live-curl-body "
        "-w '%{http_code}' "
        "--max-time 15 "
        f"{url!r} "
        "|| printf 'curl_exit:%s' \"$?\""
    )
    result = await runtime.exec(command, timeout=25)
    return result.stdout_text.strip()


async def _eventually(
    test: unittest.TestCase,
    func: Callable[[], Awaitable[object]],
    predicate: Callable[[object], bool],
    *,
    timeout: float,
    detail: str,
    label: str = "poll",
    verbose: bool = False,
):
    deadline = time.monotonic() + timeout
    last_value = None
    attempt = 0
    while time.monotonic() < deadline:
        attempt += 1
        last_value = await func()
        if verbose:
            print(
                f"[live] {label}: poll {attempt}: {_display_value(last_value)}",
                flush=True,
            )
        if predicate(last_value):
            if verbose:
                print(
                    f"[live] {label}: success: {_display_value(last_value)}", flush=True
                )
            return last_value
        await asyncio.sleep(3)
    test.fail(f"{detail}; last_value={last_value!r}")


def _display_value(value: object) -> str:
    if isinstance(value, RuntimeStatus):
        return value.value
    return repr(value)


def _validate_egress_host(value: str) -> str:
    if value.startswith("*."):
        valid = _valid_egress_host_name(value[2:])
    else:
        valid = _valid_egress_host_name(value)
    if value and len(value) <= 253 and valid:
        return value
    raise ApiError(
        f"invalid egress host '{value}'",
        status_code=400,
        code="invalid_argument",
    )


def _valid_egress_host_name(host: str) -> bool:
    return bool(host) and all(
        _valid_egress_host_label(label) for label in host.split(".")
    )


def _valid_egress_host_label(label: str) -> bool:
    return (
        bool(label)
        and len(label) <= 63
        and all(
            char.isascii()
            and (char.isalnum() or (char == "-" and 0 < index < len(label) - 1))
            for index, char in enumerate(label)
        )
    )


if __name__ == "__main__":
    unittest.main()
