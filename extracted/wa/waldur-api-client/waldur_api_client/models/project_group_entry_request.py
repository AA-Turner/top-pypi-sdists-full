from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ProjectGroupEntryRequest")


@_attrs_define
class ProjectGroupEntryRequest:
    """
    Attributes:
        project (str): Project UUID, or its slug when exactly one project with that slug has a resource or order at the
            service provider.
        gid (int):
        name (Union[Unset, str]): Group name, matching ^[a-z_][a-z0-9_-]{0,31}$; derived from the project slug when
            omitted.
    """

    project: str
    gid: int
    name: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        project = self.project

        gid = self.gid

        name = self.name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "project": project,
                "gid": gid,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        project = d.pop("project")

        gid = d.pop("gid")

        name = d.pop("name", UNSET)

        project_group_entry_request = cls(
            project=project,
            gid=gid,
            name=name,
        )

        project_group_entry_request.additional_properties = d
        return project_group_entry_request

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
