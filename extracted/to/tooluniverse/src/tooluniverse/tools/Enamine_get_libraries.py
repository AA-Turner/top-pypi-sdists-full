"""
Enamine_get_libraries

Get information about available Enamine compound libraries including REAL database, building bloc...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def Enamine_get_libraries(
    operation: str,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Get information about available Enamine compound libraries including REAL database, building bloc...

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
        {"name": "Enamine_get_libraries", "arguments": {"operation": operation}},
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["Enamine_get_libraries"]
