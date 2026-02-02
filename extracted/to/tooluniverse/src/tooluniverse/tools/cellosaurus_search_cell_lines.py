"""
cellosaurus_search_cell_lines

Search Cellosaurus cell lines using the /search/cell-line endpoint. Supports Solr query syntax fo...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def cellosaurus_search_cell_lines(
    q: str,
    offset: int,
    size: int,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Search Cellosaurus cell lines using the /search/cell-line endpoint. Supports Solr query syntax fo...

    Parameters
    ----------
    q : str
        Search query. Supports Solr syntax for field-specific searches (e.g., 'id:HeL...
    offset : int
        Number of results to skip (for pagination)
    size : int
        Maximum number of results to return
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
            "name": "cellosaurus_search_cell_lines",
            "arguments": {"q": q, "offset": offset, "size": size},
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["cellosaurus_search_cell_lines"]
