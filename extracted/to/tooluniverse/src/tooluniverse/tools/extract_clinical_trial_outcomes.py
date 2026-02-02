"""
extract_clinical_trial_outcomes

Extracts detailed trial outcome results (e.g., overall survival months, p-values, etc.) from clin...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def extract_clinical_trial_outcomes(
    nct_ids: list[str],
    outcome_measure: Optional[str] = None,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> str:
    """
    Extracts detailed trial outcome results (e.g., overall survival months, p-values, etc.) from clin...

    Parameters
    ----------
    nct_ids : list[str]
        List of NCT IDs of the clinical trials (e.g., ['NCT04852770', 'NCT01728545']).
    outcome_measure : str
        Outcome measure to extract. Example values include 'primary' (primary outcome...
    stream_callback : Callable, optional
        Callback for streaming output
    use_cache : bool, default False
        Enable caching
    validate : bool, default True
        Validate parameters

    Returns
    -------
    str
    """
    # Handle mutable defaults to avoid B006 linting error

    return get_shared_client().run_one_function(
        {
            "name": "extract_clinical_trial_outcomes",
            "arguments": {"nct_ids": nct_ids, "outcome_measure": outcome_measure},
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["extract_clinical_trial_outcomes"]
