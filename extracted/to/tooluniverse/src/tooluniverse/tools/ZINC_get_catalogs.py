"""
ZINC_get_catalogs

Get available ZINC compound catalogs and libraries. Returns list of screening libraries like In-S...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def ZINC_get_catalogs(
    operation: str,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Get available ZINC compound catalogs and libraries. Returns list of screening libraries like In-S...

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
        {"name": "ZINC_get_catalogs", "arguments": {"operation": operation}},
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["ZINC_get_catalogs"]
