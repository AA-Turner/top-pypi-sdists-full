"""
get_tool_info

Get tool information with configurable detail level. Supports single tool (string) or multiple to...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def get_tool_info(
    tool_names: str | list[str],
    detail_level: Optional[str] = "full",
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Get tool information with configurable detail level. Supports single tool (string) or multiple to...

    Parameters
    ----------
    tool_names : str | list[str]
        Single tool name (string) or list of tool names
    detail_level : str
        Detail level: 'description' returns only the description field (complete, not...
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
            "name": "get_tool_info",
            "arguments": {"tool_names": tool_names, "detail_level": detail_level},
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["get_tool_info"]
