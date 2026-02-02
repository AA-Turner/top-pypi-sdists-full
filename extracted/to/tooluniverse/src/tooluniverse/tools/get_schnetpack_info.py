"""
get_schnetpack_info

Get comprehensive information about SchNetPack – a deep-learning toolbox for molecules and materi...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def get_schnetpack_info(
    include_examples: bool,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Get comprehensive information about SchNetPack – a deep-learning toolbox for molecules and materi...

    Parameters
    ----------
    include_examples : bool
        Whether to include usage examples and a quick-start guide
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
            "name": "get_schnetpack_info",
            "arguments": {"include_examples": include_examples},
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["get_schnetpack_info"]
