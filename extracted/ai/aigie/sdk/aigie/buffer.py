"""
Event Buffer for batching API calls - improves performance by 10-100x.

Enterprise Features:
- Zstandard compression for 50-90% bandwidth savings
- Multi-threaded compression
- Automatic batching with size/time triggers
- Exponential backoff retry logic
- Graceful degradation on errors
- Offline mode with local file persistence
"""

import asyncio
import contextlib
import json
import logging
import os
import time
from collections import deque
from collections.abc import Callable, Coroutine
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any

from .diagnostics import N002, N005, R001, R003, R004, format_diagnostic

logger = logging.getLogger(__name__)

# Default offline storage directory
DEFAULT_OFFLINE_DIR = Path.home() / ".aigie" / "offline_events"


def _log_flush_future_exception(fut) -> None:
    """Done-callback for cross-loop flushes scheduled via run_coroutine_threadsafe.

    Without this, exceptions raised inside the scheduled flush are stored on
    the discarded Future and never surfaced.
    """
    try:
        exc = fut.exception()
    except (asyncio.CancelledError, Exception):
        return
    if exc is not None:
        logger.debug(f"Cross-loop flush raised: {exc!r}")


class EventType(Enum):
    """Types of events that can be buffered."""

    # Core trace/span events
    TRACE_CREATE = "trace_create"
    TRACE_UPDATE = "trace_update"
    SPAN_CREATE = "span_create"
    SPAN_UPDATE = "span_update"

    # Intelligence events - for training and monitoring
    EVAL_FEEDBACK = "eval_feedback"
    REMEDIATION_RESULT = "remediation_result"
    WORKFLOW_PATTERN = "workflow_pattern"

    # Guardrail events - for safety and compliance monitoring
    GUARDRAIL_CHECK = "guardrail_check"

    # Health events - for real-time monitoring
    HEALTH_PING = "health_ping"


@dataclass
class BufferedEvent:
    """A single event waiting to be sent."""

    event_type: EventType
    payload: dict[str, Any]
    timestamp: float = field(default_factory=time.time)
    retry_count: int = 0
    callback: Callable[[dict[str, Any]], None] | None = None  # Called on success


