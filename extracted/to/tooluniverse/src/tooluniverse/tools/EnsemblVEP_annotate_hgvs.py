"""
EnsemblVEP_annotate_hgvs

Predict functional consequences of a genetic variant using HGVS notation via the Ensembl Variant ...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def EnsemblVEP_annotate_hgvs(
    hgvs_notation: str,
    species: Optional[str] = "human",
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> Any:
    """
    Predict functional consequences of a genetic variant using HGVS notation via the Ensembl Variant ...

    Parameters
    ----------
    hgvs_notation : str
        Variant in HGVS notation. Supports protein (p.), coding DNA (c.), and genomic...
    species : str
        Species name. Default: 'human'. Other options: 'mouse', 'rat', 'zebrafish', etc.
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
            "name": "EnsemblVEP_annotate_hgvs",
            "arguments": {"hgvs_notation": hgvs_notation, "species": species},
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["EnsemblVEP_annotate_hgvs"]
