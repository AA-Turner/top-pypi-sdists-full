"""
JLCSearch_search_components

Full-text search across all electronic components available from JLCPCB/LCSC. Searches by manufac...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def JLCSearch_search_components(
    query: str,
    limit: Optional[int | Any] = None,
    package: Optional[str | Any] = None,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> Any:
    """
    Full-text search across all electronic components available from JLCPCB/LCSC. Searches by manufac...

    Parameters
    ----------
    query : str
        Search query - manufacturer part number, IC name, or keyword. Examples: 'LM35...
    limit : int | Any
        Maximum number of results to return. Default is 100.
    package : str | Any
        Filter by package type. Examples: 'SOIC-8', 'TSSOP-20', 'QFP-48', 'SOP-8', 'D...
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
            "name": "JLCSearch_search_components",
            "arguments": {"query": query, "limit": limit, "package": package},
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["JLCSearch_search_components"]
