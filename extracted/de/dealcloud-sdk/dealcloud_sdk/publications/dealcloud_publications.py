"""
Publications API operations for DealCloud.

The Publications API provides real-time event streaming for:
- Data change events (create, update, delete)
- Schema change events
- User events

This enables building real-time integrations and syncing systems.

See: https://api.docs.dealcloud.com/docs - Publications API
"""

from __future__ import annotations

import asyncio
import json
import time
from contextlib import contextmanager
from typing import Awaitable, Callable, Dict, Iterator, List, Optional

import httpx

from intapp_rest_client.exceptions import HttpError

from ..usermanagement.dealcloud_usermanagement import DealCloudUserManagement


class DealCloudPublications(DealCloudUserManagement):
    """
    One link in the linear inheritance chain; parent order is for composition
    (single DealCloud client gets all features), not dependency. Avoids mixins.
    Publications API operations.
    
    Provides real-time event streaming and polling.
    """
    
    @property
    def publications_url(self) -> str:
        """
        Get the Publications API base URL.
        
        Use this for custom publications API calls not covered by SDK methods.
        
        Returns:
            str: Publications API URL (e.g., "https://site.dealcloud.com/api/rest/v1/publication")
        
        Example:
            >>> # Custom publications endpoint call
            >>> url = f"{dc.publications_url}/topics/custom"
            >>> response = dc.client.get(url)
        """
        return self._publications_url
    
    # =========================================================================
    # Topics
    # =========================================================================
    
    def get_topics(self) -> List[str]:
        """
        Get available publication topic names.
        
        The API returns a JSON array of topic name strings.
        
        Returns:
            List of topic names (e.g. ["data", "schema", "user"])
        
        Example:
            topics = dc.get_topics()
            # ["data", "schema", "user"]
        """
        url = f"{self._publications_url}/topics"
        return self._client.get(url)
    
    # =========================================================================
    # Event Polling
    # =========================================================================
    
    @staticmethod
    def _poll_request_body(
        topics: List[str],
        count: int,
        time_out_ms: int,
    ) -> dict:
        return {
            "count": count,
            "topics": topics,
            "timeOut": time_out_ms,
        }
    
    def poll_events(
        self,
        topics: List[str],
        *,
        count: int = 100,
        time_out_ms: int,
        http_timeout_seconds: Optional[float] = None,
    ) -> List[dict]:
        """
        Poll for new events (PollRequestVm: topics, timeOut in ms, count).
        
        Call repeatedly to get new events. Events follow PublicationEventVm
        (eventId, eventGuid, topicName, topicOffset, entityType, modifiedAt, etc.).
        
        **Memory / bootstrap:** The HTTP response is a single JSON array parsed in full
        by the client. After ``init_bootstrap`` (especially for DATA), events can carry
        very large ``payload`` bodies (e.g. many rows across entry types). Prefer a **low**
        ``count`` when draining bootstrap traffic so each response stays bounded, and
        acknowledge frequently. For very large responses, use :meth:`stream_poll_events`
        to read the body incrementally (e.g. spool to disk, or parse with a streaming
        JSON library such as ``ijson``).
        
        Args:
            topics: Topic names to poll (e.g. ``["data"]``). Required; maps to PollRequestVm ``topics``.
            count: Maximum events to return per poll. Use a small value during bootstrap drain.
            time_out_ms: Server-side long-poll wait for events (**milliseconds**); sent as
                PollRequestVm ``timeOut``.
            http_timeout_seconds: Optional client (httpx) timeout for this request (connect + read).
                Increase if a single poll can take a long time to download.
        
        Returns:
            List of event objects (PublicationEventVm).
        
        Example:
            events = dc.poll_events(topics=["data"], count=100, time_out_ms=30_000)
            for e in events:
                print(e["topicName"], e["topicOffset"], e["entityType"])
            if events:
                dc.acknowledge_topic_offsets(
                    dc.topic_offsets_from_events(events)
                )
        """
        url = f"{self._publications_url}/poll"
        payload = self._poll_request_body(topics, count, time_out_ms)
        return self._client.post(url, json=payload, timeout=http_timeout_seconds)
    
    @contextmanager
    def stream_poll_events(
        self,
        topics: List[str],
        *,
        count: int = 100,
        time_out_ms: int,
        http_timeout_seconds: Optional[float] = None,
    ) -> Iterator[httpx.Response]:
        """
        POST ``/poll`` with ``httpx`` response streaming enabled.
        
        The server still returns one JSON array; this method avoids buffering the entire
        response in ``RestClient.post`` before you see it. You can copy bytes incrementally
        (``response.iter_bytes()``) to a file or feed a streaming JSON parser. Calling
        ``response.json()`` after the stream completes loads the full body into memory
        like :meth:`poll_events`.
        
        On HTTP error, reads the error body and raises :class:`~intapp_rest_client.exceptions.HttpError`.
        
        Uses the same underlying httpx client and auth as the rest of the SDK.
        
        Args:
            topics: Topic names to poll (required); same as :meth:`poll_events`.
            time_out_ms: Server long-poll wait (milliseconds); same as :meth:`poll_events`.
        
        Example:
            import fsspec

            with dc.stream_poll_events(topics=["data"], count=10, time_out_ms=30_000) as resp:
                with fsspec.open("poll_chunk.jsonl", "wb") as f:
                    for chunk in resp.iter_bytes():
                        f.write(chunk)
        """
        url = f"{self._publications_url}/poll"
        payload = self._poll_request_body(topics, count, time_out_ms)
        headers: Dict[str, str] = {
            **self._client.default_headers,
            **self._client.get_auth_headers(),
        }
        effective_timeout = (
            http_timeout_seconds
            if http_timeout_seconds is not None
            else self._client.timeout
        )
        sync_client = self._client._get_sync_client()  # noqa: SLF001 — stream API not on RestClient yet
        with sync_client.stream(
            "POST",
            url,
            json=payload,
            headers=headers,
            timeout=effective_timeout,
        ) as response:
            if response.status_code >= 400:
                body_bytes = response.read()
                try:
                    err_body = json.loads(body_bytes) if body_bytes else None
                except json.JSONDecodeError:
                    err_body = body_bytes.decode(errors="replace")[:8000]
                raise HttpError(
                    response.status_code,
                    "Publications poll failed",
                    err_body,
                    dict(response.headers),
                )
            yield response
    
    def topic_offsets_from_events(self, events: List[dict]) -> List[dict]:
        """
        Build TopicVm list (name, offset) from poll response events.
        
        For each topic, uses the maximum topicOffset in the batch so that
        acknowledging up to that offset covers all events in the batch.
        
        Args:
            events: List of PublicationEventVm from poll_events().
        
        Returns:
            List of {"name": topic_name, "offset": offset} for acknowledge.
        """
        by_topic: dict = {}
        for e in events:
            name = e.get("topicName")
            offset = e.get("topicOffset")
            if name is not None and offset is not None:
                by_topic[name] = max(by_topic.get(name, offset), offset)
        return [{"name": k, "offset": v} for k, v in by_topic.items()]
    
    def acknowledge_topic_offsets(self, topic_offsets: List[dict]) -> None:
        """
        Acknowledge by topic and offset (API: array of TopicVm).
        
        Call after successfully processing events. Each item must have
        "name" (topic name) and "offset" (topicOffset from events).
        
        Args:
            topic_offsets: List of {"name": str, "offset": int}.
        
        Returns:
            None (API returns 204 No Content).
        """
        url = f"{self._publications_url}/acknowledge"
        self._client.post(url, json=topic_offsets)
    
    # =========================================================================
    # Bootstrap (OpenAPI: initbootstrap)
    # =========================================================================
    
    def init_bootstrap(
        self,
        entity_type: int,
        entity_format: int,
    ) -> None:
        """
        Request bootstrap (ForceBootstrapRequestVm). API returns 204 No Content.
        
        Args:
            entity_type: PublicationEntityType enum value (0–21 per swagger).
            entity_format: PublicationEntityFormatType enum value (0 or 1).
        """
        url = f"{self._publications_url}/initbootstrap"
        self._client.post(url, json={"entityType": entity_type, "entityFormat": entity_format})
    
    # =========================================================================
    # Subscription Helpers
    # =========================================================================
    
    def subscribe(
        self,
        topics: List[str],
        *,
        callback: Callable[[dict], None],
        time_out_ms: int,
        poll_interval: int = 5,
        count: int = 100,
        auto_acknowledge: bool = True,
    ) -> None:
        """
        Poll in a loop and invoke callback for each event (blocking).
        
        Args:
            topics: Topic names to poll (required).
            callback: Function called for each event.
            time_out_ms: Server long-poll wait per :meth:`poll_events` (required, milliseconds).
            poll_interval: Seconds to sleep between iterations when a poll returns no events.
            count: Max events per poll.
            auto_acknowledge: If True, acknowledge processed batch by topic/offset.
        
        Note:
            On callback error the batch is not acknowledged; events may be redelivered.
            Press Ctrl+C to stop.
        """
        self._logger.info("Starting subscription (topics=%s)", topics)
        try:
            while True:
                events = self.poll_events(
                    topics=topics,
                    count=count,
                    time_out_ms=time_out_ms,
                )
                for event in events:
                    try:
                        callback(event)
                    except Exception as e:
                        self._logger.error("Error processing event: %s", e)
                if auto_acknowledge and events:
                    self.acknowledge_topic_offsets(self.topic_offsets_from_events(events))
                if not events:
                    time.sleep(poll_interval)
        except KeyboardInterrupt:
            self._logger.info("Subscription stopped by user")
    
    async def subscribe_async(
        self,
        topics: List[str],
        *,
        callback: Callable[[dict], Awaitable[None]],
        time_out_ms: int,
        poll_interval: int = 5,
        count: int = 100,
        auto_acknowledge: bool = True,
    ) -> None:
        """
        Poll in a loop and invoke async callback for each event.
        
        Args:
            topics: Topic names to poll (required).
            callback: Async function called for each event.
            time_out_ms: Server long-poll wait per :meth:`poll_events` (required, milliseconds).
            poll_interval: Seconds to sleep between iterations when a poll returns no events.
            count: Max events per poll.
            auto_acknowledge: If True, acknowledge processed batch by topic/offset.
        """
        self._logger.info("Starting async subscription (topics=%s)", topics)
        try:
            while True:
                events = self.poll_events(
                    topics=topics,
                    count=count,
                    time_out_ms=time_out_ms,
                )
                for event in events:
                    try:
                        await callback(event)
                    except Exception as e:
                        self._logger.error("Error processing event: %s", e)
                if auto_acknowledge and events:
                    self.acknowledge_topic_offsets(self.topic_offsets_from_events(events))
                if not events:
                    await asyncio.sleep(poll_interval)
        except asyncio.CancelledError:
            self._logger.info("Async subscription cancelled")


