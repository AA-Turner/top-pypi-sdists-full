"""
GlyGen_get_glycoprotein

Get detailed glycoprotein information from GlyGen by UniProt accession. Returns protein name, gly...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def GlyGen_get_glycoprotein(
    uniprot_ac: str,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> Any:
    """
    Get detailed glycoprotein information from GlyGen by UniProt accession. Returns protein name, gly...

    Parameters
    ----------
    uniprot_ac : str
        UniProt accession ID. Examples: 'P14210' (HGF), 'P02724' (Glycophorin A), 'P0...
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
        {"name": "GlyGen_get_glycoprotein", "arguments": {"uniprot_ac": uniprot_ac}},
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["GlyGen_get_glycoprotein"]
