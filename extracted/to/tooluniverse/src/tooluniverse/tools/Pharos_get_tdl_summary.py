"""
Pharos_get_tdl_summary

Get Target Development Level statistics from Pharos. Returns counts of human proteome targets at ...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def Pharos_get_tdl_summary(
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Get Target Development Level statistics from Pharos. Returns counts of human proteome targets at ...

    Parameters
    ----------
    No parameters
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
        {"name": "Pharos_get_tdl_summary", "arguments": {}},
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["Pharos_get_tdl_summary"]
