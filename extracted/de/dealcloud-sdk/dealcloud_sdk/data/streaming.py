"""Streaming data operations."""

from typing import TYPE_CHECKING, AsyncIterator, Iterator, Optional, Union

if TYPE_CHECKING:
    from .dealcloud_data import DealCloudData
    from .read import list_configured_views


def read_data_streaming(
    self: "DealCloudData",
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
        self: DealCloudData instance
        object_id: Object API name or ID
        fields: Optional list of field names to return (reduces payload size)
        query: Optional DealCloud query string (e.g., "EntryId in (1,2,3)" or MongoDB-style)
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
        
        # Query-based streaming (useful for delta sync)
        entry_ids = [12345, 12346, 12347]
        ids_str = ",".join(map(str, entry_ids))
        for batch in dc.read_data_streaming("Company", query=f"EntryId in ({ids_str})"):
            process(batch)
        
        # Parallel fetching for faster throughput
        for batch in dc.read_data_streaming("Company", max_concurrency=5):
            process(batch)
    
    Note:
        - Pagination does NOT use totalRecords. We stop only when the API returns
          an empty rows array (client get_paginated/post_paginated implements this).
        - When max_concurrency=1 (default), fetches sequentially to maintain order
        - When max_concurrency>1, fetches pages in parallel but yields in order
        - Each batch is independent - can be processed and discarded
        - For views, use read_view_streaming()
        - When query is provided, uses POST endpoint; otherwise uses GET endpoint
    """
    # Use configured values if not specified
    if page_size is None:
        page_size = self.page_size
    if max_concurrency is None:
        max_concurrency = self.read_concurrency
    
    if query:
        # Query-based read: use POST endpoint with body pagination
        from ..utils.data_utils import rows_query_payload_builder
        endpoint = f"{self._query_url}/{object_id}"
        request_body = rows_query_payload_builder(query, fields)
        
        # Use POST pagination with body (omit max_concurrency - not in httpx request())
        yield from self._client.post_paginated(
            endpoint,
            page_size=page_size,
            data_key="rows",
            json=request_body,
            skip_key="skip",
            limit_key="limit",
        )
    else:
        # Direct read: use GET endpoint
        endpoint = f"{self._rows_url}/{object_id}"
        params = {"wrapIntoArrays": "true"}
        
        if fields:
            # DealCloud uses repeated 'fields' params
            params["fields"] = fields
        
        # Pass max_concurrency so pages are fetched in parallel (yielded in order)
        yield from self._client.get_paginated(
            endpoint,
            page_size=page_size,
            data_key="rows",
            params=params,
            skip_param="skip",
            limit_param="limit",
            max_concurrency=max_concurrency,
        )


def read_view_streaming(
    self: "DealCloudData",
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
        self: DealCloudData instance
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
    
    Note:
        - Pagination does NOT use totalRecords. We stop only when the API returns
          an empty rows array (client post_paginated_params implements this).
        - When max_concurrency>1, fetches pages in parallel but yields in order
    """
    # Use configured values if not specified
    if page_size is None:
        page_size = self.page_size
    if max_concurrency is None:
        max_concurrency = self.read_concurrency

    # Validate and resolve view_id (consolidated validation logic)
    from .read import _validate_and_resolve_view_id
    resolved_view_id, _ = _validate_and_resolve_view_id(self, view_id)
    
    # Build endpoint
    endpoint = f"{self._views_url}/{resolved_view_id}"
    params = {"wrapIntoArrays": "true"}
    
    yield from self._client.post_paginated_params(
        endpoint,
        page_size=page_size,
        data_key="rows",
        json=view_filter,
        params=params,
        skip_param="skip",
        limit_param="limit",
    )


async def aread_data_streaming(
    self: "DealCloudData",
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
        self: DealCloudData instance
        object_id: Object API name or ID
        fields: Optional list of field names to return (reduces payload size)
        query: Optional DealCloud query string (e.g., "EntryId in (1,2,3)" or MongoDB-style)
        page_size: Number of rows per batch (default: from config querySettings.pageSize)
        max_concurrency: Parallel page fetches (default: from config concurrencyLimits.read)
    
    Yields:
        list[dict]: Batch of rows, each as a dictionary
    
    Example:
        # Async process and delete in batches
        async for batch in dc.aread_data_streaming("Company", fields=["EntryId"]):
            entry_ids = [row["EntryId"] for row in batch]
            await process_batch(entry_ids)
        
        # Query-based async streaming (useful for delta sync)
        entry_ids = [12345, 12346, 12347]
        ids_str = ",".join(map(str, entry_ids))
        async for batch in dc.aread_data_streaming("Company", query=f"EntryId in ({ids_str})"):
            await process(batch)
        
        # Parallel fetching for faster throughput
        async for batch in dc.aread_data_streaming("Company", max_concurrency=5):
            await process(batch)
    
    Note:
        - Pagination does NOT use totalRecords. We stop only when the API returns
          an empty rows array (client aget_paginated/apost_paginated implements this).
        - When max_concurrency=1, fetches sequentially to maintain order
        - When max_concurrency>1, fetches pages in parallel but yields in order
        - Each batch is independent - can be processed and discarded
        - For views, use aread_view_streaming()
        - When query is provided, uses POST endpoint; otherwise uses GET endpoint
    """
    # Use configured values if not specified
    if page_size is None:
        page_size = self.page_size
    if max_concurrency is None:
        max_concurrency = self.read_concurrency
    
    if query:
        # Query-based read: use POST endpoint with body pagination
        from ..utils.data_utils import rows_query_payload_builder
        endpoint = f"{self._query_url}/{object_id}"
        request_body = rows_query_payload_builder(query, fields)
        
        # Use async POST pagination with body (omit max_concurrency)
        async for batch in self._client.apost_paginated(
            endpoint,
            page_size=page_size,
            data_key="rows",
            json=request_body,
            skip_key="skip",
            limit_key="limit",
        ):
            yield batch
    else:
        # Direct read: use GET endpoint
        endpoint = f"{self._rows_url}/{object_id}"
        params = {"wrapIntoArrays": "true"}
        
        if fields:
            # DealCloud uses repeated 'fields' params
            params["fields"] = fields
        
        # Use intapp-rest-client's async pagination (parallel pages, yielded in order)
        async for batch in self._client.aget_paginated(
            endpoint,
            page_size=page_size,
            data_key="rows",
            params=params,
            skip_param="skip",
            limit_param="limit",
            max_concurrency=max_concurrency,
        ):
            yield batch


async def aread_view_streaming(
    self: "DealCloudData",
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
        self: DealCloudData instance
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
    # Use configured values if not specified
    if page_size is None:
        page_size = self.page_size
    if max_concurrency is None:
        max_concurrency = self.read_concurrency
    
    # Validate and resolve view_id (consolidated validation logic)
    from .read import _validate_and_resolve_view_id
    resolved_view_id, _ = _validate_and_resolve_view_id(self, view_id)
    
    # Build endpoint
    endpoint = f"{self._views_url}/{resolved_view_id}"
    params = {"wrapIntoArrays": "true"}
    
    # Use intapp-rest-client's async POST pagination (omit max_concurrency)
    async for batch in self._client.apost_paginated_params(
        endpoint,
        page_size=page_size,
        data_key="rows",
        json=view_filter,
        params=params,
        skip_param="skip",
        limit_param="limit",
    ):
        yield batch
