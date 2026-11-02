import asyncio
import contextlib
from dataclasses import dataclass
from typing import Literal, NotRequired, Self, TypedDict
from urllib.parse import urljoin

import httpx

from mistralai.vibe.sdk.observability import atrack, attributes_from_context, is_otel_enabled
from mistralai.vibe_agents import __version__
from mistralai.vibe_agents.user_agent import USER_AGENT
from mistralai.workflows.core.auth import get_token_provider

from ..app.config import get_app_settings

_CONTEXT_PROPERTY_KEYS = (
    "application_id",
    "parent_session_id",
    "repo_id",
    "project_id",
    "organization_id",
    "conversation_id",
)
_ENVELOPE_CONTEXT_KEYS = ("correlation_id", "customer_id", "workspace_id", "user_id")
_DATALAKE_EVENTS_PATH = "/v1/datalake/events"
_DELIVERY_TIMEOUT_SECONDS = 5.0
# The CLI exits right after a failed registration, so the event is awaited, but never for long.
_REGISTRATION_FAILURE_DELIVERY_TIMEOUT_SECONDS = 2.0
# Usage events are queued behind the model call that produced them. Past this many waiting, the
# datalake is not keeping up, and a further event is dropped rather than held in memory.
_MAX_QUEUED_USAGE_EVENTS = 256
# Enough to keep up with a busy worker's model calls over one shared connection pool.
_USAGE_DELIVERY_CONSUMERS = 4
_USAGE_DRAIN_TIMEOUT_SECONDS = 5.0

type _TelemetryEventName = Literal[
    "agents.session_started",
    "agents.agent_registration.done",
    "agents.completion.done",
]
type CompletionStatus = Literal["success", "error", "cancelled"]
type WorkerHosting = Literal["self_hosted", "managed"]
type RegistrationErrorType = Literal[
    "conflict",
    "invalid_request",
    "server_error",
    "http_error",
    "network_error",
    "unknown_error",
]


class _DatalakeEventPayload(TypedDict):
    event: _TelemetryEventName
    properties: dict[str, str | int]
    correlation_id: NotRequired[str]


@dataclass(frozen=True, slots=True)
class _TelemetryEvent:
    name: _TelemetryEventName
    properties: dict[str, str | int]
    correlation_id: str | None = None
    customer_id: str | None = None
    workspace_id: str | None = None
    user_id: str | None = None

    @classmethod
    def session_started(cls, session_id: str, agent_name: str) -> Self:
        raw_context = attributes_from_context(*_CONTEXT_PROPERTY_KEYS, *_ENVELOPE_CONTEXT_KEYS)
        context = {key: value for key, value in raw_context.items() if isinstance(value, str)}
        return cls(
            name="agents.session_started",
            properties={
                **{key: context[key] for key in _CONTEXT_PROPERTY_KEYS if key in context},
                "session_id": session_id,
                "agent_name": agent_name,
                "session_mode": "local",
                "sdk_version": __version__,
            },
            correlation_id=context.get("correlation_id"),
            customer_id=context.get("customer_id"),
            workspace_id=context.get("workspace_id"),
            user_id=context.get("user_id"),
        )


@dataclass(frozen=True, slots=True, kw_only=True)
class CompletionDone:
    """One model attempt of a deployed Session and the tokens it consumed.

    The source of truth for per-Session token usage, but not for billing: the tokens are what the
    Harness measured, and a lost or dropped event is never retried. Billing reads the gateway's
    ``quota.request_done``.
    """

    session_id: str
    parent_session_id: str | None
    agent_id: str | None
    turn_id: str | None
    action_id: str
    model: str
    provider: str
    purpose: str
    call_type: str
    status: CompletionStatus
    error_type: str | None
    duration_ms: int
    input_tokens: int
    output_tokens: int
    cache_read_tokens: int
    cache_write_tokens: int
    reasoning_tokens: int
    # None when the provider did not report a total; readers sum the parts instead of trusting a guess.
    total_tokens: int | None
    correlation_id: str | None
    customer_id: str | None
    workspace_id: str | None
    user_id: str | None

    def to_event(self) -> _TelemetryEvent:
        optional: dict[str, str | int | None] = {
            "parent_session_id": self.parent_session_id,
            "agent_id": self.agent_id,
            "turn_id": self.turn_id,
            "error_type": self.error_type,
            "total_tokens": self.total_tokens,
        }
        properties: dict[str, str | int] = {
            "session_id": self.session_id,
            "action_id": self.action_id,
            "model": self.model,
            "provider": self.provider,
            "purpose": self.purpose,
            "call_type": self.call_type,
            "status": self.status,
            "duration_ms": self.duration_ms,
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
            "cache_read_tokens": self.cache_read_tokens,
            "cache_write_tokens": self.cache_write_tokens,
            "reasoning_tokens": self.reasoning_tokens,
            "sdk_version": __version__,
            **{key: value for key, value in optional.items() if value is not None},
        }
        return _TelemetryEvent(
            name="agents.completion.done",
            properties=properties,
            correlation_id=self.correlation_id,
            customer_id=self.customer_id,
            workspace_id=self.workspace_id,
            user_id=self.user_id,
        )


