"""
get_crystallographic_properties_by_pdb_id

Retrieve crystallographic properties such as unit cell dimensions and space group for a PDB entry.
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def get_crystallographic_properties_by_pdb_id(
    pdb_id: str,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Retrieve crystallographic properties such as unit cell dimensions and space group for a PDB entry.

    Parameters
    ----------
    pdb_id : str
        PDB ID of the structure
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
            "name": "get_crystallographic_properties_by_pdb_id",
            "arguments": {"pdb_id": pdb_id},
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["get_crystallographic_properties_by_pdb_id"]
