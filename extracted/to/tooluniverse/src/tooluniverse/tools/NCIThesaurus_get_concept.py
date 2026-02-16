"""
NCIThesaurus_get_concept

Get detailed information about an NCI Thesaurus concept by its code. Returns the concept name, de...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def NCIThesaurus_get_concept(
    code: str,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> Any:
    """
    Get detailed information about an NCI Thesaurus concept by its code. Returns the concept name, de...

    Parameters
    ----------
    code : str
        NCI Thesaurus concept code. Examples: 'C3224' (Melanoma), 'C3262' (Neoplasm),...
    stream_callback : Callable, optional
        Callback for streaming output
    use_cache : bool, default False
        Enable caching
    validate : bool, default True
        Validate parameters

    Returns
    -------
    Any
    """
    # Handle mutable defaults to avoid B006 linting error

    return get_shared_client().run_one_function(
        {"name": "NCIThesaurus_get_concept", "arguments": {"code": code}},
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["NCIThesaurus_get_concept"]
