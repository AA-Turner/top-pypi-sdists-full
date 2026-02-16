"""
LipidMaps_search_by_name

Search for lipids by common abbreviation or name in LIPID MAPS Structure Database. Returns matchi...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def LipidMaps_search_by_name(
    input_value: str,
    output_item: Optional[str] = "all",
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> Any:
    """
    Search for lipids by common abbreviation or name in LIPID MAPS Structure Database. Returns matchi...

    Parameters
    ----------
    input_value : str
        Lipid abbreviation or name (e.g., 'DHA', 'EPA', 'ceramide'). Supports common ...
    output_item : str
        Type of output. Options: 'all', 'name', 'formula', 'exactmass', 'smiles', 'cl...
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
            "name": "LipidMaps_search_by_name",
            "arguments": {"input_value": input_value, "output_item": output_item},
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["LipidMaps_search_by_name"]
