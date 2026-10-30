from __future__ import annotations

import asyncio
import functools
import time
from contextvars import ContextVar, Token
from http import HTTPStatus
from typing import TYPE_CHECKING, Any, Optional, TypeGuard

import httpx
import temporalio.activity
import tenacity
from temporalio.exceptions import ApplicationError

from mistralai.workflows.core._events.event_encoder import EventPayloadEncoder, maybe_encode_event
from mistralai.workflows.core._events.event_route_publisher import EventRoutePublisher
from mistralai.workflows.core._logger import get_logger
from mistralai.workflows.core.config.config import DEFAULT_EVENTS_API_VERSION, EventsApiVersion
from mistralai.workflows.core.logging import extract_error_context
from mistralai.workflows.core.metrics import record_event_publish_retry
from mistralai.workflows.core.utils.contextvars import reset_contextvar
from mistralai.workflows.exceptions import WorkflowsException
from mistralai.workflows.protocol.v1.events import WorkflowEvent
from mistralai.workflows.protocol.v2.worker import EVENT_ROUTE_TOKEN_EXPIRED_CODE, EVENT_ROUTE_TOKEN_INVALID_CODE
from mistralai.workflows.worker_client.errors import NoResponseError, SDKError
from mistralai.workflows.worker_client.events import Events
from mistralai.workflows.worker_client.models import WorkflowEventRequestEventTypedDict
from mistralai.workflows.worker_client.sdk import PrivateWorkerClient

if TYPE_CHECKING:
    from mistralai.extra.workflows.encoding.payload_encoder import PayloadEncoder

logger = get_logger(__name__)

# Matches the NATS max_payload configured for the workflows cluster (2MB).
# Slightly under 2MiB to leave headroom for NATS message framing overhead.
# Events that would push a batch over this threshold are deferred to the next request.
_MAX_BATCH_PAYLOAD_BYTES = 2_000_000  # 2 MB

_PUBLISH_RETRY_BUDGET_SECONDS = 60.0
_PUBLISH_RETRY_INITIAL_BACKOFF_SECONDS = 0.5
_PUBLISH_RETRY_MAX_BACKOFF_SECONDS = 10.0

# PROBLEM: We want to publish events to the Workflows API from within Temporal workflows, but Temporal
# sandboxes workflows from asyncio (no event loop access, no IO) to enforce deterministic replay.
#
# SOLUTION: Store an EventContext (backed by mistral_client.workflows.events) as a global singleton, created by the
# main worker before running workflows. Workflows/activities call `EventContext.get_singleton().publish_event()`
# which executes IO on the worker's asyncio loop—outside Temporal's sandbox.
#
# WHY GLOBAL (not contextvars)? Temporal clears contextvars between workflow/activity boundaries.
# The contextvar `_is_event_context_singleton_owner` only tracks who created the singleton for cleanup.
_event_context_singleton: Optional["EventContext"] = None
_is_event_context_singleton_owner: ContextVar[bool] = ContextVar("is_event_context_singleton_owner", default=False)

# Activity-scoped background event publisher for custom task events (streaming)
_background_event_publisher: ContextVar[Optional["BackgroundEventPublisher"]] = ContextVar(
    "background_event_publisher", default=None
)


EVENT_PUBLISH_FAILED_ERROR_TYPE = "WorkflowEventPublishFailed"

_TRANSIENT_CLIENT_ERROR_STATUSES = frozenset({HTTPStatus.REQUEST_TIMEOUT, HTTPStatus.TOO_MANY_REQUESTS})
_REFRESHABLE_ROUTE_TOKEN_CODES = frozenset({EVENT_ROUTE_TOKEN_EXPIRED_CODE, EVENT_ROUTE_TOKEN_INVALID_CODE})
_TRANSIENT_ERROR_TYPES = (httpx.TransportError, TimeoutError, NoResponseError)


class V1EventRouteForbiddenError(Exception):
    """Raised when the worker forbids the v1 event route.

    Triggered by ``EVENTS_API_VERSION=v2-only`` so v2 integration tests fail if any
    event would be emitted over the v1 route.
    """


