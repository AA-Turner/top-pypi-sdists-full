"""Core data read operations."""

import itertools
from typing import TYPE_CHECKING, Callable, Optional, Union
import pandas as pd

if TYPE_CHECKING:
    import polars as pl

from ..constants import field_types
from ..models.data import Rows
from ..models.schema import Field
from ..utils.resolve_references import resolve_object

from intapp_rest_client.models import ErrorHandling

from .converters import OutputFormat, convert_to_output_format, convert_to_polars
from .models import BatchResult, ReferenceCache, ReferenceFormat
from . import references
from .streaming import read_data_streaming, read_view_streaming

if TYPE_CHECKING:
    from .dealcloud_data import DealCloudData


def list_configured_views(
    self: "DealCloudData",
    is_private: Optional[bool] = None
) -> Rows:
    """
    Return a summary of configured views.
    
    Args:
        self: DealCloudData instance
        is_private: If True, return only private views
    
    Returns:
        Rows object with view information
    """
    url = self._views_url
    if is_private is not None:
        url = f"{url}?isprivate={str(is_private).lower()}"
    
    response = self._client.get(url)
    return Rows(**response)


def resolve_view(
    self: "DealCloudData",
    view: Union[int, str],
) -> dict:
    """
    Resolve a view ID or exact view name to view metadata from list_configured_views.

    Does not read view record data — returns the summary row (id, name, primaryLists, etc.).

    Args:
        self: DealCloudData instance
        view: View ID (int) or exact view name (str)

    Returns:
        View metadata row dict from list_configured_views().rows

    Raises:
        ValueError: If view not found or multiple views share the same name
    """
    rows = list_configured_views(self).rows
    if isinstance(view, str):
        matches = [row for row in rows if row.get("name") == view]
        if len(matches) > 1:
            raise ValueError(f"Multiple views named {view!r}; use view ID")
        if not matches:
            raise ValueError(f"View {view!r} not found")
        return matches[0]
    for row in rows:
        if row.get("id") == view:
            return row
    raise ValueError(f"View {view} not found")


def resolve_view_display_name(
    self: "DealCloudData",
    view: Union[int, str],
) -> str:
    """
    Return a view's display name, or str(view_id) if the name field is missing.

    Args:
        self: DealCloudData instance
        view: View ID (int) or exact view name (str)

    Returns:
        View display name string
    """
    row = resolve_view(self, view)
    view_id = int(row["id"])
    return row.get("name") or str(view_id)


def get_choice_reference_fields(
    self: "DealCloudData",
    object_id: Union[str, int]
) -> list[Field]:
    """
    Get choice, reference, and user fields for an object.
    
    This is essential for building import tools, validation logic,
    or data transformation pipelines that need to identify which
    fields require ID lookups vs. plain values.
    
    Args:
        self: DealCloudData instance
        object_id: Object ID or API name
    
    Returns:
        List of Field objects where fieldType is CHOICE, REFERENCE, or USER
    
    Example:
        >>> # Find fields that need special handling
        >>> special_fields = dc.get_choice_reference_fields("Company")
        >>> for field in special_fields:
        ...     print(f"{field.apiName}: {field.fieldType}")
        Status: 4  # CHOICE
        PrimaryContact: 5  # REFERENCE
        Owner: 7  # USER
        
        >>> # Build a lookup map for import processing
        >>> lookup_fields = {f.apiName for f in dc.get_choice_reference_fields("Company")}
        >>> for column in df.columns:
        ...     if column in lookup_fields:
        ...         # This column needs ID resolution
        ...         df[column] = resolve_ids(df[column], column)
    """
    fields = self.get_fields(object_id)
    return [
        f for f in fields 
        if f.fieldType in [field_types.REFERENCE, field_types.CHOICE, field_types.USER]
    ]


