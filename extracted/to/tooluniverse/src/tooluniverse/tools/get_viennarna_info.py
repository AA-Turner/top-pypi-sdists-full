"""
get_viennarna_info

Get comprehensive information about ViennaRNA – RNA structure prediction and analysis
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def get_viennarna_info(
    include_examples: bool,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Get comprehensive information about ViennaRNA – RNA structure prediction and analysis

    Parameters
    ----------
    include_examples : bool
        Whether to include usage examples and quick start guide
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
            "name": "get_viennarna_info",
            "arguments": {"include_examples": include_examples},
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["get_viennarna_info"]
