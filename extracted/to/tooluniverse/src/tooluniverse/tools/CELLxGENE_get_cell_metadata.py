"""
CELLxGENE_get_cell_metadata

Query cell (observation) metadata from CELLxGENE Census. Returns cell type, tissue, disease, dono...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def CELLxGENE_get_cell_metadata(
    operation: str,
    organism: Optional[str] = "Homo sapiens",
    obs_value_filter: Optional[str] = None,
    column_names: Optional[list[str]] = None,
    census_version: Optional[str] = "stable",
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Query cell (observation) metadata from CELLxGENE Census. Returns cell type, tissue, disease, dono...

    Parameters
    ----------
    operation : str
        Operation type
    organism : str
        Organism name
    obs_value_filter : str
        Filter cells using SQL-like syntax. Format: 'field == "value"'. Operators: ==...
    column_names : list[str]
        Specific columns to return (default: all columns)
    census_version : str
        Census version to query. 'stable' (recommended, Long-Term Support release), '...
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
            "name": "CELLxGENE_get_cell_metadata",
            "arguments": {
                "operation": operation,
                "organism": organism,
                "obs_value_filter": obs_value_filter,
                "column_names": column_names,
                "census_version": census_version,
            },
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["CELLxGENE_get_cell_metadata"]
