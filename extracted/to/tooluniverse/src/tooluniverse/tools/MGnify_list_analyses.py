"""
MGnify_list_analyses

List analyses associated with a study accession (taxonomic/functional outputs). Use to enumerate ...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def MGnify_list_analyses(
    study_accession: str,
    size: Optional[int] = 10,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    List analyses associated with a study accession (taxonomic/functional outputs). Use to enumerate ...

    Parameters
    ----------
    study_accession : str
        MGnify study accession (e.g., 'MGYS00000001').
    size : int
        Number of records per page (1–100).
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
            "name": "MGnify_list_analyses",
            "arguments": {"study_accession": study_accession, "size": size},
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["MGnify_list_analyses"]
