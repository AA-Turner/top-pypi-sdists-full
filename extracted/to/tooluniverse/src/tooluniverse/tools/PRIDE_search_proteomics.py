"""
PRIDE_search_proteomics

Search the PRIDE Archive for proteomics experiments and mass spectrometry datasets. Returns proje...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def PRIDE_search_proteomics(
    query: str,
    page_size: Optional[int] = 20,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Search the PRIDE Archive for proteomics experiments and mass spectrometry datasets. Returns proje...

    Parameters
    ----------
    query : str
        Search keywords for proteomics experiments. Examples: 'cancer', 'phosphorylat...
    page_size : int
        Number of projects to return per page (default: 20, max: 100)
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
            "name": "PRIDE_search_proteomics",
            "arguments": {"query": query, "page_size": page_size},
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["PRIDE_search_proteomics"]
