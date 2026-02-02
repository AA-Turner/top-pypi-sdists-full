"""
ena_get_sequence_embl

Get nucleotide sequence in EMBL format from ENA by accession number. Returns EMBL-formatted seque...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def ena_get_sequence_embl(
    accession: str,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Get nucleotide sequence in EMBL format from ENA by accession number. Returns EMBL-formatted seque...

    Parameters
    ----------
    accession : str
        ENA accession number
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
        {"name": "ena_get_sequence_embl", "arguments": {"accession": accession}},
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["ena_get_sequence_embl"]
