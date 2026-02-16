"""
CATH_get_superfamily

Get CATH protein structure superfamily information by CATH ID. CATH classifies protein domain str...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def CATH_get_superfamily(
    superfamily_id: str,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> Any:
    """
    Get CATH protein structure superfamily information by CATH ID. CATH classifies protein domain str...

    Parameters
    ----------
    superfamily_id : str
        CATH superfamily ID in C.A.T.H format. Examples: '2.40.50.140' (Nucleic acid-...
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
            "name": "CATH_get_superfamily",
            "arguments": {"superfamily_id": superfamily_id},
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["CATH_get_superfamily"]
