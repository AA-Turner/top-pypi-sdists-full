"""
get_polymer_entity_annotations

Retrieve functional annotations (Pfam domains, GO terms) and associated UniProt accession IDs for...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def get_polymer_entity_annotations(
    entity_id: str,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Retrieve functional annotations (Pfam domains, GO terms) and associated UniProt accession IDs for...

    Parameters
    ----------
    entity_id : str
        Polymer entity ID like '1A8M_1'
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
            "name": "get_polymer_entity_annotations",
            "arguments": {"entity_id": entity_id},
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["get_polymer_entity_annotations"]
