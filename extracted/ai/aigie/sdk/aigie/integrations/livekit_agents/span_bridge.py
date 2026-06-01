"""
OTel Span Bridge — reads OTel span context for intervention hooks.

When telemetry_mode="otel", the trace/span lifecycle is managed by OTel,
not by the handler. Intervention hooks (judge, guardrails, fix) need to
know which trace/span they're operating on. This bridge provides read-only
access to the current OTel context.
"""

import logging
from typing import Any

from .otel_exporter import otel_span_id_to_str, otel_trace_id_to_uuid

logger = logging.getLogger(__name__)


class OTelSpanBridge:
    """
    Read-only bridge between OTel span context and Aigie intervention system.

    Provides trace_id and span_id to intervention hooks without creating
    any new spans or traces.
    """

    def get_trace_id(self) -> str | None:
        """Get current Aigie-format trace ID from OTel context."""
        span = self._get_current_span()
        if span is None:
            return None

        try:
            return otel_trace_id_to_uuid(span.get_span_context().trace_id)
        except Exception:
            return None

    def get_span_id(self) -> str | None:
        """Get current Aigie-format span ID from OTel context."""
        span = self._get_current_span()
        if span is None:
            return None

        try:
            return otel_span_id_to_str(span.get_span_context().span_id)
        except Exception:
            return None

    def get_intervention_context(self) -> dict[str, Any]:
        """
        Build intervention context from current OTel span.

        Returns a dict with trace_id, span_id, and span attributes
        that intervention hooks can use for evaluation and fix application.
        """
        span = self._get_current_span()
        if span is None:
            return {}

        ctx = span.get_span_context()
        attrs = {}

        try:
            if hasattr(span, "attributes") and span.attributes:
                attrs = dict(span.attributes)
        except Exception:
            pass

        return {
            "trace_id": otel_trace_id_to_uuid(ctx.trace_id),
            "span_id": otel_span_id_to_str(ctx.span_id),
            "span_name": getattr(span, "name", ""),
            "attributes": attrs,
        }

    @staticmethod
    def _get_current_span() -> Any | None:
        """Get the current OTel span, or None if unavailable."""
        try:
            from opentelemetry import trace

            span = trace.get_current_span()
            if span and span.get_span_context().trace_id != 0:
                return span
        except ImportError:
            pass
        return None
