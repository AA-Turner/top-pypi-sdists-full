"""
ComplexPortal_search_complexes

Search for curated protein complexes by gene/protein name from the EBI Complex Portal (includes C...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def ComplexPortal_search_complexes(
    query: str,
    species: Optional[str] = "9606",
    number: Optional[int] = 25,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Search for curated protein complexes by gene/protein name from the EBI Complex Portal (includes C...

    Parameters
    ----------
    query : str
        Gene symbol, protein name, or complex name to search (e.g., 'WDR7', 'RAVE com...
    species : str
        NCBI taxonomy ID to filter by species (default: '9606' for human). Use '10090...
    number : int
        Maximum complexes to return (default: 25)
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
            "name": "ComplexPortal_search_complexes",
            "arguments": {"query": query, "species": species, "number": number},
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["ComplexPortal_search_complexes"]
