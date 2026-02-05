"""
GTEx_get_tissue_sites

Get all available GTEx tissue sites with metadata. Returns tissue IDs, names, sample counts, eGen...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def GTEx_get_tissue_sites(
    operation: str,
    dataset_id: Optional[str] = "gtex_v8",
    page: Optional[int] = 0,
    items_per_page: Optional[int] = 250,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> list[Any]:
    """
    Get all available GTEx tissue sites with metadata. Returns tissue IDs, names, sample counts, eGen...

    Parameters
    ----------
    operation : str
        Operation type
    dataset_id : str
        GTEx dataset version
    page : int
        Page number
    items_per_page : int
        Results per page
    stream_callback : Callable, optional
        Callback for streaming output
    use_cache : bool, default False
        Enable caching
    validate : bool, default True
        Validate parameters

    Returns
    -------
    list[Any]
    """
    # Handle mutable defaults to avoid B006 linting error

    return get_shared_client().run_one_function(
        {
            "name": "GTEx_get_tissue_sites",
            "arguments": {
                "operation": operation,
                "dataset_id": dataset_id,
                "page": page,
                "items_per_page": items_per_page,
            },
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["GTEx_get_tissue_sites"]
