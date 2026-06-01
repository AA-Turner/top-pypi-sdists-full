import base64
import inspect
import json
import time
from unittest.mock import AsyncMock, patch

import httpx
import pytest

from mistralai.workflows.exceptions import WorkflowError
from mistralai.workflows.hooks.executor_credentials_hook import (
    AsyncExecutorCredentialsHook,
    SyncExecutorCredentialsHook,
)
from mistralai.workflows.models.payload import WorkflowContext
from mistralai.workflows.worker_client.errors import SDKDefaultError
from mistralai.workflows.worker_client.models import ExecutorIdentityTokenResponse
from mistralai.workflows.worker_client.sdk import PrivateWorkerClient

_PATCH_RETRIEVE = "mistralai.workflows.hooks.executor_credentials_hook.retrieve_context"
_HOOK_IMPLS = [AsyncExecutorCredentialsHook, SyncExecutorCredentialsHook]


def _make_jwt(exp: float) -> str:
    header = base64.urlsafe_b64encode(json.dumps({"alg": "HS256"}).encode()).rstrip(b"=").decode()
    payload = base64.urlsafe_b64encode(json.dumps({"exp": exp}).encode()).rstrip(b"=").decode()
    return f"{header}.{payload}.signature"


def _context_with_token(token: str, on_behalf_of: bool = True) -> WorkflowContext:
    return WorkflowContext(namespace="ns", execution_id="exec-1", execution_token=token, on_behalf_of=on_behalf_of)


def _patch_client(jwt: str, hook_cls: type):
    response = ExecutorIdentityTokenResponse(token=jwt)
    if hook_cls is AsyncExecutorCredentialsHook:
        return patch.object(
            PrivateWorkerClient, "executor_identity_token_async", new_callable=AsyncMock, return_value=response
        )
    return patch.object(PrivateWorkerClient, "executor_identity_token", return_value=response)


async def _maybe_await(result):
    if inspect.isawaitable(result):
        return await result
    return result


@pytest.mark.parametrize("hook_cls", _HOOK_IMPLS)
class TestExecutorCredentialsHook:
    @pytest.mark.asyncio
    async def test_sets_authorization_header(self, hook_cls):
        future_exp = time.time() + 120
        jwt = _make_jwt(future_exp)
        hook = hook_cls(server_url="http://localhost", api_key="key")

        request = httpx.Request("GET", "http://example.com")
        with _patch_client(jwt, hook_cls), patch(_PATCH_RETRIEVE, return_value=_context_with_token("tok-A")):
            await _maybe_await(hook(request))

        assert request.headers["Authorization"] == f"Bearer {jwt}"

    @pytest.mark.asyncio
    async def test_caches_jwt_across_calls(self, hook_cls):
        future_exp = time.time() + 120
        jwt = _make_jwt(future_exp)
        hook = hook_cls(server_url="http://localhost", api_key="key")

        with (
            _patch_client(jwt, hook_cls) as mock_method,
            patch(_PATCH_RETRIEVE, return_value=_context_with_token("tok-A")),
        ):
            await _maybe_await(hook(httpx.Request("GET", "http://example.com")))
            await _maybe_await(hook(httpx.Request("GET", "http://example.com")))

        assert mock_method.call_count == 1

    @pytest.mark.asyncio
    async def test_raises_when_no_context(self, hook_cls):
        hook = hook_cls(server_url="http://localhost", api_key="key")
        request = httpx.Request("GET", "http://example.com")

        with patch(_PATCH_RETRIEVE, return_value=None):
            with pytest.raises(WorkflowError, match="execution_token"):
                await _maybe_await(hook(request))

    @pytest.mark.asyncio
    async def test_raises_when_context_has_no_token(self, hook_cls):
        hook = hook_cls(server_url="http://localhost", api_key="key")
        request = httpx.Request("GET", "http://example.com")
        ctx = WorkflowContext(namespace="ns", execution_id="exec-1", execution_token=None)

        with patch(_PATCH_RETRIEVE, return_value=ctx):
            with pytest.raises(WorkflowError, match="execution_token"):
                await _maybe_await(hook(request))

    @pytest.mark.asyncio
    async def test_raises_non_retryable_when_not_on_behalf_of(self, hook_cls):
        hook = hook_cls(server_url="http://localhost", api_key="key")
        request = httpx.Request("GET", "http://example.com")
        ctx = _context_with_token("tok-A", on_behalf_of=False)

        with patch(_PATCH_RETRIEVE, return_value=ctx):
            with pytest.raises(WorkflowError, match="on_behalf_of=True") as exc_info:
                await _maybe_await(hook(request))
            assert exc_info.value.non_retryable

    @pytest.mark.asyncio
    async def test_server_403_raises_non_retryable(self, hook_cls):
        hook = hook_cls(server_url="http://localhost", api_key="key")
        request = httpx.Request("GET", "http://example.com")
        response = httpx.Response(403, text="Workflow is not configured for on-behalf-of execution")
        error = SDKDefaultError("API error occurred", response)

        method_name = (
            "executor_identity_token_async" if hook_cls is AsyncExecutorCredentialsHook else "executor_identity_token"
        )
        mock_kwargs = {"new_callable": AsyncMock} if hook_cls is AsyncExecutorCredentialsHook else {}
        with (
            patch.object(PrivateWorkerClient, method_name, side_effect=error, **mock_kwargs),
            patch(_PATCH_RETRIEVE, return_value=_context_with_token("tok-A")),
        ):
            with pytest.raises(WorkflowError) as exc_info:
                await _maybe_await(hook(request))
            assert exc_info.value.non_retryable
