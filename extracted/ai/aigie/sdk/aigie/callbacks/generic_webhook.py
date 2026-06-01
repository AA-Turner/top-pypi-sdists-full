"""
Generic Webhook Callback

Send Aigie span/trace data to any HTTP endpoint.
Inspired by LiteLLM's GenericAPILogger.

Usage:
    from aigie.callbacks import GenericWebhookCallback

    # Basic usage
    webhook = GenericWebhookCallback(
        endpoint="https://my-logging-service.com/ingest",
    )

    # With authentication and custom settings
    webhook = GenericWebhookCallback(
        endpoint="https://api.example.com/logs",
        headers={"Authorization": "Bearer my-token"},
        batch_size=50,
        flush_interval=5.0,
        timeout=10.0,
        include_raw_messages=False,  # Exclude full message content
    )

    # Add to aigie
    import aigie
    aigie.add_callback(webhook)
"""

import asyncio
import contextlib
import json
import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

import httpx

from ..exceptions import WebhookError
from .base import BaseCallback, CallbackEvent, CallbackEventType

logger = logging.getLogger(__name__)


@dataclass
class WebhookConfig:
    """Configuration for the webhook callback."""

    # Required
    endpoint: str

    # Authentication
    headers: dict[str, str] = field(default_factory=dict)

    # Batching
    batch_size: int = 100
    flush_interval: float = 5.0  # seconds

    # HTTP settings
    timeout: float = 30.0  # seconds
    max_retries: int = 3
    retry_delay: float = 1.0  # seconds

    # Content filtering
    include_raw_messages: bool = True
    include_response: bool = True
    event_types: set[CallbackEventType] | None = None  # None = all events

    # Error handling
    fail_silently: bool = True  # Don't raise exceptions on errors

    # Compression
    compress: bool = False  # Use gzip compression


