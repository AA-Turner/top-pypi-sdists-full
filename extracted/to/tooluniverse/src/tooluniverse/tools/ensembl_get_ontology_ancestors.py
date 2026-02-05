"""
ensembl_get_ontology_ancestors

Get ancestor terms for a GO (Gene Ontology) term. Returns parent terms up the ontology hierarchy ...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def ensembl_get_ontology_ancestors(
    id: str,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> list[Any]:
    """
    Get ancestor terms for a GO (Gene Ontology) term. Returns parent terms up the ontology hierarchy ...

    Parameters
    ----------
    id : str
        GO term ID (e.g., 'GO:0005737' for cytoplasm)
    stream_callback : Callable, optional
        Callback for streaming output
    use_cache : bool, default False
        Enable caching
    validate : bool, default True
        Validate parameters

    Returns
    -------
    list[Any]
    """
    # Handle mutable defaults to avoid B006 linting error

    return get_shared_client().run_one_function(
        {"name": "ensembl_get_ontology_ancestors", "arguments": {"id": id}},
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["ensembl_get_ontology_ancestors"]
