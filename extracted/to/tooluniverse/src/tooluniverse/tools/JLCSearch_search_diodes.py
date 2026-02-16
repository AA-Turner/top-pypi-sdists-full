"""
JLCSearch_search_diodes

Parametric search for diodes available from JLCPCB/LCSC. Filter by package size and specification...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def JLCSearch_search_diodes(
    package: Optional[str | Any] = None,
    limit: Optional[int | Any] = None,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> Any:
    """
    Parametric search for diodes available from JLCPCB/LCSC. Filter by package size and specification...

    Parameters
    ----------
    package : str | Any
        Diode package type. Examples: 'SOD-323', 'SOD-123', 'SMA', 'SMB', 'SOT-23', '...
    limit : int | Any
        Maximum number of results to return. Default returns up to 100 results.
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
        {
            "name": "JLCSearch_search_diodes",
            "arguments": {"package": package, "limit": limit},
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["JLCSearch_search_diodes"]
