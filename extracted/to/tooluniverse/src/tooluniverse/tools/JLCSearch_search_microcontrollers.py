"""
JLCSearch_search_microcontrollers

Parametric search for microcontrollers (MCUs) available from JLCPCB/LCSC. Filter by CPU core type...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def JLCSearch_search_microcontrollers(
    cpu_core: Optional[str | Any] = None,
    package: Optional[str | Any] = None,
    limit: Optional[int | Any] = None,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> Any:
    """
    Parametric search for microcontrollers (MCUs) available from JLCPCB/LCSC. Filter by CPU core type...

    Parameters
    ----------
    cpu_core : str | Any
        CPU core architecture filter. Examples: 'ARM-M3' (Cortex-M3), 'ARM-M4' (Corte...
    package : str | Any
        IC package type. Examples: 'LQFP-48(7x7)', 'TSSOP-20', 'QFN-32', 'SOP-8'.
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
            "name": "JLCSearch_search_microcontrollers",
            "arguments": {"cpu_core": cpu_core, "package": package, "limit": limit},
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["JLCSearch_search_microcontrollers"]
