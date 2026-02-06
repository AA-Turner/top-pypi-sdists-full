"""
ClinGen_search_actionability

Search ClinGen clinical actionability across both adult and pediatric contexts by gene. Returns a...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def ClinGen_search_actionability(
    gene: str,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Search ClinGen clinical actionability across both adult and pediatric contexts by gene. Returns a...

    Parameters
    ----------
    gene : str
        Gene symbol to search (e.g., BRCA1, MLH1, LDLR)
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
        {"name": "ClinGen_search_actionability", "arguments": {"gene": gene}},
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["ClinGen_search_actionability"]
