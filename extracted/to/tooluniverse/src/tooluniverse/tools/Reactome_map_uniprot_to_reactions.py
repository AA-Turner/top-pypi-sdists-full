"""
Reactome_map_uniprot_to_reactions

Map a UniProt protein identifier to Reactome reactions. Returns all reactions that involve this p...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def Reactome_map_uniprot_to_reactions(
    id: str,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> list[Any]:
    """
    Map a UniProt protein identifier to Reactome reactions. Returns all reactions that involve this p...

    Parameters
    ----------
    id : str
        UniProt protein identifier (e.g., 'P04637')
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
        {"name": "Reactome_map_uniprot_to_reactions", "arguments": {"id": id}},
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["Reactome_map_uniprot_to_reactions"]
