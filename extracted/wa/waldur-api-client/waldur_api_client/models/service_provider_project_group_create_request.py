from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ServiceProviderProjectGroupCreateRequest")


@_attrs_define
class ServiceProviderProjectGroupCreateRequest:
    """
    Attributes:
        project (str): Project UUID, or its slug when exactly one project with that slug has a resource or order at the
            service provider.
        gid (int):
        service_provider (UUID):
        name (Union[Unset, str]): Group name, matching ^[a-z_][a-z0-9_-]{0,31}$; derived from the project slug when
            omitted.
        allow_outside_range (Union[Unset, bool]): Accept a GID outside the range project groups draw from, e.g. one a
            directory assigned before Waldur managed it. Default: False.
    """

    project: str
    gid: int
    service_provider: UUID
    name: Union[Unset, str] = UNSET
    allow_outside_range: Union[Unset, bool] = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        project = self.project

        gid = self.gid

        service_provider = str(self.service_provider)

        name = self.name

        allow_outside_range = self.allow_outside_range

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "project": project,
                "gid": gid,
                "service_provider": service_provider,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name
        if allow_outside_range is not UNSET:
            field_dict["allow_outside_range"] = allow_outside_range

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        project = d.pop("project")

        gid = d.pop("gid")

        service_provider = UUID(d.pop("service_provider"))

        name = d.pop("name", UNSET)

        allow_outside_range = d.pop("allow_outside_range", UNSET)

        service_provider_project_group_create_request = cls(
            project=project,
            gid=gid,
            service_provider=service_provider,
            name=name,
            allow_outside_range=allow_outside_range,
        )

        service_provider_project_group_create_request.additional_properties = d
        return service_provider_project_group_create_request

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
