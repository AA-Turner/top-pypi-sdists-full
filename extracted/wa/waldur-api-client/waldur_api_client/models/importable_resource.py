from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ImportableResource")


@_attrs_define
class ImportableResource:
    """
    Attributes:
        backend_id (str): Backend identifier of the resource
        name (str): Name of the resource
        type_ (str): Type of the resource
        description (str): Description of the resource
    """

    backend_id: str
    name: str
    type_: str
    description: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        backend_id = self.backend_id

        name = self.name

        type_ = self.type_

        description = self.description

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "backend_id": backend_id,
                "name": name,
                "type": type_,
                "description": description,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        backend_id = d.pop("backend_id")

        name = d.pop("name")

        type_ = d.pop("type")

        description = d.pop("description")

        importable_resource = cls(
            backend_id=backend_id,
            name=name,
            type_=type_,
            description=description,
        )

        importable_resource.additional_properties = d
        return importable_resource

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
