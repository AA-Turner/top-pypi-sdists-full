"""Data operations for DealCloud (matching real SDK API)."""

import logging
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import (
    TYPE_CHECKING,
    AsyncIterator,
    Callable,
    Iterator,
    List,
    Literal,
    Optional,
    Tuple,
    Type,
    TypeVar,
    Union,
)

from pydantic import BaseModel, ValidationError

import pandas as pd

# Type hints for optional polars
if TYPE_CHECKING:
    import polars as pl

from ..constants import field_types
from ..models.data import EntryIdCache, Rows
from ..models.schema import Field
from ..reports.dealcloud_reports import DealCloudReports
from ..utils.data_utils import (
    calculate_pagination,
    divide_pages,
    flatten_nested_list,
    format_data,
    rows_query_payload_builder,
)
from ..utils.process_response_errors import process_errors
from ..utils.resolve_references import resolve_object

# Import from new modules
from intapp_rest_client.models import ErrorHandling

from .models import (
    BatchResult,
    DeltaSyncResult,
    ModifiedEntry,
    ReferenceCache,
    ReferenceFormat,
    RowsWriteResult,
)
from .converters import OutputFormat, convert_to_output_format, convert_to_polars
from . import (
    delta_sync,
    id_mapping,
    pagination,
    read,
    references,
    streaming,
    typed,
    write,
)

# Type variable for Pydantic model generic methods
T = TypeVar("T", bound=BaseModel)


