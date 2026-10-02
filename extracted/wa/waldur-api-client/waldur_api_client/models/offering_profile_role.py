from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="OfferingProfileRole")


@_attrs_define
class OfferingProfileRole:
    """
    Attributes:
        uuid (str):
        name (str):
        content_type (Union[None, str]):
        description (str):
    """

    uuid: str
    name: str
    content_type: Union[None, str]
    description: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = self.uuid

        name = self.name

        content_type: Union[None, str]
        content_type = self.content_type

        description = self.description

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "name": name,
                "content_type": content_type,
                "description": description,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uuid = d.pop("uuid")

        name = d.pop("name")

        def _parse_content_type(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        content_type = _parse_content_type(d.pop("content_type"))

        description = d.pop("description")

        offering_profile_role = cls(
            uuid=uuid,
            name=name,
            content_type=content_type,
            description=description,
        )

        offering_profile_role.additional_properties = d
        return offering_profile_role

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
