"""
HMDB_search

Search for metabolites by name or formula using PubChem. Returns PubChem CIDs (not HMDB IDs) with...
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
    Search for metabolites by name or formula using PubChem. Returns PubChem CIDs (not HMDB IDs) with...

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

    # Strip None values so optional parameters don't trigger schema validation errors
    _args = {
        k: v
        for k, v in {
            "operation": operation,
            "query": query,
            "search_type": search_type,
        }.items()
        if v is not None
    }
    return get_shared_client().run_one_function(
        {
            "name": "HMDB_search",
            "arguments": _args,
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["HMDB_search"]
