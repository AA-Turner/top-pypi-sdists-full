"""Auto-generated stub for module: result_cache."""
from typing import Any, Dict, Optional

# Constants
DEFAULT_CLEANUP_INTERVAL: int
DEFAULT_MAX_SIZE: int
DEFAULT_TTL_SECONDS: int

# Classes
class CachedResult:
    # Container for cached inference result with metadata.

    def is_expired(self: Any, ttl_seconds: float) -> bool:
        """
        Check if this result has expired based on TTL.
        """
        ...

    def touch(self: Any) -> None:
        """
        Update access metadata (called on cache hit).
        """
        ...

class InferenceResultCache:
    # Thread-safe LRU cache for inference results.
    #
    # Designed for high-throughput inference pipelines where:
    # - Similar frames use cached results instead of re-running inference
    # - Results are keyed by frame_id from streaming gateway
    # - Memory is bounded by max_size with LRU eviction
    # - Old entries expire after ttl_seconds
    #
    # Usage:
    #     cache = InferenceResultCache(max_size=50000, ttl_seconds=300)
    #
    #     # After inference:
    #     cache.put(frame_id, {"model_result": result, "metadata": meta})
    #
    #     # When receiving reference frame:
    #     cached = cache.get(reference_frame_id)
    #     if cached:
    #         # Use cached result
    #     else:
    #         # Cache miss - frame expired or was evicted

    def __init__(self: Any, max_size: int = DEFAULT_MAX_SIZE, ttl_seconds: float = DEFAULT_TTL_SECONDS, cleanup_interval: float = DEFAULT_CLEANUP_INTERVAL, enabled: bool = True) -> None:
        """
        Initialize InferenceResultCache.
        
        Args:
            max_size: Maximum number of cached results
            ttl_seconds: Time-to-live for cached results
            cleanup_interval: How often to clean up expired entries
            enabled: If False, cache operations are no-ops
        """
        ...

    def clear(self: Any) -> None:
        """
        Clear all cached results.
        """
        ...

    def get(self: Any, frame_id: str) -> Optional[Dict[str, Any]]:
        """
        Get cached result for a frame_id.
        
        Args:
            frame_id: Frame identifier to look up
        
        Returns:
            Cached result dict or None if not found/expired
        """
        ...

    def get_cache_info(self: Any, frame_id: str) -> Optional[Dict]:
        """
        Get detailed info about a cached entry.
        
        Args:
            frame_id: Frame to get info for
        
        Returns:
            Dict with cache entry info or None if not found
        """
        ...

    def get_metrics(self: Any) -> Dict[str, Any]:
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
        ...

    def has(self: Any, frame_id: str) -> bool:
        """
        Check if frame_id has a valid (non-expired) cached result.
        
        Note: This does NOT update LRU order - use get() if you need the result.
        
        Args:
            frame_id: Frame identifier to check
        
        Returns:
            True if valid cached result exists
        """
        ...

    def put(self: Any, frame_id: str, result: Dict[str, Any]) -> bool:
        """
        Cache inference result for a frame_id.
        
        Args:
            frame_id: Unique frame identifier from streaming gateway
            result: Inference result to cache (should include model_result, metadata)
        
        Returns:
            True if cached successfully, False otherwise
        """
        ...

    def remove(self: Any, frame_id: str) -> bool:
        """
        Remove a specific entry from cache.
        
        Args:
            frame_id: Frame identifier to remove
        
        Returns:
            True if entry was removed, False if not found
        """
        ...

