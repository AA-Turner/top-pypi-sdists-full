"""
ITIS_search_by_common_name

Search the ITIS (Integrated Taxonomic Information System) database by common/vernacular name. Ret...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def ITIS_search_by_common_name(
    common_name: str,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> Any:
    """
    Search the ITIS (Integrated Taxonomic Information System) database by common/vernacular name. Ret...

    Parameters
    ----------
    common_name : str
        Common or vernacular name to search for. Examples: 'bald eagle', 'chimpanzee'...
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
            "name": "ITIS_search_by_common_name",
            "arguments": {"common_name": common_name},
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["ITIS_search_by_common_name"]
