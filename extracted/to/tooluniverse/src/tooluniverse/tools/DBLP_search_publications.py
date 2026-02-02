"""
DBLP_search_publications

Search DBLP Computer Science Bibliography for publications. Returns publications with title, auth...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def DBLP_search_publications(
    query: str,
    limit: int,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> list[Any]:
    """
    Search DBLP Computer Science Bibliography for publications. Returns publications with title, auth...

    Parameters
    ----------
    query : str
        Search query for DBLP publications. Use keywords separated by spaces to refin...
    limit : int
        Number of publications to return. This sets the maximum number of publication...
    stream_callback : Callable, optional
        Callback for streaming output
    use_cache : bool, default False
        Enable caching
    validate : bool, default True
        Validate parameters

    Returns
    -------
    list[Any]
    """
    # Handle mutable defaults to avoid B006 linting error

    return get_shared_client().run_one_function(
        {
            "name": "DBLP_search_publications",
            "arguments": {"query": query, "limit": limit},
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["DBLP_search_publications"]
