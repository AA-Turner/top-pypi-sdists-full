"""
BLAST_protein_search

Search protein sequences using NCBI BLAST blastp against protein databases
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def BLAST_protein_search(
    sequence: str,
    database: Optional[str] = "nr",
    expect: Optional[float] = 10.0,
    hitlist_size: Optional[int] = 50,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Search protein sequences using NCBI BLAST blastp against protein databases

    Parameters
    ----------
    sequence : str
        Protein sequence to search
    database : str
        Database (nr, swissprot, etc.)
    expect : float

    hitlist_size : int

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
        {
            "name": "BLAST_protein_search",
            "arguments": {
                "sequence": sequence,
                "database": database,
                "expect": expect,
                "hitlist_size": hitlist_size,
            },
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["BLAST_protein_search"]
