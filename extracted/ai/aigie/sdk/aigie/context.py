"""
W3C Trace Context propagation for distributed tracing.

Implements W3C Trace Context standard for propagating trace context
across service boundaries (HTTP headers, message queues, etc.).
"""

from typing import Any, Optional
from uuid import uuid4


class TraceContext:
    """
    W3C Trace Context representation.

    Implements the W3C Trace Context standard for distributed tracing.
    See: https://www.w3.org/TR/trace-context/
    """

    def __init__(
        self,
        trace_id: str | None = None,
        parent_id: str | None = None,
        trace_flags: int = 1,  # 1 = sampled
        trace_state: str | None = None,
    ):
        """
        Initialize trace context.

        Args:
            trace_id: 32-character hex trace ID (16 bytes)
            parent_id: 16-character hex span ID (8 bytes)
            trace_flags: Trace flags (1 = sampled, 0 = not sampled)
            trace_state: Optional trace state string
        """
        self.trace_id = trace_id or self._generate_trace_id()
        self.parent_id = parent_id
        self.trace_flags = trace_flags
        self.trace_state = trace_state or ""

    @staticmethod
    def _generate_trace_id() -> str:
        """Generate a 32-character hex trace ID."""
        return format(uuid4().int & (1 << 128) - 1, "032x")

    @staticmethod
    def _generate_span_id() -> str:
        """Generate a 16-character hex span ID."""
        return format(uuid4().int & (1 << 64) - 1, "016x")

    def create_child(self) -> "TraceContext":
        """Create a child trace context with new parent_id."""
        return TraceContext(
            trace_id=self.trace_id,
            parent_id=self._generate_span_id(),
            trace_flags=self.trace_flags,
            trace_state=self.trace_state,
        )

    def to_headers(self) -> dict[str, str]:
        """
        Convert to W3C trace context headers.

        Returns:
            Dictionary with 'traceparent' and optionally 'tracestate' headers
        """
        # Format: version-trace_id-parent_id-trace_flags
        # version = 00 (current version)
        traceparent = f"00-{self.trace_id}-{self.parent_id or '0' * 16}-{self.trace_flags:02x}"

        headers = {"traceparent": traceparent}

        if self.trace_state:
            headers["tracestate"] = self.trace_state

        return headers

    @classmethod
    def from_headers(cls, headers: dict[str, str]) -> Optional["TraceContext"]:
        """
        Parse W3C trace context from HTTP headers.

        Args:
            headers: Dictionary of HTTP headers (case-insensitive)

        Returns:
            TraceContext if valid headers found, None otherwise
        """
        # Normalize header names (HTTP headers are case-insensitive)
        normalized = {k.lower(): v for k, v in headers.items()}

        traceparent = normalized.get("traceparent")
        if not traceparent:
            return None

        try:
            # Parse traceparent: version-trace_id-parent_id-trace_flags
            parts = traceparent.split("-")
            if len(parts) != 4:
                return None

            version, trace_id, parent_id, trace_flags_hex = parts

            # Validate version (must be 00 for now)
            if version != "00":
                return None

            # Validate lengths
            if len(trace_id) != 32 or len(parent_id) != 16:
                return None

            # Parse trace flags
            trace_flags = int(trace_flags_hex, 16)

            # Get tracestate if present
            trace_state = normalized.get("tracestate", "")

            return cls(
                trace_id=trace_id,
                parent_id=parent_id if parent_id != "0" * 16 else None,
                trace_flags=trace_flags,
                trace_state=trace_state,
            )
        except (ValueError, IndexError):
            return None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "trace_id": self.trace_id,
            "parent_id": self.parent_id,
            "trace_flags": self.trace_flags,
            "trace_state": self.trace_state,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "TraceContext":
        """Create from dictionary."""
        return cls(
            trace_id=data.get("trace_id"),
            parent_id=data.get("parent_id"),
            trace_flags=data.get("trace_flags", 1),
            trace_state=data.get("trace_state"),
        )


def extract_trace_context(headers: dict[str, str]) -> TraceContext | None:
    """
    Extract trace context from HTTP headers.

    Convenience function for extracting W3C trace context.

    Args:
        headers: HTTP headers dictionary

    Returns:
        TraceContext if found, None otherwise
    """
    return TraceContext.from_headers(headers)


def inject_trace_context(context: TraceContext) -> dict[str, str]:
    """
    Inject trace context into HTTP headers.

    Convenience function for injecting W3C trace context.

    Args:
        context: TraceContext to inject

    Returns:
        Dictionary of headers to add to HTTP request
    """
    return context.to_headers()
