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
from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field
from pathlib import Path

from aigie.diagnostics import N002, N005, R001, R003, R004, format_diagnostic
from aigie.types import EventPayload, OfflineModeStats, OfflineStorageStats

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


@dataclass
class BufferedEvent:
    """A single finalized span waiting to be sent.

    A span is built mutably in memory and emitted exactly once finalized;
    there is no longer an event-type taxonomy — every buffered event is a
    finalized span payload bound for gRPC IngestSpans.
    """

    payload: EventPayload
    timestamp: float = field(default_factory=time.time)
    retry_count: int = 0
    callback: Callable[[EventPayload], None] | None = None  # Called on success
    evaluated: bool = False


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
        events: list[BufferedEvent] = []

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
                        # Old offline files may still carry "event_type"; ignore it.
                        event = BufferedEvent(
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

    def get_stats(self) -> OfflineStorageStats:
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

        self._buffer: deque[BufferedEvent] = deque(maxlen=max_size * 2)  # Allow some overflow
        self._lock = asyncio.Lock()
        self._last_flush = time.time()
        self._flush_task: asyncio.Task[None] | None = None
        self._flusher: Callable[[list[BufferedEvent]], Awaitable[None]] | None = None
        self._running = False
        # The loop that owns this buffer's async primitives (lock, flusher's httpx
        # client, etc.). Captured the first time the buffer runs on a loop —
        # typically the SDK's persistent bg-loop in `start_background_flusher`.
        # All flush work MUST be dispatched here; scheduling on `get_running_loop()`
        # leads to "<...> is bound to a different event loop" when callers (e.g.
        # framework auto-instrumentation) invoke add() from their own loop.
        self._owner_loop: asyncio.AbstractEventLoop | None = None

        self._init_resilience_state(
            enable_offline_mode,
            offline_storage_dir,
            enable_circuit_breaker,
            circuit_breaker_threshold,
            circuit_breaker_timeout,
        )

    def _init_resilience_state(
        self,
        enable_offline_mode: bool,
        offline_storage_dir: Path | None,
        enable_circuit_breaker: bool,
        circuit_breaker_threshold: int,
        circuit_breaker_timeout: float,
    ) -> None:
        """Initialize offline-mode, connectivity, and circuit-breaker state."""
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

    async def add(
        self,
        payload: EventPayload,
        *,
        callback: Callable[[EventPayload], None] | None = None,
        evaluated: bool = False,
    ) -> None:
        """
        Add a finalized span to the buffer.

        Args:
            payload: Finalized span data
            callback: Optional callback when event is successfully sent
            evaluated: True when EvaluateSpan already fired at emit time
        """
        async with self._lock:
            event = BufferedEvent(payload=payload, callback=callback, evaluated=evaluated)
            if self._buffer.maxlen is not None and len(self._buffer) >= self._buffer.maxlen:
                logger.warning(format_diagnostic(R003))
            self._buffer.append(event)

            # Auto-flush if buffer is full — schedule on the buffer's OWNER loop,
            # not the caller's current loop. The flusher's httpx connection state
            # is bound to the owner loop. If no owner loop is registered yet, the
            # periodic background flusher will drain on its own.
            if len(self._buffer) >= self.max_size:
                self._schedule_flush_on_owner()

    def add_sync(self, payload: EventPayload, *, evaluated: bool = False) -> None:
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
        if self._buffer.maxlen is not None and len(self._buffer) >= self._buffer.maxlen:
            logger.warning(format_diagnostic(R003))
        self._buffer.append(BufferedEvent(payload=payload, evaluated=evaluated))
        self._schedule_flush_on_owner()

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
        if not self._loop_usable():
            return 0

        n = len(self._buffer)
        events_to_send = [self._buffer.popleft() for _ in range(n)]
        self._last_flush = time.time()
        if not events_to_send:
            return 0

        # Release lock before making API calls (to avoid blocking callers);
        # re-acquired in the finally so the caller's `async with` stays balanced.
        self._lock.release()
        try:
            # Circuit breaker: if open, save to offline and skip network calls
            if self._is_circuit_open():
                logger.debug(
                    f"Circuit breaker open - saving {len(events_to_send)} events to offline storage"
                )
                self._save_to_offline_storage(events_to_send)
                return 0
            return await self._send_partitioned(events_to_send)
        finally:
            await self._lock.acquire()

    async def _send_partitioned(self, events_to_send: list[BufferedEvent]) -> int:
        """Send the drained batch as a single transport leg.

        There is only one transport left (gRPC IngestSpans); the flusher
        drops non-span events itself. The TRACE_CREATE-first partition that
        used to live here ordered writes for the legacy HTTP endpoints,
        which were removed platform-side.
        """
        success_count, failed_events = await self._send_leg(events_to_send)

        # Re-queue failed events immediately — do NOT sleep inline here.
        # When _flush() is called from add() (buffer-full path) it runs on
        # the instrumentation hook's await, which is on the critical path
        # of the LLM call. The background flusher fires every
        # flush_interval seconds, which is sufficient retry spacing.
        for event in failed_events:
            self._buffer.append(event)

        return success_count

    def _loop_usable(self) -> bool:
        """True when a running, open event loop is available for the flusher."""
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            # No event loop running - this is expected during shutdown
            logger.debug(
                f"No event loop running, skipping buffer flush ({len(self._buffer)} events)"
            )
            return False
        if loop.is_closed():
            logger.debug(
                f"Event loop is closed, skipping buffer flush ({len(self._buffer)} events)"
            )
            return False
        return True

    async def _send_leg(self, leg: list[BufferedEvent]) -> tuple[int, list[BufferedEvent]]:
        """Send one transport leg; return (sent_count, events_to_retry).

        Failures are contained to the leg: classified as retryable (returned
        for re-queue), connectivity (offline storage), or dropped.
        """
        flusher = self._flusher
        if flusher is None:  # _flush() never dispatches a leg without a flusher
            return 0, leg
        try:
            await flusher(leg)
        except Exception as e:
            return 0, self._classify_leg_failure(e, leg)

        self._mark_connectivity_success()
        self._close_circuit()
        for event in leg:
            if event.callback:
                # Callbacks must not fail the flush.
                with contextlib.suppress(Exception):
                    event.callback(event.payload)
        return len(leg), []

    def _classify_leg_failure(
        self, error: Exception, leg: list[BufferedEvent]
    ) -> list[BufferedEvent]:
        """Apply retry/offline/drop policy to a failed leg; return events to re-queue."""
        self._mark_connectivity_failure(error)

        if self._is_retryable_error(error):
            to_retry, to_store = self._split_for_retry(leg)
            if to_store:
                if self._save_to_offline_storage(to_store):
                    logger.info(
                        f"Saved {len(to_store)} events to offline storage "
                        f"after {self.max_retries} retries"
                    )
                else:
                    logger.warning(
                        f"Failed to save {len(to_store)} events to offline storage, events lost"
                    )
            return to_retry

        # Non-retryable error - save to offline storage if connectivity issue
        if self._is_connectivity_error(error) and self._save_to_offline_storage(leg):
            logger.info(f"Saved {len(leg)} events to offline storage due to connectivity error")
            return []
        logger.error(
            format_diagnostic(
                R001,
                extra=f"dropping {len(leg)} events: {type(error).__name__}: {error!s}",
            )
        )
        return []

    def _split_for_retry(
        self, events: list[BufferedEvent]
    ) -> tuple[list[BufferedEvent], list[BufferedEvent]]:
        """Increment retry accounting; partition into (retryable, exhausted)."""
        to_retry: list[BufferedEvent] = []
        exhausted: list[BufferedEvent] = []
        for event in events:
            event.retry_count += 1
            if event.retry_count < self.max_retries:
                to_retry.append(event)
            else:
                exhausted.append(event)
        return to_retry, exhausted

    def set_flusher(self, flusher: Callable[[list[BufferedEvent]], Awaitable[None]]) -> None:
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
                logger.debug("background flush task failed during stop", exc_info=True)

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

        # HTTP errors. Retryable: 429 (rate limit), 5xx (server errors);
        # non-retryable: other 4xx client errors.
        if isinstance(error, httpx.HTTPStatusError):
            status_code: int = error.response.status_code
            return status_code == 429 or (500 <= status_code < 600)

        # Network errors (retryable)
        if isinstance(error, (httpx.ConnectError, httpx.TimeoutException, httpx.NetworkError)):
            return True

        # Other request errors are usually non-retryable; unknown errors
        # default to retryable (conservative).
        return not isinstance(error, httpx.RequestError)

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

    def get_offline_stats(self) -> OfflineModeStats:
        """
        Get offline mode statistics.

        Returns:
            Dict with offline storage stats
        """
        stats: OfflineModeStats = {
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
