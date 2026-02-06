"""
SAbDab_search_structures

Search SAbDab structural antibody database. SAbDab contains all antibody structures from PDB with...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def SAbDab_search_structures(
    operation: str,
    query: str,
    limit: Optional[int] = 50,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Search SAbDab structural antibody database. SAbDab contains all antibody structures from PDB with...

    Parameters
    ----------
    operation : str

    query : str
        Search query - antigen name, species, or keywords
    limit : int
        Maximum results (default: 50)
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
            "name": "SAbDab_search_structures",
            "arguments": {"operation": operation, "query": query, "limit": limit},
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["SAbDab_search_structures"]
