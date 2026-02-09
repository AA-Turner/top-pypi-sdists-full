"""
FAERS_calculate_disproportionality

Calculate statistical disproportionality measures (ROR, PRR, IC) with 95% CI for drug-event pairs...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def FAERS_calculate_disproportionality(
    operation: str,
    drug_name: str,
    adverse_event: str,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Calculate statistical disproportionality measures (ROR, PRR, IC) with 95% CI for drug-event pairs...

    Parameters
    ----------
    operation : str
        Operation type (fixed)
    drug_name : str
        Generic drug name (e.g., 'IBUPROFEN', 'ATORVASTATIN')
    adverse_event : str
        MedDRA Preferred Term (e.g., 'Hepatotoxicity', 'Myopathy')
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
            "name": "FAERS_calculate_disproportionality",
            "arguments": {
                "operation": operation,
                "drug_name": drug_name,
                "adverse_event": adverse_event,
            },
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["FAERS_calculate_disproportionality"]
