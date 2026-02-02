"""
clinvar_get_variant_details

Get detailed variant information from ClinVar by variant ID. Returns comprehensive variant data i...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def clinvar_get_variant_details(
    variant_id: str,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Get detailed variant information from ClinVar by variant ID. Returns comprehensive variant data i...

    Parameters
    ----------
    variant_id : str
        ClinVar variant ID (e.g., '12345', '123456')
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
            "name": "clinvar_get_variant_details",
            "arguments": {"variant_id": variant_id},
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["clinvar_get_variant_details"]
