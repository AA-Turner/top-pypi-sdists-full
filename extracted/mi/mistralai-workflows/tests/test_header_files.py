import asyncio
from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from mistralai.workflows._mistral_http import MISTRAL_HTTP
from mistralai.workflows.client import _get_async_client, _get_sync_client
from mistralai.workflows.core.auth import RunAs, StaticTokenProvider, startup_read
from mistralai.workflows.core.auth.header_files import HeaderFiles, get_deployment_headers
from mistralai.workflows.core.config import config_discovery
from mistralai.workflows.core.config.config import AppConfig, config
from mistralai.workflows.core.temporal import temporal_client
from mistralai.workflows.core.temporal.context_handler_interceptor import define_context
from mistralai.workflows.core.worker import run_worker
from mistralai.workflows.exceptions import WorkflowError
from mistralai.workflows.hooks.executor_credentials_hook import AsyncExecutorCredentialsHook
from mistralai.workflows.models import WorkflowContext
from mistralai.workflows.worker_client.models import ExecutorIdentityTokenResponse
from mistralai.workflows.worker_client.sdk import PrivateWorkerClient

_SERVER_URL = "https://workflows.example"
_FILE_HEADER = "x-service-token"
_STATIC_HEADER = "x-static"
_EXECUTOR_JWT = "h.eyJleHAiOjQxMDI0NDQ4MDB9.s"  # exp far in the future


@pytest.fixture
def token_file(tmp_path, monkeypatch):
    path = tmp_path / "token"
    path.write_text("token-v1\n")
    monkeypatch.setattr(config.worker, "mistral_api_headers", {_STATIC_HEADER: "static"})
    monkeypatch.setattr(config.worker, "mistral_api_header_files", {_FILE_HEADER: str(path)})
    return path


def _recording_transport(monkeypatch, redirect_to: str | None = None) -> dict[str, tuple[str | None, str | None]]:
    """Route every SDK client through a mock transport; record (static, file) header values per host."""
    seen: dict[str, tuple[str | None, str | None]] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        seen[request.url.host] = (request.headers.get(_STATIC_HEADER), request.headers.get(_FILE_HEADER))
        if redirect_to and request.url.host == "workflows.example":
            return MISTRAL_HTTP.Response(302, headers={"Location": redirect_to})
        return MISTRAL_HTTP.Response(200)

    monkeypatch.setattr(config.http, "transport_factory", lambda _: MISTRAL_HTTP.MockTransport(handler))
    return seen


class TestHeaderFiles:
    def test_reads_each_file(self, tmp_path):
        (tmp_path / "a").write_text("value-a\n")
        (tmp_path / "b").write_text("value-b")
        header_files = HeaderFiles({"x-a": str(tmp_path / "a"), "x-b": str(tmp_path / "b")})

        assert header_files.read() == {"x-a": "value-a", "x-b": "value-b"}
        assert header_files.names == {"x-a", "x-b"}

    def test_picks_up_a_rotated_file(self, tmp_path):
        path = tmp_path / "token"
        path.write_text("v1")
        header_files = HeaderFiles({_FILE_HEADER: str(path)})
        assert header_files.read() == {_FILE_HEADER: "v1"}

        path.write_text("v2")

        assert header_files.read() == {_FILE_HEADER: "v2"}

    @pytest.mark.parametrize("break_file", ["delete", "empty"])
    def test_keeps_the_last_value_when_a_reread_fails(self, tmp_path, break_file):
        path = tmp_path / "token"
        path.write_text("v1")
        header_files = HeaderFiles({_FILE_HEADER: str(path)})
        header_files.read()

        if break_file == "delete":
            path.unlink()
        else:
            path.write_text("")

        assert header_files.read() == {_FILE_HEADER: "v1"}

    def test_raises_when_a_file_was_never_read(self, tmp_path):
        header_files = HeaderFiles({_FILE_HEADER: str(tmp_path / "missing")})

        with pytest.raises(WorkflowError):
            header_files.read()

    def test_deployment_headers_merge_static_and_file_values(self, token_file):
        assert get_deployment_headers() == {_STATIC_HEADER: "static", _FILE_HEADER: "token-v1"}


