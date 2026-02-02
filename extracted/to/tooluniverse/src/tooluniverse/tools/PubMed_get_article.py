"""
PubMed_get_article

Get complete metadata for a specific PubMed article by its PMID (PubMed ID) using efetch. Returns...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def PubMed_get_article(
    pmid: str,
    api_key: Optional[str] = None,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Get complete metadata for a specific PubMed article by its PMID (PubMed ID) using efetch. Returns...

    Parameters
    ----------
    pmid : str
        PubMed ID (PMID) as string or integer (e.g., '12345678', '33250470'). Find PM...
    api_key : str
        Optional NCBI API key for higher rate limits. Get free key at https://www.ncb...
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
        {"name": "PubMed_get_article", "arguments": {"pmid": pmid, "api_key": api_key}},
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["PubMed_get_article"]
