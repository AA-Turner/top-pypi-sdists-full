from __future__ import annotations

import time
import uuid
from collections import OrderedDict
from collections.abc import Awaitable, Callable
from http import HTTPStatus
from typing import Any, TypeVar

import httpx

from mistralai.workflows.exceptions import ErrorCode, WorkflowsException
from mistralai.workflows.protocol.v2.worker import (
    EVENT_ROUTE_TOKEN_INVALID_CODE,
    EventRouteTokenRequest,
    EventRouteTokenResponse,
)
from mistralai.workflows.worker_client.httpclient import AsyncHttpClient
from mistralai.workflows.worker_client.sdk import PrivateWorkerClient

_T = TypeVar("_T")


class EventRouteUnavailableError(WorkflowsException):
    """The API exposes no v2 event route, so the caller should use v1 instead."""


def build_event_route_exception(
    exc: httpx.HTTPError,
    message: str,
    code: ErrorCode,
) -> WorkflowsException:
    translated = WorkflowsException.from_api_client_error(
        exc,
        message=message,
        code=code,
    )
    if not isinstance(exc, httpx.HTTPStatusError):
        return translated

    try:
        parsed = exc.response.json()
    except ValueError:
        parsed = None
    body = parsed if isinstance(parsed, dict) else None
    body_code = body.get("code") if body is not None else None

    # The v2 routes tag their own 404s with a code, so an untagged one means the route is absent.
    if exc.response.status_code == HTTPStatus.NOT_FOUND and body_code is None:
        return EventRouteUnavailableError(
            message="API does not expose the v2 event route",
            code=translated.code,
            status=translated.status,
            type=translated.type,
        )

    if body is None:
        return translated

    return WorkflowsException(
        message=body.get("detail") or translated.message,
        code=body_code or translated.code,
        status=translated.status,
        type=translated.type,
    )


class EventRouteTokenManager:
    """Caches signed route tokens per workflow run, shared by event publishing and sequences."""

    _CACHE_SIZE = 100
    _REFRESH_MARGIN_SECONDS = 5

    def __init__(self, worker_client: PrivateWorkerClient) -> None:
        async_client = worker_client.sdk_configuration.async_client
        if async_client is None:
            raise ValueError("PrivateWorkerClient must be initialized with an async client")
        self._async_client: AsyncHttpClient = async_client
        self._server_url = worker_client.sdk_configuration.server_url.rstrip("/")
        self._cache: OrderedDict[tuple[str, str], tuple[str, float]] = OrderedDict()

    async def execute_with_token(
        self,
        workflow_exec_id: str,
        workflow_run_id: str,
        operation: Callable[[str], Awaitable[_T]],
        execution_token: str | None = None,
    ) -> _T:
        """Run ``operation`` with a route token, refreshing it once after an expired-token 401.

        Any 401 evicts the cached token. An invalid token is not retried: a freshly minted
        token for the same run would be rejected the same way.
        """
        token = await self.get_token(workflow_exec_id, workflow_run_id, execution_token)
        try:
            return await operation(token)
        except Exception as exc:
            if not _is_unauthorized(exc):
                raise
            self.invalidate(workflow_exec_id, workflow_run_id)
            if _is_invalid_token(exc):
                raise

        refreshed_token = await self.get_token(workflow_exec_id, workflow_run_id, execution_token)
        return await operation(refreshed_token)

    async def get_token(
        self,
        workflow_exec_id: str,
        workflow_run_id: str,
        execution_token: str | None = None,
    ) -> str:
        cached_token = self._get_cached(workflow_exec_id, workflow_run_id)
        if cached_token is not None:
            return cached_token

        request = EventRouteTokenRequest(
            workflow_exec_id=workflow_exec_id,
            workflow_run_id=workflow_run_id,
            execution_token=uuid.UUID(execution_token) if execution_token is not None else None,
        )
        response = await self._post_json(
            "/v2/workflows/workers/event-route-token",
            request.model_dump(mode="json"),
            "Failed to fetch event route token",
            ErrorCode.POST_EVENT_ROUTE_TOKEN_ERROR,
        )
        route_token = EventRouteTokenResponse.model_validate(response)
        self._cache_token(
            workflow_exec_id,
            workflow_run_id,
            route_token.route_token,
            route_token.expires_in_seconds,
        )
        return route_token.route_token

    def invalidate(self, workflow_exec_id: str, workflow_run_id: str) -> None:
        self._cache.pop((workflow_exec_id, workflow_run_id), None)

    async def _post_json(
        self,
        path: str,
        payload: Any,
        message: str,
        code: ErrorCode,
    ) -> Any:
        request = self._async_client.build_request(
            "POST",
            f"{self._server_url}{path}",
            json=payload,
        )
        try:
            response = await self._async_client.send(request, follow_redirects=False)
            response.raise_for_status()
        except httpx.HTTPError as exc:
            raise build_event_route_exception(exc, message, code) from exc
        return response.json()

    def _get_cached(self, workflow_exec_id: str, workflow_run_id: str) -> str | None:
        cache_key = (workflow_exec_id, workflow_run_id)
        cached = self._cache.get(cache_key)
        if cached is None:
            return None
        token, expires_at_monotonic = cached
        if time.monotonic() >= expires_at_monotonic:
            self._cache.pop(cache_key, None)
            return None
        return token

    def _cache_token(
        self,
        workflow_exec_id: str,
        workflow_run_id: str,
        token: str,
        expires_in_seconds: int,
    ) -> None:
        cache_key = (workflow_exec_id, workflow_run_id)
        self._cache.pop(cache_key, None)
        if len(self._cache) >= self._CACHE_SIZE:
            self._cache.popitem(last=False)

        ttl_seconds = max(0, expires_in_seconds - self._REFRESH_MARGIN_SECONDS)
        self._cache[cache_key] = (token, time.monotonic() + ttl_seconds)


def _is_unauthorized(exc: Exception) -> bool:
    if isinstance(exc, WorkflowsException):
        return exc.status == HTTPStatus.UNAUTHORIZED
    return isinstance(exc, httpx.HTTPStatusError) and exc.response.status_code == HTTPStatus.UNAUTHORIZED


def _is_invalid_token(exc: Exception) -> bool:
    return isinstance(exc, WorkflowsException) and exc.code == EVENT_ROUTE_TOKEN_INVALID_CODE
