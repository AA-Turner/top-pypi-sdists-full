"""
gwas_search_studies

Search for GWAS studies by various criteria including EFO trait, disease trait, cohort, GxE inter...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def gwas_search_studies(
    efo_trait: Optional[str] = None,
    disease_trait: Optional[str] = None,
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
    Search for GWAS studies by various criteria including EFO trait, disease trait, cohort, GxE inter...

    Parameters
    ----------
    efo_trait : str
        EFO trait identifier or name
    disease_trait : str
        Disease trait name
    cohort : str
        Cohort name (e.g., 'UKB' for UK Biobank)
    gxe : bool
        Filter for Gene-by-Environment interaction studies
    full_pvalue_set : bool
        Filter for studies with full summary statistics
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
            "name": "gwas_search_studies",
            "arguments": {
                "efo_trait": efo_trait,
                "disease_trait": disease_trait,
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


__all__ = ["gwas_search_studies"]
