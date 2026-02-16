"""
Nextstrain_list_datasets

List available pathogen phylogenetic datasets from Nextstrain. Returns datasets grouped by pathog...
"""

from typing import Any, Optional, Callable
from ._shared_client import get_shared_client


def Nextstrain_list_datasets(
    pathogen: Optional[str | Any] = None,
    *,
    stream_callback: Optional[Callable[[str], None]] = None,
    use_cache: bool = False,
    validate: bool = True,
) -> Any:
    """
    List available pathogen phylogenetic datasets from Nextstrain. Returns datasets grouped by pathog...

    Parameters
    ----------
    pathogen : str | Any
        Optional pathogen name filter. Examples: 'flu', 'ebola', 'zika', 'dengue', 'm...
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
        {"name": "Nextstrain_list_datasets", "arguments": {"pathogen": pathogen}},
        stream_callback=stream_callback,
        use_cache=use_cache,
        validate=validate,
    )


__all__ = ["Nextstrain_list_datasets"]
