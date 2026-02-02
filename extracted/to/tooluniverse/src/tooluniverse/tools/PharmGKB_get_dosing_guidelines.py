"""
PharmGKB_get_dosing_guidelines

Get pharmacogenetic dosing guidelines (CPIC/DPWG) from PharmGKB. Provide a specific 'guideline_id...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def PharmGKB_get_dosing_guidelines(
    guideline_id: Optional[str] = None,
    gene: Optional[str] = None,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Get pharmacogenetic dosing guidelines (CPIC/DPWG) from PharmGKB. Provide a specific 'guideline_id...

    Parameters
    ----------
    guideline_id : str
        PharmGKB guideline ID (e.g., 'PA166124584').
    gene : str
        Gene symbol (e.g., 'CYP2D6').
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
            "name": "PharmGKB_get_dosing_guidelines",
            "arguments": {"guideline_id": guideline_id, "gene": gene},
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["PharmGKB_get_dosing_guidelines"]
