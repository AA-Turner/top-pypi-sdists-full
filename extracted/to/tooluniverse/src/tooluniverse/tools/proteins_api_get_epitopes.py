"""
proteins_api_get_epitopes

Get epitope sequences for a protein. Returns B-cell and T-cell epitope information with antigenic...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def proteins_api_get_epitopes(
    accession: str | list[Any],
    format: Optional[str] = "json",
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Get epitope sequences for a protein. Returns B-cell and T-cell epitope information with antigenic...

    Parameters
    ----------
    accession : str | list[Any]
        UniProt protein accession(s). Can be a single accession (e.g., 'P05067'), com...
    format : str
        Response format. JSON is recommended for most use cases.
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
            "name": "proteins_api_get_epitopes",
            "arguments": {"accession": accession, "format": format},
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["proteins_api_get_epitopes"]
