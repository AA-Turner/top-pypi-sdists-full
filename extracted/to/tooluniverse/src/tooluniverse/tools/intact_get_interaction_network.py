"""
intact_get_interaction_network

Get interaction network centered on a specific interactor. Returns network of interactions with c...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def intact_get_interaction_network(
    identifier: str,
    depth: Optional[int] = 1,
    format: Optional[str] = "json",
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Get interaction network centered on a specific interactor. Returns network of interactions with c...

    Parameters
    ----------
    identifier : str
        IntAct identifier, UniProt ID, or gene name
    depth : int
        Network depth: 1 for direct interactions only, 2 for 2-hop network, etc. (def...
    format : str

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
            "name": "intact_get_interaction_network",
            "arguments": {"identifier": identifier, "depth": depth, "format": format},
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["intact_get_interaction_network"]
