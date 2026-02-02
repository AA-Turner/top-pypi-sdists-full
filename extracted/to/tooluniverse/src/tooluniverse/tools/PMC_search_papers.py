"""
PMC_search_papers

Search for full-text biomedical literature using PMC (PubMed Central) API. PMC is the free full-t...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def PMC_search_papers(
    query: str,
    limit: int,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    article_type: Optional[str] = None,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> list[Any]:
    """
    Search for full-text biomedical literature using PMC (PubMed Central) API. PMC is the free full-t...

    Parameters
    ----------
    query : str
        Search query for PMC papers. Use keywords separated by spaces to refine your ...
    limit : int
        Maximum number of papers to return. This sets the maximum number of papers re...
    date_from : str
        Start date for publication date filter (YYYY/MM/DD format). Optional paramete...
    date_to : str
        End date for publication date filter (YYYY/MM/DD format). Optional parameter ...
    article_type : str
        Article type filter (e.g., 'research-article', 'review', 'case-report'). Opti...
    stream_callback : Callable, optional
        Callback for streaming output
    use_cache : bool, default False
        Enable caching
    validate : bool, default True
        Validate parameters

    Returns
    -------
    list[Any]
    """
    # Handle mutable defaults to avoid B006 linting error

    return get_shared_client().run_one_function(
        {
            "name": "PMC_search_papers",
            "arguments": {
                "query": query,
                "limit": limit,
                "date_from": date_from,
                "date_to": date_to,
                "article_type": article_type,
            },
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["PMC_search_papers"]
