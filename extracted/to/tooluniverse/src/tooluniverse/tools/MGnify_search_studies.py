"""
MGnify_search_studies

Search MGnify metagenomics/microbiome studies by biome/keyword. Use to discover study accessions ...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def MGnify_search_studies(
    biome: Optional[str] = None,
    search: Optional[str] = None,
    size: Optional[int] = 10,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Search MGnify metagenomics/microbiome studies by biome/keyword. Use to discover study accessions ...

    Parameters
    ----------
    biome : str
        Biome identifier (e.g., 'root:Host-associated').
    search : str
        Keyword to search in study titles/descriptions.
    size : int
        Number of records per page (1–100).
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
            "name": "MGnify_search_studies",
            "arguments": {"biome": biome, "search": search, "size": size},
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["MGnify_search_studies"]
