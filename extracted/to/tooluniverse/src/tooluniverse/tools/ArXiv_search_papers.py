"""
ArXiv_search_papers

Search arXiv for papers by keyword using the public arXiv API. Returns papers with title, abstrac...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def ArXiv_search_papers(
    query: str,
    limit: Optional[int] = 10,
    sort_by: Optional[str] = "relevance",
    sort_order: Optional[str] = "descending",
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> list[Any]:
    """
    Search arXiv for papers by keyword using the public arXiv API. Returns papers with title, abstrac...

    Parameters
    ----------
    query : str
        Search query for arXiv papers. Use keywords separated by spaces to refine you...
    limit : int
        Number of papers to return. This sets the maximum number of papers retrieved ...
    sort_by : str
        Sort order for results. Options: 'relevance', 'lastUpdatedDate', 'submittedDate'
    sort_order : str
        Sort direction. Options: 'ascending', 'descending'
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
            "name": "ArXiv_search_papers",
            "arguments": {
                "query": query,
                "limit": limit,
                "sort_by": sort_by,
                "sort_order": sort_order,
            },
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["ArXiv_search_papers"]
