"""
pc_search_pathways

Searches for biological pathways in Pathway Commons (PC2). Use this tool to find pathways related...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def pc_search_pathways(
    action: str,
    keyword: str,
    datasource: Optional[str] = None,
    limit: Optional[int] = 10,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Searches for biological pathways in Pathway Commons (PC2). Use this tool to find pathways related...

    Parameters
    ----------
    action : str
        The specific action to perform. Must be set to 'search_pathways'.
    keyword : str
        The search keyword to identify pathways. Examples include specific genes ('p5...
    datasource : str
        Filter results by the original data source (e.g., 'reactome', 'kegg', 'panthe...
    limit : int
        The maximum number of pathway results to return. The default is 10.
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
            "name": "pc_search_pathways",
            "arguments": {
                "action": action,
                "keyword": keyword,
                "datasource": datasource,
                "limit": limit,
            },
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["pc_search_pathways"]
