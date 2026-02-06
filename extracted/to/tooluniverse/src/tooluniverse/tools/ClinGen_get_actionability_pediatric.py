"""
ClinGen_get_actionability_pediatric

Get ClinGen clinical actionability curations for pediatric context. Returns genes with actionable...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def ClinGen_get_actionability_pediatric(
    gene: Optional[str] = None,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Get ClinGen clinical actionability curations for pediatric context. Returns genes with actionable...

    Parameters
    ----------
    gene : str
        Optional: Filter by gene symbol
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
        {"name": "ClinGen_get_actionability_pediatric", "arguments": {"gene": gene}},
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["ClinGen_get_actionability_pediatric"]
