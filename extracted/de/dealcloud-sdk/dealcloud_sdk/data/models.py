"""Data models and enums for DealCloud data operations."""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, List, Optional, Union

import pandas as pd

# Type hints for optional polars
if TYPE_CHECKING:
    import polars as pl


# ErrorHandling has been moved to intapp-rest-client
# Import it from there: from intapp_rest_client.models import ErrorHandling
# Keeping this comment for reference - the enum is now in intapp-rest-client


class ReferenceFormat(Enum):
    """How to format reference field values in results.
    
    Controls how reference/relationship fields are returned from read operations.
    Default behavior (no format specified) returns full objects as-is from the API.
    
    Attributes:
        ID: Extract just the entry ID from reference fields.
            Returns integers for single-select, List[int] for multi-select.
        NAME: Extract the display name from reference fields.
            Requires additional API calls to resolve entry names.
            Returns strings for single-select, List[str] for multi-select.
    """
    ID = "id"           # Entry ID only (e.g., 12345)
    NAME = "name"       # Display name only (e.g., "Acme Corp")


@dataclass
class ReferenceCache:
    """LRU-style cache for reference lookups with configurable max size.
    
    Used to cache reference entry name lookups to avoid repeated API calls.
    When the cache exceeds max_entries, oldest entries are evicted.
    
    For larger deployments, consider using `cachetools` library:
        pip install cachetools
        from cachetools import LRUCache
        cache = LRUCache(maxsize=10000)
    
    Or for persistent caching:
        pip install diskcache
        from diskcache import Cache
        cache = Cache('./reference_cache')
    
    Args:
        max_entries: Maximum number of entries to cache (default: 10000)
    """
    max_entries: int = 10000
    _cache: dict = field(default_factory=dict)
    _access_order: list = field(default_factory=list)
    
    def get(self, object_id: Union[int, str], entry_id: int) -> Optional[str]:
        """Get cached display name for a reference entry."""
        key = (str(object_id), entry_id)
        if key in self._cache:
            # Move to end of access order (most recently used)
            if key in self._access_order:
                self._access_order.remove(key)
            self._access_order.append(key)
            return self._cache[key]
        return None
    
    def set(self, object_id: Union[int, str], entry_id: int, name: str) -> None:
        """Cache a display name for a reference entry."""
        key = (str(object_id), entry_id)
        
        # If at capacity, evict oldest entries
        while len(self._cache) >= self.max_entries and self._access_order:
            oldest_key = self._access_order.pop(0)
            self._cache.pop(oldest_key, None)
        
        self._cache[key] = name
        if key in self._access_order:
            self._access_order.remove(key)
        self._access_order.append(key)
    
    def bulk_set(self, object_id: Union[int, str], mappings: dict) -> None:
        """Cache multiple entries at once. mappings: {entry_id: name}"""
        for entry_id, name in mappings.items():
            self.set(object_id, entry_id, name)
    
    def get_missing(self, object_id: Union[int, str], entry_ids: List[int]) -> List[int]:
        """Get list of entry_ids not in cache."""
        return [
            eid for eid in entry_ids 
            if (str(object_id), eid) not in self._cache
        ]
    
    def clear(self) -> None:
        """Clear all cached entries."""
        self._cache.clear()
        self._access_order.clear()
    
    @property
    def size(self) -> int:
        """Current number of cached entries."""
        return len(self._cache)
    
    @property
    def hit_rate_info(self) -> str:
        """Get info about cache usage."""
        return f"Cache size: {self.size}/{self.max_entries}"


@dataclass
class RowsWriteResult:
    """Structured result from a Rows API write (insert/update/upsert)."""

    rows: list = field(default_factory=list)
    ok_rows: list = field(default_factory=list)
    row_errors: list = field(default_factory=list)
    failed_inputs: list = field(default_factory=list)

    @property
    def has_row_errors(self) -> bool:
        """True if any row could not be committed after recovery."""
        return len(self.row_errors) > 0


@dataclass
class BatchResult:
    """Result from a batch operation with potential partial failures."""
    results: list = field(default_factory=list)
    errors: list = field(default_factory=list)
    row_errors: list = field(default_factory=list)
    total_requested: int = 0
    total_succeeded: int = 0
    total_failed: int = 0
    
    @property
    def has_errors(self) -> bool:
        """Check if any transport or row-level errors occurred."""
        return len(self.errors) > 0 or len(self.row_errors) > 0
    
    @property
    def success_rate(self) -> float:
        """Get success rate as a percentage."""
        if self.total_requested == 0:
            return 100.0
        return (self.total_succeeded / self.total_requested) * 100


@dataclass
class ModifiedEntry:
    """An entry that was modified or deleted since a given timestamp."""
    entry_id: int
    modified_date: datetime
    is_deleted: bool = False
    
    @classmethod
    def from_api(cls, data: dict) -> "ModifiedEntry":
        """Create from API response."""
        mod_date = data.get("modifiedDate") or data.get("ModifiedDate")
        if isinstance(mod_date, str):
            # Handle ISO format: "2024-01-15T10:30:00Z"
            mod_date = datetime.fromisoformat(mod_date.replace("Z", "+00:00"))
        return cls(
            entry_id=data.get("entryId") or data.get("EntryId"),
            modified_date=mod_date,
            is_deleted=data.get("isDeleted", False) or data.get("IsDeleted", False),
        )


@dataclass
class DeltaSyncResult:
    """Result from a delta sync operation."""
    modified_ids: List[int] = field(default_factory=list)
    deleted_ids: List[int] = field(default_factory=list)
    modified_data: Union[pd.DataFrame, "pl.DataFrame", List[dict], None] = None
    modified_since: Optional[datetime] = None
    sync_timestamp: datetime = field(default_factory=datetime.now)
    
    @property
    def total_changes(self) -> int:
        """Total number of modified + deleted entries."""
        return len(self.modified_ids) + len(self.deleted_ids)
    
    @property
    def has_modifications(self) -> bool:
        """Check if there are modified entries."""
        return len(self.modified_ids) > 0
    
    @property
    def has_deletions(self) -> bool:
        """Check if there are deleted entries."""
        return len(self.deleted_ids) > 0
