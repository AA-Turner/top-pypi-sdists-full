import inspect
from collections import OrderedDict
from collections.abc import Callable, Coroutine
from typing import Any, cast

try:
    import aiocache

    _HAS_AIOCACHE = True
except ImportError:
    _HAS_AIOCACHE = False
    aiocache = None


class InMemoryCacheError(Exception):
    def __init__(self, error_message: str) -> None:
        super().__init__(error_message)


class SimpleLRUCache:
    """
    Simple LRU (Least Recently Used) cache implementation.

    This is a lightweight, bounded-size cache that automatically evicts the least recently
    used items when the capacity is reached. It's designed for simple caching needs where
    you don't want to depend on external caching libraries.

    Example usage:
        cache = SimpleLRUCache(max_size=100)
        await cache.set("key", "value")
        value = await cache.get("key")
    """

    def __init__(self, max_size: int = 1000) -> None:
        """
        Initialize the LRU cache.

        Args:
            max_size: Maximum number of items to store in the cache.
        """
        self.max_size = max_size
        self._cache: OrderedDict[str, Any] = OrderedDict()

    async def get(self, key: str) -> Any | None:
        """
        Get a value from the cache.

        Args:
            key: The key to look up.

        Returns:
            The cached value if found, None otherwise.
        """
        if key in self._cache:
            # Move to end to mark as recently used
            value = self._cache.pop(key)
            self._cache[key] = value
            return value
        return None

    async def set(self, key: str, value: Any) -> None:
        """
        Set a value in the cache.

        Args:
            key: The key to store the value under.
            value: The value to cache.
        """
        if key in self._cache:
            # Update existing entry - move to end
            self._cache.pop(key)
        else:
            # Add new entry, evict oldest if needed
            if len(self._cache) >= self.max_size:
                self._cache.popitem(last=False)
        self._cache[key] = value

    async def delete(self, key: str) -> None:
        """
        Remove an item from the cache.

        Args:
            key: The key to remove.
        """
        self._cache.pop(key, None)

    def clear(self) -> None:
        """Clear all items from the cache."""
        self._cache.clear()

    def __len__(self) -> int:
        """Return the number of items currently in the cache."""
        return len(self._cache)


def in_memory_cache[T: Callable[..., Coroutine[Any, Any, Any]]](
    ttl: int | None = None,
    namespace: str | None = None,
    key: str | None = None,
) -> Callable[[T], T]:
    """
    In-memory cache decorator for async functions using aiocache.

    :param ttl: Seconds to store the result. none means no expiration (indefinite cache).
    :param namespace: Prefix for cache keys. Useful for grouping related cached items.
    :param key: Static key to use. If not provided, key is built from function name + args.
    """

    def decorator(func: T) -> T:
        if not inspect.iscoroutinefunction(func):
            raise InMemoryCacheError(error_message="in_memory_cache only supports async functions")
        if not _HAS_AIOCACHE:
            raise InMemoryCacheError(
                error_message="in_memory_cache requires aiocache. Install: pip install mistralai-workflows[mistralai]"
            )
        return cast(T, aiocache.cached(ttl=ttl, namespace=namespace, key=key)(func))

    return decorator
