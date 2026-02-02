"""
ENCODE_get_file

Get detailed metadata for a specific ENCODE file by its accession ID. Returns comprehensive file ...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def ENCODE_get_file(
    accession: str,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Get detailed metadata for a specific ENCODE file by its accession ID. Returns comprehensive file ...

    Parameters
    ----------
    accession : str
        ENCODE file accession identifier (format: ENCFF######, e.g., 'ENCFF001JXO', '...
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
        {"name": "ENCODE_get_file", "arguments": {"accession": accession}},
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["ENCODE_get_file"]
