"""
openalex_search_authors

Search OpenAlex authors via the /authors endpoint. Use this to discover Author IDs (A...) and the...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def openalex_search_authors(
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
    Search OpenAlex authors via the /authors endpoint. Use this to discover Author IDs (A...) and the...

    Parameters
    ----------
    search : str
        Author name search query. Example: "Yann LeCun".
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
            "name": "openalex_search_authors",
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


__all__ = ["openalex_search_authors"]
