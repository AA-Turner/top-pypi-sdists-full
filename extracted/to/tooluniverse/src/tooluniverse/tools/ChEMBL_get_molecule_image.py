"""
ChEMBL_get_molecule_image

Get molecular structure image (SVG format) for a molecule by ChEMBL ID.
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def ChEMBL_get_molecule_image(
    chembl_id: str,
    format: Optional[str] = "svg",
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Get molecular structure image (SVG format) for a molecule by ChEMBL ID.

    Parameters
    ----------
    chembl_id : str
        ChEMBL molecule ID (e.g., 'CHEMBL25'). To find a molecule ID, use ChEMBL_sear...
    format : str
        Image format
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
            "name": "ChEMBL_get_molecule_image",
            "arguments": {"chembl_id": chembl_id, "format": format},
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["ChEMBL_get_molecule_image"]
