from __future__ import annotations

import abc
import base64
import json
import time
from typing import OrderedDict

import httpx
import structlog

from mistralai.workflows._version import USER_AGENT
from mistralai.workflows.core.config.config import config
from mistralai.workflows.core.temporal.context_handler_interceptor import retrieve_context
from mistralai.workflows.exceptions import WorkflowError
from mistralai.workflows.worker_client.errors import SDKError
from mistralai.workflows.worker_client.sdk import PrivateWorkerClient

logger = structlog.get_logger(__name__)


class ExecutorCredentialsHook(abc.ABC):
    """httpx before-request hook that replaces the worker's API key with a short-lived
    JWT representing the workflow executor's identity, ensuring downstream services
    authenticate requests against the executor's credentials rather than the worker's.
    """

    _REFRESH_MARGIN_SECONDS = 30
    _JWT_CACHE_SIZE = 100

    def __init__(self, server_url: str, api_key: str) -> None:
        self._server_url = server_url.rstrip("/")
        self._api_key = api_key
        # execution_token -> (jwt, expiration_timestamp)
        self._jwt_cache: OrderedDict[str, tuple[str, float]] = OrderedDict()

    @staticmethod
    def _decode_jwt_exp(token: str) -> float:
        payload_segment = token.split(".")[1]
        padded = payload_segment + "=" * (-len(payload_segment) % 4)
        payload = json.loads(base64.urlsafe_b64decode(padded))
        return float(payload["exp"])

    def _is_jwt_cached_for(self, execution_token: str) -> bool:
        jwt_with_exp = self._jwt_cache.get(execution_token)
        if not jwt_with_exp:
            return False
        _, exp = jwt_with_exp
        if (exp - time.time()) >= self._REFRESH_MARGIN_SECONDS:
            return True
        del self._jwt_cache[execution_token]
        return False

    @staticmethod
    def _resolve_execution_token() -> str:
        context = retrieve_context()
        if not context or not context.execution_token:
            raise WorkflowError(
                "use_executor_credentials requires an execution_token but no workflow context is available; "
                "ensure the call is made from within an activity or workflow execution",
                non_retryable=True,
            )
        if not context.on_behalf_of:
            raise WorkflowError(
                "use_executor_credentials requires on_behalf_of=True on the @workflow.define decorator",
                non_retryable=True,
            )
        return context.execution_token

    @property
    def _client_headers(self) -> dict[str, str]:
        return {
            **(config.worker.mistral_api_headers or {}),
            "User-Agent": USER_AGENT,
            "Authorization": f"Bearer {self._api_key}",
        }

    def _cache_jwt(self, jwt: str, execution_token: str) -> str:
        if len(self._jwt_cache) >= self._JWT_CACHE_SIZE:
            self._jwt_cache.popitem(last=False)  # FIFO eviction: drop oldest entry
        jwt_expiration_timestamp = self._decode_jwt_exp(jwt)
        self._jwt_cache[execution_token] = (jwt, jwt_expiration_timestamp)
        logger.debug(
            "identity JWT fetched and cached",
            expires_in=f"{jwt_expiration_timestamp - time.time():.2f}s",
            expires_at=jwt_expiration_timestamp,
        )
        return jwt


class AsyncExecutorCredentialsHook(ExecutorCredentialsHook):
    """Async httpx event hook for executor credential injection."""

    def __init__(self, server_url: str, api_key: str) -> None:
        super().__init__(server_url, api_key)
        self._worker_client = PrivateWorkerClient(
            server_url=self._server_url,
            async_client=httpx.AsyncClient(
                verify=config.common.ca_bundle or True,
                headers=self._client_headers,
            ),
        )

    async def _fetch_jwt(self) -> str:
        execution_token = self._resolve_execution_token()
        if self._is_jwt_cached_for(execution_token):
            jwt = self._jwt_cache[execution_token][0]
            assert jwt
            return jwt

        try:
            response = await self._worker_client.executor_identity_token_async(execution_token=execution_token)
        except SDKError as exc:
            if exc.status_code == 403:
                raise WorkflowError(str(exc), non_retryable=True) from exc
            raise
        return self._cache_jwt(response.token, execution_token)

    async def __call__(self, request: httpx.Request) -> None:
        jwt = await self._fetch_jwt()
        request.headers["Authorization"] = f"Bearer {jwt}"


class SyncExecutorCredentialsHook(ExecutorCredentialsHook):
    """Sync httpx event hook for executor credential injection."""

    def __init__(self, server_url: str, api_key: str) -> None:
        super().__init__(server_url, api_key)
        self._worker_client = PrivateWorkerClient(
            server_url=self._server_url,
            client=httpx.Client(
                verify=config.common.ca_bundle or True,
                headers=self._client_headers,
            ),
        )

    def _fetch_jwt(self) -> str:
        execution_token = self._resolve_execution_token()
        if self._is_jwt_cached_for(execution_token):
            jwt = self._jwt_cache[execution_token][0]
            assert jwt
            return jwt

        try:
            response = self._worker_client.executor_identity_token(execution_token=execution_token)
        except SDKError as exc:
            if exc.status_code == 403:
                raise WorkflowError(str(exc), non_retryable=True) from exc
            raise
        return self._cache_jwt(response.token, execution_token)

    def __call__(self, request: httpx.Request) -> None:
        jwt = self._fetch_jwt()
        request.headers["Authorization"] = f"Bearer {jwt}"
