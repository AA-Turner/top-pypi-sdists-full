"""
search_clinical_trials

Search for clinical trials registered on clinicaltrials.gov based on title, conditions, intervent...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def search_clinical_trials(
    query_term: str,
    condition: Optional[str] = None,
    intervention: Optional[str] = None,
    pageSize: Optional[int] = None,
    pageToken: Optional[str] = None,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> Any:
    """
    Search for clinical trials registered on clinicaltrials.gov based on title, conditions, intervent...

    Parameters
    ----------
    condition : str
        Query for condition or disease using Essie expression syntax (e.g., 'lung can...
    intervention : str
        Query for intervention/treatment using Essie expression syntax (e.g., 'chemot...
    query_term : str
        Query for 'other terms' with Essie expression syntax (e.g., 'combination', 'A...
    pageSize : int
        Maximum number of studies to return per page (default 10, max 1000).
    pageToken : str
        Token to retrieve the next page of results, obtained from the 'nextPageToken'...
    stream_callback : Callable, optional
        Callback for streaming output
    use_cache : bool, default False
        Enable caching
    validate : bool, default True
        Validate parameters

    Returns
    -------
    Any
    """
    # Handle mutable defaults to avoid B006 linting error

    return get_shared_client().run_one_function(
        {
            "name": "search_clinical_trials",
            "arguments": {
                "condition": condition,
                "intervention": intervention,
                "query_term": query_term,
                "pageSize": pageSize,
                "pageToken": pageToken,
            },
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["search_clinical_trials"]
