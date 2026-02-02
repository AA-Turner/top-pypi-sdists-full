"""
arrayexpress_get_experiment_files

Get list of files associated with an ArrayExpress experiment. Returns file metadata including fil...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def arrayexpress_get_experiment_files(
    experiment_id: str,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> dict[str, Any]:
    """
    Get list of files associated with an ArrayExpress experiment. Returns file metadata including fil...

    Parameters
    ----------
    experiment_id : str
        ArrayExpress experiment ID
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
            "name": "arrayexpress_get_experiment_files",
            "arguments": {"experiment_id": experiment_id},
        },
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["arrayexpress_get_experiment_files"]
