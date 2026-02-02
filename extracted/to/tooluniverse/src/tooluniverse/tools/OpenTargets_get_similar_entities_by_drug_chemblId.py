"""
OpenTargets_get_similar_entities_by_drug_chemblId

Retrieve similar entities for a given drug chemblId using a model trained with PubMed.
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def OpenTargets_get_similar_entities_by_drug_chemblId(
    chemblId: str,
    threshold: float,
    size: int,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Retrieve similar entities for a given drug chemblId using a model trained with PubMed.

    Parameters
    ----------
    chemblId : str
        The chemblId of the disease.
    threshold : float
        Threshold similarity between 0 and 1. Only results above threshold are returned.
    size : int
        Number of similar entities to fetch.
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
            "name": "OpenTargets_get_similar_entities_by_drug_chemblId",
            "arguments": {"chemblId": chemblId, "threshold": threshold, "size": size},
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["OpenTargets_get_similar_entities_by_drug_chemblId"]
