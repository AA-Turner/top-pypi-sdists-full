"""
Online store configuration for Chalk feature stores.
"""

import inspect
from typing import Optional

from chalk.stores.lru_cache import LRUCache
from chalk.utils.config_hash import generate_config_hash
from chalk.utils.object_inspect import get_source_object_starting
from chalk.utils.source_parsing import should_skip_source_code_parsing


class OnlineStoreConfig:
    """
    Configuration for online store with optional LRU cache.

    This configuration can be passed to the @features decorator to enable
    LRU caching for specific feature classes.

    Parameters
    ----------
    lru_cache : LRUCache, optional
        LRU cache configuration. If provided, an LRU cache will be
        placed in front of the online store for this feature class.
        Each worker process will maintain its own LRU cache instance.

    Examples
    --------
    >>> from chalk.features import features, feature
    >>> from chalk.stores import LRUCache, OnlineStoreConfig
    >>>
    >>> lru_cache_config = OnlineStoreConfig(
    ...     lru_cache=LRUCache(
    ...         max_size=10000,
    ...         ttl="60s",
    ...         store_cache_misses=True,
    ...     )
    ... )
    >>>
    >>> @features(online_store_config=lru_cache_config)
    ... class User:
    ...     id: int
    ...     risk_score: float = feature(max_staleness="1h")
    """

    def __init__(
        self,
        lru_cache: Optional[LRUCache] = None,
    ):
        super().__init__()
        self.errors = []

        if not should_skip_source_code_parsing():
            try:
                internal_frame = inspect.currentframe()
                if internal_frame is not None:
                    definition_frame = internal_frame.f_back
                    if definition_frame is not None:
                        filename = definition_frame.f_code.co_filename
                        source_line_start = definition_frame.f_lineno
                        source_code, source_line_start, source_line_end = get_source_object_starting(definition_frame)
                    del internal_frame
            except Exception:
                pass

        # Validation - collect errors from LRU cache if provided
        if lru_cache is not None and hasattr(lru_cache, "errors"):
            self.errors.extend(lru_cache.errors)

        self.lru_cache = lru_cache
        self.filename = filename
        self.source_line_start = source_line_start
        self.code = source_code
        self.source_line_end = source_line_end
        self.feature_set_namespaces = set()

        # Generate hash-based ID from configuration parameters
        config_dict = {
            "lru_cache": lru_cache,
        }
        self.id = generate_config_hash(config_dict)

        # Check for duplicate configurations with same hash
        dup_online_store_config = ONLINE_STORE_CONFIG_REGISTRY.get(self.id, None)
        if dup_online_store_config is not None:
            self.errors.append(
                (
                    "OnlineStoreConfig with identical configuration already exists "
                    f"in files '{filename}' and '{dup_online_store_config.filename}'. "
                    f"Consider reusing the existing configuration."
                )
            )

        ONLINE_STORE_CONFIG_REGISTRY[self.id] = self

    def __repr__(self) -> str:
        return f"OnlineStoreConfig(id={self.id}, lru_cache={self.lru_cache!r})"


ONLINE_STORE_CONFIG_REGISTRY: dict[str, OnlineStoreConfig] = {}
