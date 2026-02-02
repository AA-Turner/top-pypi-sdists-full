"""
UniProt_get_ptm_processing_by_accession

Extract all PTM and processing sites from UniProtKB entry (feature type = MODIFIED RESIDUE or SIG...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def UniProt_get_ptm_processing_by_accession(
    accession: str,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> list[Any]:
    """
    Extract all PTM and processing sites from UniProtKB entry (feature type = MODIFIED RESIDUE or SIG...

    Parameters
    ----------
    accession : str
        UniProtKB accession, e.g., P05067.
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
        {
            "name": "UniProt_get_ptm_processing_by_accession",
            "arguments": {"accession": accession},
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["UniProt_get_ptm_processing_by_accession"]
