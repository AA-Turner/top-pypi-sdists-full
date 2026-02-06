"""
eMolecules_get_compound

Get compound details by eMolecules ID. Returns structure, vendors, pricing, and availability info...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def eMolecules_get_compound(
    operation: str,
    emol_id: str,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Get compound details by eMolecules ID. Returns structure, vendors, pricing, and availability info...

    Parameters
    ----------
    operation : str

    emol_id : str
        eMolecules compound/vendor ID
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
            "name": "eMolecules_get_compound",
            "arguments": {"operation": operation, "emol_id": emol_id},
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["eMolecules_get_compound"]
