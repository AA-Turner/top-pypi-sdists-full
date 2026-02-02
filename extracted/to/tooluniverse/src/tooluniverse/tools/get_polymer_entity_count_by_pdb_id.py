"""
get_polymer_entity_count_by_pdb_id

Get the number of distinct polymer entities (chains) in a structure.
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def get_polymer_entity_count_by_pdb_id(
    pdb_id: str,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Get the number of distinct polymer entities (chains) in a structure.

    Parameters
    ----------
    pdb_id : str
        4-character PDB ID
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
        {"name": "get_polymer_entity_count_by_pdb_id", "arguments": {"pdb_id": pdb_id}},
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["get_polymer_entity_count_by_pdb_id"]
