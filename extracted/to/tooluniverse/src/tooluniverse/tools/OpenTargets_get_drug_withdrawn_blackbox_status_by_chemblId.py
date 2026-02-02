"""
OpenTargets_get_drug_withdrawn_blackbox_status_by_chemblId

Find withdrawn and black-box warning statuses for a specific drug by chemblId.
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def OpenTargets_get_drug_withdrawn_blackbox_status_by_chemblId(
    chemblId: list[str],
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Find withdrawn and black-box warning statuses for a specific drug by chemblId.

    Parameters
    ----------
    chemblId : list[str]
        The chemblId of a drug.
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
            "name": "OpenTargets_get_drug_withdrawn_blackbox_status_by_chemblId",
            "arguments": {"chemblId": chemblId},
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["OpenTargets_get_drug_withdrawn_blackbox_status_by_chemblId"]
