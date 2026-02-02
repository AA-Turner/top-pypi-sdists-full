"""
STITCH_get_chemical_protein_interactions

Get chemical-protein interactions from STITCH. Returns known and predicted interactions between c...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def STITCH_get_chemical_protein_interactions(
    identifiers: list[str],
    species: Optional[int] = 9606,
    required_score: Optional[int] = 400,
    limit: Optional[int] = 10,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Get chemical-protein interactions from STITCH. Returns known and predicted interactions between c...

    Parameters
    ----------
    identifiers : list[str]
        Chemical names, drug names, or STITCH IDs (e.g., ['aspirin', 'ibuprofen'] or ...
    species : int
        NCBI taxonomy ID (9606 for human, 10090 for mouse).
    required_score : int
        Minimum confidence score (0-1000). 400=medium, 700=high, 900=highest.
    limit : int
        Maximum number of interaction partners per query.
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
            "name": "STITCH_get_chemical_protein_interactions",
            "arguments": {
                "identifiers": identifiers,
                "species": species,
                "required_score": required_score,
                "limit": limit,
            },
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["STITCH_get_chemical_protein_interactions"]
