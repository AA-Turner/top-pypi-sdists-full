import base64
import inspect
import json
import time
from unittest.mock import AsyncMock, patch

import httpx
import pytest

from mistralai.workflows.core.auth import StaticTokenProvider
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


def _make_jwt(claims: dict[str, object]) -> str:
    header = base64.urlsafe_b64encode(json.dumps({"alg": "HS256"}).encode()).rstrip(b"=").decode()
    payload = base64.urlsafe_b64encode(json.dumps(claims).encode()).rstrip(b"=").decode()
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
        jwt = _make_jwt({"exp": future_exp})
        hook = hook_cls(server_url="http://localhost", token_provider=StaticTokenProvider("key"))

        request = httpx.Request("GET", "http://example.com")
        with _patch_client(jwt, hook_cls), patch(_PATCH_RETRIEVE, return_value=_context_with_token("tok-A")):
            await _maybe_await(hook(request))

        assert request.headers["Authorization"] == f"Bearer {jwt}"

    @pytest.mark.asyncio
    async def test_caches_jwt_across_calls(self, hook_cls):
        future_exp = time.time() + 120
        jwt = _make_jwt({"exp": future_exp})
        hook = hook_cls(server_url="http://localhost", token_provider=StaticTokenProvider("key"))

        with (
            _patch_client(jwt, hook_cls) as mock_method,
            patch(_PATCH_RETRIEVE, return_value=_context_with_token("tok-A")),
        ):
            await _maybe_await(hook(httpx.Request("GET", "http://example.com")))
            await _maybe_await(hook(httpx.Request("GET", "http://example.com")))

        assert mock_method.call_count == 1

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "token",
        [
            pytest.param("opaque-token", id="no-segments"),
            pytest.param("not.a.jwt", id="undecodable-segments"),
            pytest.param(_make_jwt({"sub": "user"}), id="no-exp"),
        ],
    )
    async def test_non_jwt_token_raises_non_retryable(self, hook_cls, token):
        hook = hook_cls(server_url="http://localhost", token_provider=StaticTokenProvider("key"))
        request = httpx.Request("GET", "http://example.com")

        with _patch_client(token, hook_cls), patch(_PATCH_RETRIEVE, return_value=_context_with_token("tok-A")):
            with pytest.raises(WorkflowError, match="not a JWT with an 'exp' claim") as exc_info:
                await _maybe_await(hook(request))
            assert exc_info.value.non_retryable
        assert "Authorization" not in request.headers

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "status, detail, message",
        [
            pytest.param(403, "Workflow is not configured for on-behalf-of execution", "API error occurred", id="403"),
            pytest.param(
                400, "Execution is missing user_id or organization_id", "has no user identity", id="400-missing-user"
            ),
            pytest.param(400, "Bad request", "API error occurred", id="400-other"),
        ],
    )
    async def test_server_client_error_raises_non_retryable(self, hook_cls, status, detail, message):
        hook = hook_cls(server_url="http://localhost", token_provider=StaticTokenProvider("key"))
        request = httpx.Request("GET", "http://example.com")
        response = httpx.Response(status, json={"detail": detail})
        error = SDKDefaultError("API error occurred", response)

        method_name = (
            "executor_identity_token_async" if hook_cls is AsyncExecutorCredentialsHook else "executor_identity_token"
        )
        mock_kwargs = {"new_callable": AsyncMock} if hook_cls is AsyncExecutorCredentialsHook else {}
        with (
            patch.object(PrivateWorkerClient, method_name, side_effect=error, **mock_kwargs),
            patch(_PATCH_RETRIEVE, return_value=_context_with_token("tok-A")),
        ):
            with pytest.raises(WorkflowError, match=message) as exc_info:
                await _maybe_await(hook(request))
            assert exc_info.value.non_retryable
