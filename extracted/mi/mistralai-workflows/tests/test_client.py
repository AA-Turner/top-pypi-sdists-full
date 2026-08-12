import base64
import inspect
import json
import time
from unittest.mock import AsyncMock, patch

import httpx
import pytest
import temporalio.activity
from pydantic import SecretStr

from mistralai.workflows._version import __version__
from mistralai.workflows.client import _get_async_client, _get_sync_client, should_use_executor_credentials
from mistralai.workflows.core.auth import StaticTokenProvider
from mistralai.workflows.core.config.config import config
from mistralai.workflows.core.temporal.context_handler_interceptor import define_context
from mistralai.workflows.core.worker_client import get_worker_client
from mistralai.workflows.exceptions import WorkflowError
from mistralai.workflows.hooks.executor_credentials_hook import (
    AsyncExecutorCredentialsHook,
    SyncExecutorCredentialsHook,
)
from mistralai.workflows.hooks.metadata_hook import (
    inject_metadata,
    inject_metadata_async,
)
from mistralai.workflows.hooks.token_provider_hook import (
    AsyncTokenProviderHook,
    TokenProviderHook,
)
from mistralai.workflows.models.payload import WorkflowContext
from mistralai.workflows.worker_client.models import ExecutorIdentityTokenResponse
from mistralai.workflows.worker_client.sdk import PrivateWorkerClient

_CLIENT_FACTORIES = [
    pytest.param(_get_async_client, AsyncExecutorCredentialsHook, id="async"),
    pytest.param(_get_sync_client, SyncExecutorCredentialsHook, id="sync"),
]


@pytest.mark.parametrize("get_client", [_get_async_client, _get_sync_client])
class TestClientUserAgent:
    def test_default_user_agent_is_sent(self, get_client):
        client = get_client(token_provider=StaticTokenProvider("test-key"))
        assert client.headers["user-agent"] == f"mistral-client-python/workflows-worker/{__version__}"

    def test_custom_user_agent_is_preserved(self, get_client):
        client = get_client(token_provider=StaticTokenProvider("test-key"), headers={"User-Agent": "custom-agent/1.0"})
        assert client.headers["user-agent"] == "custom-agent/1.0"

    def test_custom_user_agent_case_insensitive(self, get_client):
        client = get_client(token_provider=StaticTokenProvider("test-key"), headers={"user-agent": "custom-agent/2.0"})
        assert client.headers["user-agent"] == "custom-agent/2.0"


@pytest.mark.parametrize("get_client,expected_hook_cls", _CLIENT_FACTORIES)
class TestExecutorCredentials:
    def test_client_created_without_activity_context(self, get_client, expected_hook_cls):
        client = get_client(
            token_provider=StaticTokenProvider("test-key"),
            server_url="http://localhost",
            use_executor_credentials=True,
        )
        hooks = client.event_hooks.get("request", [])
        assert any(isinstance(h, expected_hook_cls) for h in hooks)

    def test_raises_without_server_url(self, get_client, expected_hook_cls):
        with pytest.raises(WorkflowError, match="server_url"):
            get_client(token_provider=StaticTokenProvider("test-key"), use_executor_credentials=True)

    def test_raises_without_token_provider(self, get_client, expected_hook_cls, monkeypatch):
        # No explicit provider and no configured credential → nothing to resolve, so the hook setup fails.
        monkeypatch.setattr(config.common, "mistral_api_key", None)
        monkeypatch.setattr(config.common, "mistral_sa_token_path", None)
        with pytest.raises(WorkflowError, match="token_provider"):
            get_client(server_url="http://localhost", use_executor_credentials=True)


@pytest.mark.parametrize(
    "get_client,expected_hook_cls",
    [
        pytest.param(_get_async_client, AsyncTokenProviderHook, id="async"),
        pytest.param(_get_sync_client, TokenProviderHook, id="sync"),
    ],
)
class TestImplicitProviderResolution:
    """A client attaches the auth hook whenever a credential is resolvable from config (no explicit
    token_provider/api_key), so service-account auth works transparently."""

    def test_attaches_auth_hook_from_sa_token(self, monkeypatch, tmp_path, get_client, expected_hook_cls):
        monkeypatch.setattr(config.common, "mistral_sa_token_path", str(tmp_path / "token"))
        monkeypatch.setattr(config.common, "mistral_api_key", None)
        hooks = get_client().event_hooks.get("request", [])
        assert any(isinstance(h, expected_hook_cls) for h in hooks)

    def test_attaches_auth_hook_from_config_api_key(self, monkeypatch, get_client, expected_hook_cls):
        monkeypatch.setattr(config.common, "mistral_sa_token_path", None)
        monkeypatch.setattr(config.common, "mistral_api_key", SecretStr("config-key"))
        hooks = get_client().event_hooks.get("request", [])
        assert any(isinstance(h, expected_hook_cls) for h in hooks)

    def test_no_auth_hook_when_no_credentials_configured(self, monkeypatch, get_client, expected_hook_cls):
        monkeypatch.setattr(config.common, "mistral_sa_token_path", None)
        monkeypatch.setattr(config.common, "mistral_api_key", None)
        hooks = get_client().event_hooks.get("request", [])
        assert not any(isinstance(h, expected_hook_cls) for h in hooks)


