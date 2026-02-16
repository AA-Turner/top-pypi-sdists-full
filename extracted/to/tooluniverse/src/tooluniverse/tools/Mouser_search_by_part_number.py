"""
Mouser_search_by_part_number

Search Mouser Electronics by exact or partial manufacturer part number (MPN). More precise than k...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def Mouser_search_by_part_number(
    part_number: str,
    search_option: Optional[str | Any] = None,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> Any:
    """
    Search Mouser Electronics by exact or partial manufacturer part number (MPN). More precise than k...

    Parameters
    ----------
    part_number : str
        Manufacturer part number (MPN) or Mouser part number to search. Examples: 'ST...
    search_option : str | Any
        Part number matching mode. Valid values: '' (default - any match), 'Exact' (e...
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
            "name": "Mouser_search_by_part_number",
            "arguments": {"part_number": part_number, "search_option": search_option},
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["Mouser_search_by_part_number"]
