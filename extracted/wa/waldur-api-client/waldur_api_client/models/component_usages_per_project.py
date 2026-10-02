from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ComponentUsagesPerProject")


@_attrs_define
class ComponentUsagesPerProject:
    """
    Attributes:
        project_uuid (UUID): UUID of the project
        component_type (str): Type of the component
        usage (int): Total usage for the component
    """

    project_uuid: UUID
    component_type: str
    usage: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        project_uuid = str(self.project_uuid)

        component_type = self.component_type

        usage = self.usage

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "project_uuid": project_uuid,
                "component_type": component_type,
                "usage": usage,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        project_uuid = UUID(d.pop("project_uuid"))

        component_type = d.pop("component_type")

        usage = d.pop("usage")

        component_usages_per_project = cls(
            project_uuid=project_uuid,
            component_type=component_type,
            usage=usage,
        )

        component_usages_per_project.additional_properties = d
        return component_usages_per_project

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
