from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="AzureSqlServerRequest")


@_attrs_define
class AzureSqlServerRequest:
    """
    Attributes:
        name (str):
        service_settings (str):
        project (str):
        location (str):
        description (Union[Unset, str]):
        storage_mb (Union[None, Unset, int]):
    """

    name: str
    service_settings: str
    project: str
    location: str
    description: Union[Unset, str] = UNSET
    storage_mb: Union[None, Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        service_settings = self.service_settings

        project = self.project

        location = self.location

        description = self.description

        storage_mb: Union[None, Unset, int]
        if isinstance(self.storage_mb, Unset):
            storage_mb = UNSET
        else:
            storage_mb = self.storage_mb

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "service_settings": service_settings,
                "project": project,
                "location": location,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if storage_mb is not UNSET:
            field_dict["storage_mb"] = storage_mb

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        service_settings = d.pop("service_settings")

        project = d.pop("project")

        location = d.pop("location")

        description = d.pop("description", UNSET)

        def _parse_storage_mb(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        storage_mb = _parse_storage_mb(d.pop("storage_mb", UNSET))

        azure_sql_server_request = cls(
            name=name,
            service_settings=service_settings,
            project=project,
            location=location,
            description=description,
            storage_mb=storage_mb,
        )

        azure_sql_server_request.additional_properties = d
        return azure_sql_server_request

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
