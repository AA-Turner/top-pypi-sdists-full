"""
Zenodo_list_licenses

List available licenses that can be applied to Zenodo uploads. Returns license metadata including...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def Zenodo_list_licenses(
    query: Optional[str] = None,
    limit: Optional[int] = 25,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    List available licenses that can be applied to Zenodo uploads. Returns license metadata including...

    Parameters
    ----------
    query : str
        Optional search query to filter licenses by name or keyword (e.g., 'creative ...
    limit : int
        Maximum number of licenses to return (default: 25, max: 100).
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
        {"name": "Zenodo_list_licenses", "arguments": {"query": query, "limit": limit}},
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["Zenodo_list_licenses"]
