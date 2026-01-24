from datetime import timedelta
from typing import Literal, Union

from chalk.utils.duration import parse_chalk_duration


class LRUCache:
    """
    Configuration for LRU cache in front of the online store.

    Each worker process maintains its own LRU cache. If a feature value is found
    in the LRU cache, it will be returned directly. If not found in the LRU cache,
    the online store will be queried.

    Parameters
    ----------
    max_size : int
        Maximum number of entries in the LRU cache. Must be positive.
    ttl : str | timedelta | int | Literal["infinity", "all"]
        time to live (TTL) for cached entries specified as either:
            - a string, e.g. "60s", "5m", "1h",
            - a number of seconds,
            - a timedelta object,
    store_cache_misses : bool, optional
        Whether to cache misses (entries not found in online store).
        If True, cache misses against the online store are stored in
        the LRU cache and subsequent requests for the same primary key
        will not hit the online store until the TTL expires.
        Defaults to False.

    Examples
    --------
    >>> from chalk.stores import LRUCache
    >>> cache = LRUCache(
    ...     max_size=10000,
    ...     ttl="60s",
    ...     store_cache_misses=True,
    ... )
    """

    def __init__(
        self,
        max_size: int,
        ttl: Union[str, int, timedelta, Literal["infinity", "all"]],
        store_cache_misses: bool = False,
    ):
        super().__init__()
        self.errors = []

        self.max_size = max_size
        self.store_cache_misses = store_cache_misses

        # set placeholder value
        self.ttl = timedelta(seconds=0)

        # Validation
        if max_size <= 0:
            self.errors.append("max_size must be positive")

        try:
            self.ttl = parse_chalk_duration(ttl)
        except Exception as e:
            self.errors.append(f"ttl is invalid: {e}")

    def __repr__(self) -> str:
        return f"LRUCache(max_size={self.max_size}, ttl={self.ttl}, store_cache_misses={self.store_cache_misses})"
