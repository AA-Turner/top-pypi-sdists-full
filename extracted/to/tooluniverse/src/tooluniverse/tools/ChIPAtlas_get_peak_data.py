"""
ChIPAtlas_get_peak_data

Get download URLs for ChIP-Atlas peak-call data in BigWig, BED, or BigBed format. BigWig contains...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def ChIPAtlas_get_peak_data(
    operation: str,
    experiment_id: str,
    genome: Optional[str] = "hg38",
    format: Optional[str] = "bigwig",
    threshold: Optional[str] = "05",
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Get download URLs for ChIP-Atlas peak-call data in BigWig, BED, or BigBed format. BigWig contains...

    Parameters
    ----------
    operation : str

    experiment_id : str
        Experiment ID (SRX/ERX/DRX format, required)
    genome : str
        Genome assembly
    format : str
        Output format
    threshold : str
        Q-value threshold for BED/BigBed peak files. '05'=1e-5 (more peaks), '10'=1e-...
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
            "name": "ChIPAtlas_get_peak_data",
            "arguments": {
                "operation": operation,
                "experiment_id": experiment_id,
                "genome": genome,
                "format": format,
                "threshold": threshold,
            },
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["ChIPAtlas_get_peak_data"]
