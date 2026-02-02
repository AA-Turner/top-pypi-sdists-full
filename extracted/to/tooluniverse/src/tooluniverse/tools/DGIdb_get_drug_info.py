"""
DGIdb_get_drug_info

Get drug information from DGIdb including target genes and interaction details.
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def DGIdb_get_drug_info(
    drugs: list[str],
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Get drug information from DGIdb including target genes and interaction details.

    Parameters
    ----------
    drugs : list[str]
        List of drug names (e.g., ['imatinib', 'erlotinib']).
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
        {"name": "DGIdb_get_drug_info", "arguments": {"drugs": drugs}},
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["DGIdb_get_drug_info"]
