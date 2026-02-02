"""
ChEMBL_get_compound_record_activities

Get all activities for a compound record by compound record ID. Returns bioactivity measurements ...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def ChEMBL_get_compound_record_activities(
    compound_record_id__exact: str,
    limit: Optional[int] = 20,
    offset: Optional[int] = 0,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Get all activities for a compound record by compound record ID. Returns bioactivity measurements ...

    Parameters
    ----------
    compound_record_id__exact : str
        ChEMBL compound record ID. To find a compound record ID, use ChEMBL_get_compo...
    limit : int

    offset : int

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
            "name": "ChEMBL_get_compound_record_activities",
            "arguments": {
                "compound_record_id__exact": compound_record_id__exact,
                "limit": limit,
                "offset": offset,
            },
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["ChEMBL_get_compound_record_activities"]
