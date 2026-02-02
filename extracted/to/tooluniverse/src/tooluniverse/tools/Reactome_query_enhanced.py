"""
Reactome_query_enhanced

Get enhanced information about a specific entity by its Stable ID. Returns additional details bey...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def Reactome_query_enhanced(
    stId: str,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Get enhanced information about a specific entity by its Stable ID. Returns additional details bey...

    Parameters
    ----------
    stId : str
        Entity Stable ID (pathway, reaction, complex, etc., e.g., 'R-HSA-73817'). To ...
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
        {"name": "Reactome_query_enhanced", "arguments": {"stId": stId}},
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["Reactome_query_enhanced"]