class TestHttpClients:
    @pytest.mark.asyncio
    @pytest.mark.parametrize("run_as", [None, RunAs.DEPLOYMENT])
    async def test_file_headers_go_with_the_static_headers(self, monkeypatch, token_file, run_as):
        seen = _recording_transport(monkeypatch)
        client = _get_async_client(server_url=_SERVER_URL, token_provider=StaticTokenProvider("key"), run_as=run_as)

        async with client:
            with define_context(WorkflowContext(namespace="ns", execution_id="id", on_behalf_of=False)):
                await client.get(f"{_SERVER_URL}/v1/a")

        assert seen["workflows.example"] == ("static", "token-v1")

    @pytest.mark.asyncio
    async def test_long_lived_client_sends_the_rotated_value(self, monkeypatch, token_file):
        seen = _recording_transport(monkeypatch)
        client = _get_async_client(server_url=_SERVER_URL)

        async with client:
            await client.get(f"{_SERVER_URL}/v1/a")
            assert seen["workflows.example"] == ("static", "token-v1")
            token_file.write_text("token-v2")
            await client.get(f"{_SERVER_URL}/v1/b")

        assert seen["workflows.example"] == ("static", "token-v2")

    def test_sync_client(self, monkeypatch, token_file):
        seen = _recording_transport(monkeypatch)

        with _get_sync_client(server_url=_SERVER_URL) as client:
            client.get(f"{_SERVER_URL}/v1/a")

        assert seen["workflows.example"] == ("static", "token-v1")

    @pytest.mark.asyncio
    async def test_stripped_on_cross_origin_redirect(self, monkeypatch, token_file):
        seen = _recording_transport(monkeypatch, redirect_to="https://foreign.example/target")
        client = _get_async_client(server_url=_SERVER_URL)

        async with client:
            await client.get(f"{_SERVER_URL}/v1/a")

        assert seen["workflows.example"] == ("static", "token-v1")
        assert seen["foreign.example"] == (None, None)

    @pytest.mark.asyncio
    async def test_executor_identity_carries_neither(self, monkeypatch, token_file):
        seen = _recording_transport(monkeypatch)
        client = _get_async_client(server_url=_SERVER_URL, run_as=RunAs.EXECUTOR)
        context = WorkflowContext(namespace="ns", execution_id="id", execution_token="exec-tok", on_behalf_of=True)
        response = ExecutorIdentityTokenResponse(token=_EXECUTOR_JWT)

        with patch.object(
            PrivateWorkerClient, "executor_identity_token_async", new_callable=AsyncMock, return_value=response
        ):
            async with client:
                with define_context(context):
                    await client.get(f"{_SERVER_URL}/v1/a")

        assert seen["workflows.example"] == (None, None)


class TestExecutorTokenExchange:
    @pytest.mark.asyncio
    async def test_exchange_carries_the_current_file_value(self, monkeypatch, token_file):
        hook = AsyncExecutorCredentialsHook(server_url=_SERVER_URL, run_as=RunAs.EXECUTOR)
        exchange_requests: list[httpx.Request] = []

        def handler(request: httpx.Request) -> httpx.Response:
            exchange_requests.append(request)
            return httpx.Response(200, json={"token": _EXECUTOR_JWT})

        monkeypatch.setattr(
            hook._worker_client.sdk_configuration.async_client, "_transport", httpx.MockTransport(handler)
        )
        token_file.write_text("token-v2")
        context = WorkflowContext(namespace="ns", execution_id="id", execution_token="exec-tok", on_behalf_of=True)

        with define_context(context):
            await hook(httpx.Request("GET", f"{_SERVER_URL}/v1/a"))

        assert exchange_requests[0].headers[_STATIC_HEADER] == "static"
        assert exchange_requests[0].headers[_FILE_HEADER] == "token-v2"


