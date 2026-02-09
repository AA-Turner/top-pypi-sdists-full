"""
SemanticScholar_search_papers

Search for papers on Semantic Scholar including abstracts. This tool queries the Semantic Scholar...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def SemanticScholar_search_papers(
    query: str,
    limit: int,
    include_abstract: Optional[bool] = False,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> list[Any]:
    """
    Search for papers on Semantic Scholar including abstracts. This tool queries the Semantic Scholar...

    Parameters
    ----------
    query : str
        Search query for Semantic Scholar. Use keywords separated by spaces to refine...
    limit : int
        Maximum number of papers to return from Semantic Scholar.
    include_abstract : bool
        If true, best-effort fetches missing abstracts via the paper detail endpoint ...
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
            "name": "SemanticScholar_search_papers",
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


__all__ = ["SemanticScholar_search_papers"]
