"""
GtoPdb_get_target_interactions

Get all ligand interactions for a specific target by its GtoPdb target ID. Returns detailed inter...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def GtoPdb_get_target_interactions(
    target_id: int,
    action_type: Optional[str] = None,
    affinity_parameter: Optional[str] = None,
    min_affinity: Optional[float] = None,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Get all ligand interactions for a specific target by its GtoPdb target ID. Returns detailed inter...

    Parameters
    ----------
    target_id : int
        GtoPdb target identifier (e.g., 221 for GPER). Find target IDs using GtoPdb_g...
    action_type : str
        Filter by action: 'Agonist', 'Antagonist', 'Inhibitor', 'Activator', 'Channel...
    affinity_parameter : str
        Affinity type: 'pKi', 'pIC50', 'pEC50', 'pKd'. Leave empty for all affinity m...
    min_affinity : float
        Minimum affinity value (e.g., 7.0). Leave empty for all affinities.
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
            "name": "GtoPdb_get_target_interactions",
            "arguments": {
                "target_id": target_id,
                "action_type": action_type,
                "affinity_parameter": affinity_parameter,
                "min_affinity": min_affinity,
            },
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["GtoPdb_get_target_interactions"]
