"""
HPO_get_term

Get detailed information about a Human Phenotype Ontology (HPO) term by its ID. HPO provides stan...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def HPO_get_term(
    term_id: str,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> Any:
    """
    Get detailed information about a Human Phenotype Ontology (HPO) term by its ID. HPO provides stan...

    Parameters
    ----------
    term_id : str
        HPO term identifier. Must start with 'HP:' followed by 7 digits. Examples: 'H...
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
        {"name": "HPO_get_term", "arguments": {"term_id": term_id}},
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["HPO_get_term"]
