from __future__ import annotations

from collections.abc import Callable
from typing import Any, Literal, NamedTuple, Protocol

from bitfab.compress import PreparedRequest

TraceOperation = Literal["external_span", "external_trace", "internal_trace"]

# Takes an ALREADY-ENCODED request body and a timeout, and returns once the
# server has accepted it whole. Supplied by the HTTP client, which owns the
# endpoint, the auth, and what the server's answer means: a rejection arrives
# as a DeliveryError, so the transport decides whether to retry without ever
# reading a response.
#
# The request arrives already encoded, carrying its own content encoding
# and byte counts: the exporter assembles it from per-span
# encodes it has to produce anyway to size a request, so passing a dict here
# would encode the same batch twice.
DirectBatchSender = Callable[[PreparedRequest, float], None]


class DeliveryError(Exception):
    """Why a delivery failed, in the only two terms the transport acts on.

    A sender classifies everything it can see, including a network fault
    carrying no verdict; anything else reaching the transport is a fault in the
    sender and is not retried.
    """

    def __init__(
        self,
        message: str,
        *,
        retryable: bool = False,
        oversized: bool = False,
        retry_after_ms: float | None = None,
    ) -> None:
        super().__init__(message)
        self.retryable = retryable
        self.oversized = oversized
        # How long the server asked us to wait, when it said so.
        self.retry_after_ms = retry_after_ms


class CarrierRef(NamedTuple):
    """Which carrier a payload is, for delivery accounting only. Supplied by the
    caller that built the payload: the transport never reads inside one.

    ``span_id`` is None for the carrier that closes a trace, which is what tells
    the transport the trace's expected set has stopped growing.
    """

    trace_id: str
    span_id: str | None = None


class CarrierMeta(NamedTuple):
    """Everything the transport needs to know ABOUT a payload without reading
    one. Supplied by the caller that built it; each field falls back to
    something the transport can decide without looking inside.
    """

    # Delivery identity. None for carriers nobody accounts for.
    ref: CarrierRef | None = None
    # Carrier span name. None defaults to ``bitfab.<operation>``.
    name: str | None = None
    # Nanoseconds since the epoch. None lets OTel stamp the carrier itself.
    start_time_ns: int | None = None
    end_time_ns: int | None = None
    # Marks the carrier span errored.
    errored: bool = False


class TraceTransport(Protocol):
    def submit(
        self,
        operation: TraceOperation,
        payload: dict[str, Any],
        encoded_payload: str | None = None,
        meta: CarrierMeta | None = None,
    ) -> None: ...

    def flush(self, timeout: float = 30.0) -> bool: ...

    def shutdown(self, timeout: float = 30.0) -> bool: ...
