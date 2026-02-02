"""
CORE_search_papers

Search for open access academic papers using CORE API. CORE is the world's largest collection of ...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def CORE_search_papers(
    query: str,
    limit: int,
    year_from: Optional[int] = None,
    year_to: Optional[int] = None,
    language: Optional[str] = None,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> list[Any]:
    """
    Search for open access academic papers using CORE API. CORE is the world's largest collection of ...

    Parameters
    ----------
    query : str
        Search query for CORE papers. Use keywords separated by spaces to refine your...
    limit : int
        Maximum number of papers to return. This sets the maximum number of papers re...
    year_from : int
        Start year for publication date filter (e.g., 2020). Optional parameter to li...
    year_to : int
        End year for publication date filter (e.g., 2024). Optional parameter to limi...
    language : str
        Language filter for papers (e.g., 'en', 'es', 'fr'). Optional parameter to li...
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
            "name": "CORE_search_papers",
            "arguments": {
                "query": query,
                "limit": limit,
                "year_from": year_from,
                "year_to": year_to,
                "language": language,
            },
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["CORE_search_papers"]
