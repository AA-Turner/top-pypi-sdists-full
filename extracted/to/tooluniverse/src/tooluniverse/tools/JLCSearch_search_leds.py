"""
JLCSearch_search_leds

Parametric search for LEDs (Light Emitting Diodes) available from JLCPCB/LCSC. Filter by color, p...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def JLCSearch_search_leds(
    color: Optional[str | Any] = None,
    package: Optional[str | Any] = None,
    limit: Optional[int | Any] = None,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> Any:
    """
    Parametric search for LEDs (Light Emitting Diodes) available from JLCPCB/LCSC. Filter by color, p...

    Parameters
    ----------
    color : str | Any
        LED color filter. Examples: 'red', 'green', 'blue', 'white', 'yellow', 'orang...
    package : str | Any
        SMD LED package size. Examples: '0201', '0402', '0603', '0805', '1206', '3528...
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
            "name": "JLCSearch_search_leds",
            "arguments": {"color": color, "package": package, "limit": limit},
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["JLCSearch_search_leds"]
