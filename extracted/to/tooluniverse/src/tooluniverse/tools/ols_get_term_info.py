"""
ols_get_term_info

Get detailed information about a specific term in OLS
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def ols_get_term_info(
    operation: str,
    id: str,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Get detailed information about a specific term in OLS

    Parameters
    ----------
    operation : str
        The operation to perform (get_term_info)
    id : str
        The ID or IRI of the term to retrieve
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

    # Strip None values so optional parameters don't trigger schema validation errors
    _args = {
        k: v for k, v in {"operation": operation, "id": id}.items() if v is not None
    }
    return get_shared_client().run_one_function(
        {
            "name": "ols_get_term_info",
            "arguments": _args,
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["ols_get_term_info"]
