"""
Orphanet_get_classification

Get disease classification hierarchy from Orphanet. Returns parent and child disease categories s...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def Orphanet_get_classification(
    operation: str,
    orpha_code: str,
    lang: Optional[str] = "en",
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Get disease classification hierarchy from Orphanet. Returns parent and child disease categories s...

    Parameters
    ----------
    operation : str
        Operation type (fixed: get_classification)
    orpha_code : str
        Orphanet ORPHA code
    lang : str
        Language code (default: en)
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
            "name": "Orphanet_get_classification",
            "arguments": {
                "operation": operation,
                "orpha_code": orpha_code,
                "lang": lang,
            },
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["Orphanet_get_classification"]
