"""
HPO_search_terms

Search for Human Phenotype Ontology (HPO) terms by keyword. HPO contains over 18,000 standardized...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def HPO_search_terms(
    query: str,
    max_results: Optional[int | Any] = None,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> Any:
    """
    Search for Human Phenotype Ontology (HPO) terms by keyword. HPO contains over 18,000 standardized...

    Parameters
    ----------
    query : str
        Search keyword for phenotype terms. Examples: 'seizure', 'intellectual disabi...
    max_results : int | Any
        Maximum number of results to return (default 10, max 50).
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
            "name": "HPO_search_terms",
            "arguments": {"query": query, "max_results": max_results},
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["HPO_search_terms"]
