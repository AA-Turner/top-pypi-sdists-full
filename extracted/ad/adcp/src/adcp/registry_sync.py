"""Registry change feed synchronization."""

from __future__ import annotations

import asyncio
import json
import logging
from collections import defaultdict
from collections.abc import Awaitable, Callable
from fnmatch import fnmatch
from pathlib import Path
from typing import TYPE_CHECKING, Protocol, runtime_checkable

from adcp.exceptions import RegistryError

if TYPE_CHECKING:
    from adcp.registry import RegistryClient

from adcp.types.registry import FeedEvent

logger = logging.getLogger(__name__)

# Type alias for change handlers
ChangeHandler = Callable[[FeedEvent], Awaitable[None]]


@runtime_checkable
class CursorStore(Protocol):
    """Protocol for persisting the feed cursor."""

    async def load(self) -> str | None:
        """Load the saved cursor, or None if no cursor exists."""
        ...

    async def save(self, cursor: str) -> None:
        """Save the current cursor."""
        ...


class FileCursorStore:
    """Default cursor store using a local JSON file.

    Args:
        path: Path to the cursor file. Defaults to .adcp-sync-cursor.json
    """

    def __init__(self, path: str | Path = ".adcp-sync-cursor.json") -> None:
        self._path = Path(path)

    async def load(self) -> str | None:
        try:
            data = json.loads(self._path.read_text())
            return data.get("cursor")  # type: ignore[no-any-return]
        except (FileNotFoundError, json.JSONDecodeError, KeyError):
            return None

    async def save(self, cursor: str) -> None:
        temp = self._path.with_suffix(".tmp")
        temp.write_text(json.dumps({"cursor": cursor}))
        temp.replace(self._path)  # Atomic rename


class RegistrySync:
    """Polls the registry change feed and dispatches events to handlers.

    Args:
        client: RegistryClient instance for HTTP calls.
        auth_token: Bearer token for feed access.
        poll_interval: Seconds between polls (default 60).
        cursor_store: Optional CursorStore for persistence.
            Defaults to FileCursorStore.
        types: Optional event type filter (e.g., "property.*,agent.*").
        batch_size: Max events per poll (default 100, max 10000).
    """

    def __init__(
        self,
        client: RegistryClient,
        *,
        auth_token: str,
        poll_interval: float = 60.0,
        cursor_store: CursorStore | None = None,
        types: str | None = None,
        batch_size: int = 100,
    ) -> None:
        self._client = client
        self._auth_token = auth_token
        self._poll_interval = poll_interval
        self._cursor_store: CursorStore = cursor_store or FileCursorStore()
        self._types = types
        self._batch_size = min(batch_size, 10000)
        self._handlers: dict[str, list[ChangeHandler]] = defaultdict(list)
        self._all_handlers: list[ChangeHandler] = []
        self._cursor: str | None = None
        self._cursor_loaded = False
        self._stop_event: asyncio.Event | None = None
        self._running = False

    def on(self, event_type: str, handler: ChangeHandler) -> None:
        """Register a handler for a specific event type.

        Supports glob patterns: "property.*" matches "property.created",
        "property.updated", etc.
        """
        self._handlers[event_type].append(handler)

    def on_all(self, handler: ChangeHandler) -> None:
        """Register a handler for all events."""
        self._all_handlers.append(handler)

    @property
    def cursor(self) -> str | None:
        """Current cursor position."""
        return self._cursor

    async def _load_cursor(self) -> None:
        """Load cursor from store on first use."""
        if not self._cursor_loaded:
            self._cursor = await self._cursor_store.load()
            self._cursor_loaded = True

    async def _dispatch(self, event: FeedEvent) -> None:
        """Dispatch a single event to matching handlers."""
        # Dispatch to type-specific handlers
        for pattern, handlers in self._handlers.items():
            if fnmatch(event.event_type, pattern):
                for handler in handlers:
                    try:
                        await handler(event)
                    except Exception:
                        logger.exception(
                            "Handler error for event %s (%s)",
                            event.event_id,
                            event.event_type,
                        )

        # Dispatch to catch-all handlers
        for handler in self._all_handlers:
            try:
                await handler(event)
            except Exception:
                logger.exception(
                    "Handler error for event %s (%s)",
                    event.event_id,
                    event.event_type,
                )

    async def poll_once(self) -> list[FeedEvent]:
        """Poll the feed once and dispatch events.

        Returns the list of events processed.
        """
        await self._load_cursor()

        try:
            page = await self._client.get_feed(
                auth_token=self._auth_token,
                cursor=self._cursor,
                types=self._types,
                limit=self._batch_size,
            )
        except RegistryError as e:
            if e.status_code == 410:
                logger.warning("Feed cursor expired, resetting to start")
                self._cursor = None
                await self._cursor_store.save("")
                return []
            raise

        for event in page.events:
            await self._dispatch(event)

        if page.cursor:
            self._cursor = page.cursor
            await self._cursor_store.save(page.cursor)

        return list(page.events)

    async def start(self) -> None:
        """Start the polling loop. Runs until stop() is called."""
        if self._running:
            return

        self._running = True
        self._stop_event = asyncio.Event()
        logger.info("RegistrySync started (interval=%.1fs)", self._poll_interval)

        try:
            while not self._stop_event.is_set():
                try:
                    events = await self.poll_once()
                    if events:
                        logger.debug("Processed %d events", len(events))
                except RegistryError as e:
                    logger.error("Feed poll failed: %s", e)
                except Exception:
                    logger.exception("Unexpected error in feed poll")

                # Wait for interval or stop signal
                try:
                    await asyncio.wait_for(
                        self._stop_event.wait(),
                        timeout=self._poll_interval,
                    )
                except asyncio.TimeoutError:
                    pass  # Normal - poll interval elapsed
        finally:
            self._running = False
            logger.info("RegistrySync stopped")

    async def stop(self) -> None:
        """Stop the polling loop gracefully."""
        if self._stop_event is not None:
            self._stop_event.set()
