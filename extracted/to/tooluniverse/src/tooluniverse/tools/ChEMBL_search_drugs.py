"""
ChEMBL_search_drugs

Search drugs by name, approval status, or other criteria.
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def ChEMBL_search_drugs(
    drug_chembl_id: Optional[str] = None,
    pref_name__contains: Optional[str] = None,
    max_phase: Optional[int] = None,
    limit: Optional[int] = 20,
    offset: Optional[int] = 0,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Search drugs by name, approval status, or other criteria.

    Parameters
    ----------
    drug_chembl_id : str
        Filter by drug ChEMBL ID
    pref_name__contains : str
        Filter by drug name (contains)
    max_phase : int
        Filter by maximum development phase (0-4)
    limit : int

    offset : int

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
            "name": "ChEMBL_search_drugs",
            "arguments": {
                "drug_chembl_id": drug_chembl_id,
                "pref_name__contains": pref_name__contains,
                "max_phase": max_phase,
                "limit": limit,
                "offset": offset,
            },
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["ChEMBL_search_drugs"]
