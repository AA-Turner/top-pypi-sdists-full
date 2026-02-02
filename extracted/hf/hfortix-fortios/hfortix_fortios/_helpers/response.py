"""
Response parsing helpers for FortiOS API.

Utilities for extracting data from API responses.
"""

from typing import Any, Dict, List, Union


def get_name(response: Union[Dict[str, Any], Any]) -> Union[str, None]:
    """
    Extract the name/identifier from an API response.

    FortiOS API responses include 'mkey' field after successful create/update
    operations. This helper extracts it as 'name' for user convenience.

    Args:
        response: API response dictionary

    Returns:
        The object name if present, None otherwise
    """
    if isinstance(response, dict):
        return response.get("mkey")
    return None


def get_mkey(response: Union[Dict[str, Any], Any]) -> Union[str, None]:
    """
    Extract the mkey (management key) from an API response.

    This is an alias for get_name() to maintain backward compatibility.
    Prefer using get_name() for better readability.

    Args:
        response: API response dictionary

    Returns:
        The mkey value if present, None otherwise
    """
    return get_name(response)


def get_results(
    response: Union[Dict[str, Any], Any],
) -> Union[List[Any], Dict[str, Any], None]:
    """
    Extract the results from an API response.

    FortiOS API responses wrap data in a 'results' field. This helper
    extracts it cleanly.

    Args:
        response: API response dictionary

    Returns:
        The results (list or dict) if present, None otherwise
    """
    if isinstance(response, dict):
        return response.get("results")
    return None


def is_success(response: Union[Dict[str, Any], Any]) -> bool:
    """
    Check if an API response indicates success.

    Args:
        response: API response dictionary

    Returns:
        True if response status is 'success', False otherwise
    """
    if isinstance(response, dict):
        return response.get("status") == "success"
    return False
