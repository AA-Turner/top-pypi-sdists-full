from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field


from typing import cast
from typing import Literal

if TYPE_CHECKING:
    from ..models.usage_attributes import UsageAttributes


T = TypeVar("T", bound="UsageResource")


@_attrs_define
class UsageResource:
    """JSON:API resource envelope for a usage counter.

    Example:
        {'attributes': {'limit_key': 'flags.managed_flags', 'period': 'current', 'value': 5}, 'id':
            '550e8400-e29b-41d4-a716-446655440000', 'type': 'usage'}

    Attributes:
        id (str):
        type_ (Literal['usage']):
        attributes (UsageAttributes): Usage counter for a single metered limit.
    """

    id: str
    type_: Literal["usage"]
    attributes: UsageAttributes
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        type_ = self.type_

        attributes = self.attributes.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "type": type_,
                "attributes": attributes,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.usage_attributes import UsageAttributes

        d = dict(src_dict)
        id = d.pop("id")

        type_ = cast(Literal["usage"], d.pop("type"))
        if type_ != "usage":
            raise ValueError(f"type must match const 'usage', got '{type_}'")

        attributes = UsageAttributes.from_dict(d.pop("attributes"))

        usage_resource = cls(
            id=id,
            type_=type_,
            attributes=attributes,
        )

        usage_resource.additional_properties = d
        return usage_resource

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
