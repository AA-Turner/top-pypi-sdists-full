"""
NDEx_get_network_summary

Get detailed summary information for a specific biological network in NDEx by its UUID. Returns t...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def NDEx_get_network_summary(
    uuid: str,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> Any:
    """
    Get detailed summary information for a specific biological network in NDEx by its UUID. Returns t...

    Parameters
    ----------
    uuid : str
        NDEx network UUID. Get UUIDs from NDEx_search_networks results. Example: '34e...
    stream_callback : Callable, optional
        Callback for streaming output
    use_cache : bool, default False
        Enable caching
    validate : bool, default True
        Validate parameters

    Returns
    -------
    Any
    """
    # Handle mutable defaults to avoid B006 linting error

    return get_shared_client().run_one_function(
        {"name": "NDEx_get_network_summary", "arguments": {"uuid": uuid}},
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["NDEx_get_network_summary"]
