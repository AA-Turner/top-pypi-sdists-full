"""
OncoKB_get_gene_info

Get gene-level oncogenic information from OncoKB. Returns whether gene is an oncogene, tumor supp...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def OncoKB_get_gene_info(
    operation: str,
    gene: str,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Get gene-level oncogenic information from OncoKB. Returns whether gene is an oncogene, tumor supp...

    Parameters
    ----------
    operation : str
        Operation type (fixed: get_gene_info)
    gene : str
        Gene symbol (e.g., BRAF, TP53, EGFR, KRAS)
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
            "name": "OncoKB_get_gene_info",
            "arguments": {"operation": operation, "gene": gene},
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["OncoKB_get_gene_info"]
