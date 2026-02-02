"""
cBioPortal_get_mutations

Get mutation data for specific genes in a cancer study
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def cBioPortal_get_mutations(
    study_id: str,
    gene_list: str,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> list[Any]:
    """
    Get mutation data for specific genes in a cancer study

    Parameters
    ----------
    study_id : str
        Cancer study ID
    gene_list : str
        Comma-separated gene symbols
    stream_callback : Callable, optional
        Callback for streaming output
    use_cache : bool, default False
        Enable caching
    validate : bool, default True
        Validate parameters

    Returns
    -------
    list[Any]
    """
    # Handle mutable defaults to avoid B006 linting error

    return get_shared_client().run_one_function(
        {
            "name": "cBioPortal_get_mutations",
            "arguments": {"study_id": study_id, "gene_list": gene_list},
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["cBioPortal_get_mutations"]
