"""
ChEMBL_get_drug_mechanisms

Get mechanisms of action for a drug by ChEMBL drug ID. To find a drug ID, use ChEMBL_search_drugs...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def ChEMBL_get_drug_mechanisms(
    drug_chembl_id__exact: str,
    limit: Optional[int] = 20,
    offset: Optional[int] = 0,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Get mechanisms of action for a drug by ChEMBL drug ID. To find a drug ID, use ChEMBL_search_drugs...

    Parameters
    ----------
    drug_chembl_id__exact : str
        ChEMBL drug ID (e.g., 'CHEMBL1201581'). To find a drug ID, use ChEMBL_search_...
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
            "name": "ChEMBL_get_drug_mechanisms",
            "arguments": {
                "drug_chembl_id__exact": drug_chembl_id__exact,
                "limit": limit,
                "offset": offset,
            },
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["ChEMBL_get_drug_mechanisms"]
