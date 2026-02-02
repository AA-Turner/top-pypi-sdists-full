"""
ensembl_get_xrefs_by_name

Get cross-references for an Ensembl object by its name/symbol. Returns mappings to external datab...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def ensembl_get_xrefs_by_name(
    name: str,
    species: Optional[str] = "homo_sapiens",
    external_db: Optional[str] = None,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Get cross-references for an Ensembl object by its name/symbol. Returns mappings to external datab...

    Parameters
    ----------
    name : str
        Gene symbol or name (e.g., 'BRCA1', 'TP53')
    species : str
        Species name (default 'homo_sapiens')
    external_db : str
        Filter by external database name (optional)
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
            "name": "ensembl_get_xrefs_by_name",
            "arguments": {"name": name, "species": species, "external_db": external_db},
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["ensembl_get_xrefs_by_name"]
