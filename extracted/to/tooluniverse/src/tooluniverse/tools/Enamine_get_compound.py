"""
Enamine_get_compound

Get compound details by Enamine ID. Returns structure, availability, pricing, and ordering inform...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def Enamine_get_compound(
    operation: str,
    enamine_id: str,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Get compound details by Enamine ID. Returns structure, availability, pricing, and ordering inform...

    Parameters
    ----------
    operation : str

    enamine_id : str
        Enamine compound ID (e.g., Z1234567890)
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
            "name": "Enamine_get_compound",
            "arguments": {"operation": operation, "enamine_id": enamine_id},
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["Enamine_get_compound"]
