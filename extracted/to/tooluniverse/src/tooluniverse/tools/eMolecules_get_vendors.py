"""
eMolecules_get_vendors

Get list of chemical suppliers for a compound by SMILES. Returns vendor names, pricing, and avail...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def eMolecules_get_vendors(
    operation: str,
    smiles: str,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Get list of chemical suppliers for a compound by SMILES. Returns vendor names, pricing, and avail...

    Parameters
    ----------
    operation : str

    smiles : str
        SMILES string for the compound
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

    # Strip None values so optional parameters don't trigger schema validation errors
    _args = {
        k: v
        for k, v in {"operation": operation, "smiles": smiles}.items()
        if v is not None
    }
    return get_shared_client().run_one_function(
        {
            "name": "eMolecules_get_vendors",
            "arguments": _args,
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["eMolecules_get_vendors"]
