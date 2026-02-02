"""
InterPro_search_domains

Search InterPro database for protein domains and families by name or accession. Returns matching ...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def InterPro_search_domains(
    query: str,
    size: Optional[int] = 20,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Search InterPro database for protein domains and families by name or accession. Returns matching ...

    Parameters
    ----------
    query : str
        Domain name, accession, or search term (e.g., 'kinase', 'IPR000719')
    size : int
        Number of results to return (default: 20, max: 100)
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
            "name": "InterPro_search_domains",
            "arguments": {"query": query, "size": size},
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["InterPro_search_domains"]
