"""
GTEx_get_dataset_info

Get GTEx dataset metadata and version information. Returns dataset details including GENCODE vers...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def GTEx_get_dataset_info(
    operation: str,
    dataset_id: Optional[str] = None,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> list[Any]:
    """
    Get GTEx dataset metadata and version information. Returns dataset details including GENCODE vers...

    Parameters
    ----------
    operation : str
        Operation type
    dataset_id : str
        Optional: Specific dataset ID. Omit to get all datasets
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
            "name": "GTEx_get_dataset_info",
            "arguments": {"operation": operation, "dataset_id": dataset_id},
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["GTEx_get_dataset_info"]
