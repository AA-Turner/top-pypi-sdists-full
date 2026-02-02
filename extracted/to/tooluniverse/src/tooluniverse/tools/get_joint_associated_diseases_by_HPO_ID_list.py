"""
get_joint_associated_diseases_by_HPO_ID_list

Retrieve diseases associated with a list of phenotypes or symptoms by a list of HPO IDs.
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def get_joint_associated_diseases_by_HPO_ID_list(
    HPO_ID_list: list[str],
    limit: Optional[int] = None,
    offset: Optional[int] = None,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Retrieve diseases associated with a list of phenotypes or symptoms by a list of HPO IDs.

    Parameters
    ----------
    HPO_ID_list : list[str]
        List of phenotypes or symptoms
    limit : int
        Number of entries to fetch.
    offset : int
        Number of initial entries to skip.
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
            "name": "get_joint_associated_diseases_by_HPO_ID_list",
            "arguments": {"HPO_ID_list": HPO_ID_list, "limit": limit, "offset": offset},
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["get_joint_associated_diseases_by_HPO_ID_list"]
