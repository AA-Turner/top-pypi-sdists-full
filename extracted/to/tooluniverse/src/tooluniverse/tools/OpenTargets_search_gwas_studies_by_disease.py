"""
OpenTargets_search_gwas_studies_by_disease

Search for GWAS studies associated with a disease or trait in Open Targets. Takes disease ontolog...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def OpenTargets_search_gwas_studies_by_disease(
    diseaseIds: list[str],
    enableIndirect: Optional[bool] = True,
    size: Optional[int] = 10,
    index: Optional[int] = 0,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> Any:
    """
    Search for GWAS studies associated with a disease or trait in Open Targets. Takes disease ontolog...

    Parameters
    ----------
    diseaseIds : list[str]
        Disease ontology IDs (e.g., ['MONDO_0005148'] for type 2 diabetes, ['EFO_0000...
    enableIndirect : bool
        Include studies for child disease terms (default true)
    size : int
        Number of results per page (default 10)
    index : int
        Page index for pagination (0-based, default 0)
    stream_callback : Callable, optional
        Callback for streaming output
    use_cache : bool, default False
        Enable caching
    validate : bool, default True
        Validate parameters

    Returns
    -------
    Any
    """
    # Handle mutable defaults to avoid B006 linting error

    return get_shared_client().run_one_function(
        {
            "name": "OpenTargets_search_gwas_studies_by_disease",
            "arguments": {
                "diseaseIds": diseaseIds,
                "enableIndirect": enableIndirect,
                "size": size,
                "index": index,
            },
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["OpenTargets_search_gwas_studies_by_disease"]
