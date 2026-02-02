"""
get_webpage_text_from_url

Render a URL as PDF and extract its text (JavaScript supported).
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def get_webpage_text_from_url(
    url: str,
    timeout: int,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Render a URL as PDF and extract its text (JavaScript supported).

    Parameters
    ----------
    url : str
        Webpage URL to fetch and render
    timeout : int
        Request timeout in seconds
    stream_callback : Callable, optional
        Callback for streaming output
    use_cache : bool, default False
        Enable caching
    validate : bool, default True
        Validate parameters

    Returns
    -------
    dict[str, Any]
    """
    # Handle mutable defaults to avoid B006 linting error

    return get_shared_client().run_one_function(
        {
            "name": "get_webpage_text_from_url",
            "arguments": {"url": url, "timeout": timeout},
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["get_webpage_text_from_url"]
