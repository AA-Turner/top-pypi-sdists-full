"""Delta sync and incremental sync operations."""

from datetime import datetime
from typing import TYPE_CHECKING, List, Optional, Union
import pandas as pd

from .converters import convert_to_output_format
from .models import DeltaSyncResult, ModifiedEntry
from . import streaming

if TYPE_CHECKING:
    import polars as pl
    from .dealcloud_data import DealCloudData
    from .read import read_data


def get_modified_entries(
    self: "DealCloudData",
    object_id: Union[int, str],
    modified_since: Union[datetime, str],
    include_deleted: bool = True,
) -> List[ModifiedEntry]:
    """
    Get entry IDs modified or deleted since a specific datetime.
    
    Returns a lightweight list of entry IDs (no full data). This is the
    first step in a delta sync workflow - follow up with read_data()
    to fetch the actual values.
    
    Args:
        self: DealCloudData instance
        object_id: Object ID or API name (e.g., "Company" or 12345)
        modified_since: Datetime cutoff (entries modified after this time).
                       Accepts datetime object or ISO format string.
        include_deleted: If True (default), includes deleted entry IDs
    
    Returns:
        List of ModifiedEntry objects with:
        - entry_id: The entry ID
        - modified_date: When the entry was last modified
        - is_deleted: True if entry was deleted
    
    Note:
        This endpoint returns ALL modified IDs in one response (no pagination).
        For large deltas, plan your read_data() call accordingly.
    
    Example:
        >>> from datetime import datetime, timedelta
        >>> 
        >>> # Get what changed in last hour
        >>> last_sync = datetime.now() - timedelta(hours=1)
        >>> changes = dc.get_modified_entries("Company", last_sync)
        >>> 
        >>> print(f"Found {len(changes)} modified entries")
        >>> 
        >>> # Separate modifications from deletions
        >>> modified = [c for c in changes if not c.is_deleted]
        >>> deleted = [c for c in changes if c.is_deleted]
    
    See Also:
        sync_delta(): Convenience helper that implements the common pattern
        read_data(): Fetch full data for modified entries
    """
    # Convert datetime to ISO format string
    if isinstance(modified_since, datetime):
        modified_since_str = modified_since.isoformat()
    else:
        modified_since_str = modified_since
    
    # Build URL: /api/rest/v4/data/entrylist/{entryListId}/entries/history
    url = f"{self._data_url}/entrylist/{object_id}/entries/history"
    params = {
        "modifiedSince": modified_since_str,
        "includeDeleted": str(include_deleted).lower(),
    }
    
    response = self._client.get(url, params=params)
    
    # Parse response - API returns list of entry modifications
    if isinstance(response, list):
        return [ModifiedEntry.from_api(entry) for entry in response]
    elif isinstance(response, dict) and "entries" in response:
        return [ModifiedEntry.from_api(entry) for entry in response["entries"]]
    return []


async def aget_modified_entries(
    self: "DealCloudData",
    object_id: Union[int, str],
    modified_since: Union[datetime, str],
    include_deleted: bool = True,
) -> List[ModifiedEntry]:
    """
    Async version: Get entry IDs modified or deleted since a specific datetime.
    
    See get_modified_entries() for full documentation.
    
    Example:
        >>> changes = await dc.aget_modified_entries("Company", last_sync_time)
    """
    # Convert datetime to ISO format string
    if isinstance(modified_since, datetime):
        modified_since_str = modified_since.isoformat()
    else:
        modified_since_str = modified_since
    
    url = f"{self._data_url}/entrylist/{object_id}/entries/history"
    params = {
        "modifiedSince": modified_since_str,
        "includeDeleted": str(include_deleted).lower(),
    }
    
    response = await self._client.aget(url, params=params)
    
    if isinstance(response, list):
        return [ModifiedEntry.from_api(entry) for entry in response]
    elif isinstance(response, dict) and "entries" in response:
        return [ModifiedEntry.from_api(entry) for entry in response["entries"]]
    return []


