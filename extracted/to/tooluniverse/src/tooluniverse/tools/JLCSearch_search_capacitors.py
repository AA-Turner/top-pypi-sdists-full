"""
JLCSearch_search_capacitors

Parametric search for capacitors available from JLCPCB/LCSC. Filter by capacitance value, voltage...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def JLCSearch_search_capacitors(
    capacitance: Optional[float | Any] = None,
    voltage: Optional[float | Any] = None,
    package: Optional[str | Any] = None,
    limit: Optional[int | Any] = None,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> Any:
    """
    Parametric search for capacitors available from JLCPCB/LCSC. Filter by capacitance value, voltage...

    Parameters
    ----------
    capacitance : float | Any
        Capacitance value in farads. Examples: 1e-12 (1pF), 1e-9 (1nF), 1e-7 (100nF),...
    voltage : float | Any
        Voltage rating in volts. Examples: 6.3, 10, 16, 25, 50, 100.
    package : str | Any
        SMD package size. Examples: '0201', '0402', '0603', '0805', '1206'.
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
            "name": "JLCSearch_search_capacitors",
            "arguments": {
                "capacitance": capacitance,
                "voltage": voltage,
                "package": package,
                "limit": limit,
            },
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["JLCSearch_search_capacitors"]
