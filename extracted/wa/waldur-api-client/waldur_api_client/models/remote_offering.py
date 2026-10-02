from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="RemoteOffering")


@_attrs_define
class RemoteOffering:
    """
    Attributes:
        uuid (UUID):
        name (str):
        type_ (str):
        state (str):
        category_title (str):
    """

    uuid: UUID
    name: str
    type_: str
    state: str
    category_title: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        name = self.name

        type_ = self.type_

        state = self.state

        category_title = self.category_title

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "name": name,
                "type": type_,
                "state": state,
                "category_title": category_title,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        name = d.pop("name")

        type_ = d.pop("type")

        state = d.pop("state")

        category_title = d.pop("category_title")

        remote_offering = cls(
            uuid=uuid,
            name=name,
            type_=type_,
            state=state,
            category_title=category_title,
        )

        remote_offering.additional_properties = d
        return remote_offering

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
