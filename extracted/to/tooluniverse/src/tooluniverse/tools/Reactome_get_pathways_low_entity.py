"""
Reactome_get_pathways_low_entity

Get low-level pathways (most specific pathways) containing a specific entity. Returns pathways at...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def Reactome_get_pathways_low_entity(
    id: str,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> list[Any]:
    """
    Get low-level pathways (most specific pathways) containing a specific entity. Returns pathways at...

    Parameters
    ----------
    id : str
        Entity Stable ID (pathway, reaction, or physical entity, e.g., 'R-HSA-73817')...
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
        {"name": "Reactome_get_pathways_low_entity", "arguments": {"id": id}},
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["Reactome_get_pathways_low_entity"]
