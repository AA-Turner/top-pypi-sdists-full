"""
DepMap_get_gene_dependencies

Get gene dependency information from CRISPR knockout screens. Returns gene IDs and annotations. N...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def DepMap_get_gene_dependencies(
    gene_symbol: str,
    model_id: Optional[str] = None,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Get gene dependency information from CRISPR knockout screens. Returns gene IDs and annotations. N...

    Parameters
    ----------
    gene_symbol : str
        Gene symbol (e.g., 'EGFR', 'KRAS', 'TP53')
    model_id : str
        Optional: Filter by specific cell line
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
            "name": "DepMap_get_gene_dependencies",
            "arguments": {"gene_symbol": gene_symbol, "model_id": model_id},
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["DepMap_get_gene_dependencies"]
