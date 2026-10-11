"""
Error processing for API responses.

Per https://api.docs.dealcloud.com/docs - Status Codes and Handling:

| Status Code | Description | Handling |
|-------------|-------------|----------|
| 200 | Success | Process response |
| 400 | Bad Request | Check request body/params |
| 401 | Unauthorized | Re-authenticate |
| 403 | Forbidden | Check permissions |
| 404 | Not Found | Resource doesn't exist |
| 429 | Too Many Requests | Retry with backoff, respect Retry-After |
| 500 | Internal Server Error | Retry with backoff |
| 502/503/504 | Gateway errors | Retry with backoff |
"""

import logging
from functools import wraps
from typing import Any, Callable, Optional, ParamSpec, TypeVar

from intapp_rest_client.exceptions import HttpError

logger = logging.getLogger(__name__)

P = ParamSpec("P")
T = TypeVar("T")


class DealCloudApiError(Exception):
    """Base exception for DealCloud API errors."""

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        errors: Optional[list] = None,
        row_errors: Optional[list[dict[str, Any]]] = None,
    ):
        self.message = message
        self.status_code = status_code
        self.errors = errors or []
        self.row_errors = row_errors or []
        super().__init__(message)


class DealCloudValidationError(DealCloudApiError):
    """Validation errors in request data."""

    pass


class DealCloudRateLimitError(DealCloudApiError):
    """Rate limit exceeded - should retry with backoff."""

    def __init__(self, message: str, retry_after: Optional[int] = None):
        super().__init__(message, status_code=429)
        self.retry_after = retry_after


class DealCloudAuthError(DealCloudApiError):
    """Authentication or authorization error."""

    pass


