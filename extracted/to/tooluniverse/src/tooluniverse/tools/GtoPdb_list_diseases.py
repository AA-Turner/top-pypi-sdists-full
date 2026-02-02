"""
GtoPdb_list_diseases

Search and list diseases from the Guide to Pharmacology with associated pharmacological targets a...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def GtoPdb_list_diseases(
    name: Optional[str] = None,
    limit: Optional[int] = 20,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Search and list diseases from the Guide to Pharmacology with associated pharmacological targets a...

    Parameters
    ----------
    name : str
        Search diseases by name (partial match). Examples: 'diabetes', 'cancer', 'ast...
    limit : int
        Maximum number of diseases to return (default: 20, max: 1000).
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
        {"name": "GtoPdb_list_diseases", "arguments": {"name": name, "limit": limit}},
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["GtoPdb_list_diseases"]
