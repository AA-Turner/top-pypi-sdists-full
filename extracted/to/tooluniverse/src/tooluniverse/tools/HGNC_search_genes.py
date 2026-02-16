"""
HGNC_search_genes

Search for human genes in HGNC by symbol, name, or alias. Supports wildcards (e.g., 'BRCA*' finds...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def HGNC_search_genes(
    query: str,
    search_field: Optional[str | Any] = None,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> Any:
    """
    Search for human genes in HGNC by symbol, name, or alias. Supports wildcards (e.g., 'BRCA*' finds...

    Parameters
    ----------
    query : str
        Search query - gene symbol, partial name, or keyword. Supports wildcards (*)....
    search_field : str | Any
        Field to search in. Options: 'symbol', 'name', 'alias_symbol', 'prev_symbol',...
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
        {
            "name": "HGNC_search_genes",
            "arguments": {"query": query, "search_field": search_field},
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["HGNC_search_genes"]
