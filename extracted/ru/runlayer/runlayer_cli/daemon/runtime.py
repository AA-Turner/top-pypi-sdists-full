"""Long-lived daemon state: managed config, credentials, and warm HTTP pool."""

from __future__ import annotations

import threading
import time
from collections import deque
from collections.abc import Callable
from typing import Generic, TypeVar, cast

import httpx

from runlayer_cli import mdm_config
from runlayer_cli.hook import relay
from runlayer_cli.mdm_config import ManagedConfig
from runlayer_cli.tls import http_client

_CACHE_TTL_SECONDS = 30.0
_MAX_KEEPALIVE_CONNECTIONS = 8
_MAX_CONNECTIONS = 32
_KEEPALIVE_EXPIRY_SECONDS = 90.0
_PREWARM_TIMEOUT_SECONDS = 2.0
_EVENT_QUEUE_MAX_SIZE = 256
_EVENT_FLUSH_TIMEOUT_SECONDS = 5.0

T = TypeVar("T")
_MISSING = object()


class _TTLValue(Generic[T]):
    def __init__(
        self,
        loader: Callable[[], T],
        *,
        ttl: float,
        clock: Callable[[], float] = time.monotonic,
    ) -> None:
        self._loader = loader
        self._ttl = ttl
        self._clock = clock
        self._lock = threading.RLock()
        self._value: T | object = _MISSING
        self._expires_at = 0.0

    def get(self) -> T:
        with self._lock:
            now = self._clock()
            if self._value is _MISSING or now >= self._expires_at:
                self._value = self._loader()
                self._expires_at = now + self._ttl
            return cast(T, self._value)

    def invalidate(self) -> None:
        with self._lock:
            self._value = _MISSING
            self._expires_at = 0.0


class ManagedConfigCache:
    """Thread-safe copy-on-read managed config cache."""

    def __init__(
        self,
        loader: Callable[[], ManagedConfig],
        *,
        ttl: float = _CACHE_TTL_SECONDS,
        clock: Callable[[], float] = time.monotonic,
    ) -> None:
        self._value = _TTLValue(loader, ttl=ttl, clock=clock)

    def get(self) -> ManagedConfig:
        return self._value.get().copy()

    def invalidate(self) -> None:
        self._value.invalidate()


class CredentialCache:
    """Thread-safe relay credential cache coupled to managed config."""

    def __init__(
        self,
        managed_config: ManagedConfigCache,
        *,
        ttl: float = _CACHE_TTL_SECONDS,
        clock: Callable[[], float] = time.monotonic,
    ) -> None:
        self._managed_config = managed_config
        self._ttl = ttl
        self._clock = clock
        self._lock = threading.RLock()
        self._value: tuple[str, str] | None = None
        self._expires_at = 0.0

    def get(
        self,
        loader: Callable[[], tuple[str, str]],
    ) -> tuple[str, str]:
        with self._lock:
            now = self._clock()
            if self._value is None or now >= self._expires_at:
                self._value = loader()
                self._expires_at = now + self._ttl
            return self._value

    def invalidate(self) -> None:
        with self._lock:
            self._value = None
            self._expires_at = 0.0
            self._managed_config.invalidate()


class DeferredEventQueue:
    """Bounded FIFO of deferred event sends drained by one worker thread.

    Single worker preserves event send order. Overflow drops the oldest entry
    (events are already best-effort; the sync path swallows errors too) —
    including any client_flows envelope drained into that payload at schedule
    time, an accepted loss under sustained backpressure.
    ``flush_and_stop`` gives pending sends a bounded window instead of relying
    on ``daemon=True`` teardown, which would silently discard the queue.
    """

    def __init__(self, *, max_size: int = _EVENT_QUEUE_MAX_SIZE) -> None:
        self._max_size = max_size
        self._cond = threading.Condition()
        self._items: deque[Callable[[], None]] = deque()
        self._closed = False
        self._worker: threading.Thread | None = None
        self._inflight = 0

    def enqueue(self, send: Callable[[], None]) -> bool:
        """Queue a send; False once closed (caller falls back to sync POST)."""
        with self._cond:
            if self._closed:
                return False
            if len(self._items) >= self._max_size:
                self._items.popleft()
            self._items.append(send)
            if self._worker is None:
                self._worker = threading.Thread(
                    target=self._drain,
                    daemon=True,
                    name="aiwatch-daemon-event-sender",
                )
                self._worker.start()
            self._cond.notify()
        return True

    def flush_and_stop(self, *, timeout: float = _EVENT_FLUSH_TIMEOUT_SECONDS) -> bool:
        """Stop accepting sends and wait (bounded) for the queue to drain.

        Returns True when every queued send completed within the window; a
        timed-out worker is a daemon thread, so process exit reaps it.
        """
        deadline = time.monotonic() + timeout
        with self._cond:
            self._closed = True
            self._cond.notify_all()
            while self._items or self._inflight:
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    return False
                self._cond.wait(remaining)
        worker = self._worker
        if worker is not None:
            worker.join(max(0.0, deadline - time.monotonic()))
            return not worker.is_alive()
        return True

    def _drain(self) -> None:
        while True:
            with self._cond:
                while not self._items and not self._closed:
                    self._cond.wait()
                if not self._items:
                    return
                send = self._items.popleft()
                self._inflight += 1
            try:
                send()
            except Exception:
                pass
            finally:
                with self._cond:
                    self._inflight -= 1
                    self._cond.notify_all()


