"""
PRIDE_get_project_files

Get the complete list of data files for a PRIDE Archive project including raw mass spectrometry f...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def PRIDE_get_project_files(
    accession: str,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Get the complete list of data files for a PRIDE Archive project including raw mass spectrometry f...

    Parameters
    ----------
    accession : str
        PRIDE project accession identifier (format: PXD######, e.g., 'PXD000001'). Fi...
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
        {"name": "PRIDE_get_project_files", "arguments": {"accession": accession}},
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["PRIDE_get_project_files"]
