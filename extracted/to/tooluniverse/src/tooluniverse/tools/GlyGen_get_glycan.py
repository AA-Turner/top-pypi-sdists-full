"""
GlyGen_get_glycan

Get detailed glycan structure information from GlyGen by GlyTouCan accession. Returns mass, monos...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def GlyGen_get_glycan(
    glytoucan_ac: str,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> Any:
    """
    Get detailed glycan structure information from GlyGen by GlyTouCan accession. Returns mass, monos...

    Parameters
    ----------
    glytoucan_ac : str
        GlyTouCan accession ID for the glycan. Examples: 'G17689DH', 'G62765YT', 'G00...
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
        {"name": "GlyGen_get_glycan", "arguments": {"glytoucan_ac": glytoucan_ac}},
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["GlyGen_get_glycan"]
