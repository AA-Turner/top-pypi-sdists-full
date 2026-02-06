"""
BindingDB_get_ligands_by_uniprot

Get binding affinity data (Ki, IC50, Kd) for a single protein by UniProt ID. Returns SMILES struc...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def BindingDB_get_ligands_by_uniprot(
    uniprot: str,
    affinity_cutoff: Optional[int] = 10000,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> list[Any]:
    """
    Get binding affinity data (Ki, IC50, Kd) for a single protein by UniProt ID. Returns SMILES struc...

    Parameters
    ----------
    uniprot : str
        UniProt accession ID (e.g., P00533 for EGFR)
    affinity_cutoff : int
        Maximum affinity in nM (default: 10000)
    stream_callback : Callable, optional
        Callback for streaming output
    use_cache : bool, default False
        Enable caching
    validate : bool, default True
        Validate parameters

    Returns
    -------
    list[Any]
    """
    # Handle mutable defaults to avoid B006 linting error

    return get_shared_client().run_one_function(
        {
            "name": "BindingDB_get_ligands_by_uniprot",
            "arguments": {"uniprot": uniprot, "affinity_cutoff": affinity_cutoff},
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["BindingDB_get_ligands_by_uniprot"]
