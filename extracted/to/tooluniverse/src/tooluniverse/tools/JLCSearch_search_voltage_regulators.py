"""
JLCSearch_search_voltage_regulators

Parametric search for voltage regulators (LDOs and linear regulators) available from JLCPCB/LCSC....
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def JLCSearch_search_voltage_regulators(
    output_voltage: Optional[float | Any] = None,
    output_current: Optional[float | Any] = None,
    package: Optional[str | Any] = None,
    limit: Optional[int | Any] = None,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> Any:
    """
    Parametric search for voltage regulators (LDOs and linear regulators) available from JLCPCB/LCSC....

    Parameters
    ----------
    output_voltage : float | Any
        Output voltage in volts. Examples: 1.8, 2.5, 3.3, 5.0, 12.0.
    output_current : float | Any
        Minimum output current capability in amps. Examples: 0.1, 0.5, 1.0, 3.0.
    package : str | Any
        Regulator package type. Examples: 'SOT-23', 'SOT-223', 'TO-252', 'TO-263', 'S...
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
            "name": "JLCSearch_search_voltage_regulators",
            "arguments": {
                "output_voltage": output_voltage,
                "output_current": output_current,
                "package": package,
                "limit": limit,
            },
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["JLCSearch_search_voltage_regulators"]
