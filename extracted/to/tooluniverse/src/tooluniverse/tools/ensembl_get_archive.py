"""
ensembl_get_archive

Get historical (archived) gene information by stable ID. Returns gene location and status across ...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def ensembl_get_archive(
    id: str,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> Any:
    """
    Get historical (archived) gene information by stable ID. Returns gene location and status across ...

    Parameters
    ----------
    id : str
        Ensembl stable ID (gene, transcript, or protein, e.g., 'ENSG00000139618')
    stream_callback : Callable, optional
        Callback for streaming output
    use_cache : bool, default False
        Enable caching
    validate : bool, default True
        Validate parameters

    Returns
    -------
    Any
    """
    # Handle mutable defaults to avoid B006 linting error

    return get_shared_client().run_one_function(
        {"name": "ensembl_get_archive", "arguments": {"id": id}},
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["ensembl_get_archive"]
