"""
ensembl_get_variation

Get detailed information about a specific genetic variation by its ID (e.g., rs699). Returns vari...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def ensembl_get_variation(
    id: str,
    species: Optional[str] = "human",
    phenotypes: Optional[int] = 0,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Get detailed information about a specific genetic variation by its ID (e.g., rs699). Returns vari...

    Parameters
    ----------
    id : str
        Variation ID (e.g., 'rs699', 'rs1421085'). Use ensembl_get_variants to find v...
    species : str
        Species name (default 'human')
    phenotypes : int
        Include phenotype associations (0=no, 1=yes)
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
            "name": "ensembl_get_variation",
            "arguments": {"id": id, "species": species, "phenotypes": phenotypes},
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["ensembl_get_variation"]
