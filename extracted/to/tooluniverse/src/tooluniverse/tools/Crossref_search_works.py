"""
Crossref_search_works

Search Crossref Works API for scholarly articles, publications, and research outputs by keyword. ...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def Crossref_search_works(
    query: str,
    limit: int,
    filter: str,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Search Crossref Works API for scholarly articles, publications, and research outputs by keyword. ...

    Parameters
    ----------
    query : str
        Search query for Crossref works. Use keywords separated by spaces to refine y...
    limit : int
        Number of articles to return. This sets the maximum number of articles retrie...
    filter : str
        Optional filter string for Crossref API. Examples: 'type:journal-article' (on...
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
            "name": "Crossref_search_works",
            "arguments": {"query": query, "limit": limit, "filter": filter},
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["Crossref_search_works"]
