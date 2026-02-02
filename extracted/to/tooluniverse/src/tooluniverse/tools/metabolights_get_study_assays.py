"""
metabolights_get_study_assays

Get all assays associated with a MetaboLights study. Returns assay metadata including assay types...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def metabolights_get_study_assays(
    study_id: str,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Get all assays associated with a MetaboLights study. Returns assay metadata including assay types...

    Parameters
    ----------
    study_id : str
        MetaboLights study ID
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
        {"name": "metabolights_get_study_assays", "arguments": {"study_id": study_id}},
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["metabolights_get_study_assays"]
