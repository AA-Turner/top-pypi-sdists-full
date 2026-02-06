"""
DepMap_search_cell_lines

Search cancer cell lines by name. Returns matching cell lines with IDs and cancer types. Use for ...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def DepMap_search_cell_lines(
    query: str,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Search cancer cell lines by name. Returns matching cell lines with IDs and cancer types. Use for ...

    Parameters
    ----------
    query : str
        Search query (cell line name like 'A549', 'MCF7')
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
        {"name": "DepMap_search_cell_lines", "arguments": {"query": query}},
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["DepMap_search_cell_lines"]
