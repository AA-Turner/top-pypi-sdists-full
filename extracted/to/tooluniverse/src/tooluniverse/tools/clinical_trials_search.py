"""
clinical_trials_search

Searches for clinical trials on ClinicalTrials.gov using conditions and/or interventions as filte...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def clinical_trials_search(
    action: str,
    condition: Optional[str] = None,
    intervention: Optional[str] = None,
    limit: Optional[int] = 10,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Searches for clinical trials on ClinicalTrials.gov using conditions and/or interventions as filte...

    Parameters
    ----------
    action : str
        The specific action to perform. Must be set to 'search_studies'.
    condition : str
        The disease or condition to search for (e.g., 'breast cancer', 'diabetes'). U...
    intervention : str
        The drug, treatment, or intervention to search for (e.g., 'pembrolizumab', 'c...
    limit : int
        The maximum number of study summaries to return. The default is 10. Adjust th...
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
            "name": "clinical_trials_search",
            "arguments": {
                "action": action,
                "condition": condition,
                "intervention": intervention,
                "limit": limit,
            },
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["clinical_trials_search"]