class GenericWebhookCallback(BaseCallback):
    """
    Generic webhook callback for sending events to any HTTP endpoint.

    This callback buffers events and sends them in batches to reduce
    HTTP overhead. It supports authentication, retries, compression,
    and flexible event filtering.

    The webhook receives POST requests with JSON body:
    {
        "events": [
            {
                "event_type": "span_end",
                "event_id": "...",
                "timestamp": "2024-01-15T10:30:00Z",
                "trace_id": "...",
                "span_id": "...",
                ...
            },
            ...
        ],
        "batch_id": "...",
        "sent_at": "2024-01-15T10:30:05Z",
        "source": "aigie-sdk",
        "version": "0.2.2"
    }
    """

    def __init__(
        self,
        endpoint: str,
        headers: dict[str, str] | None = None,
        batch_size: int = 100,
        flush_interval: float = 5.0,
        timeout: float = 30.0,
        max_retries: int = 3,
        include_raw_messages: bool = True,
        include_response: bool = True,
        event_types: list[str] | None = None,
        fail_silently: bool = True,
        compress: bool = False,
        name: str | None = None,
    ):
        """
        Initialize the webhook callback.

        Args:
            endpoint: URL to send events to
            headers: Optional HTTP headers (e.g., for authentication)
            batch_size: Number of events to buffer before sending
            flush_interval: Seconds between automatic flushes
            timeout: HTTP request timeout in seconds
            max_retries: Number of retry attempts on failure
            include_raw_messages: Include full message content in events
            include_response: Include full response content in events
            event_types: List of event types to send (None = all)
            fail_silently: Don't raise exceptions on send errors
            compress: Use gzip compression for requests
            name: Optional name for this callback
        """
        super().__init__(name=name or f"webhook:{endpoint}")

        # Parse event types
        parsed_event_types = None
        if event_types:
            parsed_event_types = {
                CallbackEventType(et) if isinstance(et, str) else et for et in event_types
            }

        self.config = WebhookConfig(
            endpoint=endpoint,
            headers=headers or {},
            batch_size=batch_size,
            flush_interval=flush_interval,
            timeout=timeout,
            max_retries=max_retries,
            include_raw_messages=include_raw_messages,
            include_response=include_response,
            event_types=parsed_event_types,
            fail_silently=fail_silently,
            compress=compress,
        )

        # Event buffer
        self._buffer: list[CallbackEvent] = []
        self._buffer_lock = asyncio.Lock()

        # HTTP client
        self._client: httpx.AsyncClient | None = None

        # Background flush task
        self._flush_task: asyncio.Task | None = None
        self._shutdown = False

        # Stats
        self._events_sent = 0
        self._events_failed = 0
        self._batches_sent = 0
        self._last_error: str | None = None

    async def initialize(self) -> None:
        """Initialize the HTTP client and start background flush task."""
        self._client = httpx.AsyncClient(
            timeout=self.config.timeout,
            headers={
                "Content-Type": "application/json",
                "User-Agent": "aigie-sdk/0.2.2",
                **self.config.headers,
            },
        )

        # Start background flush task
        self._shutdown = False
        self._flush_task = asyncio.create_task(self._background_flush())
        logger.info(f"GenericWebhookCallback initialized: {self.config.endpoint}")

    async def shutdown(self) -> None:
        """Shutdown the callback, flushing any remaining events."""
        self._shutdown = True

        # Cancel background task
        if self._flush_task:
            self._flush_task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await self._flush_task

        # Final flush
        await self.flush()

        # Close client
        if self._client:
            await self._client.aclose()
            self._client = None

        logger.info(
            f"GenericWebhookCallback shutdown: "
            f"sent={self._events_sent}, failed={self._events_failed}"
        )

    async def on_event(self, event: CallbackEvent) -> None:
        """Buffer an event for sending."""
        if not self.enabled:
            return

        # Filter by event type
        if self.config.event_types and event.event_type not in self.config.event_types:
            return

        # Filter content if configured
        if not self.config.include_raw_messages:
            event.messages = None
        if not self.config.include_response:
            event.response = None

        async with self._buffer_lock:
            self._buffer.append(event)

            # Flush if buffer is full
            if len(self._buffer) >= self.config.batch_size:
                await self._flush_buffer()

    async def flush(self) -> None:
        """Manually flush all buffered events."""
        async with self._buffer_lock:
            await self._flush_buffer()

    async def _flush_buffer(self) -> None:
        """Internal method to flush the buffer. Must be called with lock held."""
        if not self._buffer:
            return

        events = self._buffer.copy()
        self._buffer.clear()

        await self._send_events(events)

    async def _send_events(self, events: list[CallbackEvent]) -> None:
        """Send events to the webhook endpoint."""
        if not self._client:
            if not self.config.fail_silently:
                raise WebhookError("Webhook client not initialized")
            logger.warning("Webhook client not initialized, dropping events")
            return

        if not events:
            return

        # Build request payload
        import uuid

        from .. import __version__

        payload = {
            "events": [e.to_dict() for e in events],
            "batch_id": str(uuid.uuid4()),
            "sent_at": datetime.utcnow().isoformat(),
            "source": "aigie-sdk",
            "version": __version__,
            "event_count": len(events),
        }

        # Prepare content
        content = json.dumps(payload, default=str).encode("utf-8")
        headers = {}

        # Optionally compress
        if self.config.compress:
            import gzip

            content = gzip.compress(content)
            headers["Content-Encoding"] = "gzip"

        # Send with retries
        last_error = None
        for attempt in range(self.config.max_retries):
            try:
                response = await self._client.post(
                    self.config.endpoint,
                    content=content,
                    headers=headers,
                )

                if response.status_code >= 200 and response.status_code < 300:
                    self._events_sent += len(events)
                    self._batches_sent += 1
                    logger.debug(f"Webhook sent {len(events)} events to {self.config.endpoint}")
                    return

                # Handle specific status codes
                if response.status_code == 429:  # Rate limited
                    retry_after = float(
                        response.headers.get("Retry-After", self.config.retry_delay)
                    )
                    await asyncio.sleep(retry_after)
                    continue

                if response.status_code >= 500:  # Server error, retry
                    last_error = f"HTTP {response.status_code}: {response.text[:200]}"
                    await asyncio.sleep(self.config.retry_delay * (attempt + 1))
                    continue

                # Client error, don't retry
                last_error = f"HTTP {response.status_code}: {response.text[:200]}"
                break

            except httpx.TimeoutException:
                last_error = f"Timeout after {self.config.timeout}s"
                await asyncio.sleep(self.config.retry_delay)
            except httpx.RequestError as e:
                last_error = f"Request error: {e}"
                await asyncio.sleep(self.config.retry_delay)
            except Exception as e:
                last_error = f"Unexpected error: {e}"
                break

        # Failed after all retries
        self._events_failed += len(events)
        self._last_error = last_error
        logger.warning(f"Webhook failed after {self.config.max_retries} attempts: {last_error}")

        if not self.config.fail_silently:
            raise WebhookError(
                f"Failed to send events to {self.config.endpoint}",
                webhook_url=self.config.endpoint,
                attempts=self.config.max_retries,
            )

    async def _background_flush(self) -> None:
        """Background task to periodically flush buffered events."""
        while not self._shutdown:
            try:
                await asyncio.sleep(self.config.flush_interval)
                if not self._shutdown:
                    await self.flush()
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.warning(f"Background flush error: {e}")

    def get_stats(self) -> dict[str, Any]:
        """Get callback statistics."""
        return {
            "endpoint": self.config.endpoint,
            "enabled": self.enabled,
            "events_sent": self._events_sent,
            "events_failed": self._events_failed,
            "batches_sent": self._batches_sent,
            "buffer_size": len(self._buffer),
            "last_error": self._last_error,
        }

    def __repr__(self) -> str:
        return (
            f"GenericWebhookCallback("
            f"endpoint={self.config.endpoint!r}, "
            f"enabled={self.enabled}, "
            f"sent={self._events_sent})"
        )


