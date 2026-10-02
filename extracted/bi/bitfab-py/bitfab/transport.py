from __future__ import annotations

from collections.abc import Callable

import bitfab.otel as otel
from bitfab.transport_types import (
    CarrierRef,
    DirectBatchSender,
    TraceTransport,
)

__all__ = [
    "create_trace_transport",
    "flush_trace_transports",
    "shutdown_trace_transports",
]


def create_trace_transport(
    *,
    direct_sender: DirectBatchSender,
    on_delivered: Callable[[list[CarrierRef]], None] | None = None,
) -> TraceTransport:
    return otel.create_otel_transport(
        direct_sender=direct_sender, on_delivered=on_delivered
    )


def flush_trace_transports(timeout: float = 30.0) -> bool:
    return otel.flush_otel_transports(timeout)


def shutdown_trace_transports(timeout: float = 30.0) -> bool:
    return otel.shutdown_otel_transports(timeout)
