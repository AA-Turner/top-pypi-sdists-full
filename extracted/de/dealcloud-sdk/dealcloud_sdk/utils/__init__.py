"""Utility functions for dealcloud_sdk SDK."""

from .data_utils import (
    flatten_nested_list,
    format_data,
    divide_pages,
    calculate_pagination,
    query_by_entry_id,
    rows_query_payload_builder,
    generate_page_offsets,
)
from .process_response_errors import (
    DealCloudApiError,
    DealCloudValidationError,
    DealCloudRateLimitError,
    DealCloudAuthError,
    process_errors,
    resolve_raise_on_row_errors,
    split_row_results,
    map_row_errors_to_indices,
    format_row_error_message,
    handle_http_error,
    transform_http_error,
    with_error_handling,
)
from .rate_limiter import RateLimiter, AsyncRateLimiter
from .resolve_references import resolve_object

__all__ = [
    "flatten_nested_list",
    "format_data",
    "divide_pages",
    "calculate_pagination",
    "query_by_entry_id",
    "rows_query_payload_builder",
    "generate_page_offsets",
    "DealCloudApiError",
    "DealCloudValidationError",
    "DealCloudRateLimitError",
    "DealCloudAuthError",
    "process_errors",
    "resolve_raise_on_row_errors",
    "split_row_results",
    "map_row_errors_to_indices",
    "format_row_error_message",
    "handle_http_error",
    "transform_http_error",
    "with_error_handling",
    "resolve_object",
    "RateLimiter",
    "AsyncRateLimiter",
]


