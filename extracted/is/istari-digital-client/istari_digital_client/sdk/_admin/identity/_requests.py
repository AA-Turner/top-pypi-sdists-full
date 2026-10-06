"""Build generated identity request models from facade keyword arguments."""

from __future__ import annotations

from typing import Any, TypeVar

from pydantic import BaseModel

M = TypeVar("M", bound=BaseModel)


def build_request(model: type[M], fields: dict[str, Any], *, verb: str) -> M:
    """Instantiate ``model`` from ``fields``, rejecting names it does not declare.

    The generated models ignore unknown keys, so a misspelled field would
    otherwise vanish silently and an update would send an empty patch.
    """
    declared = set(model.model_fields)
    declared.update(f.alias for f in model.model_fields.values() if f.alias)
    unknown = sorted(set(fields) - declared)
    if unknown:
        raise TypeError(
            f"{verb}() got unexpected field(s) {', '.join(unknown)}; "
            f"{model.__name__} accepts: {', '.join(model.model_fields)}"
        )
    return model(**fields)
