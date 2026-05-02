"""Type aliases used across corvic."""

import os
from collections.abc import Iterable, Mapping
from typing import Any, Literal, Protocol, TypeAlias, runtime_checkable

PathLike: TypeAlias = str | bytes | os.PathLike[Any]

JSONExpressable = (
    bool
    | int
    | str
    | float
    | None
    | Iterable["JSONExpressable"]
    | Mapping[str, "JSONExpressable"]
)


@runtime_checkable
class SupportsToJSON(Protocol):
    """Object that supports rendering itself as a JSON expressible value.

    This should output the python container equivalent rather than an actual json
    string because common consumers of json-like data (e.g., corvic.clogging) expect to
    consume python data structures rather than serialized json.
    """

    def to_json(self) -> JSONExpressable: ...


JSONAble = JSONExpressable | SupportsToJSON


def to_json(val: JSONAble) -> JSONExpressable:
    """Render some value as a json expressible value."""
    if isinstance(val, SupportsToJSON):
        return val.to_json()
    return val


VectorSimilarityMetric: TypeAlias = Literal["cosine", "euclidean"]


__all__ = [
    "JSONAble",
    "JSONExpressable",
    "PathLike",
    "SupportsToJSON",
    "VectorSimilarityMetric",
    "to_json",
]
