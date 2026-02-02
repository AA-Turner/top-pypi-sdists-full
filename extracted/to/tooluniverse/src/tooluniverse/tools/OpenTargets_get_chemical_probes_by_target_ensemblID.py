"""
OpenTargets_get_chemical_probes_by_target_ensemblID

Retrieve chemical probes associated with a specific target using its ensemblID.
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def OpenTargets_get_chemical_probes_by_target_ensemblID(
    ensemblId: str,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Retrieve chemical probes associated with a specific target using its ensemblID.

    Parameters
    ----------
    ensemblId : str
        The Ensembl ID of the target for which to retrieve chemical probes.
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
            "name": "OpenTargets_get_chemical_probes_by_target_ensemblID",
            "arguments": {"ensemblId": ensemblId},
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["OpenTargets_get_chemical_probes_by_target_ensemblID"]
