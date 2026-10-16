import asyncio
import base64
import json
import time
from contextlib import suppress
from http import HTTPStatus
from typing import Any
from unittest.mock import MagicMock

import pytest
from pydantic import SecretStr
from temporalio.runtime import Runtime

from mistralai.workflows.core.auth import FileTokenProvider, StaticTokenProvider
from mistralai.workflows.core.config.config import AppConfig
from mistralai.workflows.core.temporal import temporal_client
from mistralai.workflows.exceptions import ErrorCode, WorkflowError, WorkflowsException


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
    def _patch_sleep(monkeypatch, stop_after: int, on_sleep=None) -> list[float]:
        """Patch asyncio.sleep to record slept durations and cancel after ``stop_after`` calls.

        ``on_sleep(call_index)`` runs on each call (1-based) for tests that mutate state between polls.
        """
        captured: list[float] = []

        async def fake_sleep(seconds: float) -> None:
            captured.append(seconds)
            if on_sleep is not None:
                on_sleep(len(captured))
            if len(captured) >= stop_after:
                raise asyncio.CancelledError

        monkeypatch.setattr(temporal_client.asyncio, "sleep", fake_sleep)
        return captured

    @staticmethod
    def _use_file_provider(monkeypatch, token_file) -> None:
        cfg = AppConfig()
        monkeypatch.setattr(cfg.temporal, "api_key", None)
        monkeypatch.setattr(cfg.common, "mistral_sa_token_path", str(token_file))
        monkeypatch.setattr(temporal_client, "config", cfg)
        monkeypatch.setattr(temporal_client, "get_token_provider", lambda *a: FileTokenProvider(token_file))

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
        self._patch_sleep(monkeypatch, 2, on_sleep=lambda i: token_file.write_text(token_v2) if i == 1 else None)

        with pytest.raises(asyncio.CancelledError):
            await temporal_client.refresh_temporal_api_key(service_client)

        pushed = [c.args[0] for c in service_client.update_api_key.call_args_list]
        assert pushed == [token_v1, token_v2]

    @pytest.mark.asyncio
    async def test_pushes_once_when_token_unchanged(self, monkeypatch, tmp_path):
        token = _fresh_jwt()
        token_file = tmp_path / "token"
        token_file.write_text(token)
        self._use_file_provider(monkeypatch, token_file)

        service_client = MagicMock()
        self._patch_sleep(monkeypatch, 3)

        with pytest.raises(asyncio.CancelledError):
            await temporal_client.refresh_temporal_api_key(service_client)

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
        from mistralai.workflows.core.auth import TokenWithMaxAge

        cfg = AppConfig()
        monkeypatch.setattr(cfg.temporal, "api_key", None)
        monkeypatch.setattr(cfg.common, "mistral_sa_token_path", str(tmp_path / "token"))
        monkeypatch.setattr(temporal_client, "config", cfg)

        class FlakyProvider(FileTokenProvider):
            def __init__(self) -> None:
                super().__init__(tmp_path / "token")
                self.calls = 0

            def get_token_with_max_age(self) -> TokenWithMaxAge:
                self.calls += 1
                if self.calls == 1:
                    raise WorkflowError("transient read failure", non_retryable=True)
                return TokenWithMaxAge("recovered-token", 0.0)

        monkeypatch.setattr(temporal_client, "get_token_provider", lambda *a: FlakyProvider())

        service_client = MagicMock()
        self._patch_sleep(monkeypatch, 2)

        with pytest.raises(asyncio.CancelledError):
            await temporal_client.refresh_temporal_api_key(service_client)

        service_client.update_api_key.assert_called_once_with("recovered-token")

    @pytest.mark.asyncio
    async def test_survives_update_api_key_error(self, monkeypatch, tmp_path):
        # A failing push must not propagate (it would tear down the worker's TaskGroup); retry next cycle.
        token_file = tmp_path / "token"
        token_file.write_text(_fresh_jwt())
        self._use_file_provider(monkeypatch, token_file)

        service_client = MagicMock()
        service_client.update_api_key.side_effect = [RuntimeError("transient push failure"), None]
        self._patch_sleep(monkeypatch, 2)

        with pytest.raises(asyncio.CancelledError):
            await temporal_client.refresh_temporal_api_key(service_client)

        assert service_client.update_api_key.call_count == 2  # first push raised, loop retried and pushed again

    @pytest.mark.asyncio
    async def test_sleeps_until_refresh_plus_delay(self, monkeypatch, tmp_path):
        # exp + 600, margin 30 → wakes (600 - 30) + 5 = 575s later, i.e. 25s before expiry.
        token_file = tmp_path / "token"
        token_file.write_text(_make_jwt(exp=time.time() + 600))
        self._use_file_provider(monkeypatch, token_file)
        captured = self._patch_sleep(monkeypatch, 1)

        with pytest.raises(asyncio.CancelledError):
            await temporal_client.refresh_temporal_api_key(MagicMock())

        assert 570 <= captured[0] <= 575  # 575 minus a little time.time() drift
