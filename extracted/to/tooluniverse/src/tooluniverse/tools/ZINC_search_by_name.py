"""
ZINC_search_by_name

Search ZINC for compounds by name. Returns matching ZINC IDs with basic properties. Useful for fi...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def ZINC_search_by_name(
    operation: str,
    name: str,
    max_results: Optional[int] = 20,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Search ZINC for compounds by name. Returns matching ZINC IDs with basic properties. Useful for fi...

    Parameters
    ----------
    operation : str

    name : str
        Compound name or partial name
    max_results : int
        Maximum results (default: 20)
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
            "name": "ZINC_search_by_name",
            "arguments": {
                "operation": operation,
                "name": name,
                "max_results": max_results,
            },
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["ZINC_search_by_name"]
