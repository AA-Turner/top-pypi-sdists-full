"""
FAERS_filter_serious_events

Filter for serious adverse events (death, hospitalization, disability, life-threatening). Returns...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def FAERS_filter_serious_events(
    operation: str,
    drug_name: str,
    seriousness_type: Optional[str] = "all",
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Filter for serious adverse events (death, hospitalization, disability, life-threatening). Returns...

    Parameters
    ----------
    operation : str
        Operation type (fixed)
    drug_name : str
        Generic drug name
    seriousness_type : str
        Type of serious event to filter
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
            "name": "FAERS_filter_serious_events",
            "arguments": {
                "operation": operation,
                "drug_name": drug_name,
                "seriousness_type": seriousness_type,
            },
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["FAERS_filter_serious_events"]
