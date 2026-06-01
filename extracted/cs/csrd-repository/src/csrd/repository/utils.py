from collections.abc import Mapping, Sequence
from typing import Any

from .types import DBParams


def unpack_params(params: DBParams) -> Sequence[Any]:
    """Unpack params into a positional sequence (used by Postgres)."""
    if params is None:
        return []
    if isinstance(params, Mapping):
        return list(params.values())
    if isinstance(params, Sequence):
        return list(params)
    raise TypeError(f"Unsupported params type: {type(params)}")
