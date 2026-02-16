"""
Bgee_search_genes

Search for genes in the Bgee comparative gene expression database across 29+ animal species. Bgee...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def Bgee_search_genes(
    query: str,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> Any:
    """
    Search for genes in the Bgee comparative gene expression database across 29+ animal species. Bgee...

    Parameters
    ----------
    query : str
        Gene name, symbol, or description to search for. Examples: 'TP53', 'insulin',...
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
        {"name": "Bgee_search_genes", "arguments": {"query": query}},
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["Bgee_search_genes"]