def split_row_results(response: list[Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Split a Rows API response list into successful rows and rows with ``Errors``."""
    ok_rows: list[dict[str, Any]] = []
    error_rows: list[dict[str, Any]] = []
    for item in response:
        if not isinstance(item, dict):
            continue
        if "Errors" in item:
            error_rows.append(item)
        else:
            ok_rows.append(item)
    return ok_rows, error_rows


def _cell_entry_id(item: dict[str, Any]) -> int | None:
    for key in ("entryId", "EntryId"):
        value = item.get(key)
        if value is not None:
            return int(value)
    return None


def _cell_row_id(item: dict[str, Any]) -> int | None:
    for key in ("rowId", "RowId"):
        value = item.get(key)
        if value is not None:
            return int(value)
    return None


def _cell_create_uncommitted(entry_id: int, items: list[dict[str, Any]]) -> bool:
    """Create batches are all-or-none; uncommitted rows keep negative ``rowId``."""
    if entry_id >= 0:
        return False
    for item in items:
        row_id = _cell_row_id(item)
        if row_id is None or row_id <= 0:
            return True
    return False


def _errors_from_cell_item(item: dict[str, Any]) -> list[dict[str, Any]]:
    """Normalize Cells store result errors (``error`` dict or Rows-style ``Errors``)."""
    from .error_enrichment import iter_row_error_items

    return iter_row_error_items(item)


def split_cell_store_results(
    cell_results: list[Any],
    *,
    is_create: bool = False,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Split Cells storeResponses; aggregate per-entry ``error`` into row_errors."""
    by_entry: dict[int, list[dict[str, Any]]] = {}
    for item in cell_results:
        if not isinstance(item, dict):
            continue
        entry_id = _cell_entry_id(item)
        if entry_id is None:
            continue
        by_entry.setdefault(entry_id, []).append(item)

    ok_cells: list[dict[str, Any]] = []
    row_errors: list[dict[str, Any]] = []
    for entry_id, items in by_entry.items():
        errors: list[dict[str, Any]] = []
        for item in items:
            errors.extend(_errors_from_cell_item(item))
        if is_create and _cell_create_uncommitted(entry_id, items):
            errors.append(
                {
                    "field": "",
                    "code": 0,
                    "description": "entry not committed (batch all-or-none)",
                }
            )
        if errors:
            row_errors.append({"EntryId": entry_id, "Errors": errors})
        else:
            ok_cells.extend(items)
    return ok_cells, row_errors


def map_row_errors_to_indices(
    batch: list[dict[str, Any]],
    row_errors: list[dict[str, Any]],
    *,
    is_insert: bool,
) -> set[int]:
    """Map Rows API row error payloads back to indices in the submitted *batch*.

    Insert batches use negative request ``EntryId`` values (``-1`` → index 0).
    Update/delete batches match on positive ``EntryId``.
    """
    indices: set[int] = set()
    for err_row in row_errors:
        entry_id = err_row.get("EntryId")
        if entry_id is None:
            continue
        entry_id = int(entry_id)
        if is_insert and entry_id < 0:
            idx = -entry_id - 1
            if 0 <= idx < len(batch):
                indices.add(idx)
        elif not is_insert:
            for idx, row in enumerate(batch):
                row_eid = row.get("EntryId")
                if row_eid is not None and int(row_eid) == entry_id:
                    indices.add(idx)
                    break
    return indices


def format_row_error_message(error_row: dict[str, Any]) -> str:
    """Human-readable summary of a DealCloud row ``Errors`` payload."""
    parts: list[str] = []
    for err in error_row.get("Errors") or []:
        field_name = err.get("field", "?")
        desc = err.get("description", "")
        code = err.get("code", "")
        if code:
            parts.append(f"{field_name}: {desc} (code {code})")
        else:
            parts.append(f"{field_name}: {desc}")
    entry_id = error_row.get("EntryId")
    prefix = f"EntryId {entry_id}" if entry_id is not None else "row"
    if parts:
        return f"{prefix}: {'; '.join(parts)}"
    return f"{prefix}: {error_row}"


def finalize_list_response(
    response: list[dict],
    *,
    raise_on_row_errors: bool = False,
    log_row_errors: bool = True,
) -> tuple[list[dict], list[dict]]:
    """
    Process a Rows-shaped list response and return ``(all_rows, row_error_rows)``.

    By default logs row errors without raising. When ``raise_on_row_errors`` is True,
    raises ``DealCloudValidationError`` with ``row_errors`` attached.
    """
    if log_row_errors or raise_on_row_errors:
        process_errors(response, raise_on_row_errors=raise_on_row_errors)
    else:
        _, error_rows = split_row_results(response)
        if error_rows:
            for e in error_rows:
                logger.error("DealCloud API Error: %s", e)
    _, row_error_rows = split_row_results(response)
    return response, row_error_rows


def resolve_raise_on_row_errors(
    client_default: bool,
    override: Optional[bool],
) -> bool:
    """Resolve per-call ``raise_on_row_errors`` against client config default."""
    return client_default if override is None else override


def process_errors(
    response: list[dict],
    *,
    raise_on_row_errors: bool = False,
) -> list[dict[str, Any]]:
    """
    Process error responses from the API.

    DealCloud returns errors in the response body with this structure:
    {
        "EntryId": -1,
        "Errors": [
            {"field": "FieldName", "code": 5006, "description": "Error message"}
        ]
    }

    Args:
        response: List of row dicts from a Rows/Cells API write (HTTP 200).
        raise_on_row_errors: When True, raise ``DealCloudValidationError`` if any row
            has ``Errors``.

    Returns:
        List of row dicts that contain ``Errors`` (same objects as in *response*).
    """
    error_rows = [x for x in response if isinstance(x, dict) and "Errors" in x]

    for e in error_rows:
        logger.error("DealCloud API Error: %s", e)

    if raise_on_row_errors and error_rows:
        field_errors: list[Any] = []
        for e in error_rows:
            field_errors.extend(e.get("Errors", []))

        raise DealCloudValidationError(
            f"API returned {len(error_rows)} row error(s) ({len(field_errors)} field error(s))",
            errors=field_errors,
            row_errors=error_rows,
        )

    return error_rows


def handle_http_error(status_code: int, response_body: dict, headers: dict) -> None:
    """
    Handle HTTP error responses based on status code.

    Per DealCloud API docs status code handling.

    Args:
        status_code: HTTP status code
        response_body: Parsed response body (dict or raw text)
        headers: Response headers dict

    Raises:
        DealCloudValidationError: For 400 Bad Request
        DealCloudAuthError: For 401/403 auth errors
        DealCloudRateLimitError: For 429 rate limits
        DealCloudApiError: For other errors
    """
    errors = []
    error_message = ""

    if isinstance(response_body, dict):
        errors = response_body.get("errors", [])
        error_message = response_body.get("message", "")

        if errors:
            error_details = []
            for err in errors:
                if isinstance(err, dict):
                    msg = err.get("message", "")
                    code = err.get("errorCode", "")
                    if msg:
                        error_details.append(f"{msg} (code: {code})" if code else msg)
            if error_details:
                error_message = "; ".join(error_details)
    elif response_body:
        error_message = str(response_body)

    if status_code == 400:
        raise DealCloudValidationError(
            f"Bad Request: {error_message or response_body}",
            status_code=status_code,
            errors=errors,
        )
    elif status_code == 401:
        raise DealCloudAuthError(
            f"Unauthorized: {error_message or 'Token may be expired'}",
            status_code=status_code,
        )
    elif status_code == 403:
        raise DealCloudAuthError(
            f"Forbidden: {error_message or 'Insufficient permissions'}",
            status_code=status_code,
        )
    elif status_code == 404:
        raise DealCloudApiError(
            f"Not Found: {error_message or 'Resource does not exist'}",
            status_code=status_code,
        )
    elif status_code == 429:
        retry_after = headers.get("Retry-After") or headers.get("retry-after")
        raise DealCloudRateLimitError(
            f"Rate limit exceeded: {error_message or 'Too many requests'}",
            retry_after=int(retry_after) if retry_after else None,
        )
    else:
        raise DealCloudApiError(
            f"HTTP {status_code}: {error_message or response_body}",
            status_code=status_code,
        )


def transform_http_error(http_error: HttpError) -> None:
    """
    Transform an intapp_rest_client HttpError into a DealCloud-specific exception.

    This extracts the full response body and headers from the HttpError
    and raises the appropriate DealCloud exception with detailed error information.

    Args:
        http_error: The HttpError from intapp_rest_client

    Raises:
        DealCloudValidationError, DealCloudAuthError, DealCloudRateLimitError,
        or DealCloudApiError depending on status code

    Example:
        try:
            response = client.get("/api/resource")
        except HttpError as e:
            transform_http_error(e)  # Raises DealCloud-specific exception
    """
    status_code = http_error.status_code
    response_body = http_error.full_response_body or http_error.response_body or {}
    headers = http_error.headers or {}

    logger.error(
        "HTTP %s error - Response body: %s, Request-ID: %s",
        status_code,
        response_body,
        http_error.request_id,
    )

    handle_http_error(status_code, response_body, headers)


def with_error_handling(func: Callable[P, T]) -> Callable[P, T]:
    """
    Decorator that catches HttpError and transforms it to DealCloud exceptions.

    Use this decorator on methods that call the REST client to automatically
    transform low-level HTTP errors into meaningful DealCloud exceptions.

    Example:
        @with_error_handling
        def get_objects(self):
            return self._client.get(url)
    """

    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        try:
            return func(*args, **kwargs)
        except HttpError as e:
            transform_http_error(e)
        raise AssertionError("unreachable")

    return wrapper
