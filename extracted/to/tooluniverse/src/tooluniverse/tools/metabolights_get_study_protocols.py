"""
metabolights_get_study_protocols

Get experimental protocols used in a MetaboLights study. Returns detailed protocol information in...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def metabolights_get_study_protocols(
    study_id: str,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Get experimental protocols used in a MetaboLights study. Returns detailed protocol information in...

    Parameters
    ----------
    study_id : str
        MetaboLights study ID (e.g., 'MTBLS1'). Use metabolights_list_studies or meta...
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
            "name": "metabolights_get_study_protocols",
            "arguments": {"study_id": study_id},
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["metabolights_get_study_protocols"]
