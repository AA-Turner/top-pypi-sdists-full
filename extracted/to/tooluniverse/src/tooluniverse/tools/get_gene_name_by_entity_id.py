"""
get_gene_name_by_entity_id

Retrieve gene name(s) associated with a polymer entity.
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def get_gene_name_by_entity_id(
    entity_id: str,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Retrieve gene name(s) associated with a polymer entity.

    Parameters
    ----------
    entity_id : str
        Entity ID like '1A8M_1'
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
        {"name": "get_gene_name_by_entity_id", "arguments": {"entity_id": entity_id}},
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["get_gene_name_by_entity_id"]
