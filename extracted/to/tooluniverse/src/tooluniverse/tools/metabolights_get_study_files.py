"""
metabolights_get_study_files

Get list of files associated with a MetaboLights study. Returns file metadata including file name...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def metabolights_get_study_files(
    study_id: str,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Get list of files associated with a MetaboLights study. Returns file metadata including file name...

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
        {"name": "metabolights_get_study_files", "arguments": {"study_id": study_id}},
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["metabolights_get_study_files"]
