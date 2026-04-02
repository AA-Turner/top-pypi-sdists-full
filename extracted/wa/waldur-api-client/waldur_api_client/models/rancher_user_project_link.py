from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="RancherUserProjectLink")


@_attrs_define
class RancherUserProjectLink:
    """
    Attributes:
        project (str):
        role (str):
        project_name (str):
        project_uuid (UUID):
    """

    project: str
    role: str
    project_name: str
    project_uuid: UUID
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        project = self.project

        role = self.role

        project_name = self.project_name

        project_uuid = str(self.project_uuid)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "project": project,
                "role": role,
                "project_name": project_name,
                "project_uuid": project_uuid,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        project = d.pop("project")

        role = d.pop("role")

        project_name = d.pop("project_name")

        project_uuid = UUID(d.pop("project_uuid"))

        rancher_user_project_link = cls(
            project=project,
            role=role,
            project_name=project_name,
            project_uuid=project_uuid,
        )

        rancher_user_project_link.additional_properties = d
        return rancher_user_project_link

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
