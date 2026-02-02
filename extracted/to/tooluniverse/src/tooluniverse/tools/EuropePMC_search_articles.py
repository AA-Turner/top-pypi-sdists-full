"""
EuropePMC_search_articles

Search for articles on Europe PMC including abstracts. The tool queries the Europe PMC web servic...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def EuropePMC_search_articles(
    query: str,
    limit: Optional[int] = 5,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> list[Any]:
    """
    Search for articles on Europe PMC including abstracts. The tool queries the Europe PMC web servic...

    Parameters
    ----------
    query : str
        Search query for Europe PMC. Use keywords separated by spaces to refine your ...
    limit : int
        Number of articles to return. This sets the maximum number of articles retrie...
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
            "name": "EuropePMC_search_articles",
            "arguments": {"query": query, "limit": limit},
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["EuropePMC_search_articles"]
