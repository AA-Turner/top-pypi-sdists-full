"""
Environment utilities for the xpander.ai SDK.

This module provides utilities for reading environment variables and
configuring SDK behavior based on environment settings.
"""

from os import getenv
from typing import Optional
from urllib.parse import urlparse


def ensure_scheme(url: str) -> str:
    """Prefix https:// when the URL carries no explicit http(s) scheme."""
    if not url.lower().startswith(("http://", "https://")):
        return f"https://{url}"
    return url


def url_host(url: Optional[str]) -> str:
    """Parsed lowercase hostname of a URL, or "" when absent/unparseable."""
    return (urlparse(url or "").hostname or "").lower()


def get_base_url() -> str:
    """
    Get the base URL for xpander.ai API endpoints.

    This function determines the appropriate base URL for API requests based on
    environment variables. It supports both production and staging environments,
    with the ability to override via environment variables.

    Environment Variables:
        XPANDER_BASE_URL: Override URL for API endpoints (optional).
        IS_STG: Set to "true" for staging environment (optional, defaults to "false").

    Returns:
        str: The base URL for xpander.ai API endpoints, always prefixed with "https://".

    Example:
        >>> url = get_base_url()
        >>> print(url)  # "https://inbound.xpander.ai"

        >>> import os
        >>> os.environ["XPANDER_BASE_URL"] = "custom.api.endpoint"
        >>> url = get_base_url()
        >>> print(url)  # "https://custom.api.endpoint"
    """
    # Support override by environment variable
    base_url = getenv("XPANDER_BASE_URL")

    if not base_url:
        is_stg = getenv("IS_STG", "false") == "true"
        base_url = "inbound.stg.xpander.ai" if is_stg else "inbound.xpander.ai"

    return ensure_scheme(base_url)
