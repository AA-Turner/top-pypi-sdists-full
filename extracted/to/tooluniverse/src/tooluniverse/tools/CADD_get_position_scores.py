"""
CADD_get_position_scores

Get CADD scores for all possible substitutions at a genomic position. Returns PHRED scores for A,...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def CADD_get_position_scores(
    chrom: str,
    pos: int,
    version: Optional[str] = "GRCh38-v1.7",
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Get CADD scores for all possible substitutions at a genomic position. Returns PHRED scores for A,...

    Parameters
    ----------
    chrom : str
        Chromosome (1-22, X, Y, MT)
    pos : int
        Genomic position (1-based)
    version : str
        CADD version and genome build
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
            "name": "CADD_get_position_scores",
            "arguments": {"chrom": chrom, "pos": pos, "version": version},
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["CADD_get_position_scores"]
