"""
Fatcat_search_scholar

Search Internet Archive Scholar via Fatcat releases search. Fatcat is the underlying database pow...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def Fatcat_search_scholar(
    query: str,
    max_results: int,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> list[Any]:
    """
    Search Internet Archive Scholar via Fatcat releases search. Fatcat is the underlying database pow...

    Parameters
    ----------
    query : str
        Search query for Fatcat releases. Use keywords to search across titles, abstr...
    max_results : int
        Maximum number of results to return. Default is 10, maximum is 100.
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
            "name": "Fatcat_search_scholar",
            "arguments": {"query": query, "max_results": max_results},
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["Fatcat_search_scholar"]
