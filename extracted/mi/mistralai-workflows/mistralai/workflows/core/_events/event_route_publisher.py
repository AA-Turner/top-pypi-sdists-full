from __future__ import annotations

import asyncio
import time
import uuid
from collections import OrderedDict
from http import HTTPStatus
from typing import TYPE_CHECKING, Any

import httpx

from mistralai.workflows.core._events.event_encoder import maybe_encode_event
from mistralai.workflows.core.config.config import EventsApiVersion
from mistralai.workflows.core.temporal.context_handler_interceptor import retrieve_context

if TYPE_CHECKING:
    from mistralai.workflows.core._events.event_encoder import EventPayloadEncoder
from mistralai.workflows.exceptions import ErrorCode, WorkflowsException
from mistralai.workflows.protocol.v1.events import WorkflowEvent
from mistralai.workflows.protocol.v2.worker import (
    EVENT_ROUTE_TOKEN_EXPIRED_CODE,
    EVENT_ROUTE_TOKEN_HEADER,
    EVENT_ROUTE_TOKEN_INVALID_CODE,
    EventRouteTokenRequest,
    EventRouteTokenResponse,
)
from mistralai.workflows.worker_client.httpclient import AsyncHttpClient
from mistralai.workflows.worker_client.sdk import PrivateWorkerClient


