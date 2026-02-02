"""
intact_get_interactions

Get all interactions involving a specific interactor (protein or gene) by identifier. Uses EBI Se...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def intact_get_interactions(
    identifier: str,
    format: Optional[str] = "json",
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Get all interactions involving a specific interactor (protein or gene) by identifier. Uses EBI Se...

    Parameters
    ----------
    identifier : str
        IntAct identifier, UniProt ID, or gene name
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
            "name": "intact_get_interactions",
            "arguments": {"identifier": identifier, "format": format},
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["intact_get_interactions"]
