from __future__ import annotations

import abc
import logging
from queue import Queue, Full, Empty
import threading
import time
import typing as t
from threading import Event, Thread

import grpc
from query_cache_protobuf.query_cache.services import client_telemetry_service_pb2
from query_cache_common.models.services import client_telemetry_service_models

if t.TYPE_CHECKING:
    from dbt_state.grpc.client import QueryCacheGrpcClient
    from dbt_state._typing import ClientEvent

logger = logging.getLogger(__name__)


class TelemetryDispatcher(abc.ABC):
    """Base class for telemetry dispatchers."""

    @abc.abstractmethod
    def add_event(self, event: ClientEvent) -> None:
        """Add a telemetry event to be emitted.

        Args:
            event: The event data.
        """

    @abc.abstractmethod
    def flush(self) -> None:
        """Flushes the collected events to the service"""

    @abc.abstractmethod
    def shutdown(self, flush: bool = True) -> None:
        """Shuts down dispatcher and releases any resources.

        Args:
            flush: Whether to flush the collected events before shutting down.
        """


class AsyncTelemetryDispatcher(TelemetryDispatcher):
    """Asynchronously dispatch telemetry events in a background thread"""

    def __init__(
        self,
        query_cache_client: QueryCacheGrpcClient,
        max_emit_interval_sec: int = 5,
        max_queue_size: int = 150,
        max_retry_count: int = 3,
        max_batch_size: int = 50,
    ):
        """Initialize async telemetry dispatcher with background worker thread.

        Args:
            query_cache_client: Client for sending telemetry to server
            max_emit_interval_sec: Max seconds between batch emissions
            max_queue_size: Max events in queue before dropping oldest
            max_retry_count: Max retries for failed events
            max_batch_size: Max events per patch.
        """
        self._query_cache_client = query_cache_client
        self._max_emit_interval_sec = max_emit_interval_sec
        self._max_queue_size = max_queue_size
        self._max_retry_count = max_retry_count
        self._max_batch_size = max_batch_size

        self._event_queue: Queue[
            t.Tuple[client_telemetry_service_pb2.ClientTelemetryEvent, int]
        ] = Queue(maxsize=max_queue_size)

        self._shutdown_event = Event()

        self._emitter_thread = Thread(target=self._run_flush, name="telemetry-emitter", daemon=True)
        self._emitter_thread.start()

        self._event_order_count = 0
        self._event_order_count_lock = threading.Lock()

    def add_event(
        self,
        event: ClientEvent,
    ) -> None:
        event_order = self._get_next_event_order()

        if isinstance(event, client_telemetry_service_models.SessionStartRequest):
            telemetry_event = client_telemetry_service_pb2.ClientTelemetryEvent(
                session_start=event.to_proto(),
                event_order=event_order,
            )
        elif isinstance(event, client_telemetry_service_models.ClientPrepareEnrichedSQLRequest):
            telemetry_event = client_telemetry_service_pb2.ClientTelemetryEvent(
                enriched_sql_prepared=event.to_proto(),
                event_order=event_order,
            )
        elif isinstance(event, client_telemetry_service_models.SessionEndRequest):
            telemetry_event = client_telemetry_service_pb2.ClientTelemetryEvent(
                session_end=event.to_proto(), event_order=event_order
            )
        else:
            raise ValueError(f"Unknown event type: {type(event)}")
        self._add_events([telemetry_event])

    def _add_events(
        self, events: t.List[client_telemetry_service_pb2.ClientTelemetryEvent]
    ) -> None:
        if self._shutdown_event.is_set():
            logger.warning("Dispatcher shut down, dropping %d events", len(events))
            return

        if not events:
            return

        for event in events:
            self._put_event(event, 0)

    def _put_event(
        self, event: client_telemetry_service_pb2.ClientTelemetryEvent, retry_count: int
    ) -> None:
        """Add event to queue, dropping oldest event if full (handles race conditions)."""
        try:
            self._event_queue.put((event, retry_count), block=False)
        except Full:
            # Queue filled during operation - drop oldest and retry
            try:
                self._event_queue.get_nowait()
                logger.debug("Dropped oldest event to make room")
                try:
                    self._event_queue.put((event, retry_count), block=False)
                except Full:
                    logger.warning("Queue still full after dropping oldest, dropping new event")
            except Empty:
                # Queue emptied between Full exception and get_nowait
                try:
                    self._event_queue.put((event, retry_count), block=False)
                except Full:
                    logger.warning("Queue full, dropping event")

    def flush(self) -> None:
        """Flush queued events to the telemetry service."""
        while True:
            batch: t.List = []
            while len(batch) < self._max_batch_size:
                try:
                    batch.append(self._event_queue.get_nowait())
                except Empty:
                    break

            if not batch:
                return

            logger.debug("Emitting %d telemetry events", len(batch))

            proto_events = [event for event, _ in batch]
            try:
                batch_request = client_telemetry_service_pb2.SubmitTelemetryBatchRequest(
                    events=proto_events
                )
                self._query_cache_client.client_telemetry_stub.SubmitTelemetryBatch(
                    batch_request, timeout=self._query_cache_client.timeout
                )
            except grpc.RpcError as e:
                status_code = e.code()

                # Drop non-retriable errors immediately
                if status_code in (
                    grpc.StatusCode.UNIMPLEMENTED,
                    grpc.StatusCode.PERMISSION_DENIED,
                    grpc.StatusCode.INVALID_ARGUMENT,
                ):
                    logger.warning(
                        "Non-retriable gRPC error (%s), dropping %d telemetry events: %s",
                        status_code.name,
                        len(batch),
                        e.details(),
                    )
                    return

                logger.debug(
                    "Retriable gRPC error (%s), re-queuing %d telemetry events: %s",
                    status_code.name,
                    len(batch),
                    e.details(),
                )

                for event, retry_count in batch:
                    if retry_count < self._max_retry_count:
                        logger.debug(
                            "Re-queuing event for retry (attempt %d/%d)",
                            retry_count + 1,
                            self._max_retry_count,
                        )
                        self._put_event(event, retry_count + 1)
                    else:
                        logger.warning(
                            "Max retry count (%d) exceeded, dropping event", self._max_retry_count
                        )
                return
            except Exception as e:
                logger.warning(
                    "Unexpected error emitting %d telemetry events, dropping batch: %s",
                    len(batch),
                    e,
                )
                return

    def shutdown(self, flush: bool = True) -> None:
        """Shutdown the background thread.

        Args:
            flush: Whether to flush remaining events before shutdown
        """
        if self._shutdown_event.is_set():
            return
        self._shutdown_event.set()
        self._emitter_thread.join()

        if self._emitter_thread.is_alive():
            logger.warning("Telemetry emitter thread did not shut down after timeout")

        if flush:
            while self._event_queue.qsize() > 0:
                self.flush()

    def _run_flush(self) -> None:
        """Background thread loop that flushes when the batch sized reached or max time interval passed."""
        last_flush_time = time.time()
        while not self._shutdown_event.wait(timeout=1):
            if (
                self._event_queue.qsize() >= self._max_batch_size
                or time.time() - last_flush_time >= self._max_emit_interval_sec
            ):
                self.flush()
                last_flush_time = time.time()

    def _get_next_event_order(self) -> int:
        with self._event_order_count_lock:
            self._event_order_count += 1
            return self._event_order_count


class NoOpTelemetryDispatcher(TelemetryDispatcher):
    def add_event(self, event: ClientEvent) -> None:
        pass

    def flush(self) -> None:
        pass

    def shutdown(self, flush: bool = True) -> None:
        pass
