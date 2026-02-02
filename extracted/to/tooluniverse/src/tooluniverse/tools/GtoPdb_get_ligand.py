"""
GtoPdb_get_ligand

Get detailed information about a specific ligand by its GtoPdb ligand ID. Returns comprehensive d...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def GtoPdb_get_ligand(
    ligand_id: int,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Get detailed information about a specific ligand by its GtoPdb ligand ID. Returns comprehensive d...

    Parameters
    ----------
    ligand_id : int
        GtoPdb ligand identifier (e.g., 1016 for tamoxifen). Find ligand IDs using Gt...
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
        {"name": "GtoPdb_get_ligand", "arguments": {"ligand_id": ligand_id}},
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["GtoPdb_get_ligand"]
