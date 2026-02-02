"""
get_refinement_resolution_by_pdb_id

Retrieve the reported resolution from refinement data for X-ray structures.
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def get_refinement_resolution_by_pdb_id(
    pdb_id: str,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Retrieve the reported resolution from refinement data for X-ray structures.

    Parameters
    ----------
    pdb_id : str
        PDB entry ID
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
            "name": "get_refinement_resolution_by_pdb_id",
            "arguments": {"pdb_id": pdb_id},
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["get_refinement_resolution_by_pdb_id"]
