"""
EVE_get_gene_info

Check if EVE scores are available for a gene and get gene information. EVE covers ~3,000 disease-...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def EVE_get_gene_info(
    gene_symbol: str,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Check if EVE scores are available for a gene and get gene information. EVE covers ~3,000 disease-...

    Parameters
    ----------
    gene_symbol : str
        Gene symbol (e.g., 'TP53', 'BRCA1', 'EGFR')
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
        {"name": "EVE_get_gene_info", "arguments": {"gene_symbol": gene_symbol}},
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["EVE_get_gene_info"]
