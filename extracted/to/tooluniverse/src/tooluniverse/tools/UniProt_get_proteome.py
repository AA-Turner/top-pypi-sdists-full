"""
UniProt_get_proteome

Get proteome information by proteome ID. Returns comprehensive proteome data including taxonomy, ...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def UniProt_get_proteome(
    proteome_id: str,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Get proteome information by proteome ID. Returns comprehensive proteome data including taxonomy, ...

    Parameters
    ----------
    proteome_id : str
        UniProt proteome ID (e.g., 'UP000005640' for human, 'UP000000589' for mouse)....
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
        {"name": "UniProt_get_proteome", "arguments": {"proteome_id": proteome_id}},
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["UniProt_get_proteome"]