def get_reference_fields(
    self: "DealCloudData",
    object_id: Union[str, int]
) -> list[Field]:
    """
    Get reference (relationship) fields for an object.
    
    Reference fields point to entries in other objects. This is essential
    for understanding data relationships, building ERDs, or creating
    migration tools.
    
    Args:
        self: DealCloudData instance
        object_id: Object ID or API name
    
    Returns:
        List of Field objects where fieldType is REFERENCE (5)
    
    Example:
        >>> # Find all relationship fields on Company
        >>> ref_fields = dc.get_reference_fields("Company")
        >>> for field in ref_fields:
        ...     targets = field.entryLists or []
        ...     print(f"{field.apiName} -> {targets}")
        PrimaryContact -> [12345]  # Points to Contact object
        Deals -> [12346]  # Points to Deal object
        
        >>> # Build relationship map for the entire schema
        >>> schema = dc.get_schema()
        >>> relationships = {}
        >>> for obj_name in schema.objects:
        ...     refs = dc.get_reference_fields(obj_name)
        ...     relationships[obj_name] = [
        ...         {"field": f.apiName, "targets": f.entryLists}
        ...         for f in refs
        ...     ]
    
    Note:
        Use get_choice_reference_fields() if you also need CHOICE and USER fields.
    """
    return references.get_reference_fields(self, object_id)


def _validate_and_resolve_view_id(
    self: "DealCloudData",
    view_id: Union[int, str]
) -> tuple[int, bool]:
    """
    Validate and resolve view_id, and determine include_nulls setting.
    
    This function consolidates all view validation logic in one place:
    - Resolves string view names to integer IDs
    - Validates view existence
    - Sets include_nulls=False for all views (required workaround until API provides view column metadata)
    
    Args:
        self: DealCloudData instance
        view_id: View ID (int) or view name (str)
    
    Returns:
        Tuple of (resolved_view_id: int, include_nulls: bool)
        - resolved_view_id: Integer view ID (resolved from name if needed)
        - include_nulls: Always False for views (workaround for missing column metadata)
    
    Raises:
        AttributeError: If view name not found or multiple views with same name
    
    Note:
        include_nulls is always False for views because:
        - Views have no column metadata API (no way to know which columns are configured)
        - When include_nulls=True, the API returns all possible fields from underlying objects
        - This results in hundreds or thousands of columns instead of expected configured columns
        - TODO: Once API provides view column metadata, we can support include_nulls=True correctly
    """
    include_nulls = False
    try:
        row = resolve_view(self, view_id)
    except ValueError as e:
        raise AttributeError(str(e)) from e
    return int(row["id"]), include_nulls


