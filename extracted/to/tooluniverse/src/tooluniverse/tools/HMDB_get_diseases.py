"""
HMDB_get_diseases

Attempts to get disease associations for a metabolite from HMDB. Note: HMDB does not provide an o...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def HMDB_get_diseases(
    operation: str,
    hmdb_id: str,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Attempts to get disease associations for a metabolite from HMDB. Note: HMDB does not provide an o...

    Parameters
    ----------
    operation : str

    hmdb_id : str
        HMDB ID
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
        for k, v in {"operation": operation, "hmdb_id": hmdb_id}.items()
        if v is not None
    }
    return get_shared_client().run_one_function(
        {
            "name": "HMDB_get_diseases",
            "arguments": _args,
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["HMDB_get_diseases"]
