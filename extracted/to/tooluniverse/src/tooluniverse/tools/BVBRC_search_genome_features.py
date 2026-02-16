"""
BVBRC_search_genome_features

Search for genome features (genes, proteins, CDS) in BV-BRC pathogen genomes. Find specific genes...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def BVBRC_search_genome_features(
    gene: Optional[str | Any] = None,
    product: Optional[str | Any] = None,
    genome_id: Optional[str | Any] = None,
    limit: Optional[int | Any] = None,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> Any:
    """
    Search for genome features (genes, proteins, CDS) in BV-BRC pathogen genomes. Find specific genes...

    Parameters
    ----------
    gene : str | Any
        Gene name to search for. Examples: 'mecA' (methicillin resistance), 'blaTEM' ...
    product : str | Any
        Gene product keyword to search. Examples: 'beta-lactamase', 'penicillin-bindi...
    genome_id : str | Any
        Restrict search to a specific genome. Example: '83332.12'.
    limit : int | Any
        Maximum number of results. Default: 10. Max: 100.
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
            "name": "BVBRC_search_genome_features",
            "arguments": {
                "gene": gene,
                "product": product,
                "genome_id": genome_id,
                "limit": limit,
            },
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["BVBRC_search_genome_features"]
