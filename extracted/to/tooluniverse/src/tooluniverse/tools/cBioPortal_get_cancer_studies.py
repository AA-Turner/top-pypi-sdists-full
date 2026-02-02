"""
cBioPortal_get_cancer_studies

Get list of cancer studies from cBioPortal
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def cBioPortal_get_cancer_studies(
    limit: Optional[int] = 20,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> list[Any]:
    """
    Get list of cancer studies from cBioPortal

    Parameters
    ----------
    limit : int
        Number of studies to return
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
        {"name": "cBioPortal_get_cancer_studies", "arguments": {"limit": limit}},
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["cBioPortal_get_cancer_studies"]
