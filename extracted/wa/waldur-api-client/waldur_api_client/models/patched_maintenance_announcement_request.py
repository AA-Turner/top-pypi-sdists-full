import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.maintenance_type_enum import MaintenanceTypeEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="PatchedMaintenanceAnnouncementRequest")


@_attrs_define
class PatchedMaintenanceAnnouncementRequest:
    """
    Attributes:
        name (Union[Unset, str]):
        message (Union[Unset, str]):
        internal_notes (Union[Unset, str]):
        maintenance_type (Union[Unset, MaintenanceTypeEnum]):
        external_reference_url (Union[Unset, str]): Optional reference to an external maintenance tracker
        scheduled_start (Union[Unset, datetime.datetime]): When the maintenance is scheduled to begin
        scheduled_end (Union[Unset, datetime.datetime]): When the maintenance is scheduled to complete
        service_provider (Union[Unset, str]): Service provider announcing the maintenance
    """

    name: Union[Unset, str] = UNSET
    message: Union[Unset, str] = UNSET
    internal_notes: Union[Unset, str] = UNSET
    maintenance_type: Union[Unset, MaintenanceTypeEnum] = UNSET
    external_reference_url: Union[Unset, str] = UNSET
    scheduled_start: Union[Unset, datetime.datetime] = UNSET
    scheduled_end: Union[Unset, datetime.datetime] = UNSET
    service_provider: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        message = self.message

        internal_notes = self.internal_notes

        maintenance_type: Union[Unset, int] = UNSET
        if not isinstance(self.maintenance_type, Unset):
            maintenance_type = self.maintenance_type.value

        external_reference_url = self.external_reference_url

        scheduled_start: Union[Unset, str] = UNSET
        if not isinstance(self.scheduled_start, Unset):
            scheduled_start = self.scheduled_start.isoformat()

        scheduled_end: Union[Unset, str] = UNSET
        if not isinstance(self.scheduled_end, Unset):
            scheduled_end = self.scheduled_end.isoformat()

        service_provider = self.service_provider

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if message is not UNSET:
            field_dict["message"] = message
        if internal_notes is not UNSET:
            field_dict["internal_notes"] = internal_notes
        if maintenance_type is not UNSET:
            field_dict["maintenance_type"] = maintenance_type
        if external_reference_url is not UNSET:
            field_dict["external_reference_url"] = external_reference_url
        if scheduled_start is not UNSET:
            field_dict["scheduled_start"] = scheduled_start
        if scheduled_end is not UNSET:
            field_dict["scheduled_end"] = scheduled_end
        if service_provider is not UNSET:
            field_dict["service_provider"] = service_provider

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name", UNSET)

        message = d.pop("message", UNSET)

        internal_notes = d.pop("internal_notes", UNSET)

        _maintenance_type = d.pop("maintenance_type", UNSET)
        maintenance_type: Union[Unset, MaintenanceTypeEnum]
        if isinstance(_maintenance_type, Unset):
            maintenance_type = UNSET
        else:
            maintenance_type = MaintenanceTypeEnum(_maintenance_type)

        external_reference_url = d.pop("external_reference_url", UNSET)

        _scheduled_start = d.pop("scheduled_start", UNSET)
        scheduled_start: Union[Unset, datetime.datetime]
        if isinstance(_scheduled_start, Unset):
            scheduled_start = UNSET
        else:
            scheduled_start = isoparse(_scheduled_start)

        _scheduled_end = d.pop("scheduled_end", UNSET)
        scheduled_end: Union[Unset, datetime.datetime]
        if isinstance(_scheduled_end, Unset):
            scheduled_end = UNSET
        else:
            scheduled_end = isoparse(_scheduled_end)

        service_provider = d.pop("service_provider", UNSET)

        patched_maintenance_announcement_request = cls(
            name=name,
            message=message,
            internal_notes=internal_notes,
            maintenance_type=maintenance_type,
            external_reference_url=external_reference_url,
            scheduled_start=scheduled_start,
            scheduled_end=scheduled_end,
            service_provider=service_provider,
        )

        patched_maintenance_announcement_request.additional_properties = d
        return patched_maintenance_announcement_request

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
