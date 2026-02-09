"""
gwas_get_variants_for_trait

Get all variants associated with a specific trait with pagination support.
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def gwas_get_variants_for_trait(
    disease_trait: Optional[str] = None,
    efo_uri: Optional[str] = None,
    efo_id: Optional[str] = None,
    efo_trait: Optional[str] = None,
    size: Optional[int] = None,
    page: Optional[int] = None,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Get all variants associated with a specific trait with pagination support.

    Parameters
    ----------
    disease_trait : str
        Disease or trait name for text-based search (e.g., 'diabetes', 'breast cancer')
    efo_uri : str
        Full EFO ontology URI (e.g., 'http://www.ebi.ac.uk/efo/EFO_0001645')
    efo_id : str
        EFO/OBA term ID (e.g., 'EFO_0001645', 'OBA_2050062'). Recommended for reliabl...
    efo_trait : str
        Exact EFO trait label. Use when you know the canonical trait string.
    size : int
        Number of results to return per page
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
            "name": "gwas_get_variants_for_trait",
            "arguments": {
                "disease_trait": disease_trait,
                "efo_uri": efo_uri,
                "efo_id": efo_id,
                "efo_trait": efo_trait,
                "size": size,
                "page": page,
            },
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["gwas_get_variants_for_trait"]
