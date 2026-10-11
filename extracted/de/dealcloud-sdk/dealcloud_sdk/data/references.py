"""Reference field resolution and caching."""

import logging
from typing import TYPE_CHECKING, List, Optional, Union

from ..constants import field_types
from ..models.schema import Field
from .models import ReferenceCache, ReferenceFormat

if TYPE_CHECKING:
    from .dealcloud_data import DealCloudData


def get_reference_fields(
    schema_client,
    object_id: Union[str, int]
) -> list[Field]:
    """
    Get only reference fields for an object (not choice or user).
    
    Args:
        schema_client: Client with get_fields() method
        object_id: Object ID or API name
    
    Returns:
        List of Field objects where fieldType is REFERENCE
    """
    fields = schema_client.get_fields(object_id)
    return [f for f in fields if f.fieldType == field_types.REFERENCE]


def fetch_entry_names(
    data_client: "DealCloudData",
    object_id: Union[int, str],
    entry_ids: List[int],
    name_field: str = "Name",
) -> dict:
    """
    Fetch display names for a list of entry IDs.
    
    Args:
        data_client: DealCloudData instance with read_data() method
        object_id: Target object ID or API name
        entry_ids: List of entry IDs to fetch names for
        name_field: Field to use as display name (default: "Name")
    
    Returns:
        Dict mapping entry_id -> display_name
    """
    if not entry_ids:
        return {}
    
    # Build query for the entry IDs
    ids_csv = ",".join(str(eid) for eid in entry_ids)
    query = f"EntryId in ({ids_csv})"
    
    logger = getattr(data_client, '_logger', logging.getLogger(__name__))
    
    try:
        data = data_client.read_data(
            object_id=object_id,
            query=query,
            fields=["EntryId", name_field],
            output="list",
        )
        return {
            row.get("EntryId"): row.get(name_field, str(row.get("EntryId")))
            for row in data
        }
    except Exception as e:
        logger.warning(f"Failed to fetch names for {object_id}: {e}")
        # Return IDs as fallback
        return {eid: str(eid) for eid in entry_ids}


def resolve_reference_value(
    value: Union[dict, list, int, None],
    reference_format: ReferenceFormat,
    target_object: Optional[str] = None,
    cache: Optional[ReferenceCache] = None,
) -> Union[int, str, List[int], List[str], None]:
    """
    Resolve a single reference field value to the requested format.
    
    Args:
        value: Raw value from API (could be dict, list, int, or None)
        reference_format: ID or NAME format
        target_object: Target object for name lookups (required for NAME)
        cache: Optional cache for name lookups
    
    Returns:
        Formatted value based on reference_format
    """
    if value is None:
        return None
    
    # Handle list (multi-select reference)
    if isinstance(value, list):
        return [
            resolve_reference_value(item, reference_format, target_object, cache)
            for item in value
        ]
    
    # Handle dict (single reference with embedded data)
    if isinstance(value, dict):
        if reference_format == ReferenceFormat.ID:
            return value.get("id") or value.get("entryId") or value.get("EntryId")
        elif reference_format == ReferenceFormat.NAME:
            # Try to get name from the dict first
            name = value.get("name") or value.get("Name") or value.get("displayName")
            if name:
                return name
            # Fall back to ID if name not embedded
            entry_id = value.get("id") or value.get("entryId") or value.get("EntryId")
            if entry_id and cache and target_object:
                cached = cache.get(target_object, entry_id)
                if cached:
                    return cached
            return str(entry_id) if entry_id else None
    
    # Handle raw integer (just an ID)
    if isinstance(value, (int, float)):
        entry_id = int(value)
        if reference_format == ReferenceFormat.ID:
            return entry_id
        elif reference_format == ReferenceFormat.NAME:
            if cache and target_object:
                cached = cache.get(target_object, entry_id)
                if cached:
                    return cached
            return str(entry_id)  # Fallback
    
    return value


def apply_reference_format(
    data_client: "DealCloudData",
    rows: List[dict],
    object_id: Union[int, str],
    reference_format: ReferenceFormat,
    reference_cache: Optional[ReferenceCache] = None,
) -> List[dict]:
    """
    Apply reference format transformation to all rows.
    
    Handles both ID extraction and NAME resolution (with caching).
    
    Args:
        data_client: DealCloudData instance with schema and read methods
        rows: List of row dicts from API
        object_id: Source object ID for schema lookup
        reference_format: ID or NAME format
        reference_cache: Optional cache for name lookups
    
    Returns:
        Transformed rows with formatted reference values
    """
    if not rows:
        return rows
    
    # Get reference fields from schema
    ref_fields = get_reference_fields(data_client, object_id)
    if not ref_fields:
        return rows  # No reference fields to transform
    
    # Build mapping of field apiName -> target object
    field_targets = {}
    for field in ref_fields:
        target = None
        if field.entryLists:
            # First entry list is the target object
            target = field.entryLists[0] if len(field.entryLists) == 1 else field.entryLists
        field_targets[field.apiName] = target
    
    # For NAME format, we need to batch-fetch missing names
    if reference_format == ReferenceFormat.NAME and reference_cache is not None:
        prefetch_reference_names(data_client, rows, field_targets, reference_cache)
    
    # Transform each row
    result = []
    for row in rows:
        transformed = row.copy()
        for field_api_name, target_object in field_targets.items():
            if field_api_name in transformed:
                # Get target as string (first object if multi)
                target = target_object[0] if isinstance(target_object, list) else target_object
                transformed[field_api_name] = resolve_reference_value(
                    transformed[field_api_name],
                    reference_format,
                    target_object=str(target) if target else None,
                    cache=reference_cache,
                )
        result.append(transformed)
    
    return result


def prefetch_reference_names(
    data_client: "DealCloudData",
    rows: List[dict],
    field_targets: dict,
    cache: ReferenceCache,
) -> None:
    """
    Pre-fetch display names for all reference fields in rows.
    
    Collects all unique entry IDs per target object and batch-fetches
    their display names into the cache.
    
    Args:
        data_client: DealCloudData instance with fetch_entry_names() method
        rows: Data rows to scan for reference IDs
        field_targets: Mapping of field_api_name -> target_object
        cache: Cache to populate
    """
    # Collect all IDs per target object
    ids_by_object: dict = {}
    
    for row in rows:
        for field_api_name, target_object in field_targets.items():
            value = row.get(field_api_name)
            if not value:
                continue
            
            target = target_object[0] if isinstance(target_object, list) else target_object
            if not target:
                continue
            
            target_key = str(target)
            if target_key not in ids_by_object:
                ids_by_object[target_key] = set()
            
            # Extract entry IDs from value
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        eid = item.get("id") or item.get("entryId") or item.get("EntryId")
                        if eid:
                            ids_by_object[target_key].add(int(eid))
                    elif isinstance(item, (int, float)):
                        ids_by_object[target_key].add(int(item))
            elif isinstance(value, dict):
                eid = value.get("id") or value.get("entryId") or value.get("EntryId")
                if eid:
                    ids_by_object[target_key].add(int(eid))
            elif isinstance(value, (int, float)):
                ids_by_object[target_key].add(int(value))
    
    # Fetch missing names for each target object
    for target_object, all_ids in ids_by_object.items():
        missing_ids = cache.get_missing(target_object, list(all_ids))
        if missing_ids:
            names = fetch_entry_names(data_client, target_object, missing_ids)
            cache.bulk_set(target_object, names)
