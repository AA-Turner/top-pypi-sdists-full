"""
alphafold_get_prediction

Retrieve full AlphaFold 3D structure predictions for a given protein. IMPORTANT: The qualifier mu...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def alphafold_get_prediction(
    qualifier: str,
    sequence_checksum: str,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> list[Any]:
    """
    Retrieve full AlphaFold 3D structure predictions for a given protein. IMPORTANT: The qualifier mu...

    Parameters
    ----------
    qualifier : str
        Protein identifier: UniProt ACCESSION (e.g., 'P69905'). Do NOT use entry name...
    sequence_checksum : str
        Optional CRC64 checksum of the UniProt sequence.
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
            "name": "alphafold_get_prediction",
            "arguments": {
                "qualifier": qualifier,
                "sequence_checksum": sequence_checksum,
            },
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["alphafold_get_prediction"]
