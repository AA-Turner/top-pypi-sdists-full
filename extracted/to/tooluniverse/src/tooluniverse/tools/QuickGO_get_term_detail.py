"""
QuickGO_get_term_detail

Get detailed information about a specific Gene Ontology (GO) term from the EBI QuickGO browser. R...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def QuickGO_get_term_detail(
    go_id: str,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> Any:
    """
    Get detailed information about a specific Gene Ontology (GO) term from the EBI QuickGO browser. R...

    Parameters
    ----------
    go_id : str
        Gene Ontology term accession. Examples: 'GO:0006915' (apoptotic process), 'GO...
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
        {"name": "QuickGO_get_term_detail", "arguments": {"go_id": go_id}},
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["QuickGO_get_term_detail"]
