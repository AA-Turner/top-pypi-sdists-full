"""
DGIdb_get_gene_druggability

Get druggability information for genes. Returns gene categories indicating if a gene is druggable...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def DGIdb_get_gene_druggability(
    genes: list[str],
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Get druggability information for genes. Returns gene categories indicating if a gene is druggable...

    Parameters
    ----------
    genes : list[str]
        List of gene symbols to check druggability.
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
        {"name": "DGIdb_get_gene_druggability", "arguments": {"genes": genes}},
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["DGIdb_get_gene_druggability"]
