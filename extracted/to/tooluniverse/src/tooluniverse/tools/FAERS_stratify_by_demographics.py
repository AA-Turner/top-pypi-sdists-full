"""
FAERS_stratify_by_demographics

Stratify adverse event reports by demographics (sex, age group, country). Returns counts and perc...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def FAERS_stratify_by_demographics(
    operation: str,
    drug_name: str,
    adverse_event: str,
    stratify_by: Optional[str] = "sex",
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Stratify adverse event reports by demographics (sex, age group, country). Returns counts and perc...

    Parameters
    ----------
    operation : str
        Operation type (fixed)
    drug_name : str
        Generic drug name
    adverse_event : str
        MedDRA Preferred Term
    stratify_by : str
        Demographic dimension to stratify by
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
    _args = {
        k: v
        for k, v in {
            "operation": operation,
            "drug_name": drug_name,
            "adverse_event": adverse_event,
            "stratify_by": stratify_by,
        }.items()
        if v is not None
    }
    return get_shared_client().run_one_function(
        {
            "name": "FAERS_stratify_by_demographics",
            "arguments": _args,
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["FAERS_stratify_by_demographics"]
