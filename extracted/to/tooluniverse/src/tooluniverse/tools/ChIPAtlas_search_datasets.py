"""
ChIPAtlas_search_datasets

Search ChIP-Atlas by antigen or cell type to find available datasets. Returns number of experimen...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def ChIPAtlas_search_datasets(
    operation: str,
    antigen: Optional[str] = None,
    cell_type: Optional[str] = None,
    genome: Optional[str] = "hg38",
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Search ChIP-Atlas by antigen or cell type to find available datasets. Returns number of experimen...

    Parameters
    ----------
    operation : str

    antigen : str
        Search by antigen/protein name (e.g., 'CTCF', 'H3K27ac')
    cell_type : str
        Search by cell type (e.g., 'K-562', 'HeLa', 'MCF-7')
    genome : str
        Genome assembly
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
            "name": "ChIPAtlas_search_datasets",
            "arguments": {
                "operation": operation,
                "antigen": antigen,
                "cell_type": cell_type,
                "genome": genome,
            },
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["ChIPAtlas_search_datasets"]
