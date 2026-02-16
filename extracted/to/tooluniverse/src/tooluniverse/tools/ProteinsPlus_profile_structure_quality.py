"""
ProteinsPlus_profile_structure_quality

Comprehensive protein structure quality assessment and protein-ligand complex profiling using Str...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def ProteinsPlus_profile_structure_quality(
    pdb_id: str,
    setting: Optional[str] = None,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> Any:
    """
    Comprehensive protein structure quality assessment and protein-ligand complex profiling using Str...

    Parameters
    ----------
    pdb_id : str
        PDB identifier (e.g., '1KZK', '2OZR', '4HHB'). Required.
    setting : str
        Validation setting: 'astex' (Astex diverse set criteria), 'iridium' (Iridium ...
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
            "name": "ProteinsPlus_profile_structure_quality",
            "arguments": {"pdb_id": pdb_id, "setting": setting},
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["ProteinsPlus_profile_structure_quality"]
