"""
MetaCyc_get_reaction

Get reaction details from MetaCyc by reaction ID. Returns reaction information including substrat...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def MetaCyc_get_reaction(
    operation: str,
    reaction_id: str,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Get reaction details from MetaCyc by reaction ID. Returns reaction information including substrat...

    Parameters
    ----------
    operation : str

    reaction_id : str
        MetaCyc reaction ID (e.g., RXN-14500)
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
            "name": "MetaCyc_get_reaction",
            "arguments": {"operation": operation, "reaction_id": reaction_id},
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["MetaCyc_get_reaction"]
