"""
GPCRdb_get_mutations

Get mutation data for a GPCR from GPCRdb. Returns mutation positions, effects on ligand binding a...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def GPCRdb_get_mutations(
    operation: str,
    protein: str,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Get mutation data for a GPCR from GPCRdb. Returns mutation positions, effects on ligand binding a...

    Parameters
    ----------
    operation : str
        Operation type (fixed: get_mutations)
    protein : str
        Protein entry name (e.g., adrb2_human)
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
            "name": "GPCRdb_get_mutations",
            "arguments": {"operation": operation, "protein": protein},
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["GPCRdb_get_mutations"]
