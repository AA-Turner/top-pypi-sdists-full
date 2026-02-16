"""
SASBDB_download_data

Get download URLs and metadata for raw experimental data files, processed scattering curves, dist...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def SASBDB_download_data(
    sasbdb_id: str,
    file_type: Optional[str] = "all",
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> Optional[dict[str, Any]]:
    """
    Get download URLs and metadata for raw experimental data files, processed scattering curves, dist...

    Parameters
    ----------
    sasbdb_id : str
        SASBDB entry identifier (e.g., 'SASDBA2', 'SASDBW5'). Get from SASBDB_search_...
    file_type : str
        Type of files to retrieve: 'scattering' (DAT), 'distance_distribution' (P(r) ...
    stream_callback : Callable, optional
        Callback for streaming output
    use_cache : bool, default False
        Enable caching
    validate : bool, default True
        Validate parameters

    Returns
    -------
    Optional[dict[str, Any]]
    """
    # Handle mutable defaults to avoid B006 linting error

    return get_shared_client().run_one_function(
        {
            "name": "SASBDB_download_data",
            "arguments": {"sasbdb_id": sasbdb_id, "file_type": file_type},
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["SASBDB_download_data"]
