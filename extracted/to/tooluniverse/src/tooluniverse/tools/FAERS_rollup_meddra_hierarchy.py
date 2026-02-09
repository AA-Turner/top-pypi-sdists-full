"""
FAERS_rollup_meddra_hierarchy

Aggregate adverse events by MedDRA hierarchy (Preferred Term level). Returns top 50 PTs with coun...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def FAERS_rollup_meddra_hierarchy(
    operation: str,
    drug_name: str,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Aggregate adverse events by MedDRA hierarchy (Preferred Term level). Returns top 50 PTs with coun...

    Parameters
    ----------
    operation : str
        Operation type (fixed)
    drug_name : str
        Generic drug name
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
            "name": "FAERS_rollup_meddra_hierarchy",
            "arguments": {"operation": operation, "drug_name": drug_name},
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["FAERS_rollup_meddra_hierarchy"]
