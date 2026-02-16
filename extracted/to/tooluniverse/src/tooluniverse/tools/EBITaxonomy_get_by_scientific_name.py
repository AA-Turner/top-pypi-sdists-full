"""
EBITaxonomy_get_by_scientific_name

Look up taxonomy by scientific (Latin) name using the EBI Taxonomy service. Returns taxonomy ID, ...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def EBITaxonomy_get_by_scientific_name(
    scientific_name: str,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> Any:
    """
    Look up taxonomy by scientific (Latin) name using the EBI Taxonomy service. Returns taxonomy ID, ...

    Parameters
    ----------
    scientific_name : str
        Scientific name of the organism. Examples: 'Homo sapiens', 'Escherichia coli'...
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
            "name": "EBITaxonomy_get_by_scientific_name",
            "arguments": {"scientific_name": scientific_name},
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["EBITaxonomy_get_by_scientific_name"]
