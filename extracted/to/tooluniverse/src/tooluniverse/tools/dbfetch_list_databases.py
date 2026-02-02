"""
dbfetch_list_databases

List all available databases in Dbfetch service. Returns list of database names and descriptions.
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def dbfetch_list_databases(
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    List all available databases in Dbfetch service. Returns list of database names and descriptions.

    Parameters
    ----------
    No parameters
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
        {"name": "dbfetch_list_databases", "arguments": {}},
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["dbfetch_list_databases"]
