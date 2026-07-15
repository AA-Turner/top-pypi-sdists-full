from __future__ import annotations

import os
from collections.abc import Callable
from importlib import import_module
from typing import cast


def _load_otel_inject() -> Callable[[dict[str, str]], object] | None:
    try:
        module = import_module("opentelemetry.propagate")
    except Exception:  # pragma: no cover
        return None
    inject = getattr(module, "inject", None)
    if not callable(inject):
        return None
    return cast("Callable[[dict[str, str]], object]", inject)


_otel_inject = _load_otel_inject()


def _generate_traceparent() -> str:
    """Build a W3C traceparent header with a random trace id and span id."""
    trace_id = os.urandom(16).hex()
    span_id = os.urandom(8).hex()
    return f"00-{trace_id}-{span_id}-01"


def trace_headers() -> dict[str, str]:
    """Return W3C trace-context headers for an outbound request."""
    headers: dict[str, str] = {}
    if _otel_inject is not None:
        try:
            _otel_inject(headers)
        except Exception:
            headers = {}
    if "traceparent" not in headers:
        headers["traceparent"] = _generate_traceparent()
    return headers
