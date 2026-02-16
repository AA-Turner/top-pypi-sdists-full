"""
PomBase_search_genes

Search PomBase for fission yeast (S. pombe) genes by name, systematic ID, or protein product keyw...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def PomBase_search_genes(
    query: str,
    limit: Optional[int | Any] = None,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> Any:
    """
    Search PomBase for fission yeast (S. pombe) genes by name, systematic ID, or protein product keyw...

    Parameters
    ----------
    query : str
        Search query - gene name, systematic ID prefix, or product keyword. Examples:...
    limit : int | Any
        Maximum results to return (1-50, default 10).
    stream_callback : Callable, optional
        Callback for streaming output
    use_cache : bool, default False
        Enable caching
    validate : bool, default True
        Validate parameters

    Returns
    -------
    Any
    """
    # Handle mutable defaults to avoid B006 linting error

    return get_shared_client().run_one_function(
        {"name": "PomBase_search_genes", "arguments": {"query": query, "limit": limit}},
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["PomBase_search_genes"]
