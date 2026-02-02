"""
dbfetch_fetch_entry

Fetch a single database entry by ID from various databases (UniProt, PDB, etc.) in specified form...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def dbfetch_fetch_entry(
    db: str,
    id: str,
    format: Optional[str] = "fasta",
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Fetch a single database entry by ID from various databases (UniProt, PDB, etc.) in specified form...

    Parameters
    ----------
    db : str
        Database name (e.g., 'uniprotkb', 'pdb', 'embl', 'ensembl')
    id : str
        Entry ID (e.g., UniProt accession 'P05067', PDB ID '1A2B')
    format : str
        Output format (e.g., 'fasta', 'xml', 'json', 'txt'). Default: 'fasta'
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
            "name": "dbfetch_fetch_entry",
            "arguments": {"db": db, "id": id, "format": format},
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["dbfetch_fetch_entry"]
