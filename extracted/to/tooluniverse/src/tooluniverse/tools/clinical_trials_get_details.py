"""
clinical_trials_get_details

Retrieves comprehensive details about a specific clinical trial using its NCT ID.
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def clinical_trials_get_details(
    action: str,
    nct_id: str,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Retrieves comprehensive details about a specific clinical trial using its NCT ID.

    Parameters
    ----------
    action : str
        The specific action to perform. Must be set to 'get_study_details'.
    nct_id : str
        The unique NCT identifier of the study to retrieve (e.g., 'NCT05033756'). Thi...
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
            "name": "clinical_trials_get_details",
            "arguments": {"action": action, "nct_id": nct_id},
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["clinical_trials_get_details"]
