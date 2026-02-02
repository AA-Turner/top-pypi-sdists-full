"""
ComprehensiveDrugDiscoveryPipeline

Complete end-to-end drug discovery workflow from disease to optimized candidates. Identifies targ...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def ComprehensiveDrugDiscoveryPipeline(
    disease_efo_id: str,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Complete end-to-end drug discovery workflow from disease to optimized candidates. Identifies targ...

    Parameters
    ----------
    disease_efo_id : str
        The EFO ID of the disease for drug discovery (e.g., 'EFO_0001074' for Alzheim...
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
            "name": "ComprehensiveDrugDiscoveryPipeline",
            "arguments": {"disease_efo_id": disease_efo_id},
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["ComprehensiveDrugDiscoveryPipeline"]
