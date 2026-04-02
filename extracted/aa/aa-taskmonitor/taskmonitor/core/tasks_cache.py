"""API for caching queued tasks."""

import datetime as dt
import json
from dataclasses import dataclass
from typing import List, NamedTuple, Optional

from django.core.cache import cache
from django.utils import timezone

from taskmonitor.core import app_names


class QueuedTaskShort(NamedTuple):
    """DTO for queued tasks, optimized for size."""

    app_name: str
    id: int
    name: str
    priority: int

    @classmethod
    def from_dict(cls, obj: dict) -> "QueuedTaskShort":
        """Create QueuedTaskShort from raw task dict."""
        if "headers" not in obj:
            raise ValueError("headers missing in obj")
        headers = obj["headers"]
        properties = obj["properties"] if "properties" in obj else {}
        task_name = headers["task"]
        return cls(
            app_name=app_names.from_task_name(task_name),
            id=headers["id"],
            name=task_name,
            priority=properties.get("priority"),
        )

    @classmethod
    def from_binary_json(cls, obj_encoded: bytes) -> "QueuedTaskShort":
        """Create new object from a binary task object retrieved from Redis."""
        obj = json.loads(obj_encoded.decode("utf8"))
        return cls.from_dict(obj)


class QueuedTaskCacheEntry(NamedTuple):
    """Wrapper for storing queued tasks in cache with additional data."""

    tasks: List[QueuedTaskShort]
    created_at: dt.datetime


@dataclass(frozen=True)
class QueuedTasksCache:
    """Cache for queued tasks.

    Can be disabled when timeout is set to 0.

    Args:
        - cache_key: custom string used to store the cache
        - timeout: timeout for cache in seconds
    """

    cache_key: str
    timeout: int = 60

    def get(self) -> Optional[QueuedTaskCacheEntry]:
        """Retrieve content of cache or None if cache is expired or invalid."""
        if not self.timeout:
            return None
        data = cache.get(self.cache_key)
        if data is not None and not isinstance(data, QueuedTaskCacheEntry):
            raise TypeError("Expected data to be of type 'QueuedTaskCacheEntry'")
        return data

    def set(self, tasks: List[QueuedTaskShort]) -> Optional[QueuedTaskCacheEntry]:
        """Store given tasks in cache."""
        if not self.timeout:
            return None
        data = QueuedTaskCacheEntry(tasks=tasks, created_at=timezone.now())
        cache.set(self.cache_key, data, timeout=self.timeout)
        return data

    def clear(self):
        """Clear the cache."""
        cache.delete(self.cache_key)

    def created_at(self) -> Optional[dt.datetime]:
        """Return date when cache was created or None when cache is invalid."""
        data = self.get()
        if data is None:
            return None
        return data.created_at
