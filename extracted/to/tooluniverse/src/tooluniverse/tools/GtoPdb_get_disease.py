"""
GtoPdb_get_disease

Get detailed information about a specific disease by its GtoPdb disease ID. Returns disease descr...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def GtoPdb_get_disease(
    disease_id: int,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Get detailed information about a specific disease by its GtoPdb disease ID. Returns disease descr...

    Parameters
    ----------
    disease_id : int
        GtoPdb disease identifier. Find disease IDs using GtoPdb_list_diseases.
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
        {"name": "GtoPdb_get_disease", "arguments": {"disease_id": disease_id}},
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["GtoPdb_get_disease"]
