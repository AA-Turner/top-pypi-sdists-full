"""
chembl_disease_target_score

Extract disease-target association scores specifically from ChEMBL database. ChEMBL provides bioa...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def chembl_disease_target_score(
    efoId: str,
    pageSize: int,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Extract disease-target association scores specifically from ChEMBL database. ChEMBL provides bioa...

    Parameters
    ----------
    efoId : str
        The EFO (Experimental Factor Ontology) ID of the disease, e.g., 'EFO_0000339'...
    pageSize : int
        Number of results per page (default: 100, max: 100)
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
            "name": "chembl_disease_target_score",
            "arguments": {"efoId": efoId, "pageSize": pageSize},
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["chembl_disease_target_score"]
