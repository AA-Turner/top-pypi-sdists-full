"""
InterPro_get_domain_details

Get detailed information about a specific InterPro domain entry including description, hierarchy,...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def InterPro_get_domain_details(
    accession: str,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Get detailed information about a specific InterPro domain entry including description, hierarchy,...

    Parameters
    ----------
    accession : str
        InterPro accession ID (e.g., IPR000719, IPR000719)
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
        {"name": "InterPro_get_domain_details", "arguments": {"accession": accession}},
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["InterPro_get_domain_details"]
