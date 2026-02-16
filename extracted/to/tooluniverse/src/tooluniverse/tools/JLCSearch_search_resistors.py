"""
JLCSearch_search_resistors

Parametric search for resistors available from JLCPCB/LCSC. Filter by resistance value, package s...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def JLCSearch_search_resistors(
    resistance: Optional[float | Any] = None,
    package: Optional[str | Any] = None,
    limit: Optional[int | Any] = None,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> Any:
    """
    Parametric search for resistors available from JLCPCB/LCSC. Filter by resistance value, package s...

    Parameters
    ----------
    resistance : float | Any
        Resistance value in ohms. Examples: 100 (100 ohm), 1000 (1k), 10000 (10k), 10...
    package : str | Any
        SMD package size. Examples: '0201', '0402', '0603', '0805', '1206', '2512'.
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
            "name": "JLCSearch_search_resistors",
            "arguments": {"resistance": resistance, "package": package, "limit": limit},
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["JLCSearch_search_resistors"]
