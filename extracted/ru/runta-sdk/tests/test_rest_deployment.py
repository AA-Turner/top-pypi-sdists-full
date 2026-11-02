from __future__ import annotations

import asyncio
import os
import tempfile
import time
import unittest
import uuid
from pathlib import Path

import httpx

from runta import ApiError, AsyncRunta, EgressMode, EgressPolicy, RuntimeStatus


def _read_token_file(path: str | None) -> str | None:
    if not path:
        return None
    try:
        with open(os.path.expanduser(path), encoding="utf-8") as handle:
            token = handle.read().strip()
    except OSError:
        return None
    return token or None


REST_ENDPOINT = os.getenv("RUNTA_REST_ENDPOINT", "https://api.runta.com")
REST_TOKEN = os.getenv("RUNTA_REST_TOKEN") or _read_token_file(
    os.getenv("RUNTA_REST_TOKEN_FILE")
)
REST_LIVE_ENABLED = os.getenv("RUNTA_REST_LIVE") == "1"
REST_SKIP_REASON = (
    "set RUNTA_REST_LIVE=1 and RUNTA_REST_TOKEN or RUNTA_REST_TOKEN_FILE "
    "to dogfood the deployed REST API"
)


def _rest_ready() -> bool:
    return REST_LIVE_ENABLED and bool(REST_ENDPOINT) and bool(REST_TOKEN)


