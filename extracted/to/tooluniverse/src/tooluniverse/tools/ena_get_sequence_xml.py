"""
ena_get_sequence_xml

Get metadata in XML format from ENA for Study, Sample, Run, Experiment, Analysis, or Taxon record...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def ena_get_sequence_xml(
    accession: str,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> str:
    """
    Get metadata in XML format from ENA for Study, Sample, Run, Experiment, Analysis, or Taxon record...

    Parameters
    ----------
    accession : str
        ENA metadata record accession. Supported types: Study (ERP*, SRP*, PRJ*), Sam...
    stream_callback : Callable, optional
        Callback for streaming output
    use_cache : bool, default False
        Enable caching
    validate : bool, default True
        Validate parameters

    Returns
    -------
    str
    """
    # Handle mutable defaults to avoid B006 linting error

    return get_shared_client().run_one_function(
        {"name": "ena_get_sequence_xml", "arguments": {"accession": accession}},
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["ena_get_sequence_xml"]
