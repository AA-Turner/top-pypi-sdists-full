"""
eMolecules_search

Search eMolecules vendor aggregator by keyword or compound name. eMolecules aggregates compounds ...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def eMolecules_search(
    operation: str,
    query: str,
    max_results: Optional[int] = 20,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Search eMolecules vendor aggregator by keyword or compound name. eMolecules aggregates compounds ...

    Parameters
    ----------
    operation : str

    query : str
        Search query - compound name or keyword
    max_results : int
        Maximum results (default: 20)
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
            "max_results": max_results,
        }.items()
        if v is not None
    }
    return get_shared_client().run_one_function(
        {
            "name": "eMolecules_search",
            "arguments": _args,
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["eMolecules_search"]
