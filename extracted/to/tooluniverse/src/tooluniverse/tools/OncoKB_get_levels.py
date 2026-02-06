"""
OncoKB_get_levels

Get OncoKB evidence level definitions. Returns descriptions of all therapeutic actionability leve...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def OncoKB_get_levels(
    operation: str,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Get OncoKB evidence level definitions. Returns descriptions of all therapeutic actionability leve...

    Parameters
    ----------
    operation : str
        Operation type (fixed: get_levels)
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
        {"name": "OncoKB_get_levels", "arguments": {"operation": operation}},
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["OncoKB_get_levels"]
