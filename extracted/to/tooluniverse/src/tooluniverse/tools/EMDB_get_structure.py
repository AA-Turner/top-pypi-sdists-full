"""
EMDB_get_structure

Get 3D electron microscopy (EM) structure data from the Electron Microscopy Data Bank (EMDB). Ret...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def EMDB_get_structure(
    emdb_id: str,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Get 3D electron microscopy (EM) structure data from the Electron Microscopy Data Bank (EMDB). Ret...

    Parameters
    ----------
    emdb_id : str
        EMDB structure identifier in format 'EMD-####' (e.g., 'EMD-1234', 'EMD-0001')...
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
        {"name": "EMDB_get_structure", "arguments": {"emdb_id": emdb_id}},
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["EMDB_get_structure"]
