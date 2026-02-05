"""
NCBI_fetch_accessions

Convert GenBank UIDs to accession numbers (U00096, NC_045512, etc.). Takes UIDs from NCBI_search_...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def NCBI_fetch_accessions(
    operation: str,
    uids: list[str] | str,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> Any:
    """
    Convert GenBank UIDs to accession numbers (U00096, NC_045512, etc.). Takes UIDs from NCBI_search_...

    Parameters
    ----------
    operation : str
        Operation type (fixed: fetch_accession)
    uids : list[str] | str
        GenBank UID(s) from NCBI_search_nucleotide. Can be single UID or array of UIDs.
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
        {
            "name": "NCBI_fetch_accessions",
            "arguments": {"operation": operation, "uids": uids},
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["NCBI_fetch_accessions"]