@unittest.skipUnless(_rest_ready(), REST_SKIP_REASON)
class RestDeploymentTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        assert REST_TOKEN is not None
        self.client = AsyncRunta(endpoint=REST_ENDPOINT, token=REST_TOKEN, timeout=90)
        self.created_runtimes = []
        self.created_secrets = []

    async def asyncTearDown(self) -> None:
        for runtime in reversed(self.created_runtimes):
            try:
                await runtime.delete()
            except Exception:
                pass
        for secret_name in reversed(self.created_secrets):
            try:
                await self.client.secrets.delete(secret_name)
            except Exception:
                pass
        await self.client.close()

    async def test_healthz_is_public(self) -> None:
        async with httpx.AsyncClient(timeout=30, trust_env=False) as client:
            response = await client.get(f"{REST_ENDPOINT.rstrip('/')}/healthz")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"")

    async def test_runtime_exec_files_and_cleanup_through_rest_api(self) -> None:
        suffix = uuid.uuid4().hex[:8]
        runtime = await self.client.runtimes.create(
            f"rest-dogfood-{suffix}",
            vcpus=1,
            memory_mib=1024,
            idle_suspend_after_secs=300,
        )
        self.created_runtimes.append(runtime)

        if runtime.cached_info.status != RuntimeStatus.RUNNING:
            await runtime.boot()
        await self._wait_for_status(runtime, RuntimeStatus.RUNNING, timeout=300)

        exec_result = await runtime.exec(
            ["sh", "-lc", "printf rest-dogfood"], timeout=30
        )
        self.assertEqual(exec_result.exit_code, 0)
        self.assertEqual(exec_result.stdout_text, "rest-dogfood")

        remote_path = f"/tmp/rest-dogfood-{suffix}.txt"
        await runtime.files.write(remote_path, "file-route-ok")
        self.assertEqual(await runtime.files.read(remote_path), b"file-route-ok")

        cat_result = await runtime.exec(["cat", remote_path], timeout=30)
        self.assertEqual(cat_result.exit_code, 0)
        self.assertEqual(cat_result.stdout_text, "file-route-ok")

        await runtime.delete()
        self.created_runtimes.remove(runtime)
        await self._wait_for_deleted(runtime.id, timeout=120)

    async def test_list_get_status_and_lifecycle_transitions(self) -> None:
        suffix = uuid.uuid4().hex[:8]
        runtime = await self._create_runtime(
            f"rest-dogfood-lifecycle-{suffix}",
            egress_policy=EgressPolicy(mode=EgressMode.ALLOWLIST),
        )

        fetched = await self.client.runtimes.get(runtime.id)
        self.assertEqual(fetched.id, runtime.id)

        by_name = await self.client.runtimes.get(runtime.name)
        self.assertEqual(by_name.id, runtime.id)

        listed = await self.client.runtimes.list()
        self.assertIn(runtime.id, {item.id for item in listed})

        await self._ensure_running(runtime)
        running = await self.client.runtimes.list(status="running")
        self.assertIn(runtime.id, {item.id for item in running})

        await runtime.pause()
        await self._wait_for_status(runtime, RuntimeStatus.PAUSED, timeout=180)

        await runtime.resume()
        await self._wait_for_status(runtime, RuntimeStatus.RUNNING, timeout=240)

        await runtime.shutdown()
        await self._wait_for_status(runtime, RuntimeStatus.SHUTDOWN, timeout=180)

        await runtime.delete()
        self.created_runtimes.remove(runtime)
        await self._wait_for_deleted(runtime.id, timeout=120)

    async def test_file_upload_download_directory_and_session_exec(self) -> None:
        suffix = uuid.uuid4().hex[:8]
        runtime = await self._create_runtime(f"rest-dogfood-files-{suffix}")
        await self._ensure_running(runtime)

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            local_file = tmp_path / "payload.txt"
            local_file.write_text("upload-file-ok", encoding="utf-8")
            remote_file = f"/tmp/rest-upload-{suffix}.txt"

            await runtime.files.upload(str(local_file), remote_file)
            self.assertEqual(await runtime.files.read(remote_file), b"upload-file-ok")

            downloaded = tmp_path / "downloaded.txt"
            await runtime.files.download(remote_file, str(downloaded))
            self.assertEqual(downloaded.read_text(encoding="utf-8"), "upload-file-ok")

            local_dir = tmp_path / "tree"
            local_dir.mkdir()
            (local_dir / "a.txt").write_text("a", encoding="utf-8")
            nested = local_dir / "nested"
            nested.mkdir()
            (nested / "b.txt").write_text("b", encoding="utf-8")

            remote_dir = f"/tmp/rest-tree-{suffix}"
            await runtime.files.upload(str(local_dir), remote_dir)
            check = await runtime.exec(
                ["sh", "-lc", f"cat {remote_dir}/a.txt {remote_dir}/nested/b.txt"],
                timeout=30,
            )
            self.assertEqual(check.exit_code, 0)
            self.assertEqual(check.stdout_text, "ab")

    async def test_egress_policy_allowlist(self) -> None:
        suffix = uuid.uuid4().hex[:8]
        runtime = await self._create_runtime(
            f"rest-dogfood-egress-{suffix}",
            egress_policy=EgressPolicy(mode=EgressMode.ALLOWLIST),
        )
        await self._ensure_running(runtime)

        await runtime.egress.set_policy(EgressPolicy(mode=EgressMode.ALLOWLIST))
        self.assertEqual((await runtime.egress.get()).allowed_hosts, [])

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

        status = await self._eventually(
            lambda: self._curl_status(runtime, "http://example.com"),
            lambda value: value == "200",
            timeout=90,
            detail="example.com should be allowed after allowlist update",
        )
        self.assertEqual(status, "200")

        await runtime.egress.set_policy(EgressPolicy(mode=EgressMode.ALLOWLIST))
        self.assertEqual((await runtime.egress.get()).allowed_hosts, [])

    async def test_secret_crud_and_expected_error_mapping(self) -> None:
        secret_name = f"rest-dogfood-secret-{uuid.uuid4().hex[:8]}"
        secret = await self.client.secrets.set(
            secret_name, "secret-value", cache_ttl_secs=0
        )
        self.created_secrets.append(secret_name)

        fetched = await self.client.secrets.get(secret_name)
        self.assertEqual(fetched.id, secret.id)

        listed = await self.client.secrets.list()
        self.assertIn(secret_name, {item.display_name for item in listed})

        await self.client.secrets.delete(secret_name)
        self.created_secrets.remove(secret_name)

        with self.assertRaises(ApiError) as ctx:
            await self.client.runtimes.get(str(uuid.uuid4()))
        self.assertIn(ctx.exception.status_code, {404, 500})

    async def _create_runtime(self, name: str, **options):
        runtime = await self.client.runtimes.create(
            name,
            vcpus=1,
            memory_mib=1024,
            idle_suspend_after_secs=300,
            **options,
        )
        self.created_runtimes.append(runtime)
        return runtime

    async def _ensure_running(self, runtime) -> None:
        if runtime.cached_info.status != RuntimeStatus.RUNNING:
            await runtime.boot()
        await self._wait_for_status(runtime, RuntimeStatus.RUNNING, timeout=300)

    async def _wait_for_status(
        self, runtime, expected: RuntimeStatus, *, timeout: float
    ) -> None:
        deadline = time.monotonic() + timeout
        last_status = None
        while time.monotonic() < deadline:
            last_status = await runtime.status()
            if last_status == expected:
                return
            if last_status in {RuntimeStatus.ERROR, RuntimeStatus.CRASHED}:
                self.fail(f"runtime {runtime.id} entered {last_status.value}")
            await asyncio.sleep(3)
        self.fail(
            f"runtime {runtime.id} did not reach {expected.value} within {timeout}s; "
            f"last_status={last_status.value if last_status else 'unknown'}"
        )

    async def _wait_for_deleted(self, runtime_id: str, *, timeout: float) -> None:
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            try:
                await self.client.runtimes.get(runtime_id)
            except ApiError:
                return
            await asyncio.sleep(2)
        self.fail(f"runtime {runtime_id} was not deleted within {timeout}s")

    async def _eventually(self, func, predicate, *, timeout: float, detail: str):
        deadline = time.monotonic() + timeout
        last_value = None
        while time.monotonic() < deadline:
            last_value = await func()
            if predicate(last_value):
                return last_value
            await asyncio.sleep(3)
        self.fail(f"{detail}; last_value={last_value!r}")

    async def _curl_status(self, runtime, url: str) -> str:
        result = await runtime.exec(
            [
                "sh",
                "-lc",
                f"curl -sS -o /tmp/rest-dogfood-curl-body -w '%{{http_code}}' --max-time 20 {url!r}",
            ],
            timeout=30,
        )
        if result.exit_code != 0:
            self.fail(
                f"curl failed: stdout={result.stdout_text!r} stderr={result.stderr_text!r}"
            )
        return result.stdout_text.strip()
