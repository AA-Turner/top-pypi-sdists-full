"""
civic_search_genes

Search for genes in CIViC (Clinical Interpretation of Variants in Cancer) database. CIViC is a co...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def civic_search_genes(
    query: Optional[str] = None,
    limit: Optional[int] = 10,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Search for genes in CIViC (Clinical Interpretation of Variants in Cancer) database. CIViC is a co...

    Parameters
    ----------
    query : str
        Optional search query to filter genes by name or description. If not provided...
    limit : int
        Maximum number of genes to return (default: 10, recommended max: 100)
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
        {"name": "civic_search_genes", "arguments": {"query": query, "limit": limit}},
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["civic_search_genes"]
