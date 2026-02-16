"""
Alliance_get_disease

Get disease summary information from the Alliance of Genome Resources by Disease Ontology (DO) ID...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def Alliance_get_disease(
    disease_id: str,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> Any:
    """
    Get disease summary information from the Alliance of Genome Resources by Disease Ontology (DO) ID...

    Parameters
    ----------
    disease_id : str
        Disease Ontology (DO) ID. Examples: 'DOID:162' (cancer), 'DOID:10652' (Alzhei...
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
        {"name": "Alliance_get_disease", "arguments": {"disease_id": disease_id}},
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["Alliance_get_disease"]
