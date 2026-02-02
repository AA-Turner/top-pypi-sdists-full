"""
intact_get_interactor

Get detailed information about a specific interactor from IntAct database by IntAct identifier (e...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def intact_get_interactor(
    identifier: str,
    format: Optional[str] = "json",
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Get detailed information about a specific interactor from IntAct database by IntAct identifier (e...

    Parameters
    ----------
    identifier : str
        IntAct identifier (e.g., 'EBI-1004115') or UniProt ID (e.g., 'P04637') or gen...
    format : str
        Response format
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
            "name": "intact_get_interactor",
            "arguments": {"identifier": identifier, "format": format},
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["intact_get_interactor"]
