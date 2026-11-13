import asyncio
import base64
import concurrent.futures
import json
import threading
import time
from collections.abc import AsyncIterator, Callable
from contextlib import asynccontextmanager, suppress
from http import HTTPStatus
from typing import Any
from unittest.mock import MagicMock

import pytest
from pydantic import SecretStr
from temporalio.runtime import Runtime

from mistralai.workflows.core.auth import FileTokenProvider, StaticTokenProvider, TokenWithMaxAge
from mistralai.workflows.core.config.config import AppConfig
from mistralai.workflows.core.temporal import temporal_client
from mistralai.workflows.exceptions import ErrorCode, WorkflowError, WorkflowsException

_TEST_REFRESH_DELAY_SECONDS = 0.05


def _make_jwt(exp: float) -> str:
    """Build a minimal unsigned JWT whose payload carries the given ``exp`` (signature not verified)."""

    def _seg(obj: dict[str, Any]) -> str:
        return base64.urlsafe_b64encode(json.dumps(obj).encode()).rstrip(b"=").decode()

    return f"{_seg({'alg': 'none', 'typ': 'JWT'})}.{_seg({'exp': exp})}.sig"


def _fresh_jwt(bump: float = 0.0) -> str:
    """A JWT whose exp is already inside the refresh margin, so FileTokenProvider re-reads it every call.

    ``bump`` yields a distinct token string (different ``exp``) to simulate rotation.
    """
    return _make_jwt(exp=time.time() + bump)


def _disable_otel(monkeypatch: pytest.MonkeyPatch, cfg: AppConfig) -> None:
    monkeypatch.setattr(cfg.common, "otel_enabled", False)
    monkeypatch.setattr(temporal_client, "config", cfg)
    # No runtime is passed, so the factory calls build_client_runtime(); stub it to avoid a real runtime.
    monkeypatch.setattr(temporal_client, "build_client_runtime", lambda: MagicMock())