def read_object(
    self: "DealCloudData",
    object_id: Union[int, str],
    output: OutputFormat,
    resolve: Optional[str] = None,
    reference_format: Optional[ReferenceFormat] = None,
    reference_cache: Optional[ReferenceCache] = None,
    fields: Optional[list[str]] = None,
    query: Optional[str] = None,
    include_nulls: bool = True,
    progress_callback: Optional[Callable[[int, int], None]] = None,
    error_handling: ErrorHandling = ErrorHandling.FAIL_FAST,
) -> Union[list[dict], pd.DataFrame, "pl.DataFrame", "pl.LazyFrame", BatchResult]:
    """
    Read data from a DealCloud object.
    
    This function handles all object-specific reading logic, including:
    - URL building for object reads (GET vs POST with query)
    - Pagination and parallel fetching
    - Reference format transformation
    - Output format conversion (list, pandas, polars)
    - Legacy resolve parameter handling
    
    Args:
        self: DealCloudData instance
        object_id: Object API name or ID
        output: Output format ("list", "pandas", "polars", or "polars_lazy")
        resolve: "id" or "name" for choice/reference fields (legacy parameter)
        reference_format: How to format reference field values
        reference_cache: Optional cache for reference name lookups
        fields: Specific fields to return
        query: DealCloud query string
        include_nulls: Include null columns
        progress_callback: Optional callback for progress updates
        error_handling: How to handle errors in parallel requests
    
    Returns:
        Data in the requested format

    Note:
        Pagination does not use totalRecords. We read until the API returns
        an empty rows array (stream ends); the client's get_paginated implements this.
    """
    # Collect all batches from streaming; stop when client sees empty [] from API (no totalRecords)
    all_batches = []
    total_rows = 0
    errors = []
    
    try:
        for batch in read_data_streaming(
            self,
            object_id=object_id,
            fields=fields,
            query=query,
            page_size=self.page_size,
            max_concurrency=self.read_concurrency,
        ):
            all_batches.append(batch)
            total_rows += len(batch)
            
            # Progress callback
            if progress_callback:
                try:
                    # Estimate total (conservative - assume more pages)
                    estimated_total = total_rows + self.page_size
                    progress_callback(total_rows, estimated_total)
                except Exception as e:
                    self._logger.warning(f"Progress callback failed: {e}")
    except Exception as e:
        # Handle errors based on error_handling mode
        if error_handling == ErrorHandling.FAIL_FAST:
            raise
        elif error_handling == ErrorHandling.COLLECT:
            errors.append({"error": str(e), "error_type": type(e).__name__})
        else:  # LOG_ONLY
            self._logger.error(f"Error during read: {e}")
    
    # Flatten all batches into single list
    rows = list(itertools.chain.from_iterable(all_batches))
    
    # Create BatchResult if in COLLECT mode
    if error_handling == ErrorHandling.COLLECT:
        batch_result = BatchResult(
            results=rows,
            errors=errors,
            total_requested=total_rows,
            total_succeeded=len(rows),
            total_failed=len(errors),
        )
    else:
        batch_result = None
    
    # Handle empty results
    if len(rows) == 0:
        if error_handling == ErrorHandling.COLLECT:
            batch_result.results = convert_to_output_format([], output)
            return batch_result
        return convert_to_output_format([], output)
    
    # Apply reference format transformation (if specified)
    if reference_format is not None:
        # Create default cache if NAME format requested without one
        if reference_format == ReferenceFormat.NAME and reference_cache is None:
            reference_cache = ReferenceCache(max_entries=10000)
        
        rows = references.apply_reference_format(self, rows, object_id, reference_format, reference_cache)
        
        # Update batch_result if in COLLECT mode
        if error_handling == ErrorHandling.COLLECT:
            batch_result.results = rows
    
    # Resolve choice/reference fields to id/name (legacy `resolve` parameter).
    # Applied to the raw rows so it works for every output format (list, polars,
    # pandas) rather than only pandas. resolve_object is a local dict.get, so this
    # adds no network calls beyond the single (cached) schema lookup below.
    if resolve and reference_format is None:
        resolve_field_names = [
            f.apiName
            for f in get_choice_reference_fields(self, object_id)
            if f.apiName
        ]
        if resolve_field_names:
            for row in rows:
                for field_name in resolve_field_names:
                    value = row.get(field_name)
                    if isinstance(value, list):
                        row[field_name] = "; ".join(
                            str(resolve_object(i, resolve)) for i in value
                        )
        if error_handling == ErrorHandling.COLLECT:
            batch_result.results = rows
    
    # Return as list
    if output == "list":
        if error_handling == ErrorHandling.COLLECT:
            batch_result.results = rows
            return batch_result
        return rows
    
    # Return as polars DataFrame or LazyFrame
    if output in ("polars", "polars_lazy"):
        result = convert_to_polars(rows, output)
        if error_handling == ErrorHandling.COLLECT:
            batch_result.results = result
            return batch_result
        return result
    
    # Return as pandas DataFrame
    df = pd.DataFrame.from_records(rows)
    if 'EntryId' in df.columns:
        df = df.set_index('EntryId')
    
    # Reference resolution already happened on the raw rows above; preserve the
    # legacy behavior of normalizing empty cells to empty strings when resolving.
    if resolve and reference_format is None:
        df = df.fillna("")
    
    if error_handling == ErrorHandling.COLLECT:
        batch_result.results = df
        return batch_result
    
    return df


