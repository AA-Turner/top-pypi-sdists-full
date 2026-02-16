"""
MonarchV3_search

Search the Monarch Initiative knowledge graph for biomedical entities by name or keyword. Returns...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def MonarchV3_search(
    query: str,
    limit: Optional[int] = None,
    category: Optional[str] = None,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> Any:
    """
    Search the Monarch Initiative knowledge graph for biomedical entities by name or keyword. Returns...

    Parameters
    ----------
    query : str
        Search query. Can be gene names, disease names, phenotype terms, etc. Example...
    limit : int
        Maximum results to return (default: 10, max: 50).
    category : str
        Filter by entity category. Options: 'biolink:Gene', 'biolink:Disease', 'bioli...
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
            "name": "MonarchV3_search",
            "arguments": {"query": query, "limit": limit, "category": category},
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["MonarchV3_search"]
