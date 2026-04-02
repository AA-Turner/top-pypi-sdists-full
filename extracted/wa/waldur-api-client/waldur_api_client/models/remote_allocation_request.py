from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="RemoteAllocationRequest")


@_attrs_define
class RemoteAllocationRequest:
    """
    Attributes:
        name (str):
        service_settings (str):
        project (str):
        description (Union[Unset, str]):
        node_limit (Union[Unset, int]):
        remote_project_identifier (Union[None, Unset, str]): The identifier of the project in the remote OpenPortal
            instance.
    """

    name: str
    service_settings: str
    project: str
    description: Union[Unset, str] = UNSET
    node_limit: Union[Unset, int] = UNSET
    remote_project_identifier: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        service_settings = self.service_settings

        project = self.project

        description = self.description

        node_limit = self.node_limit

        remote_project_identifier: Union[None, Unset, str]
        if isinstance(self.remote_project_identifier, Unset):
            remote_project_identifier = UNSET
        else:
            remote_project_identifier = self.remote_project_identifier

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "service_settings": service_settings,
                "project": project,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if node_limit is not UNSET:
            field_dict["node_limit"] = node_limit
        if remote_project_identifier is not UNSET:
            field_dict["remote_project_identifier"] = remote_project_identifier

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        service_settings = d.pop("service_settings")

        project = d.pop("project")

        description = d.pop("description", UNSET)

        node_limit = d.pop("node_limit", UNSET)

        def _parse_remote_project_identifier(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        remote_project_identifier = _parse_remote_project_identifier(d.pop("remote_project_identifier", UNSET))

        remote_allocation_request = cls(
            name=name,
            service_settings=service_settings,
            project=project,
            description=description,
            node_limit=node_limit,
            remote_project_identifier=remote_project_identifier,
        )

        remote_allocation_request.additional_properties = d
        return remote_allocation_request

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