def _get_mistral_bearer_token() -> str | None:
    try:
        provider = get_token_provider()
        if provider is None:
            return None
        return provider.get_token().strip() or None
    except Exception:
        return None


async def _track(event: _TelemetryEvent) -> None:
    await atrack(
        event.name,
        correlation_id=event.correlation_id,
        customer_uuid=event.customer_id,
        workspace_uuid=event.workspace_id,
        user_uuid=event.user_id,
        properties=event.properties,
    )


async def _post(
    *,
    server_url: str,
    bearer_token: str,
    event: _TelemetryEvent,
    client: httpx.AsyncClient | None = None,
) -> None:
    http_properties = event.properties.copy()
    if event.customer_id is not None:
        http_properties["customer_id"] = event.customer_id
    payload = _DatalakeEventPayload(event=event.name, properties=http_properties)
    if event.correlation_id is not None:
        payload["correlation_id"] = event.correlation_id
    url = urljoin(server_url.rstrip("/"), _DATALAKE_EVENTS_PATH)
    headers = {"Authorization": f"Bearer {bearer_token}", "User-Agent": USER_AGENT}
    if client is not None:
        await client.post(url, json=payload, headers=headers)
        return
    async with httpx.AsyncClient(timeout=_DELIVERY_TIMEOUT_SECONDS) as owned_client:
        await owned_client.post(url, json=payload, headers=headers)


async def _deliver(event: _TelemetryEvent, *, client: httpx.AsyncClient | None = None) -> None:
    settings = get_app_settings()
    if not settings.telemetry_enabled:
        return

    if is_otel_enabled():
        await _track(event)
        return

    bearer_token = _get_mistral_bearer_token()
    if bearer_token is None:
        await _track(event)
        return

    # Never retry or switch sinks after a POST attempt: the event may already be ingested.
    await _post(
        server_url=settings.telemetry_server_url,
        bearer_token=bearer_token,
        event=event,
        client=client,
    )


async def _deliver_best_effort(event: _TelemetryEvent, *, client: httpx.AsyncClient | None = None) -> None:
    try:
        await _deliver(event, client=client)
    except Exception:
        return


class _UsageDelivery:
    """The worker's queue of usage events and the consumers that send them over one HTTP client.

    Delivery is not activity work: it has no result, needs no retry, and losing it loses one analytics
    row. So the worker starts it before it serves and drains it when it stops, and a model call only
    enqueues: activity code never starts a task. The queue is bounded and usable only from its loop.
    """

    def __init__(self) -> None:
        # Workers serving in this loop; the delivery closes when the last of them stops.
        self.owners = 0
        self._queue: asyncio.Queue[_TelemetryEvent] = asyncio.Queue(maxsize=_MAX_QUEUED_USAGE_EVENTS)
        self._client = httpx.AsyncClient(timeout=_DELIVERY_TIMEOUT_SECONDS)
        self._consumers = [
            asyncio.create_task(self._consume(), name=f"agents-sdk-telemetry:usage-{index}")
            for index in range(_USAGE_DELIVERY_CONSUMERS)
        ]

    def submit(self, event: _TelemetryEvent) -> None:
        with contextlib.suppress(asyncio.QueueFull):
            self._queue.put_nowait(event)

    async def close(self) -> None:
        with contextlib.suppress(TimeoutError):
            await asyncio.wait_for(self._queue.join(), timeout=_USAGE_DRAIN_TIMEOUT_SECONDS)
        for consumer in self._consumers:
            consumer.cancel()
        await asyncio.gather(*self._consumers, return_exceptions=True)
        await self._client.aclose()

    async def _consume(self) -> None:
        while True:
            event = await self._queue.get()
            try:
                await _deliver_best_effort(event, client=self._client)
            finally:
                self._queue.task_done()


_usage_deliveries: dict[asyncio.AbstractEventLoop, _UsageDelivery] = {}


