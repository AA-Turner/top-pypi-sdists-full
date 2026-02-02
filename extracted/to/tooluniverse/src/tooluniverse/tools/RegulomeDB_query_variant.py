"""
RegulomeDB_query_variant

Query RegulomeDB for regulatory variant annotations using rsID
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def RegulomeDB_query_variant(
    rsid: str,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Query RegulomeDB for regulatory variant annotations using rsID

    Parameters
    ----------
    rsid : str
        dbSNP rsID (e.g., rs123456)
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
        {"name": "RegulomeDB_query_variant", "arguments": {"rsid": rsid}},
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["RegulomeDB_query_variant"]
