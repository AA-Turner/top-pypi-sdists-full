"""
DigiKey_get_manufacturers

Get the list of electronic component manufacturers available on Digi-Key. Returns manufacturer na...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def DigiKey_get_manufacturers(
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> Any:
    """
    Get the list of electronic component manufacturers available on Digi-Key. Returns manufacturer na...

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
    Any
    """
    # Handle mutable defaults to avoid B006 linting error

    return get_shared_client().run_one_function(
        {"name": "DigiKey_get_manufacturers", "arguments": {}},
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["DigiKey_get_manufacturers"]
