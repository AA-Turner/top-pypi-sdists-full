"""
GtoPdb_list_ligands

Search and list ligands from the Guide to Pharmacology including synthetic drugs, natural product...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def GtoPdb_list_ligands(
    ligand_type: Optional[str] = None,
    name: Optional[str] = None,
    limit: Optional[int] = 20,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Search and list ligands from the Guide to Pharmacology including synthetic drugs, natural product...

    Parameters
    ----------
    ligand_type : str
        Filter by ligand type. Options: 'Approved' (approved drugs), 'Synthetic organ...
    name : str
        Search ligands by name (partial match). Example: 'aspirin', 'caffeine', 'insu...
    limit : int
        Maximum number of ligands to return (default: 20, max: 1000).
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
            "name": "GtoPdb_list_ligands",
            "arguments": {"ligand_type": ligand_type, "name": name, "limit": limit},
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["GtoPdb_list_ligands"]
