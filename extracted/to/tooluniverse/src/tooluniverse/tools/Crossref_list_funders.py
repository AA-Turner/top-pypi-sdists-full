"""
Crossref_list_funders

Search and list research funding organizations in the Crossref database. Returns funder details i...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def Crossref_list_funders(
    query: Optional[str] = None,
    limit: Optional[int] = 20,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Search and list research funding organizations in the Crossref database. Returns funder details i...

    Parameters
    ----------
    query : str
        Search query for funder names (e.g., 'National Science Foundation', 'NIH', 'E...
    limit : int
        Maximum number of funders to return (default: 20, max: 100).
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
            "name": "Crossref_list_funders",
            "arguments": {"query": query, "limit": limit},
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["Crossref_list_funders"]
