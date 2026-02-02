"""
openalex_search_institutions

Search OpenAlex institutions via the /institutions endpoint. Use this to discover Institution IDs...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def openalex_search_institutions(
    search: str,
    per_page: Optional[int] = 5,
    page: Optional[int] = 1,
    mailto: Optional[str] = None,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Search OpenAlex institutions via the /institutions endpoint. Use this to discover Institution IDs...

    Parameters
    ----------
    search : str
        Institution name search query. Example: "Harvard University".
    per_page : int
        Results per page (OpenAlex max 200).
    page : int
        Page number (1-indexed).
    mailto : str
        Optional contact email for OpenAlex polite pool.
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
            "name": "openalex_search_institutions",
            "arguments": {
                "search": search,
                "per_page": per_page,
                "page": page,
                "mailto": mailto,
            },
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["openalex_search_institutions"]
