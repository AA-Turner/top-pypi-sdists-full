"""
MetabolomicsWorkbench_search_by_exact_mass

Search metabolites by exact molecular mass. Useful for identifying unknown metabolites from high-...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def MetabolomicsWorkbench_search_by_exact_mass(
    mass_value: float,
    tolerance: Optional[float] = 0.1,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Search metabolites by exact molecular mass. Useful for identifying unknown metabolites from high-...

    Parameters
    ----------
    mass_value : float
        The exact mass value to search for in Daltons (e.g., 180.0634).
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
            "name": "MetabolomicsWorkbench_search_by_exact_mass",
            "arguments": {"mass_value": mass_value, "tolerance": tolerance},
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["MetabolomicsWorkbench_search_by_exact_mass"]
