"""
Schema caching for DealCloud SDK.

Provides in-memory caching of schema data to avoid repeated API calls
for short-lived client instances.
"""

import threading
import time
from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class CacheEntry:
    """A cache entry with timestamp."""
    data: Any
    timestamp: float = field(default_factory=time.time)
    
    def is_expired(self, ttl_seconds: float) -> bool:
        """Check if entry has expired."""
        return time.time() - self.timestamp > ttl_seconds


class SchemaCache:
    """
    Thread-safe in-memory cache for DealCloud schema data.
    
    Reduces API calls when creating multiple DealCloud client instances
    for the same site.
    
    Example:
        # Cache is global and shared
        cache = SchemaCache.get_instance()
        
        # Check if schema is cached
        if cache.has("site.dealcloud.com", "schema"):
            schema = cache.get("site.dealcloud.com", "schema")
        else:
            schema = dc.get_schema()
            cache.set("site.dealcloud.com", "schema", schema)
        
        # Clear cache for a site
        cache.clear("site.dealcloud.com")
        
        # Clear all caches
        cache.clear_all()
    """
    
    _instance: Optional["SchemaCache"] = None
    _lock = threading.Lock()
    
    def __init__(self, default_ttl: float = 300.0):
        """
        Initialize schema cache.
        
        Args:
            default_ttl: Default time-to-live in seconds (default: 5 minutes)
        """
        self._cache: Dict[str, Dict[str, CacheEntry]] = {}
        self._default_ttl = default_ttl
        self._cache_lock = threading.RLock()
    
    @classmethod
    def get_instance(cls, default_ttl: float = 300.0) -> "SchemaCache":
        """
        Get singleton instance of schema cache.
        
        Args:
            default_ttl: Default TTL for cache entries
        
        Returns:
            SchemaCache instance
        """
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls(default_ttl)
        return cls._instance
    
    def _make_key(self, site: str) -> str:
        """Normalize site URL to cache key."""
        # Remove protocol and trailing slashes
        key = site.lower()
        for prefix in ("https://", "http://"):
            if key.startswith(prefix):
                key = key[len(prefix):]
        return key.rstrip("/")
    
    def has(self, site: str, cache_type: str, ttl: Optional[float] = None) -> bool:
        """
        Check if cache entry exists and is not expired.
        
        Args:
            site: DealCloud site URL
            cache_type: Type of cached data ("schema", "users", etc.)
            ttl: Optional custom TTL to check against
        
        Returns:
            True if valid cache entry exists
        """
        key = self._make_key(site)
        ttl = ttl or self._default_ttl
        
        with self._cache_lock:
            if key not in self._cache:
                return False
            if cache_type not in self._cache[key]:
                return False
            
            entry = self._cache[key][cache_type]
            if entry.is_expired(ttl):
                del self._cache[key][cache_type]
                return False
            
            return True
    
    def get(self, site: str, cache_type: str, ttl: Optional[float] = None) -> Optional[Any]:
        """
        Get cached data if available and not expired.
        
        Args:
            site: DealCloud site URL
            cache_type: Type of cached data
            ttl: Optional custom TTL
        
        Returns:
            Cached data or None if not available/expired
        """
        key = self._make_key(site)
        ttl = ttl or self._default_ttl
        
        with self._cache_lock:
            if key not in self._cache:
                return None
            if cache_type not in self._cache[key]:
                return None
            
            entry = self._cache[key][cache_type]
            if entry.is_expired(ttl):
                del self._cache[key][cache_type]
                return None
            
            return entry.data
    
    def set(self, site: str, cache_type: str, data: Any) -> None:
        """
        Store data in cache.
        
        Args:
            site: DealCloud site URL
            cache_type: Type of cached data
            data: Data to cache
        """
        key = self._make_key(site)
        
        with self._cache_lock:
            if key not in self._cache:
                self._cache[key] = {}
            self._cache[key][cache_type] = CacheEntry(data=data)
    
    def clear(self, site: str, cache_type: Optional[str] = None) -> None:
        """
        Clear cache for a site.
        
        Args:
            site: DealCloud site URL
            cache_type: Specific cache type to clear (all if None)
        """
        key = self._make_key(site)
        
        with self._cache_lock:
            if key not in self._cache:
                return
            
            if cache_type:
                self._cache[key].pop(cache_type, None)
            else:
                del self._cache[key]
    
    def clear_all(self) -> None:
        """Clear all cached data."""
        with self._cache_lock:
            self._cache.clear()
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics.
        
        Returns:
            Dict with cache statistics
        """
        with self._cache_lock:
            total_entries = sum(len(site_cache) for site_cache in self._cache.values())
            return {
                "sites_cached": len(self._cache),
                "total_entries": total_entries,
                "sites": list(self._cache.keys())
            }


# Global cache instance
_schema_cache: Optional[SchemaCache] = None


def get_schema_cache(ttl: float = 300.0) -> SchemaCache:
    """
    Get global schema cache instance.
    
    Args:
        ttl: Default TTL in seconds
    
    Returns:
        SchemaCache instance
    """
    return SchemaCache.get_instance(ttl)


