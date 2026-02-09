"""
DailyMed_parse_adverse_reactions

Parse adverse reactions section from SPL XML into structured table format. Returns AE frequencies...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def DailyMed_parse_adverse_reactions(
    operation: str,
    setid: str,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Parse adverse reactions section from SPL XML into structured table format. Returns AE frequencies...

    Parameters
    ----------
    operation : str
        Operation type (fixed)
    setid : str
        SPL Set ID to parse
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
            "name": "DailyMed_parse_adverse_reactions",
            "arguments": {"operation": operation, "setid": setid},
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["DailyMed_parse_adverse_reactions"]