class EventContext:
    """Context for publishing workflow and activity lifecycle events sequentially.

    Used by workflow/activity interceptors to send lifecycle events (STARTED, COMPLETED, etc.).
    Events are sent synchronously to guarantee ordering.
    """

    def __init__(
        self,
        events_client: Events,
        worker_client: PrivateWorkerClient | None = None,
        events_api_version: EventsApiVersion = DEFAULT_EVENTS_API_VERSION,
        payload_encoder: PayloadEncoder | None = None,
        custom_event_payload_encoder: PayloadEncoder | None = None,
    ) -> None:
        self.events_client = events_client
        self._token: Optional[Token] = None
        self._batch_events_supported: bool = True
        # v2-only forbids any v1 fallback (used by v2 integration tests).
        self._forbid_v1_event_route = events_api_version == EventsApiVersion.V2_ONLY
        # Only create EventPayloadEncoder when encryption is configured
        self._event_encoder: EventPayloadEncoder | None = (
            EventPayloadEncoder(payload_encoder, custom_event_payload_encoder)
            if payload_encoder is not None and payload_encoder.encryption_config is not None
            else None
        )
        self._event_route_publisher = (
            EventRoutePublisher(
                worker_client,
                events_api_version=events_api_version,
                event_encoder=self._event_encoder,
            )
            if worker_client is not None
            else None
        )

    @staticmethod
    def has_context() -> bool:
        return bool(_event_context_singleton)

    @staticmethod
    def get_singleton() -> Optional["EventContext"]:
        """Get the current event context singleton."""
        if not temporalio.activity.in_activity() and not _event_context_singleton:
            logger.warning("EventContext not initialized - event publishing disabled for this activity execution")

        return _event_context_singleton

    async def __aenter__(self) -> "EventContext":
        """Enter the event context, setting it as the singleton."""
        global _event_context_singleton
        if _event_context_singleton is not None:
            return _event_context_singleton

        self._token = _is_event_context_singleton_owner.set(True)
        _event_context_singleton = self
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Exit the event context, cleaning up resources."""
        global _event_context_singleton
        if not _is_event_context_singleton_owner.get():
            return

        assert self._token, "Should have token because _is_event_context_singleton_owner is True"
        reset_contextvar(_is_event_context_singleton_owner, self._token)
        _event_context_singleton = None

    async def publish_event(self, event: WorkflowEvent) -> None:
        """Publish a single workflow event sequentially.

        Args:
            event: The workflow event to publish.
        """
        await self.publish_events_batch([event])

    async def publish_events_batch(self, events: list[WorkflowEvent]) -> None:
        """Publish multiple workflow events in a single batch request.

        Args:
            events: List of workflow events to publish.
        """
        if not events:
            return

        await self._publish_events_batch_internal(events)

    async def publish_event_or_raise(self, event: WorkflowEvent) -> None:
        """Drop too-large events; raise transient failures to retry, a non-retryable ApplicationError otherwise."""
        self._ensure_entered()
        try:
            await self._send_events([await maybe_encode_event(event, self._event_encoder)])
        except asyncio.CancelledError as e:
            # Temporal cancels the emitter at its start-to-close timeout, before a hung request times out.
            details = temporalio.activity.cancellation_details()
            if details is not None and details.timed_out:
                _on_emitter_retry(event, e)
            raise
        except Exception as e:
            if _is_payload_too_large(e):
                _log_dropped_too_large_event(event, e)
                return
            if not _is_permanent_publish_error(e):
                _on_emitter_retry(event, e)
                raise
            raise _permanent_publish_failure([event], e) from e

    async def publish_encoded_events_with_retry(self, events: list[WorkflowEvent]) -> None:
        """Retry transient failures within a budget, then raise a retryable ApplicationError so the attempt re-runs.

        Like publish_event_or_raise, drops a too-large event, but only that one rather than its whole batch.
        """
        self._ensure_entered()
        await self._publish_with_retry(events, deadline=time.monotonic() + _PUBLISH_RETRY_BUDGET_SECONDS)

    async def _publish_with_retry(self, events: list[WorkflowEvent], deadline: float) -> None:
        try:
            async for attempt in tenacity.AsyncRetrying(
                retry=tenacity.retry_if_exception(_is_transient_publish_error),
                stop=tenacity.stop_before_delay(deadline - time.monotonic()),
                wait=tenacity.wait_exponential(
                    multiplier=_PUBLISH_RETRY_INITIAL_BACKOFF_SECONDS, max=_PUBLISH_RETRY_MAX_BACKOFF_SECONDS
                ),
                before_sleep=functools.partial(_on_publish_retry, events),
                reraise=True,
            ):
                with attempt:
                    await self._send_events(events)
        except Exception as e:
            if _is_payload_too_large(e):
                if len(events) == 1:
                    _log_dropped_too_large_event(events[0], e)
                    return
                for event in events:
                    await self._publish_with_retry([event], deadline)
                return
            # Out of budget on the activity's last attempt, the workflow is failed by this event too.
            if _is_permanent_publish_error(e) or (
                temporalio.activity.in_activity() and activity_attempts_exhausted(temporalio.activity.info())
            ):
                raise _permanent_publish_failure(events, e) from e
            record_event_publish_retry(len(events))
            raise _publish_failed_error(events, e, non_retryable=False) from e

    async def publish_event_with_retry(self, event: WorkflowEvent) -> None:
        await self.publish_encoded_events_with_retry([await self.encode_or_raise(event)])

    async def encode_or_raise(self, event: WorkflowEvent) -> WorkflowEvent:
        try:
            return await maybe_encode_event(event, self._event_encoder)
        except Exception as e:
            raise _permanent_publish_failure([event], e) from e

    async def _publish_events_batch_internal(self, events: list[WorkflowEvent]) -> None:
        self._ensure_entered()
        if not events:
            return

        events = list(await asyncio.gather(*[maybe_encode_event(event, self._event_encoder) for event in events]))

        try:
            await self._send_events(events)
        except V1EventRouteForbiddenError:
            raise
        except Exception as e:
            logger.warning(
                "Failed to send workflow event batch",
                batch_size=len(events),
                **extract_error_context(e),
            )

    def _ensure_entered(self) -> None:
        if self._token is None:
            raise RuntimeError("EventContext not entered")

    async def _send_events(self, events: list[WorkflowEvent]) -> None:
        # v2 when configured; False falls through to v1, failures raise.
        if self._event_route_publisher is not None and await self._event_route_publisher.try_publish_via_v2(
            events, already_encoded=True
        ):
            return
        if self._forbid_v1_event_route:
            raise V1EventRouteForbiddenError(
                "EVENTS_API_VERSION=v2-only but a v2 publish did not happen; refusing v1 fallback"
            )
        # Use single event endpoint for one event, batch endpoint for multiple
        if len(events) == 1:
            await self.events_client.send_event_async(event=self._translate_event(events[0]))
            return
        if not self._batch_events_supported:
            await self._send_events_batch_fallback(events)
            return
        try:
            await self.events_client.send_events_batch_async(events=[self._translate_event(e) for e in events])
        except SDKError as e:
            # originally implemented in https://github.com/mistralai/dashboard/pull/21280
            if e.status_code == 404:
                self._batch_events_supported = False
                await self._send_events_batch_fallback(events)
                return
            raise

    def _translate_event(self, event: WorkflowEvent) -> WorkflowEventRequestEventTypedDict:
        return event.model_dump(mode="json")  # type: ignore

    async def _send_events_batch_fallback(self, events: list[WorkflowEvent]) -> None:
        """Fallback: send events one by one when the batch endpoint is not available."""
        for event in events:
            await self.events_client.send_event_async(event=self._translate_event(event))


def activity_attempts_exhausted(info: temporalio.activity.Info) -> bool:
    # Unlike _is_final_attempt, an unknown policy is not exhausted: escalating would make a retryable failure permanent.
    if info.retry_policy is None:
        return False
    max_attempts = info.retry_policy.maximum_attempts
    return max_attempts > 0 and info.attempt >= max_attempts


def is_permanent_event_publish_failure(error: BaseException | None) -> TypeGuard[ApplicationError]:
    return isinstance(error, ApplicationError) and error.type == EVENT_PUBLISH_FAILED_ERROR_TYPE and error.non_retryable


def _as_workflows_exception(error: Exception) -> WorkflowsException | None:
    if isinstance(error, WorkflowsException):
        return error
    if isinstance(error, SDKError):
        return WorkflowsException.from_sdk_error(error, message=error.message)
    return None


def _is_payload_too_large(error: Exception) -> bool:
    http_error = _as_workflows_exception(error)
    return http_error is not None and http_error.status == HTTPStatus.REQUEST_ENTITY_TOO_LARGE


def _on_emitter_retry(event: WorkflowEvent, error: BaseException) -> None:
    record_event_publish_retry(1)
    logger.warning(
        "Retrying workflow event batch",
        event_type=event.event_type,
        **(extract_error_context(error) if isinstance(error, Exception) else {}),
    )


def _on_publish_retry(events: list[WorkflowEvent], retry_state: tenacity.RetryCallState) -> None:
    record_event_publish_retry(len(events))
    error = retry_state.outcome.exception() if retry_state.outcome else None
    logger.warning(
        "Retrying workflow event batch",
        attempt=retry_state.attempt_number,
        backoff=retry_state.upcoming_sleep,
        **(extract_error_context(error) if isinstance(error, Exception) else {}),
    )


def _log_dropped_too_large_event(event: WorkflowEvent, error: Exception) -> None:
    logger.error(
        "Dropping workflow event too large to publish", event_type=event.event_type, **extract_error_context(error)
    )


def _permanent_publish_failure(events: list[WorkflowEvent], error: Exception) -> ApplicationError:
    logger.error(
        "Workflow event permanently failed to publish",
        event_types=list(dict.fromkeys(f"{event.event_type}" for event in events)),
        **extract_error_context(error),
    )
    return _publish_failed_error(events, error)


def _is_transient_publish_error(error: BaseException) -> bool:
    return isinstance(error, Exception) and not _is_permanent_publish_error(error)


def _is_permanent_publish_error(error: Exception) -> bool:
    http_error = _as_workflows_exception(error)
    if http_error is None:
        return not isinstance(error, _TRANSIENT_ERROR_TYPES)
    # The publisher evicted the cached route token, so a retry mints a fresh one.
    if http_error.status == HTTPStatus.UNAUTHORIZED and str(http_error.code) in _REFRESHABLE_ROUTE_TOKEN_CODES:
        return False
    return 400 <= http_error.status < 500 and http_error.status not in _TRANSIENT_CLIENT_ERROR_STATUSES


def _publish_failed_error(
    events: list[WorkflowEvent], error: Exception, non_retryable: bool = True
) -> ApplicationError:
    http_error = _as_workflows_exception(error)
    detail = f"HTTP {int(http_error.status)}: {http_error.message}" if http_error else str(error)
    event_types = ", ".join(dict.fromkeys(f"{event.event_type}" for event in events))
    noun = "event" if len(events) == 1 else "events"
    return ApplicationError(
        f"Workflow {noun} {event_types} could not be published: {detail}",
        type=EVENT_PUBLISH_FAILED_ERROR_TYPE,
        non_retryable=non_retryable,
    )


class BackgroundEventPublisher:
    """Publishes events from an activity without blocking the code that produces them.

    A single sender task sends queued events in FIFO order, in batches, retrying transient failures.
    The first event that can't be published stops the sender, and drain() raises it so the activity fails.
    """

    def __init__(self, event_context: EventContext):
        self.event_context = event_context
        self._event_queue: asyncio.Queue[Optional[WorkflowEvent]] = asyncio.Queue()
        self._sender_task: Optional[asyncio.Task] = None
        self._fatal_error: Optional[ApplicationError] = None

    @staticmethod
    def get_current() -> Optional["BackgroundEventPublisher"]:
        return _background_event_publisher.get()

    @staticmethod
    def set_current(publisher: Optional["BackgroundEventPublisher"]) -> Token:
        return _background_event_publisher.set(publisher)

    async def _event_sender_loop(self) -> None:
        pending: Optional[WorkflowEvent] = None
        stopping = False
        while pending is not None or not stopping:
            if pending is None:
                queued = await self._event_queue.get()
                if queued is None:
                    self._event_queue.task_done()
                    return
                pending = queued
            batch = [pending]
            pending = None
            try:
                if self._fatal_error is not None:
                    continue
                batch[0] = await self.event_context.encode_or_raise(batch[0])
                payload_size = len(batch[0].model_dump_json().encode())
                while payload_size < _MAX_BATCH_PAYLOAD_BYTES:
                    try:
                        queued = self._event_queue.get_nowait()
                    except asyncio.QueueEmpty:
                        break
                    if queued is None:
                        self._event_queue.task_done()
                        stopping = True
                        break
                    batch.append(queued)
                    batch[-1] = await self.event_context.encode_or_raise(queued)
                    event_size = len(batch[-1].model_dump_json().encode())
                    if payload_size + event_size > _MAX_BATCH_PAYLOAD_BYTES:
                        batch.pop()
                        pending = queued
                        break
                    payload_size += event_size
                await self.event_context.publish_encoded_events_with_retry(batch)
            except Exception as e:
                self._fatal_error = e if isinstance(e, ApplicationError) else _permanent_publish_failure(batch, e)
            finally:
                for _ in batch:
                    self._event_queue.task_done()

    def publish_event_background(self, event: WorkflowEvent) -> None:
        if self._sender_task is None:
            self._sender_task = asyncio.create_task(self._event_sender_loop())
        self._event_queue.put_nowait(event)

    async def drain(self) -> None:
        """Wait until every queued event is published; raise if one couldn't be."""
        if self._sender_task is not None:
            await self._event_queue.join()
        if self._fatal_error is not None:
            raise self._fatal_error

    async def drain_preserving_error(self) -> None:
        """For a caller about to raise its own error, which a publish failure must not hide."""
        try:
            await self.drain()
        except ApplicationError as e:
            logger.error("Failed to publish activity events", **extract_error_context(e))

    async def shutdown(self) -> None:
        if self._sender_task is None:
            return

        # Send sentinel value to stop the sender loop
        self._event_queue.put_nowait(None)

        try:
            await asyncio.wait_for(self._sender_task, timeout=5.0)
        except asyncio.TimeoutError:
            logger.warning("Timeout waiting for event sender task to shutdown")
            self._sender_task.cancel()
            try:
                await self._sender_task
            except asyncio.CancelledError:
                pass
        except Exception as e:
            logger.error("Error shutting down event sender task", **extract_error_context(e))
        finally:
            self._sender_task = None
