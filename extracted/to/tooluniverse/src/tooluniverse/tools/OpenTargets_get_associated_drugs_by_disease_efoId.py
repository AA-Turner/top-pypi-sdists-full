"""
OpenTargets_get_associated_drugs_by_disease_efoId

Retrieve known drugs associated with a specific disease by disease efoId.
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def OpenTargets_get_associated_drugs_by_disease_efoId(
    efoId: str,
    size: int,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Retrieve known drugs associated with a specific disease by disease efoId.

    Parameters
    ----------
    efoId : str
        The EFO ID of the disease.
    size : int
        Number of entries to fetch, recomanding a large number to avoid missing drugs.
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
            "name": "OpenTargets_get_associated_drugs_by_disease_efoId",
            "arguments": {"efoId": efoId, "size": size},
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["OpenTargets_get_associated_drugs_by_disease_efoId"]
