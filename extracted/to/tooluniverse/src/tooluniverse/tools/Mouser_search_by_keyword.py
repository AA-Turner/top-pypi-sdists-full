"""
Mouser_search_by_keyword

Search Mouser Electronics for electronic components by keyword. Returns matching parts with prici...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def Mouser_search_by_keyword(
    keyword: str,
    records: Optional[int | Any] = None,
    starting_record: Optional[int | Any] = None,
    search_options: Optional[str | Any] = None,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> Any:
    """
    Search Mouser Electronics for electronic components by keyword. Returns matching parts with prici...

    Parameters
    ----------
    keyword : str
        Search keyword - component type, part number, or description. Examples: 'STM3...
    records : int | Any
        Maximum number of results to return (1-50). Default is 10.
    starting_record : int | Any
        Starting index for pagination. Default is 0. Use with records to page through...
    search_options : str | Any
        Search filter options. Valid values: '' (none), 'InStock' (only in-stock), 'R...
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
            "name": "Mouser_search_by_keyword",
            "arguments": {
                "keyword": keyword,
                "records": records,
                "starting_record": starting_record,
                "search_options": search_options,
            },
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["Mouser_search_by_keyword"]