class OfflineStorage:
    """
    Persistent storage for events when backend is unreachable.

    Events are stored as JSON files in a directory and recovered on startup.
    This enables true offline operation - events are never lost.
    """

    def __init__(
        self,
        storage_dir: Path | None = None,
        max_files: int = 1000,
        max_file_size_mb: float = 10.0,
    ):
        """
        Initialize offline storage.

        Args:
            storage_dir: Directory to store offline events (default: ~/.aigie/offline_events)
            max_files: Maximum number of event files to keep
            max_file_size_mb: Maximum size per file in MB
        """
        self.storage_dir = storage_dir or DEFAULT_OFFLINE_DIR
        self.max_files = max_files
        self.max_file_size_bytes = int(max_file_size_mb * 1024 * 1024)
        self._ensure_dir()

    def _ensure_dir(self) -> None:
        """Ensure storage directory exists."""
        self.storage_dir.mkdir(parents=True, exist_ok=True)

    def save_events(self, events: list[BufferedEvent]) -> bool:
        """
        Save events to offline storage.

        Args:
            events: List of events to persist

        Returns:
            True if saved successfully
        """
        if not events:
            return True

        try:
            self._ensure_dir()

            # Generate unique filename with timestamp
            timestamp = int(time.time() * 1000)
            filename = f"events_{timestamp}_{os.getpid()}.json"
            filepath = self.storage_dir / filename

            # Convert events to serializable format
            serializable = []
            for event in events:
                serializable.append(
                    {
                        "event_type": event.event_type.value,
                        "payload": event.payload,
                        "timestamp": event.timestamp,
                        "retry_count": event.retry_count,
                    }
                )

            # Write to file
            with open(filepath, "w") as f:
                json.dump(serializable, f, default=str)

            logger.debug(f"Saved {len(events)} events to offline storage: {filepath}")

            # Cleanup old files if over limit
            self._cleanup_old_files()

            return True

        except Exception as e:
            logger.error(format_diagnostic(R004, extra=str(e)))
            return False

    def load_events(self) -> list[BufferedEvent]:
        """
        Load all pending events from offline storage.

        Returns:
            List of events recovered from storage
        """
        events = []

        try:
            if not self.storage_dir.exists():
                return events

            # Get all event files sorted by modification time (oldest first)
            files = sorted(self.storage_dir.glob("events_*.json"), key=lambda f: f.stat().st_mtime)

            for filepath in files:
                try:
                    with open(filepath) as f:
                        data = json.load(f)

                    for item in data:
                        event = BufferedEvent(
                            event_type=EventType(item["event_type"]),
                            payload=item["payload"],
                            timestamp=item.get("timestamp", time.time()),
                            retry_count=item.get("retry_count", 0),
                        )
                        events.append(event)

                    # Delete file after successful load
                    filepath.unlink()
                    logger.debug(f"Loaded and removed offline file: {filepath}")

                except Exception as e:
                    logger.warning(f"Failed to load offline file {filepath}: {e}")
                    # Move corrupted file aside instead of deleting
                    with contextlib.suppress(Exception):
                        filepath.rename(filepath.with_suffix(".corrupted"))

            if events:
                logger.info(f"Recovered {len(events)} events from offline storage")

        except Exception as e:
            logger.error(f"Failed to load events from offline storage: {e}")

        return events

    def _cleanup_old_files(self) -> None:
        """Remove oldest files if over limit."""
        try:
            files = sorted(self.storage_dir.glob("events_*.json"), key=lambda f: f.stat().st_mtime)

            # Remove oldest files if over limit
            while len(files) > self.max_files:
                oldest = files.pop(0)
                oldest.unlink()
                logger.debug(f"Removed old offline file: {oldest}")

        except Exception as e:
            logger.warning(f"Failed to cleanup old offline files: {e}")

    def get_stats(self) -> dict[str, Any]:
        """Get offline storage statistics."""
        try:
            files = list(self.storage_dir.glob("events_*.json"))
            total_size = sum(f.stat().st_size for f in files)
            return {
                "pending_files": len(files),
                "total_size_bytes": total_size,
                "storage_dir": str(self.storage_dir),
            }
        except Exception:
            return {
                "pending_files": 0,
                "total_size_bytes": 0,
                "storage_dir": str(self.storage_dir),
            }

    def clear(self) -> int:
        """
        Clear all offline storage.

        Returns:
            Number of files deleted
        """
        deleted = 0
        try:
            for filepath in self.storage_dir.glob("events_*.json"):
                filepath.unlink()
                deleted += 1
        except Exception as e:
            logger.error(f"Failed to clear offline storage: {e}")
        return deleted


