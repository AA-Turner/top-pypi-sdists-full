"""
PharmGKB_get_dosing_guidelines

Get pharmacogenetic dosing guidelines (CPIC/DPWG) from PharmGKB by guideline_id. Use PharmGKB_sea...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def PharmGKB_get_dosing_guidelines(
    guideline_id: str,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Get pharmacogenetic dosing guidelines (CPIC/DPWG) from PharmGKB by guideline_id. Use PharmGKB_sea...

    Parameters
    ----------
    guideline_id : str
        PharmGKB guideline ID (e.g., 'PA166124584').
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

    # Strip None values so optional parameters don't trigger schema validation errors
    _args = {k: v for k, v in {"guideline_id": guideline_id}.items() if v is not None}
    return get_shared_client().run_one_function(
        {
            "name": "PharmGKB_get_dosing_guidelines",
            "arguments": _args,
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["PharmGKB_get_dosing_guidelines"]
