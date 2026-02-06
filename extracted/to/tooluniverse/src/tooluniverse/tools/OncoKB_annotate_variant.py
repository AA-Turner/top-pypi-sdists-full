"""
OncoKB_annotate_variant

Annotate a cancer variant for oncogenic potential and treatment implications using OncoKB. Return...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def OncoKB_annotate_variant(
    operation: str,
    gene: str,
    variant: str,
    tumor_type: Optional[str] = None,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Annotate a cancer variant for oncogenic potential and treatment implications using OncoKB. Return...

    Parameters
    ----------
    operation : str
        Operation type (fixed: annotate_variant)
    gene : str
        Gene symbol (e.g., BRAF, EGFR, TP53, KRAS)
    variant : str
        Variant notation - protein change (e.g., V600E, T790M, G12D)
    tumor_type : str
        Optional OncoTree tumor type code (e.g., MEL for melanoma, LUAD for lung aden...
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
            "name": "OncoKB_annotate_variant",
            "arguments": {
                "operation": operation,
                "gene": gene,
                "variant": variant,
                "tumor_type": tumor_type,
            },
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["OncoKB_annotate_variant"]
