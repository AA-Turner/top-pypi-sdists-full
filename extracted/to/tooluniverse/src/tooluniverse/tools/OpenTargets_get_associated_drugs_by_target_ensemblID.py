"""
OpenTargets_get_associated_drugs_by_target_ensemblID

Get known drugs and information (e.g. id, name, MoA) associated with a specific target ensemblID,...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def OpenTargets_get_associated_drugs_by_target_ensemblID(
    ensemblId: str,
    size: int,
    cursor: Optional[str] = None,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Get known drugs and information (e.g. id, name, MoA) associated with a specific target ensemblID,...

    Parameters
    ----------
    ensemblId : str
        The Ensembl ID of the target.
    size : int
        Number of entries to fetch.
    cursor : str
        Cursor for pagination.
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
            "name": "OpenTargets_get_associated_drugs_by_target_ensemblID",
            "arguments": {"ensemblId": ensemblId, "size": size, "cursor": cursor},
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["OpenTargets_get_associated_drugs_by_target_ensemblID"]
