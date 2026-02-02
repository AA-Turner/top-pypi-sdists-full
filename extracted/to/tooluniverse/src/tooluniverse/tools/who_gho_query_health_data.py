"""
who_gho_query_health_data

Answer generic health questions using natural language queries. Automatically searches for releva...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def who_gho_query_health_data(
    query: str,
    country_code: Optional[str] = None,
    year: Optional[int] = None,
    top: Optional[int] = 5,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Answer generic health questions using natural language queries. Automatically searches for releva...

    Parameters
    ----------
    query : str
        Natural language query (e.g., 'smoking rate in USA', 'diabetes prevalence in ...
    country_code : str
        ISO 3-letter country code (e.g., 'USA', 'GBR'). Optional, will be extracted f...
    year : int
        Year for data (e.g., 2020). Optional, will be extracted from query if not pro...
    top : int
        Maximum number of results to return (default: 5)
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
            "name": "who_gho_query_health_data",
            "arguments": {
                "query": query,
                "country_code": country_code,
                "year": year,
                "top": top,
            },
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["who_gho_query_health_data"]
