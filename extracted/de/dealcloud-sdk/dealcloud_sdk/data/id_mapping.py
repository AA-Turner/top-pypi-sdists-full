"""ID mapping and cache utilities."""

from typing import TYPE_CHECKING, List, Optional, Union

from ..models.data import EntryIdCache

if TYPE_CHECKING:
    from .dealcloud_data import DealCloudData
    from .read import read_data


def build_entry_id_cache(
    self: "DealCloudData",
    object_id: Union[int, str],
    key_field: str,
    query: Optional[str] = None,
) -> EntryIdCache:
    """
    Build a mapping from external IDs to DealCloud Entry IDs.
    
    Reads entries from an object and builds a lookup table from your
    key field (e.g., external system ID) to the DealCloud Entry ID.
    
    Args:
        self: DealCloudData instance
        object_id: Object API name or ID
        key_field: API name of the field containing your external ID
        query: Optional DealCloud query to limit which entries are included
    
    Returns:
        EntryIdCache: A mapping object for ID lookups
    
    Example:
        >>> # Build mapping using CRM ID field as the key
        >>> id_map = dc.build_entry_id_cache("Company", "crmId")
        >>> 
        >>> # Look up DealCloud Entry ID by external ID
        >>> entry_id = id_map.get("CRM-12345")
        >>> if entry_id:
        ...     print(f"Found: {entry_id}")
        >>> 
        >>> # Use with map_ids() for bulk operations
        >>> mapped = dc.map_ids(crm_records, id_map, "crm_id")
    
    Note:
        For new integrations, consider using upsert_data() with a 
        unique key field instead, which handles this automatically.
    """
    from .read import read_data
    
    # Read entries with just EntryId and key field for efficiency
    data = read_data(
        self,
        object_id=object_id,
        fields=["EntryId", key_field],
        query=query,
        output="list",
    )
    
    cache = EntryIdCache(object_id=object_id, key_field=key_field)
    for row in data:
        key_value = row.get(key_field)
        entry_id = row.get("EntryId")
        if key_value is not None and entry_id is not None:
            cache.set(str(key_value), entry_id)
    
    return cache


def map_ids(
    data: List[dict],
    cache: EntryIdCache,
    external_id_field: str,
) -> List[dict]:
    """
    Add Entry IDs to records using an ID mapping.
    
    For each record, looks up the external ID in the cache and adds
    the corresponding DealCloud Entry ID if found.
    
    Args:
        data: List of records to map
        cache: EntryIdCache from build_entry_id_cache()
        external_id_field: Field name in data containing the external ID
    
    Returns:
        List of records with 'EntryId' populated where found.
        Records without a match are returned unchanged.
    
    Example:
        >>> # Build ID mapping
        >>> id_map = dc.build_entry_id_cache("Company", "crmId")
        >>> 
        >>> # Map external records
        >>> crm_records = [
        ...     {"crm_id": "CRM-123", "name": "Acme Corp"},
        ...     {"crm_id": "CRM-456", "name": "New Company"},
        ... ]
        >>> mapped = dc.map_ids(crm_records, id_map, "crm_id")
        >>> 
        >>> # Split into inserts vs updates
        >>> to_insert = [r for r in mapped if "EntryId" not in r]
        >>> to_update = [r for r in mapped if "EntryId" in r]
        >>> 
        >>> if to_update:
        ...     dc.update_data("Company", to_update)
        >>> if to_insert:
        ...     dc.insert_data("Company", to_insert)
    """
    result = []
    for record in data:
        mapped_record = record.copy()
        external_id = record.get(external_id_field)
        if external_id is not None:
            entry_id = cache.get(str(external_id))
            if entry_id is not None:
                mapped_record["EntryId"] = entry_id
        result.append(mapped_record)
    return result
