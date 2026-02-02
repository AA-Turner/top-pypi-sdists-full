"""
Zenodo_search_records

Search Zenodo for research data, publications, and datasets. Zenodo is an open-access repository ...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def Zenodo_search_records(
    query: str,
    limit: Optional[int] = 10,
    community: Optional[str] = None,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Search Zenodo for research data, publications, and datasets. Zenodo is an open-access repository ...

    Parameters
    ----------
    query : str
        Free text search query for Zenodo records. Use keywords to search across titl...
    limit : int
        Maximum number of results to return. Must be between 1 and 200.
    community : str
        Optional community slug to filter results by specific research community (e.g...
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
            "name": "Zenodo_search_records",
            "arguments": {"query": query, "limit": limit, "community": community},
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["Zenodo_search_records"]
