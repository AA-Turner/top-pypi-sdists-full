"""
Streaming support for real-time monitoring.

Allows streaming span updates as they happen.
"""

from collections.abc import Callable
from typing import Any


class StreamingSpan:
    """
    Span that supports streaming output.

    Usage:
        async with trace.span("llm_call", stream=True) as span:
            async for chunk in llm.astream("Hello"):
                span.append_output(chunk)
                yield chunk
    """

    def __init__(self, span_context: Any, stream: bool = False):
        """
        Initialize streaming span.

        Args:
            span_context: Underlying SpanContext
            stream: Whether to enable streaming
        """
        from datetime import datetime

        self._span = span_context
        self._stream = stream
        self._output_chunks: list[Any] = []
        self._update_callbacks: list[Callable] = []

        # TTFT (Time To First Token) tracking
        self._first_token_time: datetime | None = None
        self._request_start_time: datetime | None = None
        self._ttft_ms: float | None = None

    def append_output(self, chunk: Any) -> None:
        """
        Append output chunk to span.

        Args:
            chunk: Output chunk to append
        """
        from datetime import datetime

        # Track TTFT on first chunk
        if self._first_token_time is None:
            self._first_token_time = datetime.utcnow()
            if self._request_start_time:
                delta = self._first_token_time - self._request_start_time
                self._ttft_ms = delta.total_seconds() * 1000

        self._output_chunks.append(chunk)

        # Update span output
        if hasattr(self._span, "_output"):
            if isinstance(self._span._output, list):
                self._span._output.append(chunk)
            elif isinstance(self._span._output, dict):
                # If output is dict, try to append to a list field
                if "chunks" not in self._span._output:
                    self._span._output["chunks"] = []
                self._span._output["chunks"].append(chunk)
            else:
                # Convert to list
                self._span._output = [self._span._output, chunk]

        # Call update callbacks
        for callback in self._update_callbacks:
            try:
                callback(chunk)
            except Exception:
                pass  # Don't fail on callback errors

    def on_update(self, callback: Callable) -> None:
        """
        Register callback for output updates.

        Args:
            callback: Function to call when output is appended
        """
        self._update_callbacks.append(callback)

    async def __aenter__(self):
        """Enter context manager."""
        from datetime import datetime

        # Capture request start time for TTFT calculation
        self._request_start_time = datetime.utcnow()

        await self._span.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Exit context manager."""
        # Finalize output
        if self._output_chunks and hasattr(self._span, "set_output"):
            # Combine all chunks
            if isinstance(self._span._output, list):
                final_output = "".join(str(chunk) for chunk in self._span._output)
            else:
                final_output = self._span._output

            self._span.set_output({"output": final_output, "chunks": self._output_chunks})

        # Add streaming and TTFT metadata
        if hasattr(self._span, "_metadata"):
            streaming_metadata = {"streaming": True, "chunk_count": len(self._output_chunks)}
            if self._first_token_time:
                streaming_metadata["completion_start_time"] = self._first_token_time.isoformat()
            if self._ttft_ms is not None:
                streaming_metadata["ttft_ms"] = self._ttft_ms

            # Merge with existing metadata
            self._span._metadata.update(streaming_metadata)

        return await self._span.__aexit__(exc_type, exc_val, exc_tb)

    @property
    def id(self) -> str | None:
        """Get span ID."""
        return self._span.id if hasattr(self._span, "id") else None

    def set_input(self, data: dict[str, Any]) -> None:
        """Set span input."""
        if hasattr(self._span, "set_input"):
            self._span.set_input(data)

    def set_output(self, data: dict[str, Any]) -> None:
        """Set span output."""
        if hasattr(self._span, "set_output"):
            self._span.set_output(data)

    def set_metadata(self, data: dict[str, Any]) -> None:
        """Set span metadata."""
        if hasattr(self._span, "set_metadata"):
            self._span.set_metadata(data)

    async def complete(self, status: str = "success", error: Exception | None = None) -> None:
        """
        Manually complete the span.

        Delegates to the underlying SpanContext's complete() method.

        Args:
            status: Span status (success, failure)
            error: Optional error exception
        """
        if hasattr(self._span, "complete"):
            await self._span.complete(status=status, error=error)
