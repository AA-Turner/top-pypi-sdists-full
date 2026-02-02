"""
ChEMBL_get_drug

Get detailed information about a drug by its ChEMBL drug ID. Includes approval status, indication...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def ChEMBL_get_drug(
    drug_chembl_id: str,
    format: Optional[str] = "json",
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Get detailed information about a drug by its ChEMBL drug ID. Includes approval status, indication...

    Parameters
    ----------
    drug_chembl_id : str
        ChEMBL drug ID, e.g., 'CHEMBL1201581'
    format : str

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
            "name": "ChEMBL_get_drug",
            "arguments": {"drug_chembl_id": drug_chembl_id, "format": format},
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["ChEMBL_get_drug"]
