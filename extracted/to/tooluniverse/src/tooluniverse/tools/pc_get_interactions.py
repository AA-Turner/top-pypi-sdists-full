"""
pc_get_interactions

Retrieves the interaction network (neighborhood) for a specified list of genes. Returns interacti...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def pc_get_interactions(
    action: str,
    gene_list: list[str],
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Retrieves the interaction network (neighborhood) for a specified list of genes. Returns interacti...

    Parameters
    ----------
    action : str
        The specific action to perform. Must be set to 'get_interaction_graph'.
    gene_list : list[str]
        A list of gene symbols (e.g., ['TP53', 'MDM2']) to query interactions for.
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
            "name": "pc_get_interactions",
            "arguments": {"action": action, "gene_list": gene_list},
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["pc_get_interactions"]