def read_view(
    self: "DealCloudData",
    view_id: Union[int, str],
    output: OutputFormat,
    view_filter: Optional[list[dict]] = None,
    fields: Optional[list[str]] = None,
    progress_callback: Optional[Callable[[int, int], None]] = None,
    error_handling: ErrorHandling = ErrorHandling.FAIL_FAST,
) -> Union[list[dict], pd.DataFrame, "pl.DataFrame", "pl.LazyFrame", BatchResult]:
    """
    Read data from a DealCloud view.
    
    This function handles all view-specific reading logic, including:
    - View ID validation and name resolution
    - Setting include_nulls=False (required workaround for views)
    - View-specific API calls and pagination
    
    Args:
        self: DealCloudData instance
        view_id: View ID (int) or view name (str)
        output: Output format ("list", "pandas", "polars", or "polars_lazy")
        view_filter: Supply Value Later filter values
        fields: Specific fields to return (not typically used with views)
        progress_callback: Optional callback for progress updates
        error_handling: How to handle errors in parallel requests
    
    Returns:
        Data in the requested format
    
    Note:
        Pagination does not use totalRecords; we read until the API returns
        an empty rows array (read_view_streaming / client implement this).
        The include_nulls parameter is automatically set to False for views
        to prevent excessive columns. This is a workaround until the API
        provides view column metadata.
    """
    # Validate and resolve view_id (consolidated validation logic)
    resolved_view_id, _ = _validate_and_resolve_view_id(self, view_id)
    
    # Collect all batches from streaming; stop when client sees empty [] (no totalRecords)
    all_batches = []
    total_rows = 0
    errors = []
    
    try:
        for batch in read_view_streaming(
            self,
            view_id=resolved_view_id,  # Use resolved ID
            view_filter=view_filter,
            page_size=self.page_size,
            max_concurrency=self.read_concurrency,
        ):
            all_batches.append(batch)
            total_rows += len(batch)
            
            # Progress callback
            if progress_callback:
                try:
                    # Estimate total (conservative - assume more pages)
                    estimated_total = total_rows + self.page_size
                    progress_callback(total_rows, estimated_total)
                except Exception as e:
                    self._logger.warning(f"Progress callback failed: {e}")
    except Exception as e:
        # Handle errors based on error_handling mode
        if error_handling == ErrorHandling.FAIL_FAST:
            raise
        elif error_handling == ErrorHandling.COLLECT:
            errors.append({"error": str(e), "error_type": type(e).__name__})
        else:  # LOG_ONLY
            self._logger.error(f"Error during view read: {e}")
    
    # Flatten all batches into single list
    rows = list(itertools.chain.from_iterable(all_batches))
    
    # Create BatchResult if in COLLECT mode
    if error_handling == ErrorHandling.COLLECT:
        batch_result = BatchResult(
            results=rows,
            errors=errors,
            total_requested=total_rows,
            total_succeeded=len(rows),
            total_failed=len(errors),
        )
    else:
        batch_result = None
    
    # Handle empty results
    if len(rows) == 0:
        if error_handling == ErrorHandling.COLLECT:
            batch_result.results = convert_to_output_format([], output)
            return batch_result
        return convert_to_output_format([], output)
    
    # Return as list
    if output == "list":
        if error_handling == ErrorHandling.COLLECT:
            batch_result.results = rows
            return batch_result
        return rows
    
    # Return as polars DataFrame or LazyFrame
    if output in ("polars", "polars_lazy"):
        result = convert_to_polars(rows, output)
        if error_handling == ErrorHandling.COLLECT:
            batch_result.results = result
            return batch_result
        return result
    
    # Return as pandas DataFrame
    df = pd.DataFrame.from_records(rows)
    if 'EntryId' in df.columns:
        df = df.set_index('EntryId')
    
    if error_handling == ErrorHandling.COLLECT:
        batch_result.results = df
        return batch_result
    
    return df


