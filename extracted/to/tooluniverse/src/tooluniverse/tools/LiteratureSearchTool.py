"""
LiteratureSearchTool

Comprehensive literature search and summary tool that searches multiple databases (EuropePMC, Ope...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def LiteratureSearchTool(
    research_topic: str,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Comprehensive literature search and summary tool that searches multiple databases (EuropePMC, Ope...

    Parameters
    ----------
    research_topic : str
        The research topic or query to search for in the literature
    stream_callback : Callable, optional
        Callback for streaming output
    use_cache : bool, default False
        Enable caching
    validate : bool, default True
        Validate parameters

    Returns
    -------
    dict[str, Any]
    """
    # Handle mutable defaults to avoid B006 linting error

    return get_shared_client().run_one_function(
        {
            "name": "LiteratureSearchTool",
            "arguments": {"research_topic": research_topic},
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["LiteratureSearchTool"]
