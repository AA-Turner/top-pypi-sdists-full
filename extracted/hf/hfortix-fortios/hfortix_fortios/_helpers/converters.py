"""
Data conversion and cleaning helpers for FortiOS API.

Provides utilities for:
- Type conversion (bool to enable/disable)
- Data filtering and cleaning
- URL encoding for path parameters
"""

from typing import Any
from urllib.parse import quote


def convert_boolean_to_str(value: bool | str | int | None) -> str | None:
    """
    Convert Python boolean to FortiOS enable/disable string.

    FortiOS API typically uses 'enable'/'disable' instead of true/false.

    Args:
        value: Boolean, string, or None

    Returns:
        'enable', 'disable', the original string, or None
    """
    if value is None:
        return None
    if isinstance(value, bool):
        return "enable" if value else "disable"
    return str(value)


def filter_empty_values(payload: dict[str, Any]) -> dict[str, Any]:
    """
    Remove None values and empty collections from payload.

    Useful for cleaning up payloads before sending to FortiOS API,
    which may reject empty lists or None values in certain contexts.

    Args:
        payload: Dictionary to clean

    Returns:
        Dictionary with None and empty values removed
    """
    cleaned: dict[str, Any] = {}

    for key, value in payload.items():
        # Skip None values
        if value is None:
            continue

        # Skip empty lists and dicts
        if isinstance(value, (list, dict)) and not value:
            continue

        cleaned[key] = value

    return cleaned


def quote_path_param(value: str | int) -> str:
    """
    URL-encode a path parameter for safe inclusion in API endpoint URLs.

    FortiOS object names (mkey values) can contain characters like '/' that
    conflict with URL path separators. This function encodes such characters
    to their percent-encoded equivalents.

    Args:
        value: The path parameter value (typically an mkey like name, policyid, etc.)

    Returns:
        URL-encoded string safe for use in URL paths

    Examples:
        >>> quote_path_param("CGNAT_100.64.0.0/10")
        'CGNAT_100.64.0.0%2F10'
        >>> quote_path_param("simple-name")
        'simple-name'
        >>> quote_path_param(123)
        '123'
    """
    # Convert to string and encode, making NO characters safe
    # (even '/' must be encoded since it's a path separator)
    return quote(str(value), safe="")
