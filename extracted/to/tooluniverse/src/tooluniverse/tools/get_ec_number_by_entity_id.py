"""
get_ec_number_by_entity_id

Retrieve the Enzyme Commission (EC) number(s) for an entity.
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def get_ec_number_by_entity_id(
    entity_id: str,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Retrieve the Enzyme Commission (EC) number(s) for an entity.

    Parameters
    ----------
    entity_id : str
        Polymer entity ID (e.g., '1A8M_1')
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
        {"name": "get_ec_number_by_entity_id", "arguments": {"entity_id": entity_id}},
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["get_ec_number_by_entity_id"]
