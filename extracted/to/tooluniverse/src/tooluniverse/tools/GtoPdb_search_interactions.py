"""
GtoPdb_search_interactions

Search pharmacological interactions between targets and ligands across the Guide to Pharmacology ...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def GtoPdb_search_interactions(
    target_type: Optional[str] = None,
    ligand_type: Optional[str] = None,
    action_type: Optional[str] = None,
    affinity_parameter: Optional[str] = None,
    min_affinity: Optional[float] = None,
    approved_only: Optional[bool] = False,
    limit: Optional[int] = 100,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Search pharmacological interactions between targets and ligands across the Guide to Pharmacology ...

    Parameters
    ----------
    target_type : str
        Filter by target class: 'GPCR', 'NHR', 'LGIC', 'VGIC', 'Enzyme', 'Transporter...
    ligand_type : str
        Filter by ligand class: 'Synthetic organic', 'Metabolite', 'Peptide', 'Antibo...
    action_type : str
        Filter by interaction type: 'Agonist', 'Antagonist', 'Inhibitor', 'Activator'...
    affinity_parameter : str
        Affinity measurement type: 'pKi', 'pIC50', 'pEC50', 'pKd', 'pKB', 'pA2'.
    min_affinity : float
        Minimum affinity value (e.g., 7.0 for pKi >= 7). Higher values indicate stron...
    approved_only : bool
        Return only interactions with approved drugs (true/false).
    limit : int
        Maximum number of interactions to return (default: 100, max: 5000).
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
            "name": "GtoPdb_search_interactions",
            "arguments": {
                "target_type": target_type,
                "ligand_type": ligand_type,
                "action_type": action_type,
                "affinity_parameter": affinity_parameter,
                "min_affinity": min_affinity,
                "approved_only": approved_only,
                "limit": limit,
            },
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["GtoPdb_search_interactions"]
