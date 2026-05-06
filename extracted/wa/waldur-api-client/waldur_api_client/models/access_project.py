from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.access_resource import AccessResource


T = TypeVar("T", bound="AccessProject")


@_attrs_define
class AccessProject:
    """
    Attributes:
        name (str):
        resources (list['AccessResource']):
    """

    name: str
    resources: list["AccessResource"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        resources = []
        for resources_item_data in self.resources:
            resources_item = resources_item_data.to_dict()
            resources.append(resources_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "resources": resources,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.access_resource import AccessResource

        d = dict(src_dict)
        name = d.pop("name")

        resources = []
        _resources = d.pop("resources")
        for resources_item_data in _resources:
            resources_item = AccessResource.from_dict(resources_item_data)

            resources.append(resources_item)

        access_project = cls(
            name=name,
            resources=resources,
        )

        access_project.additional_properties = d
        return access_project

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
