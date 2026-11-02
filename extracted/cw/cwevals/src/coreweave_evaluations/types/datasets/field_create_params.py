# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Literal, Required, TypedDict

__all__ = ["FieldCreateParams", "Field"]


class FieldCreateParams(TypedDict, total=False):
    namespace: str
    """Namespace that assigned the scope reference."""

    scope_id: str
    """Project reference assigned by the namespace.

    For wandb, use the internal W&B project ID, not the project name or
    entity/project path.

    Percent-encode reserved characters so the reference occupies one URL path
    segment. Only printable ASCII is accepted. References are compared exactly,
    without parsing.
    """

    fields: Required[Iterable[Field]]


class Field(TypedDict, total=False):
    name: Required[str]

    source: Required[Literal["input", "output"]]

    value_type: Required[Literal["boolean", "integer", "number", "string", "json"]]