class TestSdkClientUserAgent:
    @pytest.mark.asyncio
    async def test_sdk_client_appends_mistral_user_agent(self, monkeypatch):
        """Verify SDK requests include the Mistral user-agent appended to the Speakeasy one."""
        captured_headers = {}

        async def capture_request(request: httpx.Request) -> httpx.Response:
            captured_headers.update(request.headers)
            return httpx.Response(
                200,
                json={
                    "worker_id": "x",
                    "executor_id": "y",
                    "deployment_name": "z",
                    "scheduler_url": "http://scheduler",
                    "namespace": "ns",
                },
            )

        client = get_worker_client(base_url="http://localhost", api_key="test-key")
        monkeypatch.setattr(
            client.sdk_configuration.async_client,
            "_transport",
            httpx.MockTransport(capture_request),
        )

        async with client:
            await client.whoami_async()

        ua = captured_headers.get("user-agent", "")
        assert f"mistral-client-python/workflows-worker/{__version__}" in ua
        assert "speakeasy-sdk" in ua

    @pytest.mark.asyncio
    async def test_sdk_client_mistral_user_agent_is_last_token(self, monkeypatch):
        """Verify the Mistral UA is appended after the Speakeasy one."""
        captured_headers = {}

        async def capture_request(request: httpx.Request) -> httpx.Response:
            captured_headers.update(request.headers)
            return httpx.Response(
                200,
                json={
                    "worker_id": "x",
                    "executor_id": "y",
                    "deployment_name": "z",
                    "scheduler_url": "http://scheduler",
                    "namespace": "ns",
                },
            )

        client = get_worker_client(base_url="http://localhost", api_key="test-key")
        monkeypatch.setattr(
            client.sdk_configuration.async_client,
            "_transport",
            httpx.MockTransport(capture_request),
        )

        async with client:
            await client.whoami_async()

        ua = captured_headers.get("user-agent", "")
        mistral_part = f"mistral-client-python/workflows-worker/{__version__}"
        assert ua.endswith(mistral_part), f"Mistral UA should be last in: {ua!r}"


_PATCH_RESOLVE_CONTEXT = "mistralai.workflows.client.retrieve_context"


class TestShouldUseExecutorCredentials:
    def test_true_when_on_behalf_of(self):
        ctx = WorkflowContext(namespace="ns", execution_id="exec-1", on_behalf_of=True)
        with patch(_PATCH_RESOLVE_CONTEXT, return_value=ctx):
            assert should_use_executor_credentials() is True

    def test_false_when_not_on_behalf_of(self):
        ctx = WorkflowContext(namespace="ns", execution_id="exec-1", on_behalf_of=False)
        with patch(_PATCH_RESOLVE_CONTEXT, return_value=ctx):
            assert should_use_executor_credentials() is False

    def test_false_when_on_behalf_of_none(self):
        ctx = WorkflowContext(namespace="ns", execution_id="exec-1", on_behalf_of=None)
        with patch(_PATCH_RESOLVE_CONTEXT, return_value=ctx):
            assert should_use_executor_credentials() is False

    def test_false_when_no_context(self):
        with patch(_PATCH_RESOLVE_CONTEXT, return_value=None):
            assert should_use_executor_credentials() is False


_METADATA_HOOK_FACTORIES = [
    pytest.param(_get_async_client, inject_metadata_async, id="async"),
    pytest.param(_get_sync_client, inject_metadata, id="sync"),
]

_PATCH_RETRIEVE = "mistralai.workflows.hooks.metadata_hook.retrieve_context"


async def _maybe_await(result):
    if inspect.isawaitable(result):
        return await result
    return result


