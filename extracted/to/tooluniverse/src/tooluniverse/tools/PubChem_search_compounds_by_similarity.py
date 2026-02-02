"""
PubChem_search_compounds_by_similarity

Search by similarity (Tanimoto coefficient), returns CID list of compounds with similarity above ...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def PubChem_search_compounds_by_similarity(
    smiles: str,
    threshold: float,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Search by similarity (Tanimoto coefficient), returns CID list of compounds with similarity above ...

    Parameters
    ----------
    smiles : str
        SMILES expression of target molecule.
    threshold : float
        Similarity threshold (between 0 and 1), e.g., 0.9 means 90% similarity.
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
            "name": "PubChem_search_compounds_by_similarity",
            "arguments": {"smiles": smiles, "threshold": threshold},
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["PubChem_search_compounds_by_similarity"]
