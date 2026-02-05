"""
biostudies_get_study_files

Get list of files associated with a BioStudies study. Returns file metadata including paths, size...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def biostudies_get_study_files(
    accession: str,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> list[Any]:
    """
    Get list of files associated with a BioStudies study. Returns file metadata including paths, size...

    Parameters
    ----------
    accession : str
        BioStudies accession number
    stream_callback : Callable, optional
        Callback for streaming output
    use_cache : bool, default False
        Enable caching
    validate : bool, default True
        Validate parameters

    Returns
    -------
    list[Any]
    """
    # Handle mutable defaults to avoid B006 linting error

    return get_shared_client().run_one_function(
        {"name": "biostudies_get_study_files", "arguments": {"accession": accession}},
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["biostudies_get_study_files"]
