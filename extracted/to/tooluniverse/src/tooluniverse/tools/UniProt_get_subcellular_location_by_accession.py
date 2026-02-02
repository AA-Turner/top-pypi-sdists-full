"""
UniProt_get_subcellular_location_by_accession

Extract subcellular localization annotations from UniProtKB entry (Comment type = SUBCELLULAR LOC...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def UniProt_get_subcellular_location_by_accession(
    accession: str,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> list[Any]:
    """
    Extract subcellular localization annotations from UniProtKB entry (Comment type = SUBCELLULAR LOC...

    Parameters
    ----------
    accession : str
        UniProtKB accession, e.g., P05067.
    stream_callback : Callable, optional
        Callback for streaming output
    use_cache : bool, default False
        Enable caching
    validate : bool, default True
        Validate parameters

    Returns
    -------
    list[Any]
    """
    # Handle mutable defaults to avoid B006 linting error

    return get_shared_client().run_one_function(
        {
            "name": "UniProt_get_subcellular_location_by_accession",
            "arguments": {"accession": accession},
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["UniProt_get_subcellular_location_by_accession"]
