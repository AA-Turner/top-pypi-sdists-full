"""
MedlinePlus_get_genetics_condition_by_name

Get detailed information from MedlinePlus Genetics corresponding to genetic condition name, suppo...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def MedlinePlus_get_genetics_condition_by_name(
    condition: str,
    format: str,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Get detailed information from MedlinePlus Genetics corresponding to genetic condition name, suppo...

    Parameters
    ----------
    condition : str
        URL slug of genetic condition, e.g., "alzheimer-disease", must match MedlineP...
    format : str
        Return format, options "json" or "xml", default "json".
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
            "name": "MedlinePlus_get_genetics_condition_by_name",
            "arguments": {"condition": condition, "format": format},
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["MedlinePlus_get_genetics_condition_by_name"]
