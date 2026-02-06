"""
ZINC_get_substance

Get compound information from ZINC by ID. Returns SMILES, molecular properties, purchasability, a...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def ZINC_get_substance(
    operation: str,
    zinc_id: str,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Get compound information from ZINC by ID. Returns SMILES, molecular properties, purchasability, a...

    Parameters
    ----------
    operation : str

    zinc_id : str
        ZINC ID (e.g., ZINC000000000001)
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
            "name": "ZINC_get_substance",
            "arguments": {"operation": operation, "zinc_id": zinc_id},
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["ZINC_get_substance"]
