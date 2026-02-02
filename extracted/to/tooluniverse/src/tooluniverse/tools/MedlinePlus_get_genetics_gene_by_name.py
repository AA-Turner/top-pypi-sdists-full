"""
MedlinePlus_get_genetics_gene_by_name

Get detailed information from MedlinePlus Genetics corresponding to gene name, supports JSON or X...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def MedlinePlus_get_genetics_gene_by_name(
    gene: str,
    format: str,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Get detailed information from MedlinePlus Genetics corresponding to gene name, supports JSON or X...

    Parameters
    ----------
    gene : str
        URL slug of gene name, e.g., "BRCA1", must match MedlinePlus page path.
    format : str
        Return format, options "json" or "xml", default "json".
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
            "name": "MedlinePlus_get_genetics_gene_by_name",
            "arguments": {"gene": gene, "format": format},
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["MedlinePlus_get_genetics_gene_by_name"]
