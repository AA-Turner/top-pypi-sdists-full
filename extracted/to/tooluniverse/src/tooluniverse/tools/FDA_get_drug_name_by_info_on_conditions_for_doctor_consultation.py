"""
FDA_get_drug_name_by_info_on_conditions_for_doctor_consultation

Retrieve the drug names that require asking a doctor before use due to a patient's specific condi...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def FDA_get_drug_name_by_info_on_conditions_for_doctor_consultation(
    condition: str,
    limit: Optional[int] = None,
    skip: Optional[int] = None,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Retrieve the drug names that require asking a doctor before use due to a patient's specific condi...

    Parameters
    ----------
    condition : str
        The condition or symptom that requires consulting a doctor.
    limit : int
        The number of records to return.
    skip : int
        The number of records to skip.
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
            "name": "FDA_get_drug_name_by_info_on_conditions_for_doctor_consultation",
            "arguments": {"condition": condition, "limit": limit, "skip": skip},
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["FDA_get_drug_name_by_info_on_conditions_for_doctor_consultation"]
