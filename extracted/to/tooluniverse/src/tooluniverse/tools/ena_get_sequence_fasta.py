"""
ena_get_sequence_fasta

Get nucleotide sequence in FASTA format from ENA by accession number. Supports EMBL/GenBank acces...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def ena_get_sequence_fasta(
    accession: str,
    download: Optional[bool] = False,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> str:
    """
    Get nucleotide sequence in FASTA format from ENA by accession number. Supports EMBL/GenBank acces...

    Parameters
    ----------
    accession : str
        EMBL/GenBank accession number. Supported formats: U#####, M#####, AJ######, A...
    download : bool
        Force download instead of inline display (default: false)
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
        {
            "name": "ena_get_sequence_fasta",
            "arguments": {"accession": accession, "download": download},
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["ena_get_sequence_fasta"]
