from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="OfferingMergeUnmatchedComponent")


@_attrs_define
class OfferingMergeUnmatchedComponent:
    """
    Attributes:
        offering_uuid (str):
        type_ (str):
        name (str):
    """

    offering_uuid: str
    type_: str
    name: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        offering_uuid = self.offering_uuid

        type_ = self.type_

        name = self.name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "offering_uuid": offering_uuid,
                "type": type_,
                "name": name,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        offering_uuid = d.pop("offering_uuid")

        type_ = d.pop("type")

        name = d.pop("name")

        offering_merge_unmatched_component = cls(
            offering_uuid=offering_uuid,
            type_=type_,
            name=name,
        )

        offering_merge_unmatched_component.additional_properties = d
        return offering_merge_unmatched_component

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
