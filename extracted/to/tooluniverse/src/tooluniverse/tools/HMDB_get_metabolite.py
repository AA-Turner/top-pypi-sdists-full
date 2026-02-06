"""
HMDB_get_metabolite

Get human metabolite information from HMDB by ID. Returns name, formula, SMILES, classification, ...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def HMDB_get_metabolite(
    operation: str,
    hmdb_id: str,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Get human metabolite information from HMDB by ID. Returns name, formula, SMILES, classification, ...

    Parameters
    ----------
    operation : str

    hmdb_id : str
        HMDB ID (e.g., HMDB0000001 or 0000001)
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
            "name": "HMDB_get_metabolite",
            "arguments": {"operation": operation, "hmdb_id": hmdb_id},
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["HMDB_get_metabolite"]
