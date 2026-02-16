"""
STRING_get_network

Retrieve protein-protein interaction network from STRING (Search Tool for Retrieval of Interactin...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def STRING_get_network(
    protein_ids: list[str],
    species: Optional[int] = 9606,
    confidence_score: Optional[float] = 0.4,
    add_nodes: Optional[int] = 0,
    network_type: Optional[str] = "functional",
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> list[Any]:
    """
    Retrieve protein-protein interaction network from STRING (Search Tool for Retrieval of Interactin...

    Parameters
    ----------
    protein_ids : list[str]
        List of protein identifiers (UniProt IDs, gene names, Ensembl IDs)
    species : int
        NCBI taxonomy ID (default: 9606 for human)
    confidence_score : float
        Minimum confidence score (0-1, default: 0.4). Use 0.7 for high confidence, 0....
    add_nodes : int
        Number of additional interacting nodes to add to network (default: 0, max: 100)
    network_type : str
        Type of network: 'functional' (all evidence), 'physical' (physical interactio...
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
            "name": "STRING_get_network",
            "arguments": {
                "protein_ids": protein_ids,
                "species": species,
                "confidence_score": confidence_score,
                "add_nodes": add_nodes,
                "network_type": network_type,
            },
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["STRING_get_network"]
