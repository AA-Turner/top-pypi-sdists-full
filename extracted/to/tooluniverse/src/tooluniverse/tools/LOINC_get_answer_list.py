"""
LOINC_get_answer_list

Get standardized answer list (permissible values) for a LOINC code. Many LOINC codes have predefi...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def LOINC_get_answer_list(
    loinc_code: str,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Get standardized answer list (permissible values) for a LOINC code. Many LOINC codes have predefi...

    Parameters
    ----------
    loinc_code : str
        LOINC code identifier for which to retrieve answer list (e.g., '883-9' for AB...
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
        {"name": "LOINC_get_answer_list", "arguments": {"loinc_code": loinc_code}},
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["LOINC_get_answer_list"]
