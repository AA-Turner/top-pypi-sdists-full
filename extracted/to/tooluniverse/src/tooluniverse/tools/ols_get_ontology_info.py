"""
ols_get_ontology_info

Get detailed information about an ontology
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def ols_get_ontology_info(
    operation: str,
    ontology_id: str,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Get detailed information about an ontology

    Parameters
    ----------
    operation : str
        The operation to perform (get_ontology_info)
    ontology_id : str
        The ID of the ontology to retrieve
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
            "name": "ols_get_ontology_info",
            "arguments": {"operation": operation, "ontology_id": ontology_id},
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["ols_get_ontology_info"]
