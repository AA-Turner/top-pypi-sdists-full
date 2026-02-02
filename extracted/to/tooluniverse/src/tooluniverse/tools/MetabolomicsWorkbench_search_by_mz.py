"""
MetabolomicsWorkbench_search_by_mz

Search metabolites by m/z (mass-to-charge ratio) value from mass spectrometry data. Essential for...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def MetabolomicsWorkbench_search_by_mz(
    mz_value: float,
    adduct: Optional[str] = "M+H",
    tolerance: Optional[float] = 0.1,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Search metabolites by m/z (mass-to-charge ratio) value from mass spectrometry data. Essential for...

    Parameters
    ----------
    mz_value : float
        The m/z value to search for (e.g., 180.0634 for glucose [M+H]+).
    adduct : str
        Adduct type. Common values: 'M+H' (protonated), 'M-H' (deprotonated), 'M+Na' ...
    tolerance : float
        Mass tolerance in Daltons for the search.
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
        {
            "name": "MetabolomicsWorkbench_search_by_mz",
            "arguments": {
                "mz_value": mz_value,
                "adduct": adduct,
                "tolerance": tolerance,
            },
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["MetabolomicsWorkbench_search_by_mz"]
