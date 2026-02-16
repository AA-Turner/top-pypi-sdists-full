"""
GOAPI_get_genes_by_function

Get genes annotated with a specific Gene Ontology (GO) term. Find all genes/proteins that have be...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def GOAPI_get_genes_by_function(
    go_id: str,
    rows: Optional[int] = None,
    taxon: Optional[str] = None,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> Any:
    """
    Get genes annotated with a specific Gene Ontology (GO) term. Find all genes/proteins that have be...

    Parameters
    ----------
    go_id : str
        Gene Ontology term ID. Examples: 'GO:0006915' (apoptotic process), 'GO:000367...
    rows : int
        Maximum number of gene annotations to return (default: 20, max: 100).
    taxon : str
        Filter by taxon. Format: NCBITaxon:ID. Examples: 'NCBITaxon:9606' (human), 'N...
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
            "name": "GOAPI_get_genes_by_function",
            "arguments": {"go_id": go_id, "rows": rows, "taxon": taxon},
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["GOAPI_get_genes_by_function"]
