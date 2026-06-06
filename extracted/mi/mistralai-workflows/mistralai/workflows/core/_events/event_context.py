from __future__ import annotations

import asyncio
from contextvars import ContextVar, Token
from typing import TYPE_CHECKING, Any, Optional

import structlog
import temporalio.activity

from mistralai.workflows.core._events.event_encoder import EventPayloadEncoder, maybe_encode_event
from mistralai.workflows.core._events.event_route_publisher import EventRoutePublisher
from mistralai.workflows.core.utils.contextvars import reset_contextvar
from mistralai.workflows.protocol.v1.events import WorkflowEvent
from mistralai.workflows.worker_client.errors import SDKError
from mistralai.workflows.worker_client.events import Events
from mistralai.workflows.worker_client.models import WorkflowEventRequestEventTypedDict
from mistralai.workflows.worker_client.sdk import PrivateWorkerClient

if TYPE_CHECKING:
    from mistralai.extra.workflows.encoding.payload_encoder import PayloadEncoder

logger = structlog.get_logger(__name__)

# Matches the NATS max_payload configured for the workflows cluster (2MB).
# Slightly under 2MiB to leave headroom for NATS message framing overhead.
# Events that would push a batch over this threshold are deferred to the next request.
_MAX_BATCH_PAYLOAD_BYTES = 2_000_000  # 2 MB

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


