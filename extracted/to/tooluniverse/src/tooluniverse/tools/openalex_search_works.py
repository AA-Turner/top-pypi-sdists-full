"""
openalex_search_works

Search OpenAlex works (papers) via the /works endpoint. Use this to discover OpenAlex Work IDs (W...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def openalex_search_works(
    search: str,
    filter: Optional[str] = None,
    per_page: Optional[int] = 10,
    page: Optional[int] = 1,
    sort: Optional[str] = None,
    mailto: Optional[str] = None,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Search OpenAlex works (papers) via the /works endpoint. Use this to discover OpenAlex Work IDs (W...

    Parameters
    ----------
    search : str
        Full-text search query for works (title/abstract/etc.). Example: "attention i...
    filter : str
        OpenAlex filter string (comma-separated). Example: "from_publication_date:202...
    per_page : int
        Results per page (OpenAlex max 200).
    page : int
        Page number (1-indexed).
    sort : str
        Sort order string, e.g. "cited_by_count:desc".
    mailto : str
        Optional contact email for OpenAlex polite pool. If omitted, ToolUniverse use...
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
            "name": "openalex_search_works",
            "arguments": {
                "search": search,
                "filter": filter,
                "per_page": per_page,
                "page": page,
                "sort": sort,
                "mailto": mailto,
            },
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["openalex_search_works"]
