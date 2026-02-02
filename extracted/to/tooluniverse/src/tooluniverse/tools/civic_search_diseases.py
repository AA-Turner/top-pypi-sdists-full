"""
civic_search_diseases

Search for diseases in CIViC database. Returns a list of cancer diseases and conditions (with IDs...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def civic_search_diseases(
    limit: Optional[int] = 20,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Search for diseases in CIViC database. Returns a list of cancer diseases and conditions (with IDs...

    Parameters
    ----------
    limit : int
        Maximum number of diseases to return (default: 20, recommended max: 100)
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
        {"name": "civic_search_diseases", "arguments": {"limit": limit}},
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["civic_search_diseases"]
