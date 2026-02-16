"""
SASBDB_get_scattering_profile

Retrieve the experimental small-angle scattering curve I(q) vs q for a SASBDB entry. Returns mome...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def SASBDB_get_scattering_profile(
    sasbdb_id: str,
    format: Optional[str] = "json",
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> Any:
    """
    Retrieve the experimental small-angle scattering curve I(q) vs q for a SASBDB entry. Returns mome...

    Parameters
    ----------
    sasbdb_id : str
        SASBDB entry identifier (e.g., 'SASDBA2', 'SASDBW5'). Get from SASBDB_search_...
    format : str
        Output format: 'json' (structured data) or 'dat' (column format for ATSAS too...
    stream_callback : Callable, optional
        Callback for streaming output
    use_cache : bool, default False
        Enable caching
    validate : bool, default True
        Validate parameters

    Returns
    -------
    Any
    """
    # Handle mutable defaults to avoid B006 linting error

    return get_shared_client().run_one_function(
        {
            "name": "SASBDB_get_scattering_profile",
            "arguments": {"sasbdb_id": sasbdb_id, "format": format},
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["SASBDB_get_scattering_profile"]
