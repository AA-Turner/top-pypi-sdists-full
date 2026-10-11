"""Pagination and parallel request infrastructure."""

import logging
from typing import Callable, List, Optional, Tuple, Union

from intapp_rest_client.models import ErrorHandling

from ..constants.data import DATA_READ_WORKER_COUNT, MAX_SPECULATIVE_PAGES
from .models import BatchResult


def parallel_requests_get(
    client,
    urls: list[str], 
    max_workers: int,
    error_handling: ErrorHandling = ErrorHandling.FAIL_FAST,
    logger: Optional[logging.Logger] = None,
) -> Union[list, Tuple[list, list]]:
    """
    Execute parallel GET requests using client's parallel_get method.
    
    This is a wrapper around client.parallel_get() for backward compatibility.
    New code should use client.parallel_get() directly.
    
    Args:
        client: HTTP client with parallel_get() method
        urls: List of URLs to request
        max_workers: Number of parallel workers
        error_handling: How to handle errors
        logger: Optional logger instance (not used, kept for compatibility)
    
    Returns:
        If FAIL_FAST: List of results (raises on first error)
        If COLLECT/LOG_ONLY: Tuple of (results, errors)
    """
    return client.parallel_get(
        endpoints=urls,
        max_workers=max_workers,
        error_handling=error_handling
    )


def parallel_requests_post(
    client,
    url: str, 
    payloads: list, 
    max_workers: int,
    error_handling: ErrorHandling = ErrorHandling.FAIL_FAST,
    logger: Optional[logging.Logger] = None,
) -> Union[list, Tuple[list, list]]:
    """
    Execute parallel POST requests using client's parallel_post method.
    
    This is a wrapper around client.parallel_post() for backward compatibility.
    New code should use client.parallel_post() directly.
    
    Args:
        client: HTTP client with parallel_post() method
        url: URL to request
        payloads: List of request bodies
        max_workers: Number of parallel workers
        error_handling: How to handle errors
        logger: Optional logger instance (not used, kept for compatibility)
    
    Returns:
        If FAIL_FAST: List of results (raises on first error)
        If COLLECT/LOG_ONLY: Tuple of (results, errors)
    """
    return client.parallel_post(
        endpoint=url,
        payloads=payloads,
        max_workers=max_workers,
        error_handling=error_handling
    )


def paginated_read_until_empty(
    client,
    base_url: str,
    method: str = "GET",
    request_body: Optional[dict] = None,
    page_size: int = 1000,
    max_workers: int = DATA_READ_WORKER_COUNT,
    progress_callback: Optional[Callable[[int, int], None]] = None,
    error_handling: ErrorHandling = ErrorHandling.FAIL_FAST,
    logger: Optional[logging.Logger] = None,
) -> Union[list[dict], BatchResult]:
    """
    Paginated read that continues until empty rows array is returned.
    Does NOT use totalRecords; we stop only when response["rows"] is empty.

    Per DealCloud API docs: "If you request beyond the available pages,
    the API will return a 200 OK response with an empty rows array."

    Strategy:
    1. Speculatively fetch multiple pages in parallel
    2. Check which pages have data
    3. If all pages had data, fetch more pages
    4. Continue until we get empty rows
    5. Merge all results
    
    Args:
        client: HTTP client with get() and post() methods
        base_url: Base URL for requests
        method: HTTP method (GET or POST)
        request_body: Optional request body for POST
        page_size: Number of rows per page
        max_workers: Number of parallel workers
        progress_callback: Optional callback (current_rows, estimated_total)
        error_handling: How to handle errors
        logger: Optional logger instance
    
    Returns:
        If FAIL_FAST: List of all rows
        If COLLECT: BatchResult with rows and errors
    """
    if logger is None:
        logger = logging.getLogger(__name__)
    
    all_rows = []
    all_errors = []
    skip = 0
    estimated_total = 0
    
    while True:
        # Generate batch of URLs/payloads for parallel fetch
        batch_size = min(max_workers, MAX_SPECULATIVE_PAGES)
        
        if method == "GET":
            # Build URLs with skip parameter
            urls = []
            for i in range(batch_size):
                offset = skip + (i * page_size)
                if "&skip=" in base_url or "?skip=" in base_url:
                    # Replace existing skip
                    url = base_url
                elif "?" in base_url:
                    url = f"{base_url}&skip={offset}"
                else:
                    url = f"{base_url}?skip={offset}"
                urls.append(url)
            
            result = parallel_requests_get(client, urls, max_workers, error_handling, logger)
            if error_handling == ErrorHandling.FAIL_FAST:
                responses = result
            else:
                responses, errors = result
                all_errors.extend(errors)
        else:
            payloads = []
            for i in range(batch_size):
                payload = {**(request_body or {}), "limit": page_size, "skip": skip + (i * page_size)}
                payloads.append(payload)
            
            result = parallel_requests_post(client, base_url, payloads, max_workers, error_handling, logger)
            if error_handling == ErrorHandling.FAIL_FAST:
                responses = result
            else:
                responses, errors = result
                all_errors.extend(errors)
        
        # Process responses and check for empty pages
        pages_with_data = 0
        for response in responses:
            rows = response.get("rows", [])
            if rows:
                all_rows.extend(rows)
                pages_with_data += 1
        
        # Call progress callback if provided
        if progress_callback:
            # Estimate total based on whether we're getting full pages
            if pages_with_data == batch_size:
                estimated_total = len(all_rows) + (batch_size * page_size)
            else:
                estimated_total = len(all_rows)
            try:
                progress_callback(len(all_rows), estimated_total)
            except Exception as e:
                logger.warning(f"Progress callback failed: {e}")
        
        # If any page was empty, we've reached the end
        if pages_with_data < batch_size:
            break
        
        # Move to next batch
        skip += batch_size * page_size
        logger.debug(f"Fetched {len(all_rows)} rows so far, continuing...")
    
    if error_handling != ErrorHandling.FAIL_FAST:
        return BatchResult(
            results=all_rows,
            errors=all_errors,
            total_requested=skip + batch_size,
            total_succeeded=len(all_rows),
            total_failed=len(all_errors)
        )
    
    return all_rows


