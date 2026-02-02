"""
SIMBAD_advanced_query

Execute advanced ADQL (Astronomical Data Query Language) queries on SIMBAD using TAP (Table Acces...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def SIMBAD_advanced_query(
    adql_query: str,
    max_results: Optional[int] = 100,
    format: Optional[str] = "json",
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Execute advanced ADQL (Astronomical Data Query Language) queries on SIMBAD using TAP (Table Acces...

    Parameters
    ----------
    adql_query : str
        ADQL query string. Example: 'SELECT TOP 10 main_id, ra, dec, otype FROM basic...
    max_results : int
        Maximum number of results to return
    format : str
        Output format. Options: 'json' or 'votable'
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
            "name": "SIMBAD_advanced_query",
            "arguments": {
                "adql_query": adql_query,
                "max_results": max_results,
                "format": format,
            },
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["SIMBAD_advanced_query"]
