"""
FourDN_get_file_metadata

Get detailed metadata for specific 4DN files including Hi-C contact matrices, TAD (Topologically ...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def FourDN_get_file_metadata(
    operation: str,
    file_accession: str,
    include_full_metadata: Optional[bool] = False,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Get detailed metadata for specific 4DN files including Hi-C contact matrices, TAD (Topologically ...

    Parameters
    ----------
    operation : str

    file_accession : str
        4DN file accession (e.g., '4DNFIIA7E3HL'). Obtain by searching with FourDN_se...
    include_full_metadata : bool
        Include complete API response in 'metadata' field (default: false). Set to tr...
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
            "name": "FourDN_get_file_metadata",
            "arguments": {
                "operation": operation,
                "file_accession": file_accession,
                "include_full_metadata": include_full_metadata,
            },
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["FourDN_get_file_metadata"]
