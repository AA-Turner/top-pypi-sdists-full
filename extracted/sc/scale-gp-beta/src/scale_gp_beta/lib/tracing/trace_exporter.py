import time
import logging
from queue import Empty, Queue
from typing import TYPE_CHECKING, List, Callable, Optional
from typing_extensions import TypeAlias

from scale_gp_beta import SGPClient
from scale_gp_beta._exceptions import APIError
from scale_gp_beta.types.span_create_param import SpanCreateParam as SpanCreateRequest

from .exceptions import ParamsCreationError

if TYPE_CHECKING:
    from .tracing import Span

INITIAL_BACKOFF = 0.4
MAX_BACKOFF = 20

log: logging.Logger = logging.getLogger(__name__)

SpanRequestBatch: TypeAlias = List[SpanCreateRequest]


class TraceExporter:
    def __init__(
        self,
        max_batch_size: int,
        max_retries: int,
        backoff: float = INITIAL_BACKOFF,
        max_backoff: float = MAX_BACKOFF,
        export_fn: Optional[Callable[[SpanRequestBatch], None]] = None,
    ):
        self.max_batch_size = max_batch_size
        self.max_retries = max_retries
        self.backoff = backoff
        self.max_backoff = max_backoff
        self.export_fn = export_fn

    def export_span(self, client: SGPClient, span: "Span") -> None:
        # only upsert endpoint is batch upsert, so we work in batches
        batch: SpanRequestBatch = self._create_one_span_batch(span)

        log.info(f"Exporting single span with id {span.span_id}")
        self._export_batch(batch, client)

    def export(self, client: SGPClient, queue: "Queue[Span]") -> None:
        # this is also thread safe, two threads can call this method with the same queue at once
        # the ordering of the requests might be randomly split between the two threads, but they should all be picked up
        batches: list[SpanRequestBatch] = self._create_batches(queue)

        if not batches:
            log.debug("No new span batches to export")
            return

        log.info(f"Exporting {len(batches)} span batches")

        for batch in batches:
            self._export_batch(batch, client)

    def _export_batch(self, batch: SpanRequestBatch, client: SGPClient) -> None:
        attempts_remaining = self.max_retries
        backoff_delay = self.backoff

        def sleep_with_backoff() -> float:
            time.sleep(backoff_delay)
            return min(backoff_delay * 2, self.max_backoff)

        while attempts_remaining > 0:
            attempts_remaining -= 1
            try:
                if self.export_fn is not None:
                    self.export_fn(batch)
                else:
                    client.spans.upsert_batch(items=batch)
                return
            except APIError as e:
                log.warning(
                    f"API error occurred while exporting batch: {e.message}, attempts remaining: {attempts_remaining}"
                )
                if attempts_remaining == 0:
                    continue
                backoff_delay = sleep_with_backoff()
            except Exception as e:
                if self.export_fn is None:
                    raise
                log.warning(
                    f"export_fn raised an unexpected error: {e}, attempts remaining: {attempts_remaining}"
                )
                if attempts_remaining == 0:
                    continue
                backoff_delay = sleep_with_backoff()

        log.error(f"Failed to export span batch after {self.max_retries} attempts, dropping...")

    def _create_batches(self, queue: "Queue[Span]") -> "list[SpanRequestBatch]":
        """Drain the queue and return a list of batches"""
        batches: list[SpanRequestBatch] = []

        while True:
            span_batch: SpanRequestBatch = []

            while len(span_batch) < self.max_batch_size and queue.qsize() > 0:
                try:
                    span: "Span" = queue.get_nowait()
                    self._add_span_to_batch(span, span_batch)
                except Empty:
                    break

            if not span_batch:
                break
            batches.append(span_batch)

        return batches

    def _create_one_span_batch(self, span: "Span") -> SpanRequestBatch:
        span_batch: SpanRequestBatch = []
        self._add_span_to_batch(span, span_batch)

        return span_batch

    def _add_span_to_batch(self, span: "Span", span_batch: SpanRequestBatch) -> None:
        try:
            span_request = span.to_request_params()
            span_batch.append(span_request)
        except ParamsCreationError as e:
            log.warning(f"ParamsCreationError: dropping span: {span}\n{e}")
