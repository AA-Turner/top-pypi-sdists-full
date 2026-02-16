"""
MonarchV3_get_associations

Query cross-species associations between biomedical entities in the Monarch Initiative knowledge ...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def MonarchV3_get_associations(
    subject: str,
    category: str,
    limit: Optional[int] = None,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> Any:
    """
    Query cross-species associations between biomedical entities in the Monarch Initiative knowledge ...

    Parameters
    ----------
    subject : str
        Subject entity CURIE. Examples: 'HGNC:11998' (TP53), 'MONDO:0005148' (type 2 ...
    category : str
        Biolink association category. Options: 'biolink:GeneToPhenotypicFeatureAssoci...
    limit : int
        Maximum number of associations to return (default: 20, max: 200).
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
            "name": "MonarchV3_get_associations",
            "arguments": {"subject": subject, "category": category, "limit": limit},
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["MonarchV3_get_associations"]
