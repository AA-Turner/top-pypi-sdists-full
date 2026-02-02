"""
PharmGKB_search_drugs

Search for drugs in PharmGKB by name or PharmGKB ID. Returns drug name, ID, and basic metadata.
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def PharmGKB_search_drugs(
    query: str,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Search for drugs in PharmGKB by name or PharmGKB ID. Returns drug name, ID, and basic metadata.

    Parameters
    ----------
    query : str
        Drug name or PharmGKB Chemical ID (e.g., 'warfarin', 'PA452637').
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
        {"name": "PharmGKB_search_drugs", "arguments": {"query": query}},
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["PharmGKB_search_drugs"]
