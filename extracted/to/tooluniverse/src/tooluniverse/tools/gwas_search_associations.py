"""
gwas_search_associations

Search for GWAS associations by various criteria including EFO trait, rs ID, accession ID, with s...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def gwas_search_associations(
    efo_trait: Optional[str] = None,
    rs_id: Optional[str] = None,
    accession_id: Optional[str] = None,
    sort: Optional[str] = None,
    direction: Optional[str] = None,
    size: Optional[int] = None,
    page: Optional[int] = None,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Search for GWAS associations by various criteria including EFO trait, rs ID, accession ID, with s...

    Parameters
    ----------
    efo_trait : str
        EFO trait identifier or name
    rs_id : str
        dbSNP rs identifier
    accession_id : str
        Study accession identifier
    sort : str
        Sort field (e.g., 'p_value', 'or_value')
    direction : str
        Sort direction ('asc' or 'desc')
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
            "name": "gwas_search_associations",
            "arguments": {
                "efo_trait": efo_trait,
                "rs_id": rs_id,
                "accession_id": accession_id,
                "sort": sort,
                "direction": direction,
                "size": size,
                "page": page,
            },
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["gwas_search_associations"]
