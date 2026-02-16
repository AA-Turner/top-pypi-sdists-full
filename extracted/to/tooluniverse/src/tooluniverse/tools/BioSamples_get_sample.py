"""
BioSamples_get_sample

Get detailed metadata for a specific biological sample from the EBI BioSamples database by access...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def BioSamples_get_sample(
    accession: str,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> Any:
    """
    Get detailed metadata for a specific biological sample from the EBI BioSamples database by access...

    Parameters
    ----------
    accession : str
        BioSamples accession. Formats: SAMEA* (EBI), SAMN* (NCBI), SAMD* (DDBJ). Exam...
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
        {"name": "BioSamples_get_sample", "arguments": {"accession": accession}},
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["BioSamples_get_sample"]
