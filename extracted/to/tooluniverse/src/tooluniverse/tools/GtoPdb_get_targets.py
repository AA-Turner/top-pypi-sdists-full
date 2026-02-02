"""
GtoPdb_get_targets

Search the IUPHAR/BPS Guide to Pharmacology (GtoPdb) for pharmacological targets including protei...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def GtoPdb_get_targets(
    target_type: Optional[str] = "protein",
    limit: Optional[int] = 20,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Search the IUPHAR/BPS Guide to Pharmacology (GtoPdb) for pharmacological targets including protei...

    Parameters
    ----------
    target_type : str
        Type of pharmacological target. Examples: 'protein', 'receptor', 'enzyme', 'i...
    limit : int
        Maximum number of targets to return (default: 20, max: 1000)
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
            "name": "GtoPdb_get_targets",
            "arguments": {"target_type": target_type, "limit": limit},
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["GtoPdb_get_targets"]