class EventContext:
    """Context for publishing workflow and activity lifecycle events sequentially.

    Used by workflow/activity interceptors to send lifecycle events (STARTED, COMPLETED, etc.).
    Events are sent synchronously to guarantee ordering.
    """

    def __init__(
        self,
        events_client: Events,
        worker_client: PrivateWorkerClient | None = None,
        events_api_version: str = "v1",
        payload_encoder: PayloadEncoder | None = None,
    ) -> None:
        self.events_client = events_client
        self._token: Optional[Token] = None
        self._batch_events_supported: bool = True
        # Only create EventPayloadEncoder when encryption is configured
        self._event_encoder: EventPayloadEncoder | None = (
            EventPayloadEncoder(payload_encoder)
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

    async def _publish_events_batch_internal(
        self,
        events: list[WorkflowEvent],
        already_encoded: bool = False,
    ) -> None:
        """Internal method to publish events.

        Args:
            events: List of workflow events to publish.
            already_encoded: If True, skip encoding (events are already encoded).
                           If False (default), encode events before publishing.
        """
        if self._token is None:
            raise RuntimeError("EventContext not entered")

        if not events:
            return

        if not already_encoded:
            events = list(await asyncio.gather(*[maybe_encode_event(event, self._event_encoder) for event in events]))

        try:
            # Try the v2 event-route publisher first when configured; fall back to
            # the legacy v1 events client when v2 is disabled or downgraded.
            # Events are already encoded at this point, skip re-encoding.
            if self._event_route_publisher is not None and await self._event_route_publisher.publish_events(
                events, already_encoded=True
            ):
                return
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
        except Exception as e:
            logger.warning(
                "Failed to send workflow event batch",
                batch_size=len(events),
                error=str(e),
            )

    def _translate_event(self, event: WorkflowEvent) -> WorkflowEventRequestEventTypedDict:
        return event.model_dump(mode="json")  # type: ignore

    async def _send_events_batch_fallback(self, events: list[WorkflowEvent]) -> None:
        """Fallback: send events one by one when the batch endpoint is not available."""
        for event in events:
            await self.events_client.send_event_async(event=self._translate_event(event))


class BackgroundEventPublisher:
    """Handles background publishing of custom task events (streaming) within an activity.

    Custom task events are sent via a FIFO queue to guarantee strict ordering.
    A single background sender task processes events sequentially.
    The activity interceptor waits for the queue to drain before marking the activity as complete.
    """

    def __init__(self, event_context: EventContext):
        self.event_context = event_context
        self._event_encoder = event_context._event_encoder
        self._event_queue: asyncio.Queue[Optional[WorkflowEvent]] = asyncio.Queue()
        self._sender_task: Optional[asyncio.Task] = None

    @staticmethod
    def get_current() -> Optional["BackgroundEventPublisher"]:
        return _background_event_publisher.get()

    @staticmethod
    def set_current(publisher: Optional["BackgroundEventPublisher"]) -> Token:
        return _background_event_publisher.set(publisher)

    async def _event_sender_loop(self) -> None:
        pending: Optional[WorkflowEvent] = None
        pending_ack = 0  # task_done owed for pending event from previous iteration
        while True:
            if pending is not None:
                first_event: WorkflowEvent = pending
                pending = None
                ack_count = pending_ack
                pending_ack = 0
            else:
                _queued = await self._event_queue.get()
                if _queued is None:
                    self._event_queue.task_done()
                    break
                try:
                    # Encode before measuring size to account for base64 overhead
                    first_event = await maybe_encode_event(_queued, self._event_encoder)
                except Exception as e:
                    logger.error("Failed to encode event", error=str(e))
                    self._event_queue.task_done()
                    continue
                ack_count = 1

            batch = [first_event]
            payload_size = len(first_event.model_dump_json().encode())

            while payload_size < _MAX_BATCH_PAYLOAD_BYTES:
                try:
                    event = self._event_queue.get_nowait()
                except asyncio.QueueEmpty:
                    break

                if event is None:
                    self._event_queue.task_done()
                    self._event_queue.put_nowait(None)
                    break

                try:
                    # Encode before measuring size to account for base64 overhead
                    encoded_event = await maybe_encode_event(event, self._event_encoder)
                except Exception as e:
                    logger.error("Failed to encode event", error=str(e))
                    self._event_queue.task_done()
                    continue

                event_size = len(encoded_event.model_dump_json().encode())
                if payload_size + event_size > _MAX_BATCH_PAYLOAD_BYTES:
                    # Too large for this batch - defer to next iteration
                    pending = encoded_event
                    pending_ack = 1
                    break

                batch.append(encoded_event)
                ack_count += 1
                payload_size += event_size

            try:
                # Events are already encoded, skip re-encoding
                await self.event_context._publish_events_batch_internal(batch, already_encoded=True)
            except Exception as e:
                logger.error(
                    "Failed to send event batch from background queue",
                    batch_size=len(batch),
                    error=str(e),
                )
            finally:
                for _ in range(ack_count):
                    self._event_queue.task_done()

    def publish_event_background(self, event: WorkflowEvent) -> None:
        """Publish a custom task event to the background queue for streaming.

        Events are processed in strict FIFO order by a single background sender task.
        The activity interceptor ensures all queued events are sent before completion.
        """
        if self._sender_task is None:
            self._sender_task = asyncio.create_task(self._event_sender_loop())
        self._event_queue.put_nowait(event)

    async def drain(
        self,
        per_event_timeout: float = 2.0,
        min_timeout: float = 10.0,
        max_timeout: Optional[float] = None,
    ) -> None:
        """Wait for all queued events to be sent.

        The timeout scales with the number of pending events to avoid premature
        timeouts when many events are in flight.
        """
        pending = self._event_queue.qsize()
        timeout = max(min_timeout, pending * per_event_timeout)
        if max_timeout is not None:
            timeout = min(timeout, max_timeout)
        try:
            await asyncio.wait_for(self._event_queue.join(), timeout=timeout)
        except asyncio.TimeoutError:
            logger.warning(
                "Timeout waiting for event queue to drain",
                pending_count=self._event_queue.qsize(),
                timeout=timeout,
            )
        except Exception as e:
            logger.error(
                "Error waiting for event queue to drain",
                error=str(e),
            )

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
            logger.error("Error shutting down event sender task", error=str(e))
        finally:
            self._sender_task = None
