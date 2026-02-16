"""
Alliance_get_gene

Get detailed gene information from the Alliance of Genome Resources, which integrates data from 7...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def Alliance_get_gene(
    gene_id: str,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> Any:
    """
    Get detailed gene information from the Alliance of Genome Resources, which integrates data from 7...

    Parameters
    ----------
    gene_id : str
        Alliance gene ID with source prefix. Examples: 'HGNC:6081' (human INS), 'MGI:...
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
        {"name": "Alliance_get_gene", "arguments": {"gene_id": gene_id}},
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["Alliance_get_gene"]
