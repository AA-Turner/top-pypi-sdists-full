"""
FAERS_count_death_related_by_drug

Count adverse events associated with patient death for a given drug. Only medicinalproduct is req...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def FAERS_count_death_related_by_drug(
    medicinalproduct: str,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> list[Any]:
    """
    Count adverse events associated with patient death for a given drug. Only medicinalproduct is req...

    Parameters
    ----------
    medicinalproduct : str
        Drug name.
    stream_callback : Callable, optional
        Callback for streaming output
    use_cache : bool, default False
        Enable caching
    validate : bool, default True
        Validate parameters

    Returns
    -------
    list[Any]
    """
    # Handle mutable defaults to avoid B006 linting error

    return get_shared_client().run_one_function(
        {
            "name": "FAERS_count_death_related_by_drug",
            "arguments": {"medicinalproduct": medicinalproduct},
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["FAERS_count_death_related_by_drug"]
