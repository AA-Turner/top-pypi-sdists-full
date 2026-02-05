"""
gwas_get_studies_for_trait

Get studies for a specific trait with optional filters for cohort, GxE interactions, and summary ...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def gwas_get_studies_for_trait(
    disease_trait: Optional[str] = None,
    efo_uri: Optional[str] = None,
    cohort: Optional[str] = None,
    gxe: Optional[bool] = None,
    full_pvalue_set: Optional[bool] = None,
    size: Optional[int] = None,
    page: Optional[int] = None,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Get studies for a specific trait with optional filters for cohort, GxE interactions, and summary ...

    Parameters
    ----------
    disease_trait : str
        Disease or trait name for text-based search (e.g., 'diabetes', 'alzheimer dis...
    efo_uri : str
        Full EFO ontology URI (e.g., 'http://www.ebi.ac.uk/efo/EFO_0001645')
    cohort : str
        Cohort name (e.g., 'UKB' for UK Biobank)
    gxe : bool
        Filter for Gene-by-Environment interaction studies
    full_pvalue_set : bool
        Filter for studies with full summary statistics
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
            "name": "gwas_get_studies_for_trait",
            "arguments": {
                "disease_trait": disease_trait,
                "efo_uri": efo_uri,
                "cohort": cohort,
                "gxe": gxe,
                "full_pvalue_set": full_pvalue_set,
                "size": size,
                "page": page,
            },
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["gwas_get_studies_for_trait"]
