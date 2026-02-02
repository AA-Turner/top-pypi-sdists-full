"""
PubChem_search_compounds_by_substructure

Search for all CIDs in PubChem that contain the given substructure (SMILES).
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def PubChem_search_compounds_by_substructure(
    smiles: str,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Search for all CIDs in PubChem that contain the given substructure (SMILES).

    Parameters
    ----------
    smiles : str
        SMILES of substructure (e.g., "c1ccccc1" corresponds to benzene ring).
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
            "name": "PubChem_search_compounds_by_substructure",
            "arguments": {"smiles": smiles},
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["PubChem_search_compounds_by_substructure"]
