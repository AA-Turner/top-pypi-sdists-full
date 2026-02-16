"""
PANTHER_gene_info

Get gene classification and functional annotation from PANTHER (Protein ANalysis THrough Evolutio...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def PANTHER_gene_info(
    gene_id: str,
    organism: Optional[int | Any] = None,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> Any:
    """
    Get gene classification and functional annotation from PANTHER (Protein ANalysis THrough Evolutio...

    Parameters
    ----------
    gene_id : str
        Gene identifier - UniProt accession, Ensembl ID, or gene symbol. Examples: 'P...
    organism : int | Any
        NCBI taxonomy ID. Default: 9606 (human). Others: 10090 (mouse), 10116 (rat), ...
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
            "name": "PANTHER_gene_info",
            "arguments": {"gene_id": gene_id, "organism": organism},
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["PANTHER_gene_info"]
