"""
LRU cache for inference results keyed by frame_id.

Used when streaming gateway sends reference_frame_id instead of content.
Server looks up cached results for the reference frame.

Thread-safe with RLock for concurrent access from multiple workers.
Memory-bounded with LRU eviction and TTL expiration.
"""

import logging
import threading
import time
from collections import OrderedDict
from dataclasses import dataclass, field
from typing import Any, Dict, Optional

# Default configuration constants (moved outside class to avoid forward reference issues)
DEFAULT_MAX_SIZE = 50000
DEFAULT_TTL_SECONDS = 300  # 5 minutes
DEFAULT_CLEANUP_INTERVAL = 60  # Cleanup expired entries every 60 seconds


@dataclass
class CachedResult:
    """Container for cached inference result with metadata."""

    result: Dict[str, Any]
    created_at: float = field(default_factory=time.time)
    access_count: int = 0
    last_accessed: float = field(default_factory=time.time)

    def is_expired(self, ttl_seconds: float) -> bool:
        """Check if this result has expired based on TTL."""
        return (time.time() - self.created_at) > ttl_seconds

    def touch(self) -> None:
        """Update access metadata (called on cache hit)."""
        self.access_count += 1
        self.last_accessed = time.time()


class InferenceResultCache:
    """
    Thread-safe LRU cache for inference results.

    Designed for high-throughput inference pipelines where:
    - Similar frames use cached results instead of re-running inference
    - Results are keyed by frame_id from streaming gateway
    - Memory is bounded by max_size with LRU eviction
    - Old entries expire after ttl_seconds

    Usage:
        cache = InferenceResultCache(max_size=50000, ttl_seconds=300)

        # After inference:
        cache.put(frame_id, {"model_result": result, "metadata": meta})

        # When receiving reference frame:
        cached = cache.get(reference_frame_id)
        if cached:
            # Use cached result
        else:
            # Cache miss - frame expired or was evicted
    """

    def __init__(
        self,
        max_size: int = DEFAULT_MAX_SIZE,
        ttl_seconds: float = DEFAULT_TTL_SECONDS,
        cleanup_interval: float = DEFAULT_CLEANUP_INTERVAL,
        enabled: bool = True,
    ):
        """
        Initialize InferenceResultCache.

        Args:
            max_size: Maximum number of cached results
            ttl_seconds: Time-to-live for cached results
            cleanup_interval: How often to clean up expired entries
            enabled: If False, cache operations are no-ops
        """
        self.max_size = max(100, max_size)
        self.ttl_seconds = max(1.0, ttl_seconds)
        self.cleanup_interval = max(1.0, cleanup_interval)
        self.enabled = enabled

        # OrderedDict for LRU - most recently used at the end
        self._cache: OrderedDict[str, CachedResult] = OrderedDict()
        self._lock = threading.RLock()

        # Cleanup tracking
        self._last_cleanup = time.time()

        # Metrics
        self._metrics: Dict[str, Any] = {
            "hits": 0,
            "misses": 0,
            "puts": 0,
            "evictions": 0,
            "expirations": 0,
        }
        self._metrics_lock = threading.Lock()

        self.logger = logging.getLogger(f"{__name__}.InferenceResultCache")

    def put(self, frame_id: str, result: Dict[str, Any]) -> bool:
        """
        Cache inference result for a frame_id.

        Args:
            frame_id: Unique frame identifier from streaming gateway
            result: Inference result to cache (should include model_result, metadata)

        Returns:
            True if cached successfully, False otherwise
        """
        if not self.enabled or not frame_id:
            return False

        try:
            with self._lock:
                # Run cleanup periodically
                self._maybe_cleanup()

                # If already exists, update and move to end (most recently used)
                if frame_id in self._cache:
                    self._cache[frame_id] = CachedResult(result=result)
                    self._cache.move_to_end(frame_id)
                else:
                    # Evict oldest if at capacity
                    while len(self._cache) >= self.max_size:
                        self._evict_oldest()

                    # Add new entry
                    self._cache[frame_id] = CachedResult(result=result)

                with self._metrics_lock:
                    self._metrics["puts"] += 1

                return True

        except Exception as e:
            self.logger.error(f"Error caching result for frame_id={frame_id}: {e}")
            return False

    def get(self, frame_id: str) -> Optional[Dict[str, Any]]:
        """
        Get cached result for a frame_id.

        Args:
            frame_id: Frame identifier to look up

        Returns:
            Cached result dict or None if not found/expired
        """
        if not self.enabled or not frame_id:
            return None

        try:
            with self._lock:
                cached = self._cache.get(frame_id)

                if cached is None:
                    with self._metrics_lock:
                        self._metrics["misses"] += 1
                    return None

                # Check expiration
                if cached.is_expired(self.ttl_seconds):
                    del self._cache[frame_id]
                    with self._metrics_lock:
                        self._metrics["misses"] += 1
                        self._metrics["expirations"] += 1
                    return None

                # Cache hit - update LRU order and access metadata
                cached.touch()
                self._cache.move_to_end(frame_id)

                with self._metrics_lock:
                    self._metrics["hits"] += 1

                return cached.result

        except Exception as e:
            self.logger.error(f"Error getting cached result for frame_id={frame_id}: {e}")
            return None

    def has(self, frame_id: str) -> bool:
        """
        Check if frame_id has a valid (non-expired) cached result.

        Note: This does NOT update LRU order - use get() if you need the result.

        Args:
            frame_id: Frame identifier to check

        Returns:
            True if valid cached result exists
        """
        if not self.enabled or not frame_id:
            return False

        with self._lock:
            cached = self._cache.get(frame_id)
            if cached is None:
                return False
            return not cached.is_expired(self.ttl_seconds)

    def remove(self, frame_id: str) -> bool:
        """
        Remove a specific entry from cache.

        Args:
            frame_id: Frame identifier to remove

        Returns:
            True if entry was removed, False if not found
        """
        with self._lock:
            if frame_id in self._cache:
                del self._cache[frame_id]
                return True
            return False

    def clear(self) -> None:
        """Clear all cached results."""
        with self._lock:
            self._cache.clear()
        self.logger.info("Cache cleared")

    def _evict_oldest(self) -> None:
        """Evict the oldest (least recently used) entry."""
        if self._cache:
            oldest_key, _ = self._cache.popitem(last=False)
            with self._metrics_lock:
                self._metrics["evictions"] += 1
            self.logger.debug(f"Evicted oldest cache entry: {oldest_key}")

    def _maybe_cleanup(self) -> None:
        """Periodically clean up expired entries."""
        now = time.time()
        if (now - self._last_cleanup) < self.cleanup_interval:
            return

        self._last_cleanup = now
        expired_keys = []

        for key, cached in self._cache.items():
            if cached.is_expired(self.ttl_seconds):
                expired_keys.append(key)

        for key in expired_keys:
            del self._cache[key]

        if expired_keys:
            with self._metrics_lock:
                self._metrics["expirations"] += len(expired_keys)
            self.logger.debug(f"Cleaned up {len(expired_keys)} expired entries")

    def get_metrics(self) -> Dict[str, Any]:
        """
        Get cache metrics for monitoring.

        Returns:
            Dict with metrics including:
            - hits: Number of cache hits
            - misses: Number of cache misses
            - puts: Number of items cached
            - evictions: LRU evictions
            - expirations: TTL expirations
            - hit_rate: Cache hit percentage
            - size: Current cache size
        """
        with self._metrics_lock:
            metrics = dict(self._metrics)

        with self._lock:
            metrics["size"] = len(self._cache)

        # Calculate hit rate
        total_lookups = metrics.get("hits", 0) + metrics.get("misses", 0)
        hits = metrics.get("hits", 0)
        hit_rate = (hits / total_lookups * 100) if total_lookups > 0 else 0.0
        metrics["hit_rate"] = hit_rate

        # Add config
        config_dict = {
            "enabled": self.enabled,
            "max_size": self.max_size,
            "ttl_seconds": self.ttl_seconds,
        }
        metrics["config"] = config_dict

        return metrics

    def get_cache_info(self, frame_id: str) -> Optional[Dict]:
        """
        Get detailed info about a cached entry.

        Args:
            frame_id: Frame to get info for

        Returns:
            Dict with cache entry info or None if not found
        """
        with self._lock:
            cached = self._cache.get(frame_id)
            if not cached:
                return None

            return {
                "frame_id": frame_id,
                "created_at": cached.created_at,
                "last_accessed": cached.last_accessed,
                "access_count": cached.access_count,
                "age_seconds": time.time() - cached.created_at,
                "is_expired": cached.is_expired(self.ttl_seconds),
                "result_keys": list(cached.result.keys()) if cached.result else [],
            }

    def __len__(self) -> int:
        """Return current cache size."""
        with self._lock:
            return len(self._cache)

    def __contains__(self, frame_id: str) -> bool:
        """Check if frame_id is in cache (may be expired)."""
        with self._lock:
            return frame_id in self._cache
