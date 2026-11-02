# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Literal, Required, TypedDict

__all__ = ["ColumnCreateParams", "DatasetField", "Scorer"]


class ColumnCreateParams(TypedDict, total=False):
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

    dataset_fields: Iterable[DatasetField]
    """Input and output columns to declare, with a name and value type for each."""

    scorers: Iterable[Scorer]
    """Named score columns to declare, with the value type each score must use."""


class DatasetField(TypedDict, total=False):
    name: Required[str]

    source: Required[Literal["input", "output"]]

    value_type: Required[Literal["boolean", "integer", "number", "string", "json"]]
    """JSON type accepted by this column.

    Use json for ordinary JSON fields and for media extension values.
    """

    extension_schema_version: int
    """Version of the media format.

    Set together with extension_type. Omit both for an ordinary field.
    """

    extension_type: Literal["wandb-image", "wandb-audio", "wandb-video"]
    """Media format stored in this field.

    Set together with extension_schema_version. Omit both for an ordinary field.
    """


class Scorer(TypedDict, total=False):
    name: Required[str]
    """Name used as a key in each row's scores object.

    Leading and trailing whitespace are not allowed.
    """

    value_type: Required[Literal["boolean", "integer", "number", "string"]]
