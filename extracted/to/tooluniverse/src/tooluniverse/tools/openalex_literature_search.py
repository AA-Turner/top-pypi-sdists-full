"""
openalex_literature_search

Search for academic literature using OpenAlex API. Retrieves papers with title, abstract, authors...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def openalex_literature_search(
    search_keywords: str,
    max_results: Optional[int] = 10,
    year_from: Optional[int] = None,
    year_to: Optional[int] = None,
    open_access: Optional[bool] = None,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> list[Any]:
    """
    Search for academic literature using OpenAlex API. Retrieves papers with title, abstract, authors...

    Parameters
    ----------
    search_keywords : str
        Keywords to search for in paper titles, abstracts, and content. Use relevant ...
    max_results : int
        Maximum number of papers to retrieve (default: 10, maximum: 200).
    year_from : int
        Start year for publication date filter (e.g., 2020). Optional parameter to li...
    year_to : int
        End year for publication date filter (e.g., 2023). Optional parameter to limi...
    open_access : bool
        Filter for open access papers only. Set to true for open access papers, false...
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
            "name": "openalex_literature_search",
            "arguments": {
                "search_keywords": search_keywords,
                "max_results": max_results,
                "year_from": year_from,
                "year_to": year_to,
                "open_access": open_access,
            },
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["openalex_literature_search"]
