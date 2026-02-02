"""
Wikipedia_get_summary

Get a brief summary/introduction from a Wikipedia article. This is a convenience tool that extrac...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def Wikipedia_get_summary(
    title: str,
    language: Optional[str] = "en",
    max_chars: Optional[int] = 500,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Get a brief summary/introduction from a Wikipedia article. This is a convenience tool that extrac...

    Parameters
    ----------
    title : str
        Wikipedia article title (exact title as it appears on Wikipedia)
    language : str
        Wikipedia language code (e.g., 'en' for English). Default: 'en'
    max_chars : int
        Maximum characters to return. Default: 500
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
            "name": "Wikipedia_get_summary",
            "arguments": {"title": title, "language": language, "max_chars": max_chars},
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["Wikipedia_get_summary"]
