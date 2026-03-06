"""
KEGG_get_gene_pathways

Get all KEGG pathways that a gene participates in. Returns pathway IDs and names for a given KEGG...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def KEGG_get_gene_pathways(
    gene_id: str,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> Any:
    """
    Get all KEGG pathways that a gene participates in. Returns pathway IDs and names for a given KEGG...

    Parameters
    ----------
    gene_id : str
        KEGG gene identifier in organism:id format. Examples: 'hsa:7157' (human TP53)...
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

    # Strip None values so optional parameters don't trigger schema validation errors
    _args = {k: v for k, v in {"gene_id": gene_id}.items() if v is not None}
    return get_shared_client().run_one_function(
        {
            "name": "KEGG_get_gene_pathways",
            "arguments": _args,
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["KEGG_get_gene_pathways"]
