"""
intact_get_interactions_by_organism

Get all interactions for a specific organism by taxonomy ID. Uses EBI Search API (IntAct domain) ...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def intact_get_interactions_by_organism(
    taxid: str,
    size: Optional[int] = 25,
    format: Optional[str] = "json",
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Get all interactions for a specific organism by taxonomy ID. Uses EBI Search API (IntAct domain) ...

    Parameters
    ----------
    taxid : str
        NCBI taxonomy ID (e.g., '9606' for human, '10090' for mouse). Find taxonomy I...
    size : int
        Maximum number of results to return (default: 25, max: 100)
    format : str

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
            "name": "intact_get_interactions_by_organism",
            "arguments": {"taxid": taxid, "size": size, "format": format},
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["intact_get_interactions_by_organism"]
