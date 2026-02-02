"""
PubMed_get_cited_by

Get a list of PubMed articles that cite a specific PMID using elink. Returns PMIDs of articles th...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def PubMed_get_cited_by(
    pmid: str,
    limit: Optional[int] = 20,
    api_key: Optional[str] = None,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Get a list of PubMed articles that cite a specific PMID using elink. Returns PMIDs of articles th...

    Parameters
    ----------
    pmid : str
        PubMed ID (PMID) for which to find citing articles (e.g., '12345678'). Find P...
    limit : int
        Maximum number of citing articles to return (default: 20, max: 100).
    api_key : str
        Optional NCBI API key for higher rate limits.
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
            "name": "PubMed_get_cited_by",
            "arguments": {"pmid": pmid, "limit": limit, "api_key": api_key},
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["PubMed_get_cited_by"]
