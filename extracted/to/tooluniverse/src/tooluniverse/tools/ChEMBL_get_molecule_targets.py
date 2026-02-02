"""
ChEMBL_get_molecule_targets

Get all targets associated with a molecule by ChEMBL ID. Returns targets that have activity data ...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def ChEMBL_get_molecule_targets(
    molecule_chembl_id__exact: str,
    limit: Optional[int] = 20,
    offset: Optional[int] = 0,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Get all targets associated with a molecule by ChEMBL ID. Returns targets that have activity data ...

    Parameters
    ----------
    molecule_chembl_id__exact : str
        ChEMBL molecule ID (e.g., 'CHEMBL25'). To find a molecule ID, use ChEMBL_sear...
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
            "name": "ChEMBL_get_molecule_targets",
            "arguments": {
                "molecule_chembl_id__exact": molecule_chembl_id__exact,
                "limit": limit,
                "offset": offset,
            },
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["ChEMBL_get_molecule_targets"]
