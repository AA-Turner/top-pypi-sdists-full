"""
get_deeppurpose_info

Get comprehensive information about DeepPurpose – deep learning toolkit for drug discovery
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def get_deeppurpose_info(
    info_type: str,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Get comprehensive information about DeepPurpose – deep learning toolkit for drug discovery

    Parameters
    ----------
    info_type : str
        Type of information to retrieve about DeepPurpose
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
        {"name": "get_deeppurpose_info", "arguments": {"info_type": info_type}},
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["get_deeppurpose_info"]
