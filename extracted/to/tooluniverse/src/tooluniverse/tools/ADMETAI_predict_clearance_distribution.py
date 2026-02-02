"""
ADMETAI_predict_clearance_distribution

Predicts clearance and distribution endpoints (Clearance_Hepatocyte_AZ, Clearance_Microsome_AZ, H...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def ADMETAI_predict_clearance_distribution(
    smiles: list[str],
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Predicts clearance and distribution endpoints (Clearance_Hepatocyte_AZ, Clearance_Microsome_AZ, H...

    Parameters
    ----------
    smiles : list[str]
        The list of SMILES strings.
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
            "name": "ADMETAI_predict_clearance_distribution",
            "arguments": {"smiles": smiles},
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["ADMETAI_predict_clearance_distribution"]