async def _return_http2_unauthorized(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
    # The Temporal bridge speaks HTTP/2 directly. Return a real HTTP/2 401 response so this test exercises
    # the bridge's current RuntimeError text instead of copying that unstable text into a fixture.
    await reader.readexactly(24)  # HTTP/2 client preface
    writer.write(b"\x00\x00\x00\x04\x00\x00\x00\x00\x00")  # empty SETTINGS frame
    await writer.drain()
    while True:
        frame_header = await reader.readexactly(9)
        payload_length = int.from_bytes(frame_header[:3])
        frame_type = frame_header[3]
        stream_id = int.from_bytes(frame_header[5:]) & 0x7FFFFFFF
        if payload_length:
            await reader.readexactly(payload_length)
        if frame_type == 1 and stream_id:
            break

    # HPACK literal for `:status: 401`, followed by an END_HEADERS | END_STREAM HEADERS frame.
    header_block = b"\x08\x03" + b"401"
    writer.write(len(header_block).to_bytes(3) + b"\x01\x05" + stream_id.to_bytes(4) + header_block)
    await writer.drain()
    writer.close()
    with suppress(ConnectionError):
        await writer.wait_closed()


def _capture_connect_config(monkeypatch: pytest.MonkeyPatch) -> list[Any]:
    captured: list[Any] = []

    async def fake_connect(connect_config: Any) -> MagicMock:
        captured.append(connect_config)
        return MagicMock()

    monkeypatch.setattr(temporal_client.TemporalServiceClient, "connect", fake_connect)
    return captured


class TestTemporalTokenResolution:
    @pytest.mark.asyncio
    async def test_explicit_temporal_api_key_takes_precedence(self, monkeypatch):
        cfg = AppConfig()
        monkeypatch.setattr(cfg.temporal, "api_key", SecretStr("temporal-key"))
        _disable_otel(monkeypatch, cfg)
        captured = _capture_connect_config(monkeypatch)

        await temporal_client.create_temporal_service_client()

        assert captured[0].api_key == "temporal-key"

    @pytest.mark.asyncio
    async def test_falls_back_to_token_provider(self, monkeypatch):
        cfg = AppConfig()
        monkeypatch.setattr(cfg.temporal, "api_key", None)
        _disable_otel(monkeypatch, cfg)
        monkeypatch.setattr(temporal_client, "get_token_provider", lambda *a: StaticTokenProvider("provider-token"))
        captured = _capture_connect_config(monkeypatch)

        await temporal_client.create_temporal_service_client()

        assert captured[0].api_key == "provider-token"

    @pytest.mark.asyncio
    async def test_no_token_when_provider_absent(self, monkeypatch):
        cfg = AppConfig()
        monkeypatch.setattr(cfg.temporal, "api_key", None)
        _disable_otel(monkeypatch, cfg)
        monkeypatch.setattr(temporal_client, "get_token_provider", lambda *a: None)
        captured = _capture_connect_config(monkeypatch)

        await temporal_client.create_temporal_service_client()

        assert captured[0].api_key is None


class TestTemporalConnectionErrors:
    @pytest.mark.asyncio
    async def test_real_bridge_unauthorized_response_is_preserved(self, monkeypatch: pytest.MonkeyPatch) -> None:
        server = await asyncio.start_server(_return_http2_unauthorized, "127.0.0.1", 0)
        port = server.sockets[0].getsockname()[1]
        cfg = AppConfig()
        monkeypatch.setattr(cfg.temporal, "server_url", f"127.0.0.1:{port}")
        monkeypatch.setattr(cfg.temporal, "tls", False)
        monkeypatch.setattr(cfg.temporal, "api_key", SecretStr("invalid-key"))
        monkeypatch.setattr(temporal_client, "config", cfg)

        try:
            with pytest.raises(WorkflowsException) as exc_info:
                await temporal_client.create_temporal_service_client(runtime=Runtime.default())
        finally:
            server.close()
            await server.wait_closed()

        assert exc_info.value.status == HTTPStatus.UNAUTHORIZED
        assert exc_info.value.code == ErrorCode.TEMPORAL_CONNECTION_ERROR
        assert "code: Unauthenticated" in exc_info.value.logging_properties["temporal_connection_error"]

    @pytest.mark.parametrize(
        ("message", "uses_http_connect_proxy", "expected_status"),
        [
            (
                "Failed client connect: `get_system_info` call error after connection: "
                'Status { code: Internal, message: "invalid compression flag 3 (valid flags are 0 and 1) '
                'while receiving response with status: 401 Unauthorized" }',
                False,
                HTTPStatus.UNAUTHORIZED,
            ),
            (
                "Failed client connect: `get_system_info` call error after connection: "
                'Status { code: Unauthenticated, message: "invalid API key" }',
                False,
                HTTPStatus.UNAUTHORIZED,
            ),
            (
                "Failed client connect: `get_system_info` call error after connection: "
                'Status { code: Internal, message: "invalid compression flag 3 (valid flags are 0 and 1) '
                'while receiving response with status: 401 Unauthorized" }',
                True,
                HTTPStatus.UNAUTHORIZED,
            ),
            (
                "Failed client connect: `get_system_info` call error after connection: "
                'Status { code: Unauthenticated, message: "invalid API key" }',
                True,
                HTTPStatus.UNAUTHORIZED,
            ),
            # Temporal sdk-core/crates/client/src/proxy.rs:76 emits this only for a failed CONNECT tunnel.
            ("CONNECT call failed with status: 401 Unauthorized", True, HTTPStatus.INTERNAL_SERVER_ERROR),
            ("Failed client connect: DNS resolution error", False, HTTPStatus.INTERNAL_SERVER_ERROR),
        ],
    )
    def test_connection_error_status(self, message, uses_http_connect_proxy, expected_status):
        status = temporal_client._connection_error_status(
            RuntimeError(message),
            uses_http_connect_proxy=uses_http_connect_proxy,
        )

        assert status == expected_status


class TestReadTemporalToken:
    class _FlakyProvider(FileTokenProvider):
        def __init__(self, failures: int) -> None:
            super().__init__("/unused")
            self._failures = failures
            self.calls = 0

        def get_token(self) -> str:
            self.calls += 1
            if self.calls <= self._failures:
                raise WorkflowError("transient mount blip", non_retryable=False)
            return "ok-token"

    @staticmethod
    def _patch_sleep(monkeypatch) -> None:
        async def fake_sleep(_seconds: float) -> None:
            return None

        monkeypatch.setattr(temporal_client.asyncio, "sleep", fake_sleep)

    @pytest.mark.asyncio
    async def test_retries_transient_read_failure_then_succeeds(self, monkeypatch):
        self._patch_sleep(monkeypatch)
        provider = self._FlakyProvider(failures=1)
        assert await temporal_client._read_temporal_token(provider) == "ok-token"
        assert provider.calls == 2

    @pytest.mark.asyncio
    async def test_raises_after_exhausting_attempts(self, monkeypatch):
        self._patch_sleep(monkeypatch)
        provider = self._FlakyProvider(failures=99)
        with pytest.raises(WorkflowError):
            await temporal_client._read_temporal_token(provider)
        assert provider.calls == temporal_client._TEMPORAL_TOKEN_STARTUP_READ_ATTEMPTS


class TestTemporalTokenRefresh:
    @staticmethod
    def _use_file_provider(monkeypatch, token_file, provider: FileTokenProvider | None = None) -> None:
        cfg = AppConfig()
        monkeypatch.setattr(cfg.temporal, "api_key", None)
        monkeypatch.setattr(cfg.common, "mistral_sa_token_path", str(token_file))
        monkeypatch.setattr(temporal_client, "config", cfg)
        resolved = provider or FileTokenProvider(token_file)
        monkeypatch.setattr(temporal_client, "get_token_provider", lambda *a: resolved)

    @staticmethod
    def _rotate(token_file, token: str) -> None:
        # Swap the file in one step, like the kubelet does, so a concurrent reader never sees a half-written token.
        staged = token_file.with_name(f"{token_file.name}.staged")
        staged.write_text(token)
        staged.replace(token_file)

    @staticmethod
    def _pushed(service_client: MagicMock) -> list[str]:
        return [c.args[0] for c in service_client.update_api_key.call_args_list]

    @staticmethod
    async def _wait_until(condition: Callable[[], bool], timeout: float = 2.0) -> None:
        deadline = time.monotonic() + timeout
        while not condition():
            assert time.monotonic() < deadline, "condition not met before timeout"
            await asyncio.sleep(0.01)

    @staticmethod
    @asynccontextmanager
    async def _refreshing(service_client: MagicMock) -> AsyncIterator[None]:
        """Run the refresh like the worker does: a task cancelled on exit."""
        task = asyncio.create_task(
            temporal_client.refresh_temporal_api_key(service_client, delay_seconds=_TEST_REFRESH_DELAY_SECONDS)
        )
        try:
            yield
        finally:
            task.cancel()
            with suppress(asyncio.CancelledError):
                await task

    @pytest.mark.asyncio
    async def test_pushes_rotated_token(self, monkeypatch, tmp_path):
        # A near-expiry JWT is re-read every get_token(), so a rotated file is picked up and pushed.
        token_v1 = _fresh_jwt()
        token_v2 = _fresh_jwt(bump=1.0)
        assert token_v1 != token_v2
        token_file = tmp_path / "token"
        token_file.write_text(token_v1)
        self._use_file_provider(monkeypatch, token_file)
        service_client = MagicMock()

        async with self._refreshing(service_client):
            await self._wait_until(lambda: self._pushed(service_client) == [token_v1])
            self._rotate(token_file, token_v2)
            await self._wait_until(lambda: self._pushed(service_client) == [token_v1, token_v2])

    @pytest.mark.asyncio
    async def test_pushes_rotated_token_while_event_loop_is_blocked(self, monkeypatch, tmp_path):
        # An async activity running CPU-bound code blocks the loop; the pollers must still get the rotated token.
        token_v1 = _fresh_jwt()
        token_v2 = _fresh_jwt(bump=1.0)
        token_file = tmp_path / "token"
        token_file.write_text(token_v1)
        self._use_file_provider(monkeypatch, token_file)
        service_client = MagicMock()

        async with self._refreshing(service_client):
            await self._wait_until(lambda: self._pushed(service_client) == [token_v1])
            self._rotate(token_file, token_v2)
            time.sleep(20 * _TEST_REFRESH_DELAY_SECONDS)
            assert self._pushed(service_client) == [token_v1, token_v2]

    @pytest.mark.asyncio
    async def test_stops_pushing_once_cancelled(self, monkeypatch, tmp_path):
        token_v1 = _fresh_jwt()
        token_v2 = _fresh_jwt(bump=1.0)
        token_file = tmp_path / "token"
        token_file.write_text(token_v1)
        self._use_file_provider(monkeypatch, token_file)
        service_client = MagicMock()

        async with self._refreshing(service_client):
            await self._wait_until(lambda: self._pushed(service_client) == [token_v1])
        self._rotate(token_file, token_v2)
        await asyncio.sleep(5 * _TEST_REFRESH_DELAY_SECONDS)

        assert self._pushed(service_client) == [token_v1]

    @pytest.mark.asyncio
    async def test_thread_exits_cleanly_when_cancelled_twice(self, monkeypatch, tmp_path):
        # On shutdown the worker cancels this task twice: the TaskGroup abort, then run_worker's finally.
        reading = threading.Event()
        release = threading.Event()

        class BlockingProvider(FileTokenProvider):
            def get_token_with_max_age(self) -> TokenWithMaxAge:
                reading.set()
                release.wait()
                return TokenWithMaxAge("token", 0.0)

        self._use_file_provider(monkeypatch, tmp_path / "token", BlockingProvider(tmp_path / "token"))
        thread_errors: list[threading.ExceptHookArgs] = []
        monkeypatch.setattr(threading, "excepthook", thread_errors.append)
        task = asyncio.create_task(
            temporal_client.refresh_temporal_api_key(MagicMock(), delay_seconds=_TEST_REFRESH_DELAY_SECONDS)
        )
        await self._wait_until(reading.is_set)
        (refresh_thread,) = [t for t in threading.enumerate() if t.name == "temporal-token-refresh"]

        task.cancel()
        await asyncio.sleep(_TEST_REFRESH_DELAY_SECONDS)
        task.cancel()
        with pytest.raises(asyncio.CancelledError):
            await task
        release.set()
        await self._wait_until(lambda: not refresh_thread.is_alive())

        assert thread_errors == []

    @pytest.mark.asyncio
    async def test_pushes_once_when_token_unchanged(self, monkeypatch, tmp_path):
        token = _fresh_jwt()
        token_file = tmp_path / "token"
        token_file.write_text(token)
        self._use_file_provider(monkeypatch, token_file)
        service_client = MagicMock()

        async with self._refreshing(service_client):
            await self._wait_until(lambda: service_client.update_api_key.called)
            await asyncio.sleep(5 * _TEST_REFRESH_DELAY_SECONDS)

        service_client.update_api_key.assert_called_once_with(token)

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "temporal_api_key",
        [SecretStr("temporal-key"), None],
        ids=["explicit-temporal-key", "no-credentials"],
    )
    async def test_noop_when_not_rotating(self, monkeypatch, temporal_api_key):
        # Non-rotating providers (explicit static key, or no credentials) → nothing is pushed, no loop.
        cfg = AppConfig()
        monkeypatch.setattr(cfg.temporal, "api_key", temporal_api_key)
        monkeypatch.setattr(cfg.common, "mistral_sa_token_path", None)
        monkeypatch.setattr(cfg.common, "mistral_api_key", None)
        monkeypatch.setattr(temporal_client, "config", cfg)
        service_client = MagicMock()

        await temporal_client.refresh_temporal_api_key(service_client)

        service_client.update_api_key.assert_not_called()

    @pytest.mark.asyncio
    async def test_survives_transient_read_error(self, monkeypatch, tmp_path):
        # The refresh loop reads via get_token_with_max_age; a transient read failure must be swallowed
        # and retried on the next cycle rather than tearing down the loop.
        class FlakyProvider(FileTokenProvider):
            def __init__(self) -> None:
                super().__init__(tmp_path / "token")
                self.calls = 0

            def get_token_with_max_age(self) -> TokenWithMaxAge:
                self.calls += 1
                if self.calls == 1:
                    raise WorkflowError("transient read failure", non_retryable=True)
                return TokenWithMaxAge("recovered-token", 0.0)

        self._use_file_provider(monkeypatch, tmp_path / "token", FlakyProvider())
        service_client = MagicMock()

        async with self._refreshing(service_client):
            await self._wait_until(lambda: service_client.update_api_key.called)

        service_client.update_api_key.assert_called_once_with("recovered-token")

    @pytest.mark.asyncio
    async def test_survives_update_api_key_error(self, monkeypatch, tmp_path):
        # A failing push must not propagate (it would tear down the worker's TaskGroup); retry next cycle.
        token_file = tmp_path / "token"
        token_file.write_text(_fresh_jwt())
        self._use_file_provider(monkeypatch, token_file)
        service_client = MagicMock()
        service_client.update_api_key.side_effect = [RuntimeError("transient push failure"), None]

        async with self._refreshing(service_client):
            await self._wait_until(lambda: service_client.update_api_key.call_count == 2)

    @pytest.mark.asyncio
    async def test_waits_until_refresh_plus_delay(self, monkeypatch, tmp_path):
        # The provider says the token is good for 0.3s, so the next read waits at least 0.3s plus the delay.
        max_age = 0.3

        class RecordingProvider(FileTokenProvider):
            def __init__(self) -> None:
                super().__init__(tmp_path / "token")
                self.read_at: list[float] = []

            def get_token_with_max_age(self) -> TokenWithMaxAge:
                self.read_at.append(time.monotonic())
                return TokenWithMaxAge(f"token-{len(self.read_at)}", max_age)

        provider = RecordingProvider()
        self._use_file_provider(monkeypatch, tmp_path / "token", provider)

        async with self._refreshing(MagicMock()):
            await self._wait_until(lambda: len(provider.read_at) >= 2)

        assert provider.read_at[1] - provider.read_at[0] >= max_age + _TEST_REFRESH_DELAY_SECONDS

    @pytest.mark.asyncio
    async def test_pushes_while_default_executor_is_saturated(self, monkeypatch, tmp_path):
        # Activities share the loop's default executor; a full executor must not delay the refresh.
        token = _fresh_jwt()
        token_file = tmp_path / "token"
        token_file.write_text(token)
        self._use_file_provider(monkeypatch, token_file)
        service_client = MagicMock()
        release = threading.Event()
        loop = asyncio.get_running_loop()
        loop.set_default_executor(concurrent.futures.ThreadPoolExecutor(max_workers=1))
        busy = loop.run_in_executor(None, release.wait)
        async with self._refreshing(service_client):
            try:
                await self._wait_until(lambda: self._pushed(service_client) == [token])
            finally:
                # Free the executor before cancelling, or a refresh queued behind it would never finish.
                release.set()
        await busy

    @pytest.mark.asyncio
    async def test_keeps_running_when_max_age_exceeds_wait_limit(self, monkeypatch, tmp_path):
        class FarFutureProvider(FileTokenProvider):
            def get_token_with_max_age(self) -> TokenWithMaxAge:
                return TokenWithMaxAge("far-future-token", threading.TIMEOUT_MAX * 2)

        self._use_file_provider(monkeypatch, tmp_path / "token", FarFutureProvider(tmp_path / "token"))
        service_client = MagicMock()

        async with self._refreshing(service_client):
            await self._wait_until(lambda: service_client.update_api_key.called)
            await asyncio.sleep(5 * _TEST_REFRESH_DELAY_SECONDS)

        service_client.update_api_key.assert_called_once_with("far-future-token")
