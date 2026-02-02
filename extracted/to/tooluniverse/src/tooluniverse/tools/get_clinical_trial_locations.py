"""
get_clinical_trial_locations

Retrieves the locations where the clinical trials are being conducted, using their NCT IDs.
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def get_clinical_trial_locations(
    nct_ids: list[str],
    location: str,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> list[Any]:
    """
    Retrieves the locations where the clinical trials are being conducted, using their NCT IDs.

    Parameters
    ----------
    nct_ids : list[str]
        List of NCT IDs of the clinical trials (e.g., ['NCT04852770', 'NCT01728545']).
    location : str
        Placeholder.
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
            "name": "get_clinical_trial_locations",
            "arguments": {"nct_ids": nct_ids, "location": location},
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["get_clinical_trial_locations"]
