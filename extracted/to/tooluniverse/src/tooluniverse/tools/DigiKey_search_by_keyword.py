"""
DigiKey_search_by_keyword

Search Digi-Key Electronics for electronic components by keyword. Returns matching products with ...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def DigiKey_search_by_keyword(
    keywords: str,
    limit: Optional[int | Any] = None,
    offset: Optional[int | Any] = None,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> Any:
    """
    Search Digi-Key Electronics for electronic components by keyword. Returns matching products with ...

    Parameters
    ----------
    keywords : str
        Search keywords - part description, MPN, or component type. Examples: 'STM32F...
    limit : int | Any
        Maximum number of results to return (1-50). Default is 10.
    offset : int | Any
        Starting record offset for pagination. Default is 0.
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
        {
            "name": "DigiKey_search_by_keyword",
            "arguments": {"keywords": keywords, "limit": limit, "offset": offset},
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["DigiKey_search_by_keyword"]
