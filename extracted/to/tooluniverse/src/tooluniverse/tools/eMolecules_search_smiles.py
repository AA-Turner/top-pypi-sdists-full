"""
eMolecules_search_smiles

Search eMolecules by chemical structure (SMILES). Supports exact match, substructure, and similar...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def eMolecules_search_smiles(
    operation: str,
    smiles: str,
    search_type: Optional[str] = "similarity",
    max_results: Optional[int] = 20,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Search eMolecules by chemical structure (SMILES). Supports exact match, substructure, and similar...

    Parameters
    ----------
    operation : str

    smiles : str
        SMILES string for the query compound
    search_type : str
        Search type: exact, substructure, similarity (default: similarity)
    max_results : int
        Maximum results (default: 20)
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
            "name": "eMolecules_search_smiles",
            "arguments": {
                "operation": operation,
                "smiles": smiles,
                "search_type": search_type,
                "max_results": max_results,
            },
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["eMolecules_search_smiles"]