def parallel_get(
    client,
    urls: list[str],
    max_workers: int = 8,
    error_handling: ErrorHandling = ErrorHandling.FAIL_FAST,
    logger: Optional[logging.Logger] = None,
) -> Union[list, Tuple[list, list]]:
    """
    Execute parallel GET requests with consistent error handling.
    
    This is a wrapper around client.parallel_get() for backward compatibility.
    New code should use client.parallel_get() directly.
    
    Args:
        client: HTTP client with parallel_get() method
        urls: List of URLs to request (can be full URLs or endpoints)
        max_workers: Number of parallel workers (default: 8)
        error_handling: How to handle errors:
            - FAIL_FAST: Raise on first error
            - COLLECT: Collect errors, return partial results
            - LOG_ONLY: Log errors, continue processing
        logger: Optional logger instance (not used, kept for compatibility)
    
    Returns:
        If FAIL_FAST: List of JSON responses
        If COLLECT/LOG_ONLY: Tuple of (results, errors)
    
    Example:
        >>> # Fetch multiple objects in parallel
        >>> urls = [
        ...     f"{dc.api_url}/schema/entryTypes/{obj}"
        ...     for obj in ["Company", "Contact", "Deal"]
        ... ]
        >>> results = pagination.parallel_get(dc._client, urls)
        
        >>> # With error collection
        >>> results, errors = pagination.parallel_get(
        ...     dc._client, urls, 
        ...     error_handling=ErrorHandling.COLLECT
        ... )
        >>> if errors:
        ...     print(f"Failed: {len(errors)} requests")
    """
    return client.parallel_get(
        endpoints=urls,
        max_workers=max_workers,
        error_handling=error_handling
    )


def parallel_post(
    client,
    url: str,
    payloads: list[dict],
    max_workers: int = 8,
    error_handling: ErrorHandling = ErrorHandling.FAIL_FAST,
    logger: Optional[logging.Logger] = None,
) -> Union[list, Tuple[list, list]]:
    """
    Execute parallel POST requests with consistent error handling.
    
    This is a wrapper around client.parallel_post() for backward compatibility.
    New code should use client.parallel_post() directly.
    
    Args:
        client: HTTP client with parallel_post() method
        url: URL to send all requests to
        payloads: List of JSON payloads (one per request)
        max_workers: Number of parallel workers (default: 8)
        error_handling: How to handle errors
        logger: Optional logger instance (not used, kept for compatibility)
    
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
        >>> results = pagination.parallel_post(dc._client, query_url, payloads)
        
        >>> # With error handling
        >>> results, errors = pagination.parallel_post(
        ...     dc._client, url, payloads,
        ...     error_handling=ErrorHandling.COLLECT
        ... )
    """
    return client.parallel_post(
        endpoint=url,
        payloads=payloads,
        max_workers=max_workers,
        error_handling=error_handling
    )


def paginated_read(
    client,
    url: str,
    method: str = "GET",
    request_body: Optional[dict] = None,
    page_size: int = 1000,
    max_workers: int = 8,
    progress_callback: Optional[Callable[[int, int], None]] = None,
    error_handling: ErrorHandling = ErrorHandling.FAIL_FAST,
    logger: Optional[logging.Logger] = None,
) -> Union[list[dict], BatchResult]:
    """
    Generic paginated read for any endpoint.
    
    Use this for custom or undocumented endpoints that need pagination
    support. Uses the same parallel speculative fetching strategy as
    read_data() for optimal performance.
    
    Args:
        client: HTTP client with get() and post() methods
        url: Base URL (skip/limit will be added)
        method: HTTP method - "GET" or "POST"
        request_body: Optional body for POST requests
        page_size: Number of rows per page (default: 1000)
        max_workers: Number of parallel workers (default: 8)
        progress_callback: Optional callback(current_rows, estimated_total)
        error_handling: How to handle errors
        logger: Optional logger instance
    
    Returns:
        If FAIL_FAST: List of all rows from all pages
        If COLLECT: BatchResult with rows and errors
    
    Example:
        >>> # Custom endpoint with GET pagination
        >>> all_data = pagination.paginated_read(
        ...     dc._client,
        ...     f"{dc.api_url}/custom/endpoint?filter=active",
        ...     page_size=500
        ... )
        
        >>> # POST endpoint with body
        >>> all_data = pagination.paginated_read(
        ...     dc._client,
        ...     f"{dc.api_url}/data/query",
        ...     method="POST",
        ...     request_body={"filter": {"status": "Active"}},
        ...     page_size=1000
        ... )
        
        >>> # With progress tracking
        >>> def on_progress(current, total):
        ...     print(f"Loaded {current}/{total} rows")
        >>> data = pagination.paginated_read(dc._client, url, progress_callback=on_progress)
    
    Note:
        - Responses must have a "rows" key containing the data array
        - Pagination stops when an empty "rows" array is returned
        - Uses speculative parallel fetching for better performance
    """
    return paginated_read_until_empty(
        client=client,
        base_url=url,
        method=method,
        request_body=request_body,
        page_size=page_size,
        max_workers=max_workers,
        progress_callback=progress_callback,
        error_handling=error_handling,
        logger=logger,
    )
