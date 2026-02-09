"""
PubMed_search_articles

Search PubMed biomedical literature database using NCBI E-utilities (esearch + esummary). Returns...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def PubMed_search_articles(
    query: str,
    limit: Optional[int] = 10,
    include_abstract: Optional[bool] = False,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> list[Any]:
    """
    Search PubMed biomedical literature database using NCBI E-utilities (esearch + esummary). Returns...

    Parameters
    ----------
    query : str
        Search query for PubMed articles. Use keywords, author names, journal names, ...
    limit : int
        Number of articles to return. This sets the maximum number of articles retrie...
    include_abstract : bool
        If true, best-effort fetches abstracts via efetch (adds abstract/abstract_sou...
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
            "name": "PubMed_search_articles",
            "arguments": {
                "query": query,
                "limit": limit,
                "include_abstract": include_abstract,
            },
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["PubMed_search_articles"]
