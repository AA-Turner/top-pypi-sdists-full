"""
metabolights_search_studies

Search MetaboLights studies by query string. Returns a list of matching study IDs. Use metaboligh...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def metabolights_search_studies(
    query: str,
    size: Optional[int] = 20,
    page: Optional[int] = 0,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Search MetaboLights studies by query string. Returns a list of matching study IDs. Use metaboligh...

    Parameters
    ----------
    query : str
        Search query string (e.g., organism name, disease, metabolite name)
    size : int
        Number of results per page (default: 20)
    page : int
        Page number (default: 0)
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
            "name": "metabolights_search_studies",
            "arguments": {"query": query, "size": size, "page": page},
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["metabolights_search_studies"]
