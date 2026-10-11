"""Data models (matching real SDK)."""

from dataclasses import dataclass, field
from typing import Dict, Optional, Union

from pydantic import BaseModel


class Rows(BaseModel):
    """Describes the rows response from DealCloud."""
    totalRecords: int
    rows: list


@dataclass
class EntryIdCache:
    """
    Mapping from external IDs to DealCloud Entry IDs.
    
    Enables efficient upsert operations by maintaining a lookup table
    from your external system's IDs to DealCloud's internal Entry IDs.
    
    This is an in-memory data structure - the caller is responsible for
    persistence if needed.
    
    Example:
        >>> # Build cache from existing data
        >>> cache = dc.build_entry_id_cache("Company", "crmId")
        >>> 
        >>> # Look up Entry ID by external ID
        >>> entry_id = cache.get("CRM-12345")
        >>> 
        >>> # Check if external ID exists
        >>> if "CRM-12345" in cache:
        ...     print("Found!")
        >>> 
        >>> # Manually add mapping after insert
        >>> cache.set("CRM-99999", 54321)
    """
    object_id: Union[int, str]
    key_field: str  # API name of field used as lookup key
    _cache: Dict[str, int] = field(default_factory=dict)
    
    def get(self, external_id: str) -> Optional[int]:
        """
        Get Entry ID for an external ID.
        
        Args:
            external_id: The external system's ID
        
        Returns:
            DealCloud Entry ID, or None if not found
        """
        return self._cache.get(str(external_id))
    
    def set(self, external_id: str, entry_id: int) -> None:
        """
        Set a mapping from external ID to Entry ID.
        
        Args:
            external_id: The external system's ID
            entry_id: The DealCloud Entry ID
        """
        self._cache[str(external_id)] = entry_id
    
    def bulk_set(self, mappings: Dict[str, int]) -> None:
        """
        Set multiple mappings at once.
        
        Args:
            mappings: Dict of {external_id: entry_id}
        """
        self._cache.update({str(k): v for k, v in mappings.items()})
    
    def remove(self, external_id: str) -> bool:
        """
        Remove a mapping.
        
        Args:
            external_id: The external system's ID to remove
        
        Returns:
            True if removed, False if not found
        """
        if str(external_id) in self._cache:
            del self._cache[str(external_id)]
            return True
        return False
    
    def clear(self) -> None:
        """Remove all mappings."""
        self._cache.clear()
    
    def __contains__(self, external_id: str) -> bool:
        """Check if external ID exists in cache."""
        return str(external_id) in self._cache
    
    def __len__(self) -> int:
        """Return number of mappings."""
        return len(self._cache)
    
    def __iter__(self):
        """Iterate over external IDs."""
        return iter(self._cache)
    
    def items(self):
        """Return all mappings as (external_id, entry_id) pairs."""
        return self._cache.items()
    
    def keys(self):
        """Return all external IDs."""
        return self._cache.keys()
    
    def values(self):
        """Return all Entry IDs."""
        return self._cache.values()


