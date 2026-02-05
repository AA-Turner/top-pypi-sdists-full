"""
CELLxGENE_get_expression_data

Query gene expression data from CELLxGENE Census as AnnData object summary. Filter cells and gene...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def CELLxGENE_get_expression_data(
    operation: str,
    organism: Optional[str] = "Homo sapiens",
    obs_value_filter: Optional[str] = None,
    var_value_filter: Optional[str] = None,
    obs_column_names: Optional[list[str]] = None,
    var_column_names: Optional[list[str]] = None,
    census_version: Optional[str] = "stable",
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Query gene expression data from CELLxGENE Census as AnnData object summary. Filter cells and gene...

    Parameters
    ----------
    operation : str
        Operation type
    organism : str
        Organism name
    obs_value_filter : str
        Cell filter (e.g., 'tissue == "lung" and disease == "COVID-19"')
    var_value_filter : str
        Gene filter (e.g., 'feature_name in ["CD4", "CD8A"]')
    obs_column_names : list[str]
        Cell metadata columns to include
    var_column_names : list[str]
        Gene metadata columns to include
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
            "name": "CELLxGENE_get_expression_data",
            "arguments": {
                "operation": operation,
                "organism": organism,
                "obs_value_filter": obs_value_filter,
                "var_value_filter": var_value_filter,
                "obs_column_names": obs_column_names,
                "var_column_names": var_column_names,
                "census_version": census_version,
            },
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["CELLxGENE_get_expression_data"]
