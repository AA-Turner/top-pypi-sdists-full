"""
PubChem_get_CID_by_compound_name

Retrieve corresponding CID list (IdentifierList) by chemical name.
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def PubChem_get_CID_by_compound_name(
    name: str,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Retrieve corresponding CID list (IdentifierList) by chemical name.

    Parameters
    ----------
    name : str
        Chemical name (e.g., "Aspirin" or IUPAC name).
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
        {"name": "PubChem_get_CID_by_compound_name", "arguments": {"name": name}},
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["PubChem_get_CID_by_compound_name"]
