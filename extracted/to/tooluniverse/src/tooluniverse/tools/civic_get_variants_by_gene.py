"""
civic_get_variants_by_gene

Get all variants associated with a specific gene in CIViC database. Returns variant information i...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def civic_get_variants_by_gene(
    gene_id: int,
    limit: Optional[int] = 50,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Get all variants associated with a specific gene in CIViC database. Returns variant information i...

    Parameters
    ----------
    gene_id : int
        CIViC gene ID (e.g., 4244 for ABCB1). Find gene IDs using civic_search_genes.
    limit : int
        Maximum number of variants to return (default: 50, recommended max: 200)
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
            "name": "civic_get_variants_by_gene",
            "arguments": {"gene_id": gene_id, "limit": limit},
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["civic_get_variants_by_gene"]
