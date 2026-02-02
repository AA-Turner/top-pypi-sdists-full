"""
dbfetch_list_formats

List available output formats for a specific database. Returns supported formats for the database.
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def dbfetch_list_formats(
    db: str,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    List available output formats for a specific database. Returns supported formats for the database.

    Parameters
    ----------
    db : str
        Database name
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
        {"name": "dbfetch_list_formats", "arguments": {"db": db}},
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["dbfetch_list_formats"]
