"""
ols_find_similar_terms

Find similar terms using LLM-based similarity
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def ols_find_similar_terms(
    operation: str,
    term_iri: str,
    ontology: str,
    size: Optional[int] = 10,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Find similar terms using LLM-based similarity

    Parameters
    ----------
    operation : str
        The operation to perform (find_similar_terms)
    term_iri : str
        The IRI of the term to find similar terms for
    ontology : str
        The ontology ID
    size : int
        Number of similar terms to return (default: 10)
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
            "name": "ols_find_similar_terms",
            "arguments": {
                "operation": operation,
                "term_iri": term_iri,
                "ontology": ontology,
                "size": size,
            },
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["ols_find_similar_terms"]
