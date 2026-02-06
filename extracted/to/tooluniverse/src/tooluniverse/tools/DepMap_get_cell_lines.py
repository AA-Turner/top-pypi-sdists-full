"""
DepMap_get_cell_lines

Get list of cancer cell lines from DepMap/Sanger with metadata. Filter by tissue or cancer type. ...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def DepMap_get_cell_lines(
    tissue: Optional[str] = None,
    cancer_type: Optional[str] = None,
    page_size: Optional[int] = 20,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Get list of cancer cell lines from DepMap/Sanger with metadata. Filter by tissue or cancer type. ...

    Parameters
    ----------
    tissue : str
        Filter by tissue type (e.g., 'Lung', 'Breast', 'Colon')
    cancer_type : str
        Filter by cancer type (e.g., 'Non-Small Cell Lung Carcinoma')
    page_size : int
        Number of results (1-100)
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
            "name": "DepMap_get_cell_lines",
            "arguments": {
                "tissue": tissue,
                "cancer_type": cancer_type,
                "page_size": page_size,
            },
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["DepMap_get_cell_lines"]
