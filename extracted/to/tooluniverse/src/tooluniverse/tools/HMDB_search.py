"""
HMDB_search

Search HMDB for metabolites by name, formula, or mass. Returns matching metabolites with HMDB IDs...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def HMDB_search(
    operation: str,
    query: str,
    search_type: Optional[str] = "name",
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Search HMDB for metabolites by name, formula, or mass. Returns matching metabolites with HMDB IDs...

    Parameters
    ----------
    operation : str

    query : str
        Search query - metabolite name, formula, or keyword
    search_type : str
        Search type: name, formula, mass (default: name)
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
            "name": "HMDB_search",
            "arguments": {
                "operation": operation,
                "query": query,
                "search_type": search_type,
            },
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["HMDB_search"]
