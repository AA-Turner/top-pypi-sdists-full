"""
ITIS_search_by_scientific_name

Search the ITIS (Integrated Taxonomic Information System) database by scientific name. ITIS is th...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def ITIS_search_by_scientific_name(
    scientific_name: str,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> Any:
    """
    Search the ITIS (Integrated Taxonomic Information System) database by scientific name. ITIS is th...

    Parameters
    ----------
    scientific_name : str
        Scientific name to search for (genus, species, or binomial). Examples: 'Homo ...
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
            "name": "ITIS_search_by_scientific_name",
            "arguments": {"scientific_name": scientific_name},
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["ITIS_search_by_scientific_name"]