class DaemonRuntime:
    """Own all process-lifetime daemon resources and relay seams."""

    def __init__(
        self,
        *,
        clock: Callable[[], float] = time.monotonic,
        client: httpx.Client | None = None,
    ) -> None:
        self._clock = clock
        self.managed_config = ManagedConfigCache(
            mdm_config._read_managed_config_uncached,
            clock=clock,
        )
        self.credentials = CredentialCache(
            self.managed_config,
            clock=clock,
        )
        self.client = client or http_client(
            limits=httpx.Limits(
                max_keepalive_connections=_MAX_KEEPALIVE_CONNECTIONS,
                max_connections=_MAX_CONNECTIONS,
                keepalive_expiry=_KEEPALIVE_EXPIRY_SECONDS,
            )
        )
        self.events = DeferredEventQueue()
        self._prewarm_lock = threading.Lock()
        self._last_hook_at: float | None = None
        self._installed = False
        self._closed = False

    def install(self) -> None:
        mdm_config.set_managed_config_provider(self.managed_config.get)
        relay.set_credential_cache(self.credentials)
        relay.set_shared_http_client_provider(lambda: self.client)
        relay.set_deferred_event_sender(self.events.enqueue)
        self._installed = True

    def close(self) -> None:
        # Clear the deferred seam before flushing so late forward_event calls
        # POST synchronously instead of racing the closing queue; the pooled
        # client stays installed through the flush so queued sends reuse it.
        if self._installed:
            relay.set_deferred_event_sender(None)
        self.events.flush_and_stop()
        if self._installed:
            relay.set_shared_http_client_provider(None)
            relay.set_credential_cache(None)
            mdm_config.set_managed_config_provider(None)
            self._installed = False
        with self._prewarm_lock:
            self._closed = True
            self.client.close()

    def daemon_is_enabled(self) -> bool:
        return mdm_config.daemon_gate_open(self.managed_config.get())

    def prewarm(self, *, force: bool = False) -> None:
        """Open one TLS connection on start and after keepalive expiry."""
        with self._prewarm_lock:
            if not self._reserve_prewarm(force=force):
                return
            self._perform_prewarm()

    def prewarm_background(self, *, force: bool = False) -> None:
        """Schedule best-effort prewarming without delaying hook dispatch."""
        with self._prewarm_lock:
            if not self._reserve_prewarm(force=force):
                return
        threading.Thread(
            target=self._perform_reserved_prewarm,
            daemon=True,
            name="aiwatch-daemon-prewarm",
        ).start()

    def before_hook(self) -> None:
        self.prewarm_background()

    def _reserve_prewarm(self, *, force: bool) -> bool:
        if self._closed:
            return False
        now = self._clock()
        idle = (
            self._last_hook_at is None
            or now - self._last_hook_at >= _KEEPALIVE_EXPIRY_SECONDS
        )
        self._last_hook_at = now
        return force or idle

    def _perform_reserved_prewarm(self) -> None:
        with self._prewarm_lock:
            if not self._closed:
                self._perform_prewarm()

    def _perform_prewarm(self) -> None:
        try:
            host, _secret = relay._load_credentials()
            self.client.head(host, timeout=_PREWARM_TIMEOUT_SECONDS)
        except Exception:
            pass