# Convenience factory functions


def create_webhook(
    endpoint: str,
    api_key: str | None = None,
    bearer_token: str | None = None,
    **kwargs,
) -> GenericWebhookCallback:
    """
    Create a webhook callback with common authentication patterns.

    Args:
        endpoint: Webhook URL
        api_key: API key (added as X-API-Key header)
        bearer_token: Bearer token (added as Authorization header)
        **kwargs: Additional arguments passed to GenericWebhookCallback

    Returns:
        Configured GenericWebhookCallback instance
    """
    headers = kwargs.pop("headers", {})

    if api_key:
        headers["X-API-Key"] = api_key
    if bearer_token:
        headers["Authorization"] = f"Bearer {bearer_token}"

    return GenericWebhookCallback(
        endpoint=endpoint,
        headers=headers,
        **kwargs,
    )


def create_datadog_callback(
    api_key: str,
    site: str = "datadoghq.com",
    service: str = "aigie",
    **kwargs,
) -> GenericWebhookCallback:
    """
    Create a webhook callback for Datadog logs.

    Args:
        api_key: Datadog API key
        site: Datadog site (e.g., "datadoghq.com", "datadoghq.eu")
        service: Service name in Datadog
        **kwargs: Additional arguments

    Returns:
        Configured callback for Datadog
    """
    return GenericWebhookCallback(
        endpoint=f"https://http-intake.logs.{site}/api/v2/logs",
        headers={
            "DD-API-KEY": api_key,
            "Content-Type": "application/json",
        },
        name=f"datadog:{service}",
        **kwargs,
    )


def create_splunk_callback(
    hec_token: str,
    hec_url: str,
    source: str = "aigie",
    **kwargs,
) -> GenericWebhookCallback:
    """
    Create a webhook callback for Splunk HEC.

    Args:
        hec_token: Splunk HEC token
        hec_url: HEC endpoint URL
        source: Source identifier
        **kwargs: Additional arguments

    Returns:
        Configured callback for Splunk
    """
    return GenericWebhookCallback(
        endpoint=hec_url,
        headers={
            "Authorization": f"Splunk {hec_token}",
        },
        name=f"splunk:{source}",
        **kwargs,
    )