@pytest.mark.usefixtures("restore_config_sections")
class TestWorkerStartup:
    @pytest.mark.asyncio
    async def test_config_discovery_gets_a_header_file_empty_during_rotation(self, monkeypatch, tmp_path):
        path = tmp_path / "token"
        path.write_text("")
        monkeypatch.setattr(config.worker, "mistral_api_headers", None)
        monkeypatch.setattr(config.worker, "mistral_api_header_files", {_FILE_HEADER: str(path)})

        async def fake_sleep(_seconds: float) -> None:
            path.write_text("token-v1")

        monkeypatch.setattr(startup_read.asyncio, "sleep", fake_sleep)
        discovery_headers: list[dict[str, str]] = []

        def get_worker_client(**kwargs: Any) -> Any:
            discovery_headers.append(kwargs["headers"])
            raise _StopStartup

        monkeypatch.setattr(config_discovery, "get_worker_client", get_worker_client)

        with pytest.raises(_StopStartup):
            await run_worker([], enable_config_discovery=True)

        assert discovery_headers == [{_FILE_HEADER: "token-v1"}]


class _StopStartup(Exception):
    pass


class TestTemporalConnection:
    @pytest.mark.asyncio
    async def test_connects_with_the_deployment_headers_as_rpc_metadata(self, monkeypatch, token_file):
        cfg = AppConfig()
        monkeypatch.setattr(cfg.common, "otel_enabled", False)
        monkeypatch.setattr(cfg.temporal, "api_key", None)
        monkeypatch.setattr(temporal_client, "config", cfg)
        monkeypatch.setattr(temporal_client, "build_client_runtime", lambda: MagicMock())
        monkeypatch.setattr(temporal_client, "get_token_provider", lambda *a: None)
        captured: list[Any] = []

        async def fake_connect(connect_config: Any) -> MagicMock:
            captured.append(connect_config)
            return MagicMock()

        monkeypatch.setattr(temporal_client.TemporalServiceClient, "connect", fake_connect)

        await temporal_client.create_temporal_service_client()

        assert captured[0].rpc_metadata == {_STATIC_HEADER: "static", _FILE_HEADER: "token-v1"}

    @pytest.mark.asyncio
    async def test_startup_read_retries_a_header_file_empty_during_rotation(self, monkeypatch, tmp_path):
        path = tmp_path / "token"
        path.write_text("")
        monkeypatch.setattr(config.worker, "mistral_api_headers", None)
        monkeypatch.setattr(config.worker, "mistral_api_header_files", {_FILE_HEADER: str(path)})
        sleeps = 0

        async def fake_sleep(_seconds: float) -> None:
            nonlocal sleeps
            sleeps += 1
            path.write_text("token-v1")

        monkeypatch.setattr(temporal_client.asyncio, "sleep", fake_sleep)

        assert await temporal_client._read_temporal_rpc_metadata() == {_FILE_HEADER: "token-v1"}
        assert sleeps == 1

    @pytest.mark.asyncio
    async def test_refresh_pushes_rotated_values_once(self, monkeypatch, token_file):
        sleeps = 0

        async def fake_sleep(_seconds: float) -> None:
            nonlocal sleeps
            sleeps += 1
            if sleeps == 2:
                token_file.write_text("token-v2")
            if sleeps == 4:
                raise asyncio.CancelledError

        monkeypatch.setattr(temporal_client.asyncio, "sleep", fake_sleep)
        service_client = MagicMock()

        with pytest.raises(asyncio.CancelledError):
            await temporal_client.refresh_temporal_header_files(service_client)

        pushed = [c.args[0] for c in service_client.update_rpc_metadata.call_args_list]
        assert pushed == [
            {_STATIC_HEADER: "static", _FILE_HEADER: "token-v1"},
            {_STATIC_HEADER: "static", _FILE_HEADER: "token-v2"},
        ]

    @pytest.mark.asyncio
    async def test_refresh_is_a_noop_without_header_files(self, monkeypatch):
        monkeypatch.setattr(config.worker, "mistral_api_header_files", None)
        service_client = MagicMock()

        await temporal_client.refresh_temporal_header_files(service_client)

        service_client.update_rpc_metadata.assert_not_called()
