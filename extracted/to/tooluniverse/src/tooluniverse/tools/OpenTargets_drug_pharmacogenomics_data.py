"""
OpenTargets_drug_pharmacogenomics_data

Retrieve pharmacogenomics data for a specific drug, including evidence levels and genotype annota...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def OpenTargets_drug_pharmacogenomics_data(
    chemblId: str,
    page: Optional[dict[str, Any]] = None,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Retrieve pharmacogenomics data for a specific drug, including evidence levels and genotype annota...

    Parameters
    ----------
    chemblId : str
        The ChEMBL ID of the drug.
    page : dict[str, Any]
        Pagination options.
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
            "name": "OpenTargets_drug_pharmacogenomics_data",
            "arguments": {"chemblId": chemblId, "page": page},
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["OpenTargets_drug_pharmacogenomics_data"]
