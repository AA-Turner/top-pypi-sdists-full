"""
DigiKey_get_categories

Get electronic component product categories from Digi-Key. Returns category hierarchy including c...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def DigiKey_get_categories(
    category_id: Optional[int | Any] = None,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> Any:
    """
    Get electronic component product categories from Digi-Key. Returns category hierarchy including c...

    Parameters
    ----------
    category_id : int | Any
        Optional category ID to get details for a specific category. Omit to get top-...
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
        {"name": "DigiKey_get_categories", "arguments": {"category_id": category_id}},
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["DigiKey_get_categories"]