def read_data(
    self: "DealCloudData",
    object_id: Optional[Union[int, str]] = None,
    view_id: Optional[Union[int, str]] = None,
    output: Optional[OutputFormat] = None,
    resolve: Optional[str] = None,
    reference_format: Optional[ReferenceFormat] = None,
    reference_cache: Optional[ReferenceCache] = None,
    view_filter: Optional[list[dict]] = None,
    fields: Optional[list[str]] = None,
    query: Optional[str] = None,
    include_nulls: bool = True,
    column_headers: str = "api",
    progress_callback: Optional[Callable[[int, int], None]] = None,
    error_handling: ErrorHandling = ErrorHandling.FAIL_FAST,
) -> Union[list[dict], pd.DataFrame, "pl.DataFrame", "pl.LazyFrame", BatchResult]:
    """
    Read data from a DealCloud object or view.
    
    Args:
        self: DealCloudData instance
        object_id: Object API name or ID
        view_id: View ID or name
        output: Output format:
               - "list": List of dictionaries
               - "pandas": pandas DataFrame
               - "polars": Polars DataFrame (faster, less memory)
               - "polars_lazy": Polars LazyFrame (for query optimization)
               **MIGRATION NOTE:** This parameter no longer has a default.
               You must explicitly specify the output format.
        resolve: "id" or "name" for choice/reference fields (legacy parameter,
                use reference_format for more control)
        reference_format: How to format reference field values:
                - None (default): Return full reference objects as-is
                - ReferenceFormat.ID: Extract entry IDs only
                - ReferenceFormat.NAME: Extract display names (requires lookups)
        reference_cache: Optional cache for reference name lookups.
                Improves performance when reference_format=NAME.
                Create with: ReferenceCache(max_entries=10000)
        view_filter: Supply Value Later filter values
        fields: Specific fields to return
        query: DealCloud query string
        include_nulls: Include null columns (ignored for views, always False)
        column_headers: "api", "name", or "id" for column naming
        progress_callback: Optional callback for progress updates (current_rows, estimated_total)
        error_handling: How to handle errors in parallel requests
    
    Returns:
        Data in the requested format:
        - output="list": list[dict]
        - output="pandas": pandas.DataFrame
        - output="polars": polars.DataFrame (requires: pip install dealcloud-sdk[polars])
        - output="polars_lazy": polars.LazyFrame (for query optimization)
        If error_handling=COLLECT, returns BatchResult with partial results.
    
    Note:
        Only one of object_id or view_id can be specified.
        
        When reading from views, the include_nulls parameter is automatically
        set to False to prevent excessive columns. This is a workaround until
        the API provides view column metadata.
    
    Example:
        >>> # pandas DataFrame
        >>> df = dc.read_data("Company", output="pandas")
        >>> 
        >>> # Polars DataFrame (10-100x faster for large datasets)
        >>> df = dc.read_data("Company", output="polars")
        >>> 
        >>> # Polars LazyFrame for query optimization
        >>> lf = dc.read_data("Company", output="polars_lazy")
        >>> result = lf.filter(pl.col("Revenue") > 1000000).collect()
        >>> 
        >>> # Reference formatting
        >>> df = dc.read_data(
        ...     "Contact",
        ...     output="polars",
        ...     reference_format=ReferenceFormat.NAME,
        ... )
        >>> 
        >>> # Reading from a view
        >>> df = dc.read_data(view_id="My View", output="pandas")
    """
    if object_id and view_id:
        raise AttributeError('Only one of "object_id" and "view_id" can be entered')
    if not object_id and not view_id:
        raise AttributeError('Must pass one of "object_id" and "view_id"')
    
    # Require explicit output format (migration from v0.x which defaulted to "pandas")
    if output is None:
        raise ValueError(
            'The "output" parameter is required. '
            'Specify output="pandas", "list", "polars", or "polars_lazy". '
            'This is a breaking change from v0.x which defaulted to "pandas".'
        )
    
    valid_outputs = ("pandas", "list", "polars", "polars_lazy")
    if output not in valid_outputs:
        raise ValueError(f'output must be one of {valid_outputs}')
    
    # Delegate to appropriate function based on input
    if object_id:
        return read_object(
            self,
            object_id=object_id,
            output=output,
            resolve=resolve,
            reference_format=reference_format,
            reference_cache=reference_cache,
            fields=fields,
            query=query,
            include_nulls=include_nulls,
            progress_callback=progress_callback,
            error_handling=error_handling,
        )
    return read_view(
        self,
        view_id=view_id,
        output=output,
        view_filter=view_filter,
        fields=fields,
        progress_callback=progress_callback,
        error_handling=error_handling,
    )
