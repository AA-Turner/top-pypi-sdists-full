"""
ENCODE_get_experiment

Get comprehensive metadata for a specific ENCODE experiment by its accession ID. Returns detailed...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def ENCODE_get_experiment(
    accession: str,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Get comprehensive metadata for a specific ENCODE experiment by its accession ID. Returns detailed...

    Parameters
    ----------
    accession : str
        ENCODE experiment accession identifier (format: ENCSR######, e.g., 'ENCSR000A...
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
        {"name": "ENCODE_get_experiment", "arguments": {"accession": accession}},
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["ENCODE_get_experiment"]
