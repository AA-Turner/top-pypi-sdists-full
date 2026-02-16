"""
ENAPortal_search_studies

Search the European Nucleotide Archive (ENA) for sequencing studies using text queries or taxonom...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def ENAPortal_search_studies(
    query: str,
    limit: Optional[int | Any] = None,
    fields: Optional[str | Any] = None,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> Any:
    """
    Search the European Nucleotide Archive (ENA) for sequencing studies using text queries or taxonom...

    Parameters
    ----------
    query : str
        ENA search query. Examples: 'description="cancer"', 'tax_tree(9606)' (human),...
    limit : int | Any
        Maximum results to return (1-100, default 10).
    fields : str | Any
        Comma-separated fields to return. Default: 'study_accession,study_title,cente...
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
            "name": "ENAPortal_search_studies",
            "arguments": {"query": query, "limit": limit, "fields": fields},
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["ENAPortal_search_studies"]