@pytest.mark.parametrize("get_client,expected_hook", _METADATA_HOOK_FACTORIES)
class TestMetadataHeader:
    def test_metadata_hook_registered_in_event_hooks(self, get_client, expected_hook):
        client = get_client(token_provider=StaticTokenProvider("test-key"))
        hooks = client.event_hooks.get("request", [])
        assert expected_hook in hooks

    @pytest.mark.asyncio
    async def test_sets_call_type_always(self, get_client, expected_hook):
        request = httpx.Request("GET", "http://example.com")
        with patch(_PATCH_RETRIEVE, return_value=None):
            await _maybe_await(expected_hook(request))

        metadata = json.loads(request.headers["x-metadata"])
        assert metadata["call_type"] == "workflows"

    @pytest.mark.asyncio
    async def test_no_execution_id_outside_activity_context(self, get_client, expected_hook):
        request = httpx.Request("GET", "http://example.com")
        with patch(_PATCH_RETRIEVE, return_value=None):
            await _maybe_await(expected_hook(request))

        metadata = json.loads(request.headers["x-metadata"])
        assert "execution_id" not in metadata

    @pytest.mark.asyncio
    async def test_sets_execution_id_inside_activity_context(self, get_client, expected_hook):
        ctx = WorkflowContext(namespace="ns", execution_id="exec-abc-123")
        request = httpx.Request("GET", "http://example.com")
        with patch(_PATCH_RETRIEVE, return_value=ctx):
            await _maybe_await(expected_hook(request))

        metadata = json.loads(request.headers["x-metadata"])
        assert metadata["execution_id"] == "exec-abc-123"
        assert metadata["call_type"] == "workflows"

    @pytest.mark.asyncio
    async def test_sets_activity_metadata_inside_activity_context(self, get_client, expected_hook):
        request = httpx.Request("GET", "http://example.com")
        activity_info = type(
            "ActivityInfo",
            (),
            {"workflow_id": "exec-abc-123", "workflow_run_id": "run-1", "activity_id": "task-1", "attempt": 2},
        )()
        with (
            patch.object(temporalio.activity, "in_activity", return_value=True),
            patch.object(temporalio.activity, "info", return_value=activity_info),
        ):
            await _maybe_await(expected_hook(request))

        metadata = json.loads(request.headers["x-metadata"])
        assert metadata == {
            "call_type": "workflows",
            "execution_id": "exec-abc-123",
            "run_id": "run-1",
            "task_id": "task-1",
            "attempt": "2",
        }


_WORKER_KEY = "worker-api-key"


def _make_jwt(exp: float) -> str:
    header = base64.urlsafe_b64encode(json.dumps({"alg": "HS256"}).encode()).rstrip(b"=").decode()
    payload = base64.urlsafe_b64encode(json.dumps({"exp": exp}).encode()).rstrip(b"=").decode()
    return f"{header}.{payload}.signature"


def _patch_executor_token(jwt: str, hook_cls: type):
    response = ExecutorIdentityTokenResponse(token=jwt)
    if hook_cls is AsyncExecutorCredentialsHook:
        return patch.object(
            PrivateWorkerClient, "executor_identity_token_async", new_callable=AsyncMock, return_value=response
        )
    return patch.object(PrivateWorkerClient, "executor_identity_token", return_value=response)


@pytest.mark.parametrize("get_client,expected_hook_cls", _CLIENT_FACTORIES)
class TestOboVsNonOboCredentials:
    """A connector call made from an OBO workflow is authenticated as the executor
    (a per-execution JWT), while the same call from a non-OBO workflow is
    authenticated as the worker (its static API key).
    """

    @staticmethod
    async def _run_request_hooks(client, request: httpx.Request) -> None:
        for hook in client.event_hooks.get("request", []):
            await _maybe_await(hook(request))

    @staticmethod
    def _request() -> httpx.Request:
        return httpx.Request(
            "GET", "http://localhost/v1/connectors", headers={"Authorization": f"Bearer {_WORKER_KEY}"}
        )

    @pytest.mark.asyncio
    async def test_obo_request_uses_executor_jwt(self, get_client, expected_hook_cls):
        jwt = _make_jwt(time.time() + 120)
        obo_ctx = WorkflowContext(namespace="ns", execution_id="exec-1", execution_token="tok", on_behalf_of=True)
        request = self._request()
        with define_context(obo_ctx):
            client = get_client(
                token_provider=StaticTokenProvider(_WORKER_KEY),
                server_url="http://localhost",
                use_executor_credentials=should_use_executor_credentials(),
            )
            assert any(isinstance(h, expected_hook_cls) for h in client.event_hooks["request"])
            with _patch_executor_token(jwt, expected_hook_cls):
                await self._run_request_hooks(client, request)

        assert request.headers["Authorization"] == f"Bearer {jwt}"

    @pytest.mark.asyncio
    async def test_non_obo_request_uses_worker_key(self, get_client, expected_hook_cls):
        non_obo_ctx = WorkflowContext(namespace="ns", execution_id="exec-1", on_behalf_of=False)
        request = self._request()
        with define_context(non_obo_ctx):
            client = get_client(
                token_provider=StaticTokenProvider(_WORKER_KEY),
                server_url="http://localhost",
                use_executor_credentials=should_use_executor_credentials(),
            )
            assert not any(isinstance(h, expected_hook_cls) for h in client.event_hooks["request"])
            await self._run_request_hooks(client, request)

        assert request.headers["Authorization"] == f"Bearer {_WORKER_KEY}"
