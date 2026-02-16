"""
SASBDB_search_entries

Search SASBDB (Small Angle Scattering Biological Data Bank) for protein structure entries. SASBDB...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def SASBDB_search_entries(
    query: str,
    method: Optional[str] = "all",
    limit: Optional[int] = 20,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> Optional[dict[str, Any]]:
    """
    Search SASBDB (Small Angle Scattering Biological Data Bank) for protein structure entries. SASBDB...

    Parameters
    ----------
    query : str
        Search query for SASBDB entries. Examples: 'immunoglobulin', 'BSA', 'lysozyme...
    method : str
        Filter by experimental method: 'SAXS' (X-ray), 'SANS' (neutron), or 'all' (de...
    limit : int
        Maximum number of entries to return (default: 20, max: 100).
    stream_callback : Callable, optional
        Callback for streaming output
    use_cache : bool, default False
        Enable caching
    validate : bool, default True
        Validate parameters

    Returns
    -------
    Optional[dict[str, Any]]
    """
    # Handle mutable defaults to avoid B006 linting error

    return get_shared_client().run_one_function(
        {
            "name": "SASBDB_search_entries",
            "arguments": {"query": query, "method": method, "limit": limit},
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["SASBDB_search_entries"]
