"""
gwas_search_snps

Search for GWAS single nucleotide polymorphisms (SNPs) by rs ID or mapped gene.
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def gwas_search_snps(
    rs_id: Optional[str] = None,
    mapped_gene: Optional[str] = None,
    size: Optional[int] = None,
    page: Optional[int] = None,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Search for GWAS single nucleotide polymorphisms (SNPs) by rs ID or mapped gene.

    Parameters
    ----------
    rs_id : str
        dbSNP rs identifier
    mapped_gene : str
        Gene name or symbol
    size : int
        Number of results to return
    page : int
        Page number for pagination
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
            "name": "gwas_search_snps",
            "arguments": {
                "rs_id": rs_id,
                "mapped_gene": mapped_gene,
                "size": size,
                "page": page,
            },
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["gwas_search_snps"]
