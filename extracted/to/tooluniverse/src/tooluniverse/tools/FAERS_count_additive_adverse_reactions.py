"""
FAERS_count_additive_adverse_reactions

Aggregate adverse reaction counts across specified medicinal products. Only medicinalproducts is ...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def FAERS_count_additive_adverse_reactions(
    medicinalproducts: list[str],
    patientsex: Optional[str] = None,
    patientagegroup: Optional[str] = None,
    occurcountry: Optional[str] = None,
    serious: Optional[str] = None,
    seriousnessdeath: Optional[str] = None,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> Any:
    """
    Aggregate adverse reaction counts across specified medicinal products. Only medicinalproducts is ...

    Parameters
    ----------
    medicinalproducts : list[str]
        Array of medicinal product names.
    patientsex : str
        Optional: Filter by patient sex. Omit this parameter if you don't want to fil...
    patientagegroup : str
        Optional: Filter by patient age group. Omit this parameter if you don't want ...
    occurcountry : str
        Optional: Filter by country where event occurred (ISO2 code, e.g., 'US', 'GB'...
    serious : str
        Optional: Filter by event seriousness. Omit this parameter if you don't want ...
    seriousnessdeath : str
        Optional: Filter for fatal outcomes. Omit this parameter if you don't want to...
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
            "name": "FAERS_count_additive_adverse_reactions",
            "arguments": {
                "medicinalproducts": medicinalproducts,
                "patientsex": patientsex,
                "patientagegroup": patientagegroup,
                "occurcountry": occurcountry,
                "serious": serious,
                "seriousnessdeath": seriousnessdeath,
            },
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["FAERS_count_additive_adverse_reactions"]
