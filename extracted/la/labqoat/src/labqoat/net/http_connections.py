"""Bounded idle HTTP connections with exclusive per-request ownership and deterministic cleanup."""

import http.client
import select
import time
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from queue import Empty, Full, LifoQueue
from threading import Lock


class HttpConnections:
    """Reuse fully consumed connections without sharing an active socket between worker threads.

    The service keeps an idle connection for about thirty seconds. A socket is reused for twenty, and only
    while the service has sent nothing on it: a close it already announced reads as pending input.
    """

    IDLE_SECONDS = 20.0

    def __init__(self, factory: Callable[[], http.client.HTTPConnection], maximum: int = 16) -> None:
        """Retain a lazy connection factory and a bounded idle budget without opening sockets."""
        self._factory = factory
        self._idle: LifoQueue[tuple[float, http.client.HTTPConnection]] = LifoQueue(maximum)
        self._lock = Lock()
        self._closed = False

    @contextmanager
    def using(self) -> Iterator[http.client.HTTPConnection]:
        """Discard uncertain connections on every exceptional exit rather than replaying worker mutations."""
        connection = self._take()
        try:
            yield connection
        except BaseException:
            connection.close()
            raise
        else:
            self._release(connection)

    def _take(self) -> http.client.HTTPConnection:
        """Borrow an idle socket or create an independent connection outside the pool lock."""
        with self._lock:
            if self._closed:
                raise RuntimeError("HTTP connections are closed")
            try:
                returned_at, connection = self._idle.get_nowait()
            except Empty:
                pass
            else:
                if time.monotonic() - returned_at < self.IDLE_SECONDS and not self._ended(connection):
                    return connection
                connection.close()
        return self._factory()

    @staticmethod
    def _ended(connection: http.client.HTTPConnection) -> bool:
        """An idle socket with input waiting was closed or reset by its peer; a mutation must not be sent on it."""
        try:
            return bool(select.select([connection.sock], [], [], 0)[0])
        except (OSError, ValueError):
            return True

    def _release(self, connection: http.client.HTTPConnection) -> None:
        """Keep only connected sockets within the idle budget, including concurrent shutdown."""
        with self._lock:
            if not self._closed and connection.sock is not None:
                try:
                    self._idle.put_nowait((time.monotonic(), connection))
                    return
                except Full:
                    pass
            connection.close()

    def close(self) -> None:
        """Close all idle connections; in-flight requests close their own sockets when returned."""
        with self._lock:
            self._closed = True
            while True:
                try:
                    self._idle.get_nowait()[1].close()
                except Empty:
                    return