class DealCloudData(DealCloudReports):
    """
    One link in the linear inheritance chain; parent order is for composition
    (single DealCloud client gets all features), not dependency. Avoids mixins.
    Data Endpoint Methods.
    """

    def list_configured_views(self, is_private: Optional[bool] = None) -> Rows:
        """
        Return a summary of configured views.
        
        Args:
            is_private: If True, return only private views
        
        Returns:
            Rows object with view information
        """
        return read.list_configured_views(self, is_private)

    def resolve_view(self, view: Union[int, str]) -> dict:
        """
        Resolve a view ID or exact view name to view metadata from list_configured_views.

        Does not read view record data — returns the summary row (id, name, primaryLists, etc.).

        Args:
            view: View ID (int) or exact view name (str)

        Returns:
            View metadata row dict

        Raises:
            ValueError: If view not found or multiple views share the same name
        """
        return read.resolve_view(self, view)

    def resolve_view_display_name(self, view: Union[int, str]) -> str:
        """
        Return a view's display name, or str(view_id) if the name field is missing.

        Args:
            view: View ID (int) or exact view name (str)

        Returns:
            View display name string
        """
        return read.resolve_view_display_name(self, view)

    def get_choice_reference_fields(self, object_id: Union[str, int]) -> list[Field]:
        """
        Get choice, reference, and user fields for an object.
        
        This is essential for building import tools, validation logic,
        or data transformation pipelines that need to identify which
        fields require ID lookups vs. plain values.
        
        Args:
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
        return read.get_choice_reference_fields(self, object_id)

    def _get_reference_fields(self, object_id: Union[str, int]) -> list[Field]:
        """Get only reference fields for an object (not choice or user)."""
        return references.get_reference_fields(self, object_id)
    
    def get_reference_fields(self, object_id: Union[str, int]) -> list[Field]:
        """
        Get reference (relationship) fields for an object.
        
        Reference fields point to entries in other objects. This is essential
        for understanding data relationships, building ERDs, or creating
        migration tools.
        
        Args:
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
        return read.get_reference_fields(self, object_id)

    def _fetch_entry_names(
        self,
        object_id: Union[int, str],
        entry_ids: List[int],
        name_field: str = "Name",
    ) -> dict:
        """
        Fetch display names for a list of entry IDs.
        
        Args:
            object_id: Target object ID or API name
            entry_ids: List of entry IDs to fetch names for
            name_field: Field to use as display name (default: "Name")
        
        Returns:
            Dict mapping entry_id -> display_name
        """
        return references.fetch_entry_names(self, object_id, entry_ids, name_field)
    
    def fetch_entry_names(
        self,
        object_id: Union[int, str],
        entry_ids: List[int],
        name_field: str = "Name",
    ) -> dict:
        """
        Fetch display names for a list of entry IDs.
        
        This is one of the most common operations - resolving DealCloud
        Entry IDs to human-readable names for reports, exports, and UIs.
        
        Args:
            object_id: Object ID or API name (e.g., "Company", "Contact")
            entry_ids: List of Entry IDs to resolve
            name_field: Field containing the display name (default: "Name")
        
        Returns:
            Dict mapping entry_id (int) to display_name (str)
        
        Example:
            >>> # Resolve company IDs to names
            >>> company_ids = [123, 456, 789]
            >>> names = dc.fetch_entry_names("Company", company_ids)
            >>> names
            {123: "Acme Corp", 456: "Beta Inc", 789: "Gamma LLC"}
            
            >>> # Use in a DataFrame transformation
            >>> df["CompanyName"] = df["CompanyId"].map(
            ...     dc.fetch_entry_names("Company", df["CompanyId"].unique().tolist())
            ... )
            
            >>> # With custom name field
            >>> users = dc.fetch_entry_names("User", user_ids, name_field="FullName")
        
        Note:
            - Returns the entry ID as a string if the name lookup fails
            - For bulk operations with caching, consider using ReferenceCache
        """
        return references.fetch_entry_names(self, object_id, entry_ids, name_field)

    def _resolve_reference_value(
        self,
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
        return references.resolve_reference_value(value, reference_format, target_object, cache)

    def _apply_reference_format(
        self,
        rows: List[dict],
        object_id: Union[int, str],
        reference_format: ReferenceFormat,
        reference_cache: Optional[ReferenceCache] = None,
    ) -> List[dict]:
        """
        Apply reference format transformation to all rows.
        
        Handles both ID extraction and NAME resolution (with caching).
        
        Args:
            rows: List of row dicts from API
            object_id: Source object ID for schema lookup
            reference_format: ID or NAME format
            reference_cache: Optional cache for name lookups
        
        Returns:
            Transformed rows with formatted reference values
        """
        return references.apply_reference_format(self, rows, object_id, reference_format, reference_cache)
    
    def apply_reference_format(
        self,
        rows: List[dict],
        object_id: Union[int, str],
        reference_format: ReferenceFormat = None,
        reference_cache: Optional[ReferenceCache] = None,
    ) -> List[dict]:
        """
        Apply reference format transformation to rows from any source.
        
        Use this to transform DealCloud data that wasn't fetched via read_data(),
        such as CSV exports, external API responses, or data warehouse extracts.
        The method uses the object's schema to identify reference fields and
        transforms them to the requested format.
        
        Args:
            rows: List of row dicts with DealCloud field structure
            object_id: Object API name or ID (for schema lookup)
            reference_format: ID (extract integer IDs) or NAME (resolve to display names).
                            Defaults to ReferenceFormat.ID if not specified.
            reference_cache: Optional cache for name lookups. Recommended when using
                           NAME format for better performance on repeated lookups.
        
        Returns:
            List of transformed rows with reference fields in requested format
        
        Example:
            >>> # Transform imported CSV data to extract reference IDs
            >>> import pandas as pd
            >>> from dealcloud_sdk import ReferenceFormat
            >>> 
            >>> csv_data = pd.read_csv("dealcloud_export.csv").to_dict("records")
            >>> transformed = dc.apply_reference_format(
            ...     csv_data, 
            ...     "Company", 
            ...     ReferenceFormat.ID
            ... )
            
            >>> # Convert reference fields to display names with caching
            >>> from dealcloud_sdk import ReferenceCache
            >>> cache = ReferenceCache()
            >>> 
            >>> transformed = dc.apply_reference_format(
            ...     csv_data, 
            ...     "Company", 
            ...     ReferenceFormat.NAME,
            ...     cache
            ... )
            >>> # Cache can be reused across multiple calls for performance
            
            >>> # Process data from external API
            >>> external_data = fetch_from_data_warehouse("Company")
            >>> normalized = dc.apply_reference_format(
            ...     external_data,
            ...     "Company",
            ...     ReferenceFormat.ID
            ... )
        
        Note:
            - Requires the object's schema to be accessible (identifies reference fields)
            - For NAME format, display names are fetched from DealCloud
            - Using a ReferenceCache significantly improves performance for NAME format
            - Original rows are not modified; returns new list with transformed copies
        """
        if reference_format is None:
            reference_format = ReferenceFormat.ID
        return references.apply_reference_format(self, rows, object_id, reference_format, reference_cache)

    def _prefetch_reference_names(
        self,
        rows: List[dict],
        field_targets: dict,
        cache: ReferenceCache,
    ) -> None:
        """
        Pre-fetch display names for all reference fields in rows.
        
        Collects all unique entry IDs per target object and batch-fetches
        their display names into the cache.
        
        Args:
            rows: Data rows to scan for reference IDs
            field_targets: Mapping of field_api_name -> target_object
            cache: Cache to populate
        """
        references.prefetch_reference_names(self, rows, field_targets, cache)

    def read_data(
        self,
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
            include_nulls: Include null columns
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
        """
        return read.read_data(
            self,
            object_id=object_id,
            view_id=view_id,
            output=output,
            resolve=resolve,
            reference_format=reference_format,
            reference_cache=reference_cache,
            view_filter=view_filter,
            fields=fields,
            query=query,
            include_nulls=include_nulls,
            column_headers=column_headers,
            progress_callback=progress_callback,
            error_handling=error_handling,
        )

    # =========================================================================
    # Public Parallel Execution Methods
    # =========================================================================
    
    def parallel_get(
        self,
        urls: list[str],
        max_workers: int = 8,
        error_handling: ErrorHandling = ErrorHandling.FAIL_FAST,
    ) -> Union[list, Tuple[list, list]]:
        """
        Execute parallel GET requests with consistent error handling.
        
        Use this for custom multi-endpoint operations that need parallel
        execution with the same error handling and authentication as the SDK.
        
        Args:
            urls: List of URLs to request (can be full URLs or endpoints)
            max_workers: Number of parallel workers (default: 8)
            error_handling: How to handle errors:
                - FAIL_FAST: Raise on first error
                - COLLECT: Collect errors, return partial results
                - LOG_ONLY: Log errors, continue processing
        
        Returns:
            If FAIL_FAST: List of JSON responses
            If COLLECT/LOG_ONLY: Tuple of (results, errors)
        
        Example:
            >>> # Fetch multiple objects in parallel
            >>> urls = [
            ...     f"{dc.api_url}/schema/entryTypes/{obj}"
            ...     for obj in ["Company", "Contact", "Deal"]
            ... ]
            >>> results = dc.parallel_get(urls)
            
            >>> # With error collection
            >>> results, errors = dc.parallel_get(
            ...     urls, 
            ...     error_handling=ErrorHandling.COLLECT
            ... )
            >>> if errors:
            ...     print(f"Failed: {len(errors)} requests")
        """
        return pagination.parallel_get(self._client, urls, max_workers, error_handling, self._logger)
    
    def parallel_post(
        self,
        url: str,
        payloads: list[dict],
        max_workers: int = 8,
        error_handling: ErrorHandling = ErrorHandling.FAIL_FAST,
    ) -> Union[list, Tuple[list, list]]:
        """
        Execute parallel POST requests with consistent error handling.
        
        Use this for bulk operations that need parallel execution,
        such as multi-object queries or batch processing.
        
        Args:
            url: URL to send all requests to
            payloads: List of JSON payloads (one per request)
            max_workers: Number of parallel workers (default: 8)
            error_handling: How to handle errors
        
        Returns:
            If FAIL_FAST: List of JSON responses
            If COLLECT/LOG_ONLY: Tuple of (results, errors)
        
        Example:
            >>> # Parallel queries across multiple objects
            >>> query_url = f"{dc.api_url}/data/entrydata/rows/query"
            >>> payloads = [
            ...     {"objectApiName": "Company", "query": "Status = 'Active'"},
            ...     {"objectApiName": "Contact", "query": "Status = 'Active'"},
            ...     {"objectApiName": "Deal", "query": "Stage = 'Closed'"},
            ... ]
            >>> results = dc.parallel_post(query_url, payloads)
            
            >>> # With error handling
            >>> results, errors = dc.parallel_post(
            ...     url, payloads,
            ...     error_handling=ErrorHandling.COLLECT
            ... )
        """
        return pagination.parallel_post(self._client, url, payloads, max_workers, error_handling, self._logger)
    
    def paginated_read(
        self,
        url: str,
        method: str = "GET",
        request_body: Optional[dict] = None,
        page_size: int = 1000,
        max_workers: int = 8,
        progress_callback: Optional[Callable[[int, int], None]] = None,
        error_handling: ErrorHandling = ErrorHandling.FAIL_FAST,
    ) -> Union[list[dict], BatchResult]:
        """
        Generic paginated read for any endpoint.
        
        Use this for custom or undocumented endpoints that need pagination
        support. Uses the same parallel speculative fetching strategy as
        read_data() for optimal performance.
        
        Args:
            url: Base URL (skip/limit will be added)
            method: HTTP method - "GET" or "POST"
            request_body: Optional body for POST requests
            page_size: Number of rows per page (default: 1000)
            max_workers: Number of parallel workers (default: 8)
            progress_callback: Optional callback(current_rows, estimated_total)
            error_handling: How to handle errors
        
        Returns:
            If FAIL_FAST: List of all rows from all pages
            If COLLECT: BatchResult with rows and errors
        
        Example:
            >>> # Custom endpoint with GET pagination
            >>> all_data = dc.paginated_read(
            ...     f"{dc.api_url}/custom/endpoint?filter=active",
            ...     page_size=500
            ... )
            
            >>> # POST endpoint with body
            >>> all_data = dc.paginated_read(
            ...     f"{dc.api_url}/data/query",
            ...     method="POST",
            ...     request_body={"filter": {"status": "Active"}},
            ...     page_size=1000
            ... )
            
            >>> # With progress tracking
            >>> def on_progress(current, total):
            ...     print(f"Loaded {current}/{total} rows")
            >>> data = dc.paginated_read(url, progress_callback=on_progress)
        
        Note:
            - Responses must have a "rows" key containing the data array
            - Pagination stops when an empty "rows" array is returned
            - Uses speculative parallel fetching for better performance
        """
        return pagination.paginated_read(
            self._client,
            url,
            method,
            request_body,
            page_size,
            max_workers,
            progress_callback,
            error_handling,
            self._logger,
        )
    
    # Private methods for backward compatibility with tests
    def _parallel_requests_get(
        self,
        urls: list[str],
        max_workers: int = 8,
        error_handling: ErrorHandling = ErrorHandling.FAIL_FAST,
    ) -> Union[list, Tuple[list, list]]:
        """Private method for backward compatibility with tests."""
        return self._client.parallel_get(
            endpoints=urls,
            max_workers=max_workers,
            error_handling=error_handling
        )
    
    def _parallel_requests_post(
        self,
        url: str,
        payloads: list[dict],
        max_workers: int = 8,
        error_handling: ErrorHandling = ErrorHandling.FAIL_FAST,
    ) -> Union[list, Tuple[list, list]]:
        """Private method for backward compatibility with tests."""
        return self._client.parallel_post(
            endpoint=url,
            payloads=payloads,
            max_workers=max_workers,
            error_handling=error_handling
        )
    
    def _paginated_read_until_empty(
        self,
        base_url: str,
        method: str = "GET",
        request_body: Optional[dict] = None,
        page_size: int = 1000,
        max_workers: int = 8,
        progress_callback: Optional[Callable[[int, int], None]] = None,
        error_handling: ErrorHandling = ErrorHandling.FAIL_FAST,
    ) -> Union[list[dict], BatchResult]:
        """Private method for backward compatibility. Deprecated: use read_data_streaming/read_view_streaming."""
        import warnings
        warnings.warn(
            "_paginated_read_until_empty is deprecated; read methods use "
            "read_data_streaming/read_view_streaming.",
            DeprecationWarning,
            stacklevel=2,
        )
        return pagination.paginated_read_until_empty(
            self._client,
            base_url,
            method,
            request_body,
            page_size,
            max_workers,
            progress_callback,
            error_handling,
            self._logger,
        )

    def get_total_record_count(self, object_api_name: str) -> int:
        """
        Return the total number of records for an object (single GET with limit=1).

        Use this for cheap "is empty?" checks instead of read_data() which paginates
        through all rows.
        """
        resp = self._client.get(
            f"{self._rows_url}/{object_api_name}?wrapIntoArrays=false&limit=1"
        )
        return resp.get("totalRecords", 0)

    def read_data_streaming(
        self,
        object_id: Union[int, str],
        fields: Optional[list[str]] = None,
        query: Optional[str] = None,
        page_size: Optional[int] = None,
        max_concurrency: Optional[int] = None,
    ) -> Iterator[list[dict]]:
        """
        Stream data from a DealCloud object in batches.
        
        Memory-efficient generator that yields batches of rows as they're fetched,
        without loading all data into memory. Ideal for bulk operations like:
        - Bulk delete (process batch → delete → repeat)
        - Large exports (stream to file)
        - ETL pipelines (process incrementally)
        
        Args:
            object_id: Object API name or ID
            fields: Optional list of field names to return (reduces payload size)
            query: Optional DealCloud query string (e.g., "EntryId in (1,2,3)" or MongoDB-style).
                   When provided, uses POST endpoint; otherwise uses GET.
            page_size: Number of rows per batch (default: from config querySettings.pageSize)
            max_concurrency: Parallel page fetches (default: from config concurrencyLimits.read)
        
        Yields:
            list[dict]: Batch of rows, each as a dictionary
        
        Example:
            # Process and delete in batches (efficient for millions of rows)
            for batch in dc.read_data_streaming("Company", fields=["EntryId"]):
                entry_ids = [row["EntryId"] for row in batch]
                dc.delete_data("Company", entry_ids)
                print(f"Deleted {len(entry_ids)} rows")
            
            # Stream to CSV file (fsspec supports local paths and URIs)
            import fsspec

            with fsspec.open("export.csv", "w") as f:
                first_batch = True
                for batch in dc.read_data_streaming("Contact"):
                    df = pd.DataFrame(batch)
                    df.to_csv(f, header=first_batch, index=False)
                    first_batch = False
            
            # Query-based streaming (e.g. delta sync)
            ids_str = ",".join(map(str, entry_ids))
            for batch in dc.read_data_streaming("Company", query=f"EntryId in ({ids_str})"):
                process(batch)
            
            # Parallel fetching for faster throughput
            for batch in dc.read_data_streaming("Company", max_concurrency=5):
                process(batch)
        
        Note:
            - When max_concurrency=1 (default), fetches sequentially to maintain order
            - When max_concurrency>1, fetches pages in parallel but yields in order
            - Each batch is independent - can be processed and discarded
            - Stops when API returns empty rows array
            - For views, use read_view_streaming()
            - When query is provided, uses POST endpoint; otherwise uses GET.
        """
        yield from streaming.read_data_streaming(self, object_id, fields, query, page_size, max_concurrency)

    def query_data(
        self,
        object_id: Union[int, str],
        query: str,
        fields: Optional[list[str]] = None,
        limit: Optional[int] = None,
        skip: Optional[int] = None,
    ) -> dict:
        """
        Run a single rows/query request and return the full API response.
        
        Convenience helper for the POST .../data/entrydata/rows/query/{object_id}
        endpoint. Use when you need one page of results or the raw response
        (rows, totalRecords, etc.). For large result sets or streaming, use
        read_data() or read_data_streaming() with the same query.
        
        Args:
            object_id: Object API name or ID
            query: DealCloud query string (e.g. "Status = 'Active'", "{entryid: 123}")
            fields: Optional list of field names to return
            limit: Max rows to return (optional)
            skip: Number of rows to skip (optional)
        
        Returns:
            Full response dict from the API, typically with "rows" and optionally
            "totalRecords". Example: {"rows": [...], "totalRecords": 42}
        
        Example:
            >>> resp = dc.query_data("Company", "Status = 'Active'", limit=10)
            >>> rows = resp["rows"]
            >>> total = resp.get("totalRecords")
        """
        endpoint = f"{self._query_url}/{object_id}"
        body = rows_query_payload_builder(query, fields=fields, limit=limit, skip=skip)
        return self._client.post(endpoint, json=body)

    def read_view_streaming(
        self,
        view_id: Union[int, str],
        view_filter: Optional[list[dict]] = None,
        page_size: Optional[int] = None,
        max_concurrency: Optional[int] = None,
    ) -> Iterator[list[dict]]:
        """
        Stream data from a DealCloud view in batches.
        
        Memory-efficient generator for views, similar to read_data_streaming.
        Uses POST with query string pagination (DealCloud View API format).
        
        Args:
            view_id: View ID or name
            view_filter: Optional Supply Value Later filter values
            page_size: Number of rows per batch (default: from config querySettings.pageSize)
            max_concurrency: Parallel page fetches (default: from config concurrencyLimits.read)
        
        Yields:
            list[dict]: Batch of rows, each as a dictionary
        
        Example:
            # Delete all entries from a filtered view
            for batch in dc.read_view_streaming(12345):
                entry_ids = [row["EntryId"] for row in batch]
                if entry_ids:
                    dc.delete_data("Company", entry_ids)
            
            # Parallel fetching for faster throughput
            for batch in dc.read_view_streaming("My View", max_concurrency=5):
                process(batch)
        """
        yield from streaming.read_view_streaming(self, view_id, view_filter, page_size, max_concurrency)

    async def aread_data_streaming(
        self,
        object_id: Union[int, str],
        fields: Optional[list[str]] = None,
        query: Optional[str] = None,
        page_size: Optional[int] = None,
        max_concurrency: Optional[int] = None,
    ) -> AsyncIterator[list[dict]]:
        """
        Async stream data from a DealCloud object in batches.
        
        Memory-efficient async generator that yields batches of rows as they're
        fetched, without loading all data into memory. Ideal for async bulk
        operations and concurrent processing.
        
        Args:
            object_id: Object API name or ID
            fields: Optional list of field names to return (reduces payload size)
            query: Optional DealCloud query string (e.g., "EntryId in (1,2,3)" or MongoDB-style).
                   When provided, uses POST endpoint; otherwise uses GET.
            page_size: Number of rows per batch (default: from config querySettings.pageSize)
            max_concurrency: Parallel page fetches (default: from config concurrencyLimits.read)
        
        Yields:
            list[dict]: Batch of rows, each as a dictionary
        
        Example:
            # Async process and delete in batches
            async for batch in dc.aread_data_streaming("Company", fields=["EntryId"]):
                entry_ids = [row["EntryId"] for row in batch]
                await process_batch(entry_ids)
            
            # Query-based async streaming (e.g. delta sync)
            ids_str = ",".join(map(str, entry_ids))
            async for batch in dc.aread_data_streaming("Company", query=f"EntryId in ({ids_str})"):
                await process(batch)
            
            # Parallel fetching for faster throughput
            async for batch in dc.aread_data_streaming("Company", max_concurrency=5):
                await process(batch)
        
        Note:
            - When max_concurrency=1, fetches sequentially to maintain order
            - When max_concurrency>1, fetches pages in parallel but yields in order
            - Each batch is independent - can be processed and discarded
            - Stops when API returns empty rows array
            - For views, use aread_view_streaming()
            - When query is provided, uses POST endpoint; otherwise uses GET.
        """
        async for batch in streaming.aread_data_streaming(self, object_id, fields, query, page_size, max_concurrency):
            yield batch

    async def aread_view_streaming(
        self,
        view_id: Union[int, str],
        view_filter: Optional[list[dict]] = None,
        page_size: Optional[int] = None,
        max_concurrency: Optional[int] = None,
    ) -> AsyncIterator[list[dict]]:
        """
        Async stream data from a DealCloud view in batches.
        
        Memory-efficient async generator for views. Uses POST with query string
        pagination (DealCloud View API format).
        
        Args:
            view_id: View ID or name
            view_filter: Optional Supply Value Later filter values
            page_size: Number of rows per batch (default: from config querySettings.pageSize)
            max_concurrency: Parallel page fetches (default: from config concurrencyLimits.read)
        
        Yields:
            list[dict]: Batch of rows, each as a dictionary
        
        Example:
            # Async delete all entries from a filtered view
            async for batch in dc.aread_view_streaming(12345):
                entry_ids = [row["EntryId"] for row in batch]
                if entry_ids:
                    await delete_batch(entry_ids)
            
            # Parallel fetching for faster throughput
            async for batch in dc.aread_view_streaming("My View", max_concurrency=5):
                await process(batch)
        """
        async for batch in streaming.aread_view_streaming(self, view_id, view_filter, page_size, max_concurrency):
            yield batch

    def insert_data(
        self,
        object_api_name: str,
        data: Union[list[dict], pd.DataFrame, "pl.DataFrame"],
        use_dealcloud_ids: bool = True,
        lookup_column: Optional[str] = None,
        output: str = "list",
        progress_callback: Optional[Callable[[int, int], None]] = None,
        error_handling: ErrorHandling = ErrorHandling.FAIL_FAST,
        raise_on_row_errors: Optional[bool] = None,
    ) -> Union[list[dict], pd.DataFrame, "pl.DataFrame", BatchResult, RowsWriteResult]:
        """
        Insert data into DealCloud.
        
        Args:
            object_api_name: API name of the object
            data: Data to insert. Accepts:
                  - list[dict]
                  - pandas.DataFrame
                  - polars.DataFrame (requires: pip install dealcloud-sdk[polars])
            use_dealcloud_ids: Use DealCloud IDs for references
            lookup_column: Column to use for lookup
            output: Output format:
                   - "list": List of dictionaries (default)
                   - "write_result": :class:`RowsWriteResult`
                   - "pandas": pandas DataFrame
                   - "polars": Polars DataFrame (requires: pip install dealcloud-sdk[polars])
            progress_callback: Optional callback (current, total)
            error_handling: Parallel **transport** error behavior. Does not control row
                ``Errors`` in HTTP 200 responses.
            raise_on_row_errors: When True, raise on row ``Errors`` in HTTP 200 body.
                When None, uses ``DealCloudConfig.raiseOnRowErrors``.
        
        Returns:
            Insert results in requested format. If error_handling=COLLECT, returns BatchResult.
        
        Example:
            >>> import polars as pl
            >>> df = pl.DataFrame({"Name": ["Acme", "Beta"], "Revenue": [1000, 2000]})
            >>> result = dc.insert_data("Company", df, output="polars")
        """
        return write.insert_data(
            self, object_api_name, data, use_dealcloud_ids, lookup_column,
            output, progress_callback, error_handling, raise_on_row_errors,
        )

    def update_data(
        self,
        object_api_name: str,
        data: Union[list[dict], pd.DataFrame, "pl.DataFrame"],
        use_dealcloud_ids: bool = True,
        lookup_column: Optional[str] = None,
        output: str = "list",
        progress_callback: Optional[Callable[[int, int], None]] = None,
        error_handling: ErrorHandling = ErrorHandling.FAIL_FAST,
        raise_on_row_errors: Optional[bool] = None,
    ) -> Union[list[dict], pd.DataFrame, "pl.DataFrame", BatchResult, RowsWriteResult]:
        """
        Update data in DealCloud.
        
        Args:
            object_api_name: API name of the object
            data: Data to update. Accepts:
                  - list[dict]
                  - pandas.DataFrame
                  - polars.DataFrame (requires: pip install dealcloud-sdk[polars])
            use_dealcloud_ids: Use DealCloud IDs for references
            lookup_column: Column to use for lookup
            output: Output format:
                   - "list": List of dictionaries (default)
                   - "write_result": :class:`RowsWriteResult`
                   - "pandas": pandas DataFrame
                   - "polars": Polars DataFrame (requires: pip install dealcloud-sdk[polars])
            progress_callback: Optional callback (current, total)
            error_handling: Parallel **transport** error behavior. Does not control row
                ``Errors`` in HTTP 200 responses.
            raise_on_row_errors: When True, raise on row ``Errors`` in HTTP 200 body.
                When None, uses ``DealCloudConfig.raiseOnRowErrors``.
        
        Returns:
            Update results in requested format. If error_handling=COLLECT, returns BatchResult.
        
        Example:
            >>> import polars as pl
            >>> df = pl.DataFrame({"EntryId": [123, 456], "Revenue": [1500, 2500]})
            >>> result = dc.update_data("Company", df, output="polars")
        """
        return write.update_data(
            self, object_api_name, data, use_dealcloud_ids, lookup_column,
            output, progress_callback, error_handling, raise_on_row_errors,
        )

    def upsert_data(
        self,
        object_api_name: str,
        data: Union[list[dict], pd.DataFrame, "pl.DataFrame"],
        use_dealcloud_ids: bool = True,
        lookup_column: Optional[str] = None,
        output: str = "list",
        progress_callback: Optional[Callable[[int, int], None]] = None,
        error_handling: ErrorHandling = ErrorHandling.FAIL_FAST,
        raise_on_row_errors: Optional[bool] = None,
    ) -> Union[list[dict], pd.DataFrame, "pl.DataFrame", BatchResult, RowsWriteResult]:
        """
        Insert or update data based on EntryId presence.
        
        Args:
            object_api_name: API name of the object
            data: Data to upsert. Accepts:
                  - list[dict]
                  - pandas.DataFrame
                  - polars.DataFrame (requires: pip install dealcloud-sdk[polars])
            use_dealcloud_ids: Use DealCloud IDs for references
            lookup_column: Column to use for lookup
            output: Output format:
                   - "list": List of dictionaries (default)
                   - "write_result": :class:`RowsWriteResult`
                   - "pandas": pandas DataFrame
                   - "polars": Polars DataFrame (requires: pip install dealcloud-sdk[polars])
            progress_callback: Optional callback (current, total)
            error_handling: Parallel **transport** error behavior for insert/update paths.
            raise_on_row_errors: When True, raise on row ``Errors`` in HTTP 200 body.
                When None, uses ``DealCloudConfig.raiseOnRowErrors``.
        
        Returns:
            Upsert results in requested format. If error_handling=COLLECT, returns BatchResult.
        
        Example:
            >>> import polars as pl
            >>> df = pl.DataFrame({
            ...     "EntryId": [123, None],  # 123 will update, None will insert
            ...     "Name": ["Updated Corp", "New Corp"],
            ... })
            >>> result = dc.upsert_data("Company", df, output="polars")
        """
        return write.upsert_data(
            self, object_api_name, data, use_dealcloud_ids, lookup_column, output,
            progress_callback, error_handling, raise_on_row_errors,
        )

    def delete_data(
        self,
        object_api_name: str,
        records: list[int],
        page_size: Optional[int] = None,
        progress_callback: Optional[Callable[[int, int], None]] = None,
        error_handling: ErrorHandling = ErrorHandling.FAIL_FAST,
        raise_on_row_errors: Optional[bool] = None,
    ) -> Union[list[dict], BatchResult]:
        """
        Delete data from DealCloud.
        
        Args:
            object_api_name: API name of the object
            records: List of entry IDs to delete
            page_size: Batch size for deletes
            progress_callback: Optional callback (current, total)
            error_handling: Parallel **transport** error behavior. Does not control row
                ``Errors`` in HTTP 200 responses.
            raise_on_row_errors: When True, raise on row ``Errors`` in HTTP 200 body.
                When None, uses ``DealCloudConfig.raiseOnRowErrors``.
        
        Returns:
            Delete results. If error_handling=COLLECT, returns BatchResult.
        """
        return write.delete_data(
            self,
            object_api_name,
            records,
            page_size,
            progress_callback,
            error_handling,
            raise_on_row_errors,
        )

    def validate_field_mapping(
        self,
        object_api_name: str,
        columns: Union[set[str], list[str]],
    ) -> bool:
        """
        Validate that column names exist in a DealCloud object.
        
        Use this for pre-flight validation before attempting insert/update
        operations. Get clear error messages upfront rather than mid-batch failures.
        
        Args:
            object_api_name: Object API name (e.g., "Company")
            columns: Column names to validate (set or list)
        
        Returns:
            True if all columns are valid
        
        Raises:
            KeyError: If any columns don't exist, lists the invalid columns
        
        Example:
            >>> # Validate before import
            >>> df = pd.read_csv("import_data.csv")
            >>> try:
            ...     dc.validate_field_mapping("Company", set(df.columns))
            ...     print("All columns valid!")
            ...     dc.insert_data("Company", df)
            ... except KeyError as e:
            ...     print(f"Invalid columns: {e}")
            
            >>> # Check programmatically
            >>> columns = {"Name", "Status", "InvalidField"}
            >>> try:
            ...     dc.validate_field_mapping("Company", columns)
            ... except KeyError as e:
            ...     invalid = str(e)  # Contains list of invalid fields
            ...     print(f"Please fix these columns: {invalid}")
        
        Note:
            "EntryId" is always considered valid even though it's not a field.
        """
        return write.validate_field_mapping(self, object_api_name, columns)

    # -------------------------------------------------------------------------
    # ID Mapping Methods
    # -------------------------------------------------------------------------

    def build_entry_id_cache(
        self,
        object_id: Union[int, str],
        key_field: str,
        query: Optional[str] = None,
    ) -> EntryIdCache:
        """
        Build a mapping from external IDs to DealCloud Entry IDs.
        
        Reads entries from an object and builds a lookup table from your
        key field (e.g., external system ID) to the DealCloud Entry ID.
        
        Args:
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
        return id_mapping.build_entry_id_cache(self, object_id, key_field, query)

    def map_ids(
        self,
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
        return id_mapping.map_ids(data, cache, external_id_field)

    # -------------------------------------------------------------------------
    # Delta Sync / Incremental Sync Methods
    # -------------------------------------------------------------------------

    def get_modified_entries(
        self,
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
        return delta_sync.get_modified_entries(self, object_id, modified_since, include_deleted)

    async def aget_modified_entries(
        self,
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
        return await delta_sync.aget_modified_entries(self, object_id, modified_since, include_deleted)

    def sync_delta(
        self,
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
        return delta_sync.sync_delta(self, object_id, modified_since, fields, output, resolve, stream_threshold)

    # -------------------------------------------------------------------------
    # Typed Data Methods (Pydantic Models)
    # -------------------------------------------------------------------------

    def typed_read_data(
        self,
        model: Type[T],
        object_id: Optional[Union[int, str]] = None,
        view_id: Optional[Union[int, str]] = None,
        query: Optional[str] = None,
        fields: Optional[List[str]] = None,
        reference_format: Optional[ReferenceFormat] = None,
        reference_cache: Optional[ReferenceCache] = None,
        skip_validation_errors: bool = False,
        **kwargs,
    ) -> List[T]:
        """
        Read data as typed Pydantic models.
        
        Typed wrapper around read_data() - returns List[T] instead of 
        list[dict] or DataFrame. Customer defines their own Pydantic models
        matching their DealCloud schema.
        
        Args:
            model: Pydantic model class to deserialize into
            object_id: Object API name or ID
            view_id: View ID (alternative to object_id)
            query: Optional DealCloud query string
            fields: Fields to fetch (default: auto-detect from model)
            reference_format: How to format reference fields (ID, NAME, or None for full)
            reference_cache: Optional cache for reference name lookups
            skip_validation_errors: If True, skip rows that fail validation
                                   (logs warning). If False (default), raises.
            **kwargs: Additional args passed to read_data()
        
        Returns:
            List of model instances
        
        Example:
            >>> from pydantic import BaseModel
            >>> from typing import Optional
            >>> 
            >>> class Company(BaseModel):
            ...     EntryId: int
            ...     Name: str
            ...     Industry: Optional[str] = None
            ...     Revenue: Optional[float] = None
            >>> 
            >>> # Read from object
            >>> companies = dc.typed_read_data(Company, object_id="Company")
            >>> for c in companies:
            ...     print(f"{c.Name}: {c.Industry}")  # Full autocomplete!
            >>> 
            >>> # Read from view
            >>> deals = dc.typed_read_data(DealSummary, view_id="Active Deals")
            >>> 
            >>> # With query filter and reference names
            >>> active = dc.typed_read_data(
            ...     Company,
            ...     object_id="Company",
            ...     query="Status = 'Active'",
            ...     reference_format=ReferenceFormat.NAME
            ... )
        """
        return typed.typed_read_data(
            self, model, object_id, view_id, query, fields,
            reference_format, reference_cache, skip_validation_errors, **kwargs
        )

    def typed_read_data_polars(
        self,
        model: Type[T],
        object_id: Optional[Union[int, str]] = None,
        view_id: Optional[Union[int, str]] = None,
        query: Optional[str] = None,
        fields: Optional[List[str]] = None,
        reference_format: Optional[ReferenceFormat] = None,
        reference_cache: Optional[ReferenceCache] = None,
        lazy: bool = False,
        **kwargs,
    ) -> Union["pl.DataFrame", "pl.LazyFrame"]:
        """
        Read data as a Polars DataFrame with schema derived from Pydantic model.
        
        Combines the performance of Polars with the type documentation of Pydantic
        models. The model defines which fields to fetch and documents the expected
        types, but data is returned as a Polars DataFrame for efficient processing.
        
        Args:
            model: Pydantic model class (used for field selection, not validation)
            object_id: Object API name or ID
            view_id: View ID (alternative to object_id)
            query: Optional DealCloud query string
            fields: Fields to fetch (default: auto-detect from model)
            reference_format: How to format reference fields (ID, NAME, or None for full)
            reference_cache: Optional cache for reference name lookups
            lazy: If True, return LazyFrame for deferred execution
            **kwargs: Additional args passed to read_data()
        
        Returns:
            Polars DataFrame (or LazyFrame if lazy=True)
        
        Example:
            >>> from pydantic import BaseModel
            >>> 
            >>> class Company(BaseModel):
            ...     EntryId: int
            ...     Name: str
            ...     Revenue: float
            >>> 
            >>> # Get polars DataFrame with model-defined fields
            >>> df = dc.typed_read_data_polars(Company, object_id="Company")
            >>> 
            >>> # Fast Polars operations
            >>> high_revenue = df.filter(pl.col("Revenue") > 1000000)
            >>> 
            >>> # LazyFrame for query optimization
            >>> lf = dc.typed_read_data_polars(Company, object_id="Company", lazy=True)
            >>> result = lf.filter(pl.col("Revenue") > 1000000).collect()
        
        Note:
            Unlike typed_read_data(), this does NOT validate data against the model.
            The model is only used for field selection and documentation.
            For validation, use typed_read_data() instead.
        """
        return typed.typed_read_data_polars(
            self, model, object_id, view_id, query, fields,
            reference_format, reference_cache, lazy, **kwargs
        )

    def typed_read_data_streaming(
        self,
        model: Type[T],
        object_id: Optional[Union[int, str]] = None,
        view_id: Optional[Union[int, str]] = None,
        query: Optional[str] = None,
        fields: Optional[List[str]] = None,
        reference_format: Optional[ReferenceFormat] = None,
        reference_cache: Optional[ReferenceCache] = None,
        skip_validation_errors: bool = False,
        **kwargs,
    ) -> Iterator[T]:
        """
        Stream data as typed Pydantic models (memory-efficient).
        
        Typed wrapper around read_data_streaming() - yields model instances
        one at a time instead of dicts.
        
        Args:
            model: Pydantic model class
            object_id: Object API name or ID
            view_id: View ID (alternative to object_id)
            query: Optional DealCloud query string
            fields: Fields to fetch (default: auto-detect from model)
            reference_format: How to format reference fields
            reference_cache: Optional cache for reference name lookups
            skip_validation_errors: If True, skip invalid rows
            **kwargs: Additional args passed to read_data_streaming()
        
        Yields:
            Model instances one at a time
        
        Example:
            >>> for company in dc.typed_read_data_streaming(Company, object_id="Company"):
            ...     process(company)  # Memory-efficient for large datasets
        """
        yield from typed.typed_read_data_streaming(
            self, model, object_id, view_id, query, fields,
            reference_format, reference_cache, skip_validation_errors, **kwargs
        )

    async def typed_aread_data_streaming(
        self,
        model: Type[T],
        object_id: Optional[Union[int, str]] = None,
        view_id: Optional[Union[int, str]] = None,
        query: Optional[str] = None,
        fields: Optional[List[str]] = None,
        reference_format: Optional[ReferenceFormat] = None,
        reference_cache: Optional[ReferenceCache] = None,
        skip_validation_errors: bool = False,
        **kwargs,
    ) -> AsyncIterator[T]:
        """
        Async stream data as typed Pydantic models.
        
        Typed wrapper around aread_data_streaming() - async yields model
        instances one at a time.
        
        Args:
            model: Pydantic model class
            object_id: Object API name or ID
            view_id: View ID (alternative to object_id)
            query: Optional DealCloud query string
            fields: Fields to fetch (default: auto-detect from model)
            reference_format: How to format reference fields
            reference_cache: Optional cache for reference name lookups
            skip_validation_errors: If True, skip invalid rows
            **kwargs: Additional args passed to aread_data_streaming()
        
        Yields:
            Model instances one at a time (async)
        
        Example:
            >>> async for company in dc.typed_aread_data_streaming(Company, object_id="Company"):
            ...     await process_async(company)
        """
        async for item in typed.typed_aread_data_streaming(
            self, model, object_id, view_id, query, fields,
            reference_format, reference_cache, skip_validation_errors, **kwargs
        ):
            yield item

    def typed_insert_data(
        self,
        object_id: Union[int, str],
        data: List[T],
        model: Type[T],
        **kwargs,
    ) -> List[T]:
        """
        Insert typed records into DealCloud.
        
        Typed wrapper around insert_data() - accepts and returns Pydantic
        model instances instead of dicts.
        
        Args:
            object_id: Object API name or ID
            data: List of Pydantic model instances to insert
            model: Model class (for return type deserialization)
            **kwargs: Additional args passed to insert_data()
        
        Returns:
            List of inserted records as model instances (with EntryIds populated)
        
        Example:
            >>> from pydantic import BaseModel
            >>> from typing import Optional
            >>> 
            >>> class Company(BaseModel):
            ...     EntryId: Optional[int] = None
            ...     Name: str
            ...     Industry: Optional[str] = None
            >>> 
            >>> new_companies = [
            ...     Company(Name="Acme Corp", Industry="Technology"),
            ...     Company(Name="Beta Inc", Industry="Finance"),
            ... ]
            >>> 
            >>> inserted = dc.typed_insert_data("Company", new_companies, Company)
            >>> for c in inserted:
            ...     print(f"Created {c.Name} with ID {c.EntryId}")
        """
        return typed.typed_insert_data(self, object_id, data, model, **kwargs)

    def typed_update_data(
        self,
        object_id: Union[int, str],
        data: List[T],
        model: Type[T],
        **kwargs,
    ) -> List[T]:
        """
        Update typed records in DealCloud.
        
        Typed wrapper around update_data() - accepts and returns Pydantic
        model instances instead of dicts.
        
        Args:
            object_id: Object API name or ID
            data: List of Pydantic models with EntryId set
            model: Model class (for return type deserialization)
            **kwargs: Additional args passed to update_data()
        
        Returns:
            List of updated records as model instances
        
        Example:
            >>> # Fetch, modify, update
            >>> companies = dc.typed_read_data(Company, object_id="Company", query="Industry = 'Tech'")
            >>> for c in companies:
            ...     c.Industry = "Technology"  # Standardize
            >>> 
            >>> updated = dc.typed_update_data("Company", companies, Company)
            >>> print(f"Updated {len(updated)} companies")
        """
        return typed.typed_update_data(self, object_id, data, model, **kwargs)

    def typed_upsert_data(
        self,
        object_id: Union[int, str],
        data: List[T],
        model: Type[T],
        match_field: str,
        **kwargs,
    ) -> List[T]:
        """
        Upsert typed records (insert or update based on match field).
        
        Typed wrapper around upsert_data() - accepts and returns Pydantic
        model instances instead of dicts.
        
        Args:
            object_id: Object API name or ID
            data: List of Pydantic model instances
            model: Model class (for return type deserialization)
            match_field: Field API name to match on (must be unique in DealCloud)
            **kwargs: Additional args passed to upsert_data()
        
        Returns:
            List of upserted records as model instances (with EntryIds)
        
        Example:
            >>> class Company(BaseModel):
            ...     EntryId: Optional[int] = None
            ...     Name: str
            ...     CrmId: str  # External system ID
            ...     Revenue: Optional[float] = None
            >>> 
            >>> # Sync from external CRM system
            >>> crm_companies = [
            ...     Company(Name="Acme Corp", CrmId="CRM-123", Revenue=1000000),
            ...     Company(Name="New Corp", CrmId="CRM-456", Revenue=500000),
            ... ]
            >>> 
            >>> result = dc.typed_upsert_data(
            ...     "Company",
            ...     crm_companies,
            ...     Company,
            ...     match_field="CrmId"  # Match on CRM ID
            ... )
            >>> 
            >>> for c in result:
            ...     print(f"{c.Name}: EntryId={c.EntryId}")
        """
        return typed.typed_upsert_data(self, object_id, data, model, match_field, **kwargs)
