"""
openalex_get_work_by_doi

Get a single OpenAlex work (paper) by DOI. Provide a DOI string like "10.65215/2q58a426" (you can...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def openalex_get_work_by_doi(
    doi: str,
    mailto: Optional[str] = None,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Get a single OpenAlex work (paper) by DOI. Provide a DOI string like "10.65215/2q58a426" (you can...

    Parameters
    ----------
    doi : str
        DOI identifier (preferred) or DOI URL.
    mailto : str
        Optional contact email for OpenAlex polite pool.
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
            "name": "openalex_get_work_by_doi",
            "arguments": {"doi": doi, "mailto": mailto},
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["openalex_get_work_by_doi"]
