"""
BioRxiv_search_preprints

Search bioRxiv preprints using the public bioRxiv API. Returns preprints with title, authors, yea...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def BioRxiv_search_preprints(
    query: str,
    max_results: int,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> list[Any]:
    """
    Search bioRxiv preprints using the public bioRxiv API. Returns preprints with title, authors, yea...

    Parameters
    ----------
    query : str
        Search query for bioRxiv preprints. Use keywords separated by spaces to refin...
    max_results : int
        Maximum number of preprints to return. Default is 10, maximum is 200.
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
            "name": "BioRxiv_search_preprints",
            "arguments": {"query": query, "max_results": max_results},
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["BioRxiv_search_preprints"]
