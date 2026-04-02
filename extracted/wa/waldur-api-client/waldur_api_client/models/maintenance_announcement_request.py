import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.maintenance_type_enum import MaintenanceTypeEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="MaintenanceAnnouncementRequest")


@_attrs_define
class MaintenanceAnnouncementRequest:
    """
    Attributes:
        name (str):
        scheduled_start (datetime.datetime): When the maintenance is scheduled to begin
        scheduled_end (datetime.datetime): When the maintenance is scheduled to complete
        service_provider (str): Service provider announcing the maintenance
        message (Union[Unset, str]):
        internal_notes (Union[Unset, str]):
        maintenance_type (Union[Unset, MaintenanceTypeEnum]):
        external_reference_url (Union[Unset, str]): Optional reference to an external maintenance tracker
    """

    name: str
    scheduled_start: datetime.datetime
    scheduled_end: datetime.datetime
    service_provider: str
    message: Union[Unset, str] = UNSET
    internal_notes: Union[Unset, str] = UNSET
    maintenance_type: Union[Unset, MaintenanceTypeEnum] = UNSET
    external_reference_url: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        scheduled_start = self.scheduled_start.isoformat()

        scheduled_end = self.scheduled_end.isoformat()

        service_provider = self.service_provider

        message = self.message

        internal_notes = self.internal_notes

        maintenance_type: Union[Unset, int] = UNSET
        if not isinstance(self.maintenance_type, Unset):
            maintenance_type = self.maintenance_type.value

        external_reference_url = self.external_reference_url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "scheduled_start": scheduled_start,
                "scheduled_end": scheduled_end,
                "service_provider": service_provider,
            }
        )
        if message is not UNSET:
            field_dict["message"] = message
        if internal_notes is not UNSET:
            field_dict["internal_notes"] = internal_notes
        if maintenance_type is not UNSET:
            field_dict["maintenance_type"] = maintenance_type
        if external_reference_url is not UNSET:
            field_dict["external_reference_url"] = external_reference_url

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        scheduled_start = isoparse(d.pop("scheduled_start"))

        scheduled_end = isoparse(d.pop("scheduled_end"))

        service_provider = d.pop("service_provider")

        message = d.pop("message", UNSET)

        internal_notes = d.pop("internal_notes", UNSET)

        _maintenance_type = d.pop("maintenance_type", UNSET)
        maintenance_type: Union[Unset, MaintenanceTypeEnum]
        if isinstance(_maintenance_type, Unset):
            maintenance_type = UNSET
        else:
            maintenance_type = MaintenanceTypeEnum(_maintenance_type)

        external_reference_url = d.pop("external_reference_url", UNSET)

        maintenance_announcement_request = cls(
            name=name,
            scheduled_start=scheduled_start,
            scheduled_end=scheduled_end,
            service_provider=service_provider,
            message=message,
            internal_notes=internal_notes,
            maintenance_type=maintenance_type,
            external_reference_url=external_reference_url,
        )

        maintenance_announcement_request.additional_properties = d
        return maintenance_announcement_request

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
