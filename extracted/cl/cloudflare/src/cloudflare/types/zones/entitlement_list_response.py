# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Union
from typing_extensions import Literal, TypeAlias

from ..._models import BaseModel

__all__ = ["EntitlementListResponse", "Allocation", "AllocationValue", "AllocationValueUnionMember4", "Feature"]


class AllocationValueUnionMember4(BaseModel):
    max: int

    min: int


AllocationValue: TypeAlias = Union[bool, int, str, List[float], AllocationValueUnionMember4]


class Allocation(BaseModel):
    """Represents the allocation value for an entitlement.

    The shape of `value` depends on `type`: `bool` uses a boolean, `max_count` uses an integer, `enum_number` uses an array of numbers, `range` uses an object with `min` and `max` integer fields, and `string` uses a string.
    """

    type: Literal["bool", "max_count", "enum_number", "range", "string"]
    """Allocation type discriminator."""

    value: AllocationValue
    """
    Contains the allocation value whose concrete type the `type` field determines:
    bool yields a boolean, max_count yields an integer, enum_number yields an array
    of numbers, range yields an object with `min` and `max`, and string yields a
    string.
    """


class Feature(BaseModel):
    """Describes a product feature associated with an entitlement."""

    id: int
    """Numeric identifier of the feature."""

    feature_set: str
    """The logical grouping (set) this feature belongs to."""

    key: str
    """Unique string key for the feature."""

    name: str
    """Human-readable name of the feature."""


class EntitlementListResponse(BaseModel):
    """A single entitlement record for a zone or account."""

    id: str
    """Entitlement identifier — equal to the feature key."""

    allocation: Allocation
    """Represents the allocation value for an entitlement.

    The shape of `value` depends on `type`: `bool` uses a boolean, `max_count` uses
    an integer, `enum_number` uses an array of numbers, `range` uses an object with
    `min` and `max` integer fields, and `string` uses a string.
    """

    created_date: str
    """
    ISO 8601 timestamp (microsecond precision, no timezone offset) when the
    entitlement was created. Format: `YYYY-MM-DDTHH:MM:SS.ffffff`.
    """

    deleted_date: str
    """
    ISO 8601 timestamp when the entitlement was deleted, or empty string if not
    deleted.
    """

    edited_date: str
    """
    ISO 8601 timestamp (microsecond precision, no timezone offset) when the
    entitlement was last edited.
    """

    feature: Feature
    """Describes a product feature associated with an entitlement."""
