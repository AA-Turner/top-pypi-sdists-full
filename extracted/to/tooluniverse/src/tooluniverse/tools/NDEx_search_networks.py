"""
NDEx_search_networks

Search the NDEx biological network repository for published networks by keyword. NDEx hosts thous...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def NDEx_search_networks(
    query: str,
    size: Optional[int] = None,
    start: Optional[int] = None,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> Any:
    """
    Search the NDEx biological network repository for published networks by keyword. NDEx hosts thous...

    Parameters
    ----------
    query : str
        Search query for finding biological networks. Can include gene names, pathway...
    size : int
        Maximum number of results to return (default: 10, max: 100).
    start : int
        Offset for pagination (default: 0).
    stream_callback : Callable, optional
        Callback for streaming output
    use_cache : bool, default False
        Enable caching
    validate : bool, default True
        Validate parameters

    Returns
    -------
    Any
    """
    # Handle mutable defaults to avoid B006 linting error

    return get_shared_client().run_one_function(
        {
            "name": "NDEx_search_networks",
            "arguments": {"query": query, "size": size, "start": start},
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["NDEx_search_networks"]
