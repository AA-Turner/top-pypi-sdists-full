"""
GTEx_get_median_gene_expression

Get median gene expression levels across GTEx tissues. Returns median expression in TPM (Transcri...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def GTEx_get_median_gene_expression(
    operation: str,
    gencode_id: str | list[str],
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
    Get median gene expression levels across GTEx tissues. Returns median expression in TPM (Transcri...

    Parameters
    ----------
    operation : str
        Operation type
    gencode_id : str | list[str]
        Versioned GENCODE ID(s), e.g. 'ENSG00000141510.16' for TP53. Can be single st...
    tissue_site_detail_id : list[str]
        Optional: Tissue IDs to filter (e.g. ['Liver', 'Brain_Cortex']). Omit for all...
    dataset_id : str
        GTEx dataset version (default: gtex_v10 for Adult GTEx V11)
    page : int
        Page number for pagination (0-based)
    items_per_page : int
        Results per page
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
            "name": "GTEx_get_median_gene_expression",
            "arguments": {
                "operation": operation,
                "gencode_id": gencode_id,
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


__all__ = ["GTEx_get_median_gene_expression"]
