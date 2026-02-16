"""
EnsemblCompara_get_paralogues

Find paralogous genes (genes within the same species that arose from gene duplication events) usi...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def EnsemblCompara_get_paralogues(
    gene: str,
    species: Optional[str] = None,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> Any:
    """
    Find paralogous genes (genes within the same species that arose from gene duplication events) usi...

    Parameters
    ----------
    gene : str
        Gene symbol or Ensembl gene ID. Examples: 'TP53', 'BRCA1', 'ENSG00000141510'.
    species : str
        Species (default: 'human'). Examples: 'human', 'mouse', 'zebrafish'.
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
        {
            "name": "EnsemblCompara_get_paralogues",
            "arguments": {"gene": gene, "species": species},
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["EnsemblCompara_get_paralogues"]
