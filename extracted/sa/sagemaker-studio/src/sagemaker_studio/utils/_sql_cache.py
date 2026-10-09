"""Internal module for SQL connection cache management."""

import logging
from dataclasses import dataclass
from datetime import datetime
from threading import RLock
from typing import Dict, List, Optional

from sqlalchemy.engine import Connection, Engine

logger = logging.getLogger(__name__)


@dataclass
class ManagedConnection:
    """Represents a managed database connection with its engine and lifecycle metadata."""

    engine: Engine
    connection: Optional[Connection]  # None for non-persisted sessions
    id: str  # Unique identifier for this cache entry (UUID)
    cache_key: str  # Full cache key including config: "conn_123::catalog_name=prod"
    created_at: Optional[datetime] = None
    last_used: Optional[datetime] = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.last_used is None:
            self.last_used = datetime.now()


class ConnectionCache:
    """
    Manages persistent database connections for reuse across queries.

    Connections are cached by their identifier (connection_id or connection_name)
    and remain open until explicitly closed or the kernel restarts.
    """

    def __init__(self):
        self._cache: Dict[str, ManagedConnection] = {}  # cache_key -> ManagedConnection
        self._id_to_key: Dict[str, str] = {}  # id (UUID) -> cache_key
        # The async path writes/reads the cache from the foreground while a background
        # materialization thread runs, so guard mutations with a reentrant lock.
        self._lock = RLock()

    def get(self, key: str) -> Optional[ManagedConnection]:
        """Retrieve a cached connection by key."""
        evict = False
        with self._lock:
            cached = self._cache.get(key)
            if not cached:
                return None

            # Lazy health check - validate connection is not closed. Only DECIDE eviction
            # under the lock; the actual removal (which does blocking connection.close()/
            # engine.dispose() teardown) runs AFTER releasing the lock, so a slow teardown
            # does not block get/put/snapshot/__len__.
            try:
                if cached.connection is not None and cached.connection.closed:
                    logger.warning(f"Cached connection {key} is closed, removing from cache")
                    evict = True
                else:
                    cached.last_used = datetime.now()
                    return cached
            except Exception as e:
                logger.warning(f"Error checking connection {key} status: {e}, removing from cache")
                evict = True

        if evict:
            # Compare-and-swap eviction: only remove/tear down the SAME stale object we
            # checked. If another thread called put(key, fresh) after we released the lock,
            # _remove_if_same leaves that fresh entry alone (avoids tearing down a healthy
            # connection). Either way this stale read returns None.
            self._remove_if_same(key, cached)
            return None
        return None  # pragma: no cover - defensive; every path above already returns

    def put(self, key: str, managed_conn: ManagedConnection) -> None:
        """Cache a connection."""
        with self._lock:
            # If this key already held a DIFFERENT connection, drop its stale id->key
            # mapping first; otherwise the orphaned id would let a later remove_by_id(old_id)
            # resolve back to `key` and tear down the current (healthy) connection.
            prev = self._cache.get(key)
            if prev is not None and prev.id != managed_conn.id:
                self._id_to_key.pop(prev.id, None)
            self._cache[key] = managed_conn
            self._id_to_key[managed_conn.id] = key

    @staticmethod
    def _teardown(cached: ManagedConnection, key: str) -> None:
        """Blocking teardown of a detached cache entry. MUST be called OUTSIDE the lock."""
        try:
            if cached.connection is not None:
                cached.connection.close()
        except Exception as e:
            logger.warning(f"Error closing connection {key}: {e}")
        try:
            cached.engine.dispose()
        except Exception as e:
            logger.warning(f"Error disposing engine for {key}: {e}")

    def _remove_if_same(self, key: str, expected: ManagedConnection) -> bool:
        """Pop and tear down the entry at `key` ONLY if it is still `expected` (guards the
        get()-eviction TOCTOU: a concurrent put() may have replaced it with a fresh, healthy
        connection that must not be torn down). Teardown runs outside the lock."""
        with self._lock:
            cached = self._cache.get(key)
            if cached is not expected:
                return False
            self._cache.pop(key, None)
            self._id_to_key.pop(cached.id, None)
        self._teardown(cached, key)
        return True

    def remove(self, key: str) -> bool:
        """
        Remove and close a cached connection.

        Returns:
            bool: True if connection was found and closed, False otherwise.
        """
        # Pop the entry under the lock (fast dict mutation only), then do the potentially
        # blocking teardown (connection.close()/engine.dispose() are network I/O) OUTSIDE the
        # lock, so a slow teardown does not block get/put/snapshot/__len__ for its duration.
        with self._lock:
            cached = self._cache.pop(key, None)
            if cached is None:
                return False
            self._id_to_key.pop(cached.id, None)

        self._teardown(cached, key)
        return True

    def remove_by_id(self, id: str) -> bool:
        """
        Remove and close a cached connection by its unique ID.

        Args:
            id: Unique identifier of the connection to remove

        Returns:
            bool: True if connection was found and closed, False otherwise.
        """
        # Resolve the entry under the lock and route teardown through the compare-and-swap
        # helper: between resolving the key and tearing it down, a concurrent put(key, fresh)
        # could replace the entry, and a plain remove(cache_key) would tear down that fresh,
        # healthy connection. _remove_if_same only removes when the entry is still the one we
        # resolved (same TOCTOU guard get() uses).
        with self._lock:
            cache_key = self._id_to_key.get(id)
            expected = self._cache.get(cache_key) if cache_key is not None else None
        if expected is None or expected.id != id:
            return False
        return self._remove_if_same(cache_key, expected)

    def clear(self) -> int:
        """
        Close and remove all cached connections.

        Returns:
            int: Number of connections closed.
        """
        # Snapshot the keys under the lock, then remove WITHOUT holding the outer lock, so
        # each remove()'s blocking teardown runs outside the lock (holding it across the whole
        # loop would serialize every teardown under the lock -- the exact thing remove() avoids).
        with self._lock:
            keys = list(self._cache.keys())
        count = 0
        for key in keys:
            if self.remove(key):
                count += 1
        return count

    def list_keys(self) -> List[str]:
        """Return list of all cached connection identifiers."""
        # Guard the read: another thread (user code calling close_*/new queries) may
        # put/remove while the foreground iterates, which would raise "dictionary changed
        # size during iteration".
        with self._lock:
            return list(self._cache.keys())

    def snapshot(self) -> List[ManagedConnection]:
        """Return a point-in-time list of the cached ManagedConnections, taken under the
        lock so callers can iterate safely without touching the live dict."""
        with self._lock:
            return list(self._cache.values())

    def __len__(self) -> int:
        """Return number of cached connections."""
        with self._lock:
            return len(self._cache)

    def __contains__(self, key: str) -> bool:
        """Check if a connection is cached."""
        with self._lock:
            return key in self._cache
