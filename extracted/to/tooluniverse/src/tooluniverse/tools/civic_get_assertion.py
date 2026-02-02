"""
civic_get_assertion

Get detailed information about a specific assertion in CIViC database by assertion ID. Assertions...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def civic_get_assertion(
    assertion_id: int,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Get detailed information about a specific assertion in CIViC database by assertion ID. Assertions...

    Parameters
    ----------
    assertion_id : int
        CIViC assertion ID (e.g., 101)
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
        {"name": "civic_get_assertion", "arguments": {"assertion_id": assertion_id}},
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["civic_get_assertion"]
