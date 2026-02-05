"""
ensembl_get_taxonomy

Get taxonomic classification for a species. Returns complete lineage from kingdom to species leve...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def ensembl_get_taxonomy(
    id: str,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> list[Any]:
    """
    Get taxonomic classification for a species. Returns complete lineage from kingdom to species leve...

    Parameters
    ----------
    id : str
        NCBI Taxonomy ID (e.g., '9606' for human, '10090' for mouse) or species name ...
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
        {"name": "ensembl_get_taxonomy", "arguments": {"id": id}},
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["ensembl_get_taxonomy"]
