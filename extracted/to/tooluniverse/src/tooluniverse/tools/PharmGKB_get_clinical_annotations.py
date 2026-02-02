"""
PharmGKB_get_clinical_annotations

Get clinical annotations showing gene-drug-phenotype relationships. Returns variant-level clinica...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def PharmGKB_get_clinical_annotations(
    annotation_id: Optional[str] = None,
    gene_id: Optional[str] = None,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Get clinical annotations showing gene-drug-phenotype relationships. Returns variant-level clinica...

    Parameters
    ----------
    annotation_id : str
        PharmGKB clinical annotation ID (e.g., '1449309855').
    gene_id : str
        PharmGKB Gene Accession ID (e.g., 'PA128').
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
            "name": "PharmGKB_get_clinical_annotations",
            "arguments": {"annotation_id": annotation_id, "gene_id": gene_id},
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["PharmGKB_get_clinical_annotations"]
