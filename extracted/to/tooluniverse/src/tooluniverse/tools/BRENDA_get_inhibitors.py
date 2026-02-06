"""
BRENDA_get_inhibitors

Get enzyme inhibitor data from BRENDA via SPARQL endpoint. Returns Ki (inhibition constant) value...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def BRENDA_get_inhibitors(
    operation: str,
    ec_number: str,
    organism: Optional[str] = None,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Get enzyme inhibitor data from BRENDA via SPARQL endpoint. Returns Ki (inhibition constant) value...

    Parameters
    ----------
    operation : str
        Operation type (fixed: get_inhibitors)
    ec_number : str
        EC number
    organism : str
        Optional organism filter
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
            "name": "BRENDA_get_inhibitors",
            "arguments": {
                "operation": operation,
                "ec_number": ec_number,
                "organism": organism,
            },
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["BRENDA_get_inhibitors"]
