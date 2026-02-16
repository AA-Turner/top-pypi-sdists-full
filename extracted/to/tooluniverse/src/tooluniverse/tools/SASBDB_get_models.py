"""
SASBDB_get_models

Retrieve derived structural models for a SASBDB entry including ab initio bead models, atomistic ...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def SASBDB_get_models(
    sasbdb_id: str,
    model_type: Optional[str] = "all",
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> Optional[dict[str, Any]]:
    """
    Retrieve derived structural models for a SASBDB entry including ab initio bead models, atomistic ...

    Parameters
    ----------
    sasbdb_id : str
        SASBDB entry identifier (e.g., 'SASDBA2', 'SASDBW5'). Obtain from SASBDB_sear...
    model_type : str
        Type of model: 'ab_initio' (bead models from DAMMIF/GASBOR), 'atomistic' (PDB...
    stream_callback : Callable, optional
        Callback for streaming output
    use_cache : bool, default False
        Enable caching
    validate : bool, default True
        Validate parameters

    Returns
    -------
    Optional[dict[str, Any]]
    """
    # Handle mutable defaults to avoid B006 linting error

    return get_shared_client().run_one_function(
        {
            "name": "SASBDB_get_models",
            "arguments": {"sasbdb_id": sasbdb_id, "model_type": model_type},
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["SASBDB_get_models"]
