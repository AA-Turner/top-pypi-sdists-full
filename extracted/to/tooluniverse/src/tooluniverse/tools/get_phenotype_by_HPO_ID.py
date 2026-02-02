"""
get_phenotype_by_HPO_ID

Retrieve a phenotype or symptom by its HPO ID.
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def get_phenotype_by_HPO_ID(
    id: str,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Retrieve a phenotype or symptom by its HPO ID.

    Parameters
    ----------
    id : str
        The HPO ID of the phenotype or symptom.
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
        {"name": "get_phenotype_by_HPO_ID", "arguments": {"id": id}},
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["get_phenotype_by_HPO_ID"]
