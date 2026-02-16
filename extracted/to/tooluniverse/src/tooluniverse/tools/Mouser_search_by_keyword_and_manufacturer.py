"""
Mouser_search_by_keyword_and_manufacturer

Search Mouser Electronics by keyword filtered to a specific manufacturer. Useful when you want co...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def Mouser_search_by_keyword_and_manufacturer(
    keyword: str,
    manufacturer: str,
    records: Optional[int | Any] = None,
    starting_record: Optional[int | Any] = None,
    search_options: Optional[str | Any] = None,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> Any:
    """
    Search Mouser Electronics by keyword filtered to a specific manufacturer. Useful when you want co...

    Parameters
    ----------
    keyword : str
        Search keyword for component type or description. Examples: 'microcontroller'...
    manufacturer : str
        Manufacturer name to filter results. Examples: 'STMicroelectronics', 'Texas I...
    records : int | Any
        Maximum number of results (1-50). Default is 10.
    starting_record : int | Any
        Starting index for pagination. Default is 0.
    search_options : str | Any
        Filter: '' (none), 'InStock', 'RoHS', 'RoHSAndInStock'. Default is ''.
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
            "name": "Mouser_search_by_keyword_and_manufacturer",
            "arguments": {
                "keyword": keyword,
                "manufacturer": manufacturer,
                "records": records,
                "starting_record": starting_record,
                "search_options": search_options,
            },
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["Mouser_search_by_keyword_and_manufacturer"]
