"""
EnsemblVEP_annotate_rsid

Predict functional consequences of a genetic variant using its dbSNP rs identifier via the Ensemb...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def EnsemblVEP_annotate_rsid(
    variant_id: str,
    species: Optional[str] = "human",
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> Any:
    """
    Predict functional consequences of a genetic variant using its dbSNP rs identifier via the Ensemb...

    Parameters
    ----------
    variant_id : str
        dbSNP rs identifier. Examples: 'rs7903146' (TCF7L2, type 2 diabetes), 'rs4293...
    species : str
        Species name. Default: 'human'.
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
            "name": "EnsemblVEP_annotate_rsid",
            "arguments": {"variant_id": variant_id, "species": species},
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["EnsemblVEP_annotate_rsid"]