def _build_event_route_exception(
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
        body = exc.response.json()
    except ValueError:
        return translated

    if not isinstance(body, dict):
        return translated

    return WorkflowsException(
        message=body.get("detail") or translated.message,
        code=body.get("code") or translated.code,
        status=translated.status,
        type=translated.type,
    )


class EventRoutePublisher:
    _EVENT_ROUTE_TOKEN_CACHE_SIZE = 100
    _EVENT_ROUTE_TOKEN_REFRESH_MARGIN_SECONDS = 5

    def __init__(
        self,
        worker_client: PrivateWorkerClient,
        events_api_version: str = "v1",
        event_encoder: EventPayloadEncoder | None = None,
    ) -> None:
        self._events_api_version = events_api_version
        async_client = worker_client.sdk_configuration.async_client
        if async_client is None:
            raise ValueError("PrivateWorkerClient must be initialized with an async client")
        self._async_client: AsyncHttpClient = async_client
        self._server_url = worker_client.sdk_configuration.server_url.rstrip("/")
        self._event_route_token_cache: OrderedDict[tuple[str, str], tuple[str, float]] = OrderedDict()
        self._event_encoder = event_encoder

    async def try_publish_via_v2(
        self,
        events: list[WorkflowEvent],
        already_encoded: bool = False,
    ) -> bool:
        """Publish events via v2 event route.

        Returns True if published via v2, False if v2 is not the route (caller uses v1).
        Raises WorkflowsException if a v2 publish is attempted and fails.
        """
        if not events:
            return False

        if self._events_api_version not in (EventsApiVersion.V2, EventsApiVersion.V2_ONLY):
            return False

        first_event = events[0]
        first_scope = (first_event.workflow_exec_id, first_event.workflow_run_id)
        if any((event.workflow_exec_id, event.workflow_run_id) != first_scope for event in events):
            raise WorkflowsException(
                message="v2 event route does not support mixed-scope batches",
                code=ErrorCode.INVALID_ARGUMENTS_ERROR,
                status=HTTPStatus.BAD_REQUEST,
            )

        # Backward compat ONLY: send the execution_token when we have one (entrypoint/activity
        # events) so older APIs that still require it can mint. Remove this token-send as soon as
        # the minimum supported API mints by run identity — handler/reset events already rely on
        # that, and the API no longer needs the token (it has workflow_exec_id/run_id).
        workflow_context = retrieve_context()
        execution_token = workflow_context.execution_token if workflow_context is not None else None

        if not already_encoded:
            events = list(await asyncio.gather(*[maybe_encode_event(event, self._event_encoder) for event in events]))

        try:
            await self._publish_events_v2(events, execution_token)
        except WorkflowsException as exc:
            # An API without run-identity minting rejects a token-less request with 422;
            # fall back to v1 for those (handler/reset) paths instead of dropping the event.
            if execution_token is None and exc.status == HTTPStatus.UNPROCESSABLE_ENTITY:
                return False
            raise
        return True

    # TODO: Replace with generated Speakeasy client methods once v2 event endpoints are published.
    async def _post_json(
        self,
        path: str,
        payload: Any,
        message: str,
        code: ErrorCode,
        route_token: str | None = None,
    ) -> Any:
        headers = {EVENT_ROUTE_TOKEN_HEADER: route_token} if route_token is not None else None
        request = self._async_client.build_request(
            "POST",
            f"{self._server_url}{path}",
            json=payload,
            headers=headers,
        )

        try:
            response = await self._async_client.send(request, follow_redirects=False)
            response.raise_for_status()
        except httpx.HTTPError as exc:
            raise _build_event_route_exception(exc, message, code) from exc

        return response.json()

    def _get_cached_event_route_token(self, workflow_exec_id: str, workflow_run_id: str) -> str | None:
        cached = self._event_route_token_cache.get((workflow_exec_id, workflow_run_id))
        if cached is None:
            return None
        route_token, expires_at_monotonic = cached
        if time.monotonic() >= expires_at_monotonic:
            self._event_route_token_cache.pop((workflow_exec_id, workflow_run_id), None)
            return None
        return route_token

    def _cache_event_route_token(
        self,
        workflow_exec_id: str,
        workflow_run_id: str,
        route_token: str,
        expires_in_seconds: int,
    ) -> None:
        cache_key = (workflow_exec_id, workflow_run_id)
        self._event_route_token_cache.pop(cache_key, None)
        if len(self._event_route_token_cache) >= self._EVENT_ROUTE_TOKEN_CACHE_SIZE:
            self._event_route_token_cache.popitem(last=False)

        ttl_seconds = max(0, expires_in_seconds - self._EVENT_ROUTE_TOKEN_REFRESH_MARGIN_SECONDS)
        self._event_route_token_cache[cache_key] = (route_token, time.monotonic() + ttl_seconds)

    def _invalidate_event_route_token(self, workflow_exec_id: str, workflow_run_id: str) -> None:
        self._event_route_token_cache.pop((workflow_exec_id, workflow_run_id), None)

    async def _get_route_token(
        self,
        workflow_exec_id: str,
        workflow_run_id: str,
        execution_token: str | None = None,
    ) -> str:
        cached_token = self._get_cached_event_route_token(workflow_exec_id, workflow_run_id)
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
        self._cache_event_route_token(
            workflow_exec_id,
            workflow_run_id,
            route_token.route_token,
            route_token.expires_in_seconds,
        )
        return route_token.route_token

    async def _send_events_with_token(self, events: list[WorkflowEvent], route_token: str) -> None:
        if len(events) == 1:
            await self._post_json(
                "/v2/workflows/events",
                {"event": events[0].model_dump(mode="json")},
                "Failed to send workflow event",
                ErrorCode.POST_EVENTS_ERROR,
                route_token,
            )
            return

        await self._post_json(
            "/v2/workflows/events/batch",
            {"events": [event.model_dump(mode="json") for event in events]},
            "Failed to send workflow event batch",
            ErrorCode.POST_EVENTS_ERROR,
            route_token,
        )

    async def _publish_events_v2(self, events: list[WorkflowEvent], execution_token: str | None = None) -> None:
        first_event = events[0]
        route_token = await self._get_route_token(
            first_event.workflow_exec_id,
            first_event.workflow_run_id,
            execution_token,
        )

        try:
            await self._send_events_with_token(events, route_token)
        except WorkflowsException as exc:
            is_expired = exc.status == HTTPStatus.UNAUTHORIZED and exc.code == EVENT_ROUTE_TOKEN_EXPIRED_CODE
            is_invalid = exc.status == HTTPStatus.UNAUTHORIZED and exc.code == EVENT_ROUTE_TOKEN_INVALID_CODE
            # Unknown token errors are not recoverable here; let the caller handle them.
            if not (is_expired or is_invalid):
                raise

            # Expired and invalid tokens must both be evicted from the cache.
            self._invalidate_event_route_token(first_event.workflow_exec_id, first_event.workflow_run_id)
            # Invalid tokens cannot be recovered with a retry.
            if is_invalid:
                raise

            # Expired tokens can be refreshed once before surfacing the error.
            refreshed_route_token = await self._get_route_token(
                first_event.workflow_exec_id,
                first_event.workflow_run_id,
                execution_token,
            )
            await self._send_events_with_token(events, refreshed_route_token)