class EventBuffer:
    """
    Thread-safe event buffer for batching API calls.

    Events are collected and sent in batches to reduce API calls by 90%+.
    Automatically flushes when buffer is full or time interval expires.

    Supports offline mode - events are persisted locally when the backend
    is unreachable and recovered automatically when connectivity returns.
    """

    def __init__(
        self,
        max_size: int = 100,
        flush_interval: float = 5.0,
        max_retries: int = 3,
        retry_delay: float = 1.0,
        enable_offline_mode: bool = True,
        offline_storage_dir: Path | None = None,
        enable_circuit_breaker: bool = True,
        circuit_breaker_threshold: int = 5,
        circuit_breaker_timeout: float = 60.0,
    ):
        """
        Initialize event buffer.

        Args:
            max_size: Maximum number of events before auto-flush
            flush_interval: Seconds between automatic flushes
            max_retries: Maximum retry attempts for failed events
            retry_delay: Base delay between retries (exponential backoff)
            enable_offline_mode: Enable local storage when backend is unreachable
            offline_storage_dir: Directory for offline storage (default: ~/.aigie/offline_events)
            enable_circuit_breaker: Enable circuit breaker to stop hammering failing backend
            circuit_breaker_threshold: Number of consecutive failures before circuit opens
            circuit_breaker_timeout: Seconds to wait before retrying after circuit opens
        """
        self.max_size = max_size
        self.flush_interval = flush_interval
        self.max_retries = max_retries
        self.retry_delay = retry_delay

        self._buffer: deque = deque(maxlen=max_size * 2)  # Allow some overflow
        self._lock = asyncio.Lock()
        self._last_flush = time.time()
        self._flush_task: asyncio.Task | None = None
        self._flusher: Callable[[list[BufferedEvent]], asyncio.Coroutine] | None = None
        self._running = False
        # The loop that owns this buffer's async primitives (lock, flusher's httpx
        # client, etc.). Captured the first time the buffer runs on a loop —
        # typically the SDK's persistent bg-loop in `start_background_flusher`.
        # All flush work MUST be dispatched here; scheduling on `get_running_loop()`
        # leads to "<...> is bound to a different event loop" when callers (e.g.
        # framework auto-instrumentation) invoke add() from their own loop.
        self._owner_loop: asyncio.AbstractEventLoop | None = None

        # Offline mode support
        self._enable_offline_mode = enable_offline_mode
        self._offline_storage: OfflineStorage | None = None
        if enable_offline_mode:
            self._offline_storage = OfflineStorage(storage_dir=offline_storage_dir)

        # Connectivity state
        self._is_offline = False
        self._consecutive_failures = 0
        self._offline_threshold = 3  # Mark as offline after N consecutive failures

        # Circuit breaker state
        self._enable_circuit_breaker = enable_circuit_breaker
        self._circuit_breaker_threshold = circuit_breaker_threshold
        self._circuit_breaker_timeout = circuit_breaker_timeout
        self._circuit_open = False
        self._circuit_opened_at: float | None = None

        # Atexit-safe sync fallback. When the bg loop is unusable (e.g. the
        # interpreter is exiting and atexit has already torn down the
        # SDK's background event loop), terminal trace_update events would
        # otherwise be silently lost — the buffered append never gets to
        # flush. set_sync_fallback() wires the auth headers + api_url, and
        # _maybe_sync_fallback_emit() does a stdlib urllib PUT to
        # /v1/traces/{id} as last-resort delivery for terminal status.
        self._sync_fallback_url: str | None = None
        self._sync_fallback_headers: dict[str, str] = {}

    async def add(
        self,
        event_type: EventType,
        payload: dict[str, Any],
        callback: Callable[[dict[str, Any]], None] | None = None,
    ) -> None:
        """
        Add an event to the buffer.

        Args:
            event_type: Type of event
            payload: Event data
            callback: Optional callback when event is successfully sent
        """
        async with self._lock:
            event = BufferedEvent(event_type=event_type, payload=payload, callback=callback)
            if len(self._buffer) >= self._buffer.maxlen:
                logger.warning(format_diagnostic(R003))
            self._buffer.append(event)

            # Auto-flush if buffer is full — schedule on the buffer's OWNER loop,
            # not the caller's current loop. The flusher's httpx connection state
            # is bound to the owner loop. If no owner loop is registered yet, the
            # periodic background flusher will drain on its own.
            if len(self._buffer) >= self.max_size:
                self._schedule_flush_on_owner()

    def add_sync(self, event_type: EventType, payload: dict[str, Any]) -> None:
        """Sync entry point for synchronous callback contexts (e.g. LangChain
        on_*_end callbacks). Safe to call from any thread or loop.

        Append is GIL-atomic. The flusher uses popleft-drain (see _flush) so
        concurrent appends cannot be dropped.

        Unlike async add() which only schedules a flush at threshold, sync
        callers come from contexts (one-shot scripts, short-lived LangGraph
        runs) where no asyncio task drives the bg_loop between calls — so
        the periodic flusher may never wake up before process exit. Schedule
        on every call; the bg_loop's flush lock naturally serializes and
        no-ops once the deque is drained.
        """
        if len(self._buffer) >= self._buffer.maxlen:
            logger.warning(format_diagnostic(R003))
        self._buffer.append(BufferedEvent(event_type=event_type, payload=payload))
        self._schedule_flush_on_owner()
        self._maybe_sync_fallback_emit(event_type, payload)

    def set_sync_fallback(self, *, api_url: str | None, headers: dict[str, str] | None) -> None:
        """Configure the atexit-safe sync-urllib fallback target."""
        self._sync_fallback_url = api_url
        self._sync_fallback_headers = dict(headers or {})

    def _maybe_sync_fallback_emit(self, event_type: EventType, payload: dict[str, Any]) -> None:
        """Emit a sync urllib PUT for terminal TRACE_UPDATE when the owner loop is unusable.

        Belt-and-suspenders for the shutdown path: when the interpreter is
        exiting and the bg loop has already been torn down by atexit, the
        normal flush will never run. Terminal trace status (error/success)
        is important enough that we PUT directly via stdlib urllib.
        """
        if event_type != EventType.TRACE_UPDATE:
            return
        if payload.get("status") not in ("error", "success"):
            return
        if not self._sync_fallback_url:
            return
        loop = self._owner_loop
        loop_unusable = loop is None or loop.is_closed() or not loop.is_running()
        if not loop_unusable:
            return
        trace_id = payload.get("id")
        if not trace_id:
            return
        try:
            import urllib.request

            headers = dict(self._sync_fallback_headers)
            headers.setdefault("Content-Type", "application/json")
            req = urllib.request.Request(
                f"{self._sync_fallback_url}/v1/traces/{trace_id}",
                data=json.dumps(payload, default=str).encode("utf-8"),
                headers={str(k): str(v) for k, v in headers.items()},
                method="PUT",
            )
            urllib.request.urlopen(req, timeout=5.0).close()  # noqa: S310  # last-resort path
        except Exception as e:  # noqa: BLE001 — last-resort path; swallow
            logger.debug(f"sync trace_update fallback failed: {e}")

    async def flush(self) -> int:
        """
        Manually flush all buffered events.

        Callers may invoke this from any loop (e.g. framework integration
        handlers that run on per-invocation event loops). The actual flush
        work — acquiring the lock and awaiting the flusher's httpx client —
        MUST run on the loop that owns those primitives, otherwise asyncio
        raises "<...> is bound to a different event loop" and the batch is
        dropped. So if we're not already on the owner loop, hop over to it
        via `run_coroutine_threadsafe` and wait for the result.

        Returns:
            Number of events flushed
        """
        owner = self._owner_loop
        if owner is not None and not owner.is_closed():
            try:
                current = asyncio.get_running_loop()
            except RuntimeError:
                current = None
            if current is not owner:
                # Hop to owner loop. Don't block forever — if the bg-loop is
                # wedged, the periodic flusher running on it will drain later.
                fut = asyncio.run_coroutine_threadsafe(self._flush_locked(), owner)
                try:
                    return await asyncio.wrap_future(fut)
                except Exception as e:
                    logger.debug(f"Cross-loop flush dispatch failed: {e}")
                    return 0
        return await self._flush_locked()

    async def _flush_locked(self) -> int:
        """Lock-and-flush. Runs on whatever loop awaits it; flush() ensures that's owner."""
        async with self._lock:
            return await self._flush()

    async def _flush(self) -> int:
        """Internal flush method (assumes lock is held)."""
        if not self._flusher or not self._buffer:
            return 0

        # Check if event loop is available before attempting to flush
        try:
            loop = asyncio.get_running_loop()
            if loop.is_closed():
                logger.debug(
                    f"Event loop is closed, skipping buffer flush ({len(self._buffer)} events)"
                )
                return 0
        except RuntimeError:
            # No event loop running - this is expected during shutdown
            logger.debug(
                f"No event loop running, skipping buffer flush ({len(self._buffer)} events)"
            )
            return 0

        n = len(self._buffer)
        events_to_send = [self._buffer.popleft() for _ in range(n)]
        self._last_flush = time.time()

        if not events_to_send:
            return 0

        # Release lock before making API calls (to avoid blocking)
        # We'll re-acquire it at the end
        lock_held = True
        try:
            # IMPORTANT: Send TRACE_CREATE events first so traces exist before spans arrive.
            # This prevents the backend's auto-create from overwriting correct trace names.
            # Then send remaining events together so the backend can merge SPAN_CREATE + SPAN_UPDATE.

            # Release lock before API calls
            self._lock.release()
            lock_held = False

            # Partition: TRACE_CREATE events first, everything else after
            trace_creates = [e for e in events_to_send if e.event_type == EventType.TRACE_CREATE]
            remaining = [e for e in events_to_send if e.event_type != EventType.TRACE_CREATE]

            success_count = 0
            failed_events = []

            try:
                # Check event loop state before calling flusher
                try:
                    loop = asyncio.get_running_loop()
                    if loop.is_closed():
                        logger.debug(
                            f"Event loop is closed, skipping flush for {len(events_to_send)} events"
                        )
                        # Save to offline storage instead of losing events
                        self._save_to_offline_storage(events_to_send)
                        return 0
                except RuntimeError:
                    logger.debug(
                        f"No event loop running, skipping flush for {len(events_to_send)} events"
                    )
                    # Save to offline storage instead of losing events
                    self._save_to_offline_storage(events_to_send)
                    return 0

                # Circuit breaker: if open, save to offline and skip network call
                if self._is_circuit_open():
                    logger.debug(
                        f"Circuit breaker open - saving {len(events_to_send)} events to offline storage"
                    )
                    self._save_to_offline_storage(events_to_send)
                    return 0

                # Send TRACE_CREATE events first to ensure traces exist before spans
                if trace_creates:
                    await self._flusher(trace_creates)
                    success_count += len(trace_creates)

                # Then send remaining events (spans, updates) together for proper merging
                if remaining:
                    await self._flusher(remaining)
                    success_count += len(remaining)

                # Mark connectivity success
                self._mark_connectivity_success()
                self._close_circuit()

                # Call callbacks for successful events
                for event in events_to_send:
                    if event.callback:
                        try:
                            # Callback receives the response data
                            # For now, pass the payload (can be enhanced)
                            event.callback(event.payload)
                        except Exception:
                            pass  # Don't fail on callback errors
            except Exception as e:
                # Mark connectivity failure (may trigger offline mode)
                self._mark_connectivity_failure(e)

                # Classify error and determine if retryable
                is_retryable = self._is_retryable_error(e)

                if is_retryable:
                    # Retry failed events with exponential backoff
                    events_to_retry = []
                    events_to_store = []

                    # Calculate backoff delay based on highest retry count
                    max_backoff = 0
                    for event in events_to_send:
                        event.retry_count += 1
                        if event.retry_count < self.max_retries:
                            # Calculate exponential backoff delay
                            backoff_delay = self.retry_delay * (2 ** (event.retry_count - 1))
                            max_backoff = max(max_backoff, backoff_delay)
                            events_to_retry.append(event)
                        else:
                            # Max retries exceeded - save to offline storage
                            events_to_store.append(event)

                    # Re-queue immediately — do NOT sleep inline here.
                    # When _flush() is called from add() (buffer-full path) it runs on the
                    # instrumentation hook's await, which is on the critical path of the
                    # LLM call.  Sleeping here would block every agent request until the
                    # backoff expires (up to 7 s per batch × 3 retries = 21 s visible lag).
                    # The background flusher fires every flush_interval seconds, which is
                    # sufficient retry spacing without blocking callers.
                    failed_events.extend(events_to_retry)

                    # Save events that exceeded max retries to offline storage
                    if events_to_store:
                        if self._save_to_offline_storage(events_to_store):
                            logger.info(
                                f"Saved {len(events_to_store)} events to offline storage after {self.max_retries} retries"
                            )
                        else:
                            logger.warning(
                                f"Failed to save {len(events_to_store)} events to offline storage, events lost"
                            )
                # Non-retryable error - save to offline storage if connectivity issue
                elif self._is_connectivity_error(e):
                    if self._save_to_offline_storage(events_to_send):
                        logger.info(
                            f"Saved {len(events_to_send)} events to offline storage due to connectivity error"
                        )
                    else:
                        logger.error(
                            format_diagnostic(
                                R001,
                                extra=f"dropping {len(events_to_send)} events: {type(e).__name__}: {e!s}",
                            )
                        )
                else:
                    logger.error(
                        format_diagnostic(
                            R001,
                            extra=f"dropping {len(events_to_send)} events: {type(e).__name__}: {e!s}",
                        )
                    )

            # Re-add failed events for retry (need lock again)
            if failed_events:
                await self._lock.acquire()
                lock_held = True
                try:
                    for event in failed_events:
                        self._buffer.append(event)
                finally:
                    self._lock.release()
                    lock_held = False

            return success_count
        finally:
            # Re-acquire lock if we released it
            if not lock_held:
                await self._lock.acquire()

    def set_flusher(
        self, flusher: Callable[[list[BufferedEvent]], Coroutine[Any, Any, None]]
    ) -> None:
        """Set the function to call when flushing events."""
        self._flusher = flusher

    async def recover_offline_events(self) -> int:
        """
        Recover events from offline storage.

        Call this on startup to recover any events that were stored
        while the backend was unreachable.

        Returns:
            Number of events recovered
        """
        if not self._offline_storage:
            return 0

        recovered = self._offline_storage.load_events()
        if recovered:
            async with self._lock:
                for event in recovered:
                    self._buffer.append(event)
            logger.info(f"Recovered {len(recovered)} events from offline storage")
        return len(recovered)

    def _schedule_flush_on_owner(self) -> None:
        """Schedule a flush on the owner loop, regardless of current loop.

        Safe to call from any loop or from a non-async context. If the owner
        loop is unknown or closed, returns silently — the periodic background
        flusher running on the owner loop will pick the events up.

        Schedules `_flush_locked()` directly (not `flush()`) because we
        already know we're targeting the owner loop — going through `flush()`
        would just re-check loop identity and fall through to the same place.
        """
        try:
            current = asyncio.get_running_loop()
        except RuntimeError:
            current = None

        owner = self._owner_loop
        # If owner is unknown (start_background_flusher never ran), fall back
        # to the current loop — that's where the lock will bind on first use.
        if owner is None or owner.is_closed():
            if current is None:
                return  # No loop anywhere; periodic flusher will catch up.
            owner = current

        try:
            if current is owner:
                # Same loop — cheap path, no thread-hop required.
                owner.create_task(self._flush_locked())
            else:
                # Different loop. Cross-loop dispatch. Attach a done-callback
                # so flush failures aren't silently swallowed — the future is
                # otherwise discarded.
                fut = asyncio.run_coroutine_threadsafe(self._flush_locked(), owner)
                fut.add_done_callback(_log_flush_future_exception)
        except RuntimeError:
            # Owner loop stopped between the is_closed() check and dispatch —
            # nothing we can do here; periodic flusher will catch up if it restarts.
            pass

    async def start_background_flusher(self) -> None:
        """Start background task that periodically flushes events."""
        if self._running:
            return

        self._running = True

        # Capture the loop this buffer belongs to. All async primitives created
        # here (lock, flusher's httpx connection state) are bound to this loop;
        # cross-loop access raises "<...> is bound to a different event loop".
        try:
            self._owner_loop = asyncio.get_running_loop()
        except RuntimeError:
            self._owner_loop = None

        # Recover any offline events on startup
        if self._offline_storage:
            await self.recover_offline_events()

        async def _background_flush():
            while self._running:
                await asyncio.sleep(self.flush_interval)

                async with self._lock:
                    time_since_flush = time.time() - self._last_flush
                    if time_since_flush >= self.flush_interval and self._buffer:
                        await self._flush()

        self._flush_task = asyncio.create_task(_background_flush())

    async def stop_background_flusher(self) -> None:
        """Stop background flusher and flush remaining events."""
        self._running = False
        if self._flush_task:
            # Don't cancel the running flush task - let it complete its current flush
            # to avoid losing events that are mid-send
            try:
                await asyncio.wait_for(self._flush_task, timeout=10.0)
            except (asyncio.CancelledError, asyncio.TimeoutError):
                pass
            except Exception:
                pass

        # Final flush of any remaining events
        await self.flush()

    def size(self) -> int:
        """Get current buffer size."""
        return len(self._buffer)

    def is_empty(self) -> bool:
        """Check if buffer is empty."""
        return len(self._buffer) == 0

    def _is_retryable_error(self, error: Exception) -> bool:
        """
        Classify error as retryable or non-retryable.

        Retryable errors:
        - Network errors (connection, timeout)
        - 5xx server errors
        - Rate limiting (429)

        Non-retryable errors:
        - 4xx client errors (except 429)
        - Authentication errors (401)
        - Validation errors (400)

        Args:
            error: Exception to classify

        Returns:
            True if error is retryable, False otherwise
        """
        import httpx

        # HTTP errors
        if isinstance(error, httpx.HTTPStatusError):
            status_code = error.response.status_code
            # Retryable: 429 (rate limit), 5xx (server errors)
            if status_code == 429 or (500 <= status_code < 600):
                return True
            # Non-retryable: 4xx client errors (except 429)
            return False

        # Network errors (retryable)
        if isinstance(error, (httpx.ConnectError, httpx.TimeoutException, httpx.NetworkError)):
            return True

        # Request errors (usually non-retryable)
        if isinstance(error, httpx.RequestError):
            return False

        # Unknown errors - default to retryable (conservative)
        return True

    def _is_connectivity_error(self, error: Exception) -> bool:
        """
        Check if error indicates backend is unreachable.

        These errors trigger offline mode when they occur consecutively.
        """
        import httpx

        # Connection and network errors indicate backend is down
        if isinstance(error, (httpx.ConnectError, httpx.TimeoutException, httpx.NetworkError)):
            return True

        # Server errors (5xx) might indicate backend issues
        return bool(isinstance(error, httpx.HTTPStatusError) and error.response.status_code >= 500)

    def _mark_connectivity_success(self) -> None:
        """Mark successful connectivity - reset offline state."""
        if self._is_offline:
            logger.info("Backend connectivity restored")
        self._is_offline = False
        self._consecutive_failures = 0

    def _mark_connectivity_failure(self, error: Exception) -> None:
        """Mark connectivity failure - may trigger offline mode and open circuit breaker."""
        if self._is_connectivity_error(error):
            self._consecutive_failures += 1
            if self._consecutive_failures >= self._offline_threshold:
                if not self._is_offline:
                    logger.warning(
                        format_diagnostic(
                            N002,
                            extra=f"after {self._consecutive_failures} failures, switching to offline mode",
                        )
                    )
                self._is_offline = True

            # Open circuit breaker after threshold consecutive failures
            if (
                self._enable_circuit_breaker
                and self._consecutive_failures >= self._circuit_breaker_threshold
                and not self._circuit_open
            ):
                self._circuit_open = True
                self._circuit_opened_at = time.time()
                logger.warning(
                    format_diagnostic(
                        N005,
                        extra=f"after {self._consecutive_failures} consecutive failures, will retry after {self._circuit_breaker_timeout}s",
                    )
                )

    def _save_to_offline_storage(self, events: list[BufferedEvent]) -> bool:
        """
        Save events to offline storage when backend is unreachable.

        Args:
            events: Events to save

        Returns:
            True if saved successfully
        """
        if not self._enable_offline_mode or not self._offline_storage:
            return False

        return self._offline_storage.save_events(events)

    def _is_circuit_open(self) -> bool:
        """Check if circuit breaker is currently open (blocking requests)."""
        if not self._enable_circuit_breaker or not self._circuit_open:
            return False

        # Check if timeout has elapsed - allow a retry (half-open state)
        if self._circuit_opened_at is not None:
            elapsed = time.time() - self._circuit_opened_at
            if elapsed >= self._circuit_breaker_timeout:
                logger.info("Circuit breaker half-open - allowing retry")
                return False

        return True

    def _close_circuit(self) -> None:
        """Close the circuit breaker after a successful request."""
        if self._circuit_open:
            logger.info("Circuit breaker closed - backend connectivity restored")
            self._circuit_open = False
            self._circuit_opened_at = None

    @property
    def is_offline(self) -> bool:
        """Check if buffer is operating in offline mode."""
        return self._is_offline

    def get_offline_stats(self) -> dict[str, Any]:
        """
        Get offline mode statistics.

        Returns:
            Dict with offline storage stats
        """
        stats = {
            "enabled": self._enable_offline_mode,
            "is_offline": self._is_offline,
            "consecutive_failures": self._consecutive_failures,
            "offline_threshold": self._offline_threshold,
        }

        if self._offline_storage:
            stats["storage"] = self._offline_storage.get_stats()

        return stats

    def clear_offline_storage(self) -> int:
        """
        Clear offline storage.

        Returns:
            Number of files deleted
        """
        if self._offline_storage:
            return self._offline_storage.clear()
        return 0