def sync_delta(
    self: "DealCloudData",
    object_id: Union[int, str],
    modified_since: Union[datetime, str],
    fields: Optional[List[str]] = None,
    output: str = "list",
    resolve: Optional[str] = None,
    stream_threshold: int = 500,
) -> DeltaSyncResult:
    """
    The Most Common Pattern: Get changes and fetch modified data.
    
    This is a convenience helper that implements the typical delta sync
    workflow:
    1. Get entry IDs modified since last sync
    2. Separate modifications from deletions
    3. Fetch full data for modified entries
    
    For custom workflows, use get_modified_entries() + read_data() directly.
    
    Args:
        self: DealCloudData instance
        object_id: Object ID or API name (e.g., "Company")
        modified_since: Datetime cutoff (entries modified after this time)
        fields: Optional list of field API names to retrieve.
               If None, retrieves all fields.
        output: Output format for modified_data:
               - "list": List of dictionaries (default)
               - "pandas": pandas DataFrame
               - "polars": Polars DataFrame (requires: pip install dealcloud-sdk[polars])
               - "polars_lazy": Polars LazyFrame
        resolve: Reference field handling:
                - None: Return raw reference IDs (default)
                - "name": Return reference display names
                - "full": Return full reference objects
        stream_threshold: If more than this many modifications, uses
                         streaming internally for memory efficiency (default: 500)
    
    Returns:
        DeltaSyncResult with:
        - modified_ids: List of modified entry IDs
        - deleted_ids: List of deleted entry IDs
        - modified_data: Full data for modified entries (list or DataFrame)
        - modified_since: The cutoff datetime used
        - sync_timestamp: When this sync was performed
    
    Example - Basic Usage:
        >>> from datetime import datetime, timedelta
        >>> 
        >>> # Get what changed in last 24 hours
        >>> last_sync = datetime.now() - timedelta(days=1)
        >>> result = dc.sync_delta("Company", last_sync)
        >>> 
        >>> print(f"Modified: {len(result.modified_ids)}")
        >>> print(f"Deleted: {len(result.deleted_ids)}")
        >>> 
        >>> # Process modified data
        >>> for row in result.modified_data:
        ...     print(row)
        >>> 
        >>> # Handle deletions in your system
        >>> for entry_id in result.deleted_ids:
        ...     your_db.mark_deleted(entry_id)
    
    Example - With Pandas and Reference Names:
        >>> result = dc.sync_delta(
        ...     "Contact",
        ...     modified_since=last_sync,
        ...     output="pandas",
        ...     resolve="name",  # Get company names, not IDs
        ...     fields=["Name", "Email", "Company"],
        ... )
        >>> 
        >>> df = result.modified_data
        >>> print(df.head())
    
    Example - Custom Workflow (Build Your Own):
        >>> # For more control, use the building blocks directly:
        >>> changes = dc.get_modified_entries("Company", last_sync)
        >>> 
        >>> modified_ids = [c.entry_id for c in changes if not c.is_deleted]
        >>> deleted_ids = [c.entry_id for c in changes if c.is_deleted]
        >>> 
        >>> # Use streaming for large datasets
        >>> if len(modified_ids) > 1000:
        ...     for row in dc.read_data_streaming(
        ...         "Company",
        ...         query=f"EntryId in ({','.join(map(str, modified_ids))})"
        ...     ):
        ...         process_row(row)
    
    See Also:
        get_modified_entries(): Get just the entry IDs (building block)
        aget_modified_entries(): Async version of get_modified_entries
        read_data(): Fetch data with full control
    """
    from .read import read_data
    
    # Record when sync started
    sync_start = datetime.now()
    
    # Parse modified_since if string
    if isinstance(modified_since, str):
        modified_since_dt = datetime.fromisoformat(modified_since.replace("Z", "+00:00"))
    else:
        modified_since_dt = modified_since
    
    # Step 1: Get modified entry IDs
    changes = get_modified_entries(
        self,
        object_id=object_id,
        modified_since=modified_since,
        include_deleted=True,
    )
    
    # Step 2: Separate modifications from deletions
    modified_ids = [c.entry_id for c in changes if not c.is_deleted]
    deleted_ids = [c.entry_id for c in changes if c.is_deleted]
    
    # Step 3: Fetch full data for modifications
    modified_data: Union[pd.DataFrame, "pl.DataFrame", List[dict], None] = None
    
    if modified_ids:
        # Build query for modified entry IDs
        ids_csv = ",".join(map(str, modified_ids))
        query = f"EntryId in ({ids_csv})"
        
        if len(modified_ids) > stream_threshold:
            # Large batch - use read_data with query (more efficient than filtering)
            modified_data = read_data(
                self,
                object_id=object_id,
                fields=fields,
                query=query,
                output=output,
                resolve=resolve,
            )
        else:
            # Small batch - direct read
            modified_data = read_data(
                self,
                object_id=object_id,
                fields=fields,
                query=query,
                output=output,
                resolve=resolve,
            )
    else:
        # No modifications - return empty in appropriate format
        modified_data = convert_to_output_format([], output)
    
    return DeltaSyncResult(
        modified_ids=modified_ids,
        deleted_ids=deleted_ids,
        modified_data=modified_data,
        modified_since=modified_since_dt,
        sync_timestamp=sync_start,
    )
