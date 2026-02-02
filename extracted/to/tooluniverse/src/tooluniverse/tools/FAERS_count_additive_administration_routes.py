"""
FAERS_count_additive_administration_routes

Enumerate and count administration routes for adverse events across specified medicinal products....
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def FAERS_count_additive_administration_routes(
    medicinalproducts: list[str],
    serious: Optional[str] = None,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> list[Any]:
    """
    Enumerate and count administration routes for adverse events across specified medicinal products....

    Parameters
    ----------
    medicinalproducts : list[str]
        Array of medicinal product names.
    serious : str
        Optional: Filter by event seriousness. Omit this parameter if you don't want ...
    stream_callback : Callable, optional
        Callback for streaming output
    use_cache : bool, default False
        Enable caching
    validate : bool, default True
        Validate parameters

    Returns
    -------
    list[Any]
    """
    # Handle mutable defaults to avoid B006 linting error

    return get_shared_client().run_one_function(
        {
            "name": "FAERS_count_additive_administration_routes",
            "arguments": {"medicinalproducts": medicinalproducts, "serious": serious},
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["FAERS_count_additive_administration_routes"]
