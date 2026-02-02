"""
kegg_get_gene_info

Get detailed gene information from KEGG by gene ID. Returns gene data including sequence, functio...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def kegg_get_gene_info(
    gene_id: str,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Get detailed gene information from KEGG by gene ID. Returns gene data including sequence, functio...

    Parameters
    ----------
    gene_id : str
        KEGG gene identifier (e.g., 'hsa:348', 'hsa:3480')
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
        {"name": "kegg_get_gene_info", "arguments": {"gene_id": gene_id}},
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["kegg_get_gene_info"]