def telemetry_enabled() -> bool:
    """Whether this process may send SDK telemetry at all (``AGENTS_SDK_TELEMETRY_ENABLED``)."""
    return get_app_settings().telemetry_enabled


def start_background_deliveries() -> None:
    """Start, or join, the usage delivery of the running loop before a worker serves.

    Every call must be matched by one ``drain_background_deliveries`` when that worker stops.
    """
    loop = asyncio.get_running_loop()
    delivery = _usage_deliveries.get(loop)
    if delivery is None:
        delivery = _usage_deliveries[loop] = _UsageDelivery()
    delivery.owners += 1


def completion_done(completion: CompletionDone) -> None:
    """Queue a deployed Session's model attempt for the datalake without delaying the activity that made it.

    Dropped when this worker started no delivery in the running loop: there is nothing to send it.
    """
    delivery = _usage_deliveries.get(asyncio.get_running_loop())
    if delivery is None:
        return
    delivery.submit(completion.to_event())


async def drain_background_deliveries() -> None:
    """Leave the usage delivery as a worker stops; the last worker out drains and closes it.

    Draining sends the queued events for a few seconds, then drops the rest.
    """
    loop = asyncio.get_running_loop()
    delivery = _usage_deliveries.get(loop)
    if delivery is None:
        return
    delivery.owners -= 1
    if delivery.owners > 0:
        return
    del _usage_deliveries[loop]
    await delivery.close()


def _registration_error_type(error: Exception) -> RegistrationErrorType | None:
    if isinstance(error, httpx.HTTPStatusError):
        status_code = error.response.status_code
        if status_code == httpx.codes.UNAUTHORIZED:
            # The event would be sent with the key the control plane just rejected.
            return None
        if status_code == httpx.codes.CONFLICT:
            return "conflict"
        # Deploy passes the Workflows API's own rejection through, usually a 400 (an invalid revision, for example).
        if status_code in (httpx.codes.BAD_REQUEST, httpx.codes.UNPROCESSABLE_ENTITY):
            return "invalid_request"
        if status_code >= httpx.codes.INTERNAL_SERVER_ERROR:
            return "server_error"
        return "http_error"
    if isinstance(error, httpx.TransportError):
        return "network_error"
    # The rest has no reliable meaning from its type alone: a pydantic error can come from our own request or
    # from the server's response, so these are reported without guessing.
    return "unknown_error"


async def agent_registration_failed(
    error: Exception,
    *,
    agent_name: str,
    workflow_name: str,
    worker_hosting: WorkerHosting,
) -> None:
    """Report that `agents serve` or `agents deploy` could not register the agent with the control plane.

    Only the outcome category and the HTTP status are sent, never the control plane's message. Delivery is
    awaited for at most two seconds and never raises, so it cannot change how the command fails.
    """
    error_type = _registration_error_type(error)
    if error_type is None:
        return
    # Only failures are reported today, so `status` is always `error`; a success outcome can join the same event.
    properties: dict[str, str | int] = {
        "status": "error",
        "error_type": error_type,
        "worker_hosting": worker_hosting,
        "agent_name": agent_name,
        "workflow_name": workflow_name,
        "sdk_version": __version__,
    }
    if isinstance(error, httpx.HTTPStatusError):
        properties["http_status_code"] = error.response.status_code
    event = _TelemetryEvent(name="agents.agent_registration.done", properties=properties)
    with contextlib.suppress(TimeoutError):
        await asyncio.wait_for(_deliver_best_effort(event), timeout=_REGISTRATION_FAILURE_DELIVERY_TIMEOUT_SECONDS)


class LocalSessionTelemetry:
    """Deliver telemetry without delaying a local Session and drain it when the Session closes."""

    def __init__(self) -> None:
        self._delivery: asyncio.Task[None] | None = None

    def session_started(self, session_id: str, *, agent_name: str) -> None:
        self._delivery = asyncio.create_task(
            _deliver_session_started_best_effort(session_id, agent_name),
            name=f"agents-sdk-telemetry:{session_id}",
        )

    async def close(self) -> None:
        if self._delivery is not None:
            await asyncio.gather(self._delivery, return_exceptions=True)


async def _deliver_session_started_best_effort(session_id: str, agent_name: str) -> None:
    try:
        event = _TelemetryEvent.session_started(session_id, agent_name)
    except Exception:
        return
    await _deliver_best_effort(event)


__all__ = [
    "CompletionDone",
    "CompletionStatus",
    "LocalSessionTelemetry",
    "agent_registration_failed",
    "completion_done",
    "drain_background_deliveries",
    "start_background_deliveries",
    "telemetry_enabled",
]
