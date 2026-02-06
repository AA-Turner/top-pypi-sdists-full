"""
SAbDab_get_summary

Get SAbDab database summary and statistics. Returns information about database content, features,...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def SAbDab_get_summary(
    operation: str,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Get SAbDab database summary and statistics. Returns information about database content, features,...

    Parameters
    ----------
    operation : str

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
        {"name": "SAbDab_get_summary", "arguments": {"operation": operation}},
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["SAbDab_get_summary"]
