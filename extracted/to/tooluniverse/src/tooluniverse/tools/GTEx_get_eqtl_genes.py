"""
GTEx_get_eqtl_genes

Get eQTL genes (eGenes) with significant cis-eQTLs. Returns genes with at least one significant e...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def GTEx_get_eqtl_genes(
    operation: str,
    tissue_site_detail_id: Optional[list[str]] = None,
    dataset_id: Optional[str] = "gtex_v10",
    page: Optional[int] = 0,
    items_per_page: Optional[int] = 250,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> list[Any]:
    """
    Get eQTL genes (eGenes) with significant cis-eQTLs. Returns genes with at least one significant e...

    Parameters
    ----------
    operation : str
        Operation type
    tissue_site_detail_id : list[str]
        Optional: Filter by tissue IDs. Omit for all tissues
    dataset_id : str
        GTEx dataset version
    page : int

    items_per_page : int

    stream_callback : Callable, optional
        Callback for streaming output
    use_cache : bool, default False
        Enable caching
    validate : bool, default True
        Validate parameters

    Returns
    -------
    list[Any]
    """
    # Handle mutable defaults to avoid B006 linting error

    return get_shared_client().run_one_function(
        {
            "name": "GTEx_get_eqtl_genes",
            "arguments": {
                "operation": operation,
                "tissue_site_detail_id": tissue_site_detail_id,
                "dataset_id": dataset_id,
                "page": page,
                "items_per_page": items_per_page,
            },
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["GTEx_get_eqtl_genes"]
