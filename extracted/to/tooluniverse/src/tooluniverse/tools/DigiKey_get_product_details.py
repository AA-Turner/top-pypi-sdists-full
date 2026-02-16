"""
DigiKey_get_product_details

Get detailed product information from Digi-Key by part number (Digi-Key PN or manufacturer PN). R...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def DigiKey_get_product_details(
    product_number: str,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> Any:
    """
    Get detailed product information from Digi-Key by part number (Digi-Key PN or manufacturer PN). R...

    Parameters
    ----------
    product_number : str
        Digi-Key part number or manufacturer part number. Examples: 'STM32F103C8T6', ...
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
            "name": "DigiKey_get_product_details",
            "arguments": {"product_number": product_number},
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["DigiKey_get_product_details"]
