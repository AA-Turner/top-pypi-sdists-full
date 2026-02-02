"""
cellosaurus_get_cell_line_info

Get detailed information about a specific cell line using its Cellosaurus accession number (CVCL_...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def cellosaurus_get_cell_line_info(
    accession: str,
    format: str,
    fields: list[str],
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Get detailed information about a specific cell line using its Cellosaurus accession number (CVCL_...

    Parameters
    ----------
    accession : str
        Cellosaurus accession number (must start with 'CVCL_')
    format : str
        Response format
    fields : list[str]
        Specific fields to retrieve (e.g., ['id', 'ox', 'char']). If not specified, a...
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
            "name": "cellosaurus_get_cell_line_info",
            "arguments": {"accession": accession, "format": format, "fields": fields},
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["cellosaurus_get_cell_line_info"]
