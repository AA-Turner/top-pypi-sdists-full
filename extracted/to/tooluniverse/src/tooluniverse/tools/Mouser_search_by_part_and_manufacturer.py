"""
Mouser_search_by_part_and_manufacturer

Search Mouser Electronics by part number AND manufacturer name for precise matching. Use when a p...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def Mouser_search_by_part_and_manufacturer(
    part_number: str,
    manufacturer: str,
    records: Optional[int | Any] = None,
    starting_record: Optional[int | Any] = None,
    search_option: Optional[str | Any] = None,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> Any:
    """
    Search Mouser Electronics by part number AND manufacturer name for precise matching. Use when a p...

    Parameters
    ----------
    part_number : str
        Manufacturer part number (MPN). Examples: 'LM358', 'NE555', 'STM32F103C8T6'.
    manufacturer : str
        Manufacturer name. Examples: 'Texas Instruments', 'STMicroelectronics', 'Micr...
    records : int | Any
        Maximum number of results (1-50). Default is 10.
    starting_record : int | Any
        Starting index for pagination. Default is 0.
    search_option : str | Any
        Part number matching mode: '' (default), 'Exact', 'BeginsWith'.
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
            "name": "Mouser_search_by_part_and_manufacturer",
            "arguments": {
                "part_number": part_number,
                "manufacturer": manufacturer,
                "records": records,
                "starting_record": starting_record,
                "search_option": search_option,
            },
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["Mouser_search_by_part_and_manufacturer"]
