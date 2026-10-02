from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.maintenance_type_enum import MaintenanceTypeEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="PatchedMaintenanceAnnouncementTemplateRequest")


@_attrs_define
class PatchedMaintenanceAnnouncementTemplateRequest:
    """
    Attributes:
        name (Union[Unset, str]):
        message (Union[Unset, str]):
        maintenance_type (Union[Unset, MaintenanceTypeEnum]):
        service_provider (Union[Unset, str]): Service provider announcing the maintenance
    """

    name: Union[Unset, str] = UNSET
    message: Union[Unset, str] = UNSET
    maintenance_type: Union[Unset, MaintenanceTypeEnum] = UNSET
    service_provider: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        message = self.message

        maintenance_type: Union[Unset, int] = UNSET
        if not isinstance(self.maintenance_type, Unset):
            maintenance_type = self.maintenance_type.value

        service_provider = self.service_provider

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if message is not UNSET:
            field_dict["message"] = message
        if maintenance_type is not UNSET:
            field_dict["maintenance_type"] = maintenance_type
        if service_provider is not UNSET:
            field_dict["service_provider"] = service_provider

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name", UNSET)

        message = d.pop("message", UNSET)

        _maintenance_type = d.pop("maintenance_type", UNSET)
        maintenance_type: Union[Unset, MaintenanceTypeEnum]
        if isinstance(_maintenance_type, Unset):
            maintenance_type = UNSET
        else:
            maintenance_type = MaintenanceTypeEnum(_maintenance_type)

        service_provider = d.pop("service_provider", UNSET)

        patched_maintenance_announcement_template_request = cls(
            name=name,
            message=message,
            maintenance_type=maintenance_type,
            service_provider=service_provider,
        )

        patched_maintenance_announcement_template_request.additional_properties = d
        return patched_maintenance_announcement_template_request

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
