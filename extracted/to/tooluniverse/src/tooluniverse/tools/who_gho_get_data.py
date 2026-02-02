"""
who_gho_get_data

Retrieve health data from WHO GHO for a specific indicator. Supports filtering by country, year, ...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def who_gho_get_data(
    indicator_code: str,
    country_code: Optional[str] = None,
    year: Optional[int] = None,
    top: Optional[int] = 100,
    skip: Optional[int] = 0,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Retrieve health data from WHO GHO for a specific indicator. Supports filtering by country, year, ...

    Parameters
    ----------
    indicator_code : str
        The WHO GHO indicator code (e.g., 'WHOSIS_000001', 'Adult_curr_cig_smoking')
    country_code : str
        ISO 3-letter country code (e.g., 'USA', 'GBR', 'CHN'). Optional, returns all ...
    year : int
        Year to filter data (e.g., 2020). Optional, returns all years if not specified.
    top : int
        Maximum number of results to return (default: 100, max: 1000)
    skip : int
        Number of results to skip for pagination (default: 0)
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
            "name": "who_gho_get_data",
            "arguments": {
                "indicator_code": indicator_code,
                "country_code": country_code,
                "year": year,
                "top": top,
                "skip": skip,
            },
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["who_gho_get_data"]
