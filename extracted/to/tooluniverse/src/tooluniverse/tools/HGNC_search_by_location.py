"""
HGNC_search_by_location

Search HGNC for genes at a specific chromosomal location. Returns all genes mapped to that cytoge...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def HGNC_search_by_location(
    location: str,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> Any:
    """
    Search HGNC for genes at a specific chromosomal location. Returns all genes mapped to that cytoge...

    Parameters
    ----------
    location : str
        Cytogenetic band location. Examples: '17p13.1' (TP53 region), '17q21.31' (BRC...
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
        {"name": "HGNC_search_by_location", "arguments": {"location": location}},
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["HGNC_search_by_location"]
