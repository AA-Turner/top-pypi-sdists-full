from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ScopedOfferingRequest")


@_attrs_define
class ScopedOfferingRequest:
    """
    Attributes:
        uuid (str):
        name (str):
        has_live_resources (bool):
    """

    uuid: str
    name: str
    has_live_resources: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = self.uuid

        name = self.name

        has_live_resources = self.has_live_resources

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "name": name,
                "has_live_resources": has_live_resources,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uuid = d.pop("uuid")

        name = d.pop("name")

        has_live_resources = d.pop("has_live_resources")

        scoped_offering_request = cls(
            uuid=uuid,
            name=name,
            has_live_resources=has_live_resources,
        )

        scoped_offering_request.additional_properties = d
        return scoped_offering_request

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
