"""
loinc_search_codes

Search for LOINC (Logical Observation Identifiers Names and Codes) codes using UMLS. Returns matc...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def loinc_search_codes(
    query: str,
    pageNumber: Optional[int] = 1,
    pageSize: Optional[int] = 25,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Search for LOINC (Logical Observation Identifiers Names and Codes) codes using UMLS. Returns matc...

    Parameters
    ----------
    query : str
        Search query (test name, component, or LOINC code)
    pageNumber : int
        Page number for pagination (default: 1)
    pageSize : int
        Number of results per page (default: 25, max: 25)
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
            "name": "loinc_search_codes",
            "arguments": {
                "query": query,
                "pageNumber": pageNumber,
                "pageSize": pageSize,
            },
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["loinc_search_codes"]
