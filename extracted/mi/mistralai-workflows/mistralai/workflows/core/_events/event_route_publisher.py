from __future__ import annotations

import asyncio
from http import HTTPStatus
from typing import TYPE_CHECKING, Any

import httpx

from mistralai.workflows.core._events.event_encoder import maybe_encode_event
from mistralai.workflows.core._events.event_route_token_manager import (
    EventRouteTokenManager,
    EventRouteUnavailableError,
    build_event_route_exception,
)
from mistralai.workflows.core.config.config import EventsApiVersion
from mistralai.workflows.core.metrics import EventRouteFallbackReason, record_event_route_v1_fallback
from mistralai.workflows.core.temporal.context_handler_interceptor import retrieve_context

if TYPE_CHECKING:
    from mistralai.workflows.core._events.event_encoder import EventPayloadEncoder
from mistralai.workflows.exceptions import ErrorCode, WorkflowsException
from mistralai.workflows.protocol.v1.events import WorkflowEvent
from mistralai.workflows.protocol.v2.worker import EVENT_ROUTE_TOKEN_HEADER
from mistralai.workflows.worker_client.httpclient import AsyncHttpClient
from mistralai.workflows.worker_client.sdk import PrivateWorkerClient


class EventRoutePublisher:
    """Publishes workflow events to Abraxas over the v2 event route, using a shared route-token cache."""

    def __init__(
        self,
        worker_client: PrivateWorkerClient,
        events_api_version: EventsApiVersion,
        event_encoder: EventPayloadEncoder | None = None,
        route_token_manager: EventRouteTokenManager | None = None,
    ) -> None:
        self._events_api_version = events_api_version
        async_client = worker_client.sdk_configuration.async_client
        if async_client is None:
            raise ValueError("PrivateWorkerClient must be initialized with an async client")
        self._async_client: AsyncHttpClient = async_client
        self._server_url = worker_client.sdk_configuration.server_url.rstrip("/")
        self._route_token_manager = route_token_manager or EventRouteTokenManager(worker_client)
        self._event_encoder = event_encoder

    @property
    def route_token_manager(self) -> EventRouteTokenManager:
        return self._route_token_manager

    def _fall_back_to_v1(self, reason: EventRouteFallbackReason) -> bool:
        # v2-only raises upstream rather than using v1, so that is not a fallback worth counting.
        if self._events_api_version != EventsApiVersion.V2_ONLY:
            record_event_route_v1_fallback(reason)
        return False

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
        except EventRouteUnavailableError:
            return self._fall_back_to_v1(EventRouteFallbackReason.ROUTE_UNAVAILABLE)
        except WorkflowsException as exc:
            # The route exists but its token service is off (Abraxas or Albe), so v2 cannot work here.
            if exc.status == HTTPStatus.SERVICE_UNAVAILABLE:
                return self._fall_back_to_v1(EventRouteFallbackReason.TOKEN_SERVICE_UNAVAILABLE)
            # An API without run-identity minting rejects a token-less request with 422;
            # fall back to v1 for those (handler/reset) paths instead of dropping the event.
            if execution_token is None and exc.status == HTTPStatus.UNPROCESSABLE_ENTITY:
                return self._fall_back_to_v1(EventRouteFallbackReason.TOKEN_REQUIRED)
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
            raise build_event_route_exception(exc, message, code) from exc

        return response.json()

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
        await self._route_token_manager.execute_with_token(
            first_event.workflow_exec_id,
            first_event.workflow_run_id,
            lambda route_token: self._send_events_with_token(events, route_token),
            execution_token,
        )
