"""Reference resolution utilities."""

from typing import Any


def resolve_object(data: dict, resolve: str) -> Any:
    """Resolve object to id or name."""
    try:
        resolved = data.get(resolve)
        if resolved:
            return resolved
        else:
            return data
    except AttributeError:
        return data


