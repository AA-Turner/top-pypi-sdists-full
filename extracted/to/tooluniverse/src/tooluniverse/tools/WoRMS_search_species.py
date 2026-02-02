"""
WoRMS_search_species

Search marine species in World Register of Marine Species
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def WoRMS_search_species(
    query: str,
    limit: Optional[int] = 20,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Search marine species in World Register of Marine Species

    Parameters
    ----------
    query : str
        Species name or search term
    limit : int
        Number of results
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
        {"name": "WoRMS_search_species", "arguments": {"query": query, "limit": limit}},
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["WoRMS_search_species"]
