"""
ensembl_get_variants

Get genetic variants (SNPs, indels) in a genomic region. Returns variant information including po...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def ensembl_get_variants(
    region: str,
    species: Optional[str] = "human",
    feature: Optional[str] = "variation",
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Get genetic variants (SNPs, indels) in a genomic region. Returns variant information including po...

    Parameters
    ----------
    region : str
        Genomic region in format 'chromosome:start-end' (e.g., '13:32315086-32400268'...
    species : str
        Species name (default 'human'). Examples: 'human', 'mouse', 'rat'
    feature : str
        Feature type to retrieve (default 'variation')
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
            "name": "ensembl_get_variants",
            "arguments": {"region": region, "species": species, "feature": feature},
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["ensembl_get_variants"]
