import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.maintenance_announcement_state_enum import MaintenanceAnnouncementStateEnum
from ..models.maintenance_type_enum import MaintenanceTypeEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.maintenance_announcement_offering import MaintenanceAnnouncementOffering


T = TypeVar("T", bound="MaintenanceAnnouncement")


@_attrs_define
class MaintenanceAnnouncement:
    """
    Attributes:
        url (str):
        uuid (UUID):
        name (str):
        state (MaintenanceAnnouncementStateEnum):
        scheduled_start (datetime.datetime): When the maintenance is scheduled to begin
        scheduled_end (datetime.datetime): When the maintenance is scheduled to complete
        actual_start (Union[None, datetime.datetime]): When the maintenance actually began
        actual_end (Union[None, datetime.datetime]): When the maintenance actually completed
        service_provider (str): Service provider announcing the maintenance
        created_by (Union[None, str]):
        affected_offerings (list['MaintenanceAnnouncementOffering']):
        service_provider_name (str):
        backend_id (str):
        message (Union[Unset, str]):
        internal_notes (Union[Unset, str]):
        maintenance_type (Union[Unset, MaintenanceTypeEnum]):
        external_reference_url (Union[Unset, str]): Optional reference to an external maintenance tracker
    """

    url: str
    uuid: UUID
    name: str
    state: MaintenanceAnnouncementStateEnum
    scheduled_start: datetime.datetime
    scheduled_end: datetime.datetime
    actual_start: Union[None, datetime.datetime]
    actual_end: Union[None, datetime.datetime]
    service_provider: str
    created_by: Union[None, str]
    affected_offerings: list["MaintenanceAnnouncementOffering"]
    service_provider_name: str
    backend_id: str
    message: Union[Unset, str] = UNSET
    internal_notes: Union[Unset, str] = UNSET
    maintenance_type: Union[Unset, MaintenanceTypeEnum] = UNSET
    external_reference_url: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        uuid = str(self.uuid)

        name = self.name

        state = self.state.value

        scheduled_start = self.scheduled_start.isoformat()

        scheduled_end = self.scheduled_end.isoformat()

        actual_start: Union[None, str]
        if isinstance(self.actual_start, datetime.datetime):
            actual_start = self.actual_start.isoformat()
        else:
            actual_start = self.actual_start

        actual_end: Union[None, str]
        if isinstance(self.actual_end, datetime.datetime):
            actual_end = self.actual_end.isoformat()
        else:
            actual_end = self.actual_end

        service_provider = self.service_provider

        created_by: Union[None, str]
        created_by = self.created_by

        affected_offerings = []
        for affected_offerings_item_data in self.affected_offerings:
            affected_offerings_item = affected_offerings_item_data.to_dict()
            affected_offerings.append(affected_offerings_item)

        service_provider_name = self.service_provider_name

        backend_id = self.backend_id

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
                "url": url,
                "uuid": uuid,
                "name": name,
                "state": state,
                "scheduled_start": scheduled_start,
                "scheduled_end": scheduled_end,
                "actual_start": actual_start,
                "actual_end": actual_end,
                "service_provider": service_provider,
                "created_by": created_by,
                "affected_offerings": affected_offerings,
                "service_provider_name": service_provider_name,
                "backend_id": backend_id,
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
        from ..models.maintenance_announcement_offering import MaintenanceAnnouncementOffering

        d = dict(src_dict)
        url = d.pop("url")

        uuid = UUID(d.pop("uuid"))

        name = d.pop("name")

        state = MaintenanceAnnouncementStateEnum(d.pop("state"))

        scheduled_start = isoparse(d.pop("scheduled_start"))

        scheduled_end = isoparse(d.pop("scheduled_end"))

        def _parse_actual_start(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                actual_start_type_0 = isoparse(data)

                return actual_start_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        actual_start = _parse_actual_start(d.pop("actual_start"))

        def _parse_actual_end(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                actual_end_type_0 = isoparse(data)

                return actual_end_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        actual_end = _parse_actual_end(d.pop("actual_end"))

        service_provider = d.pop("service_provider")

        def _parse_created_by(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        created_by = _parse_created_by(d.pop("created_by"))

        affected_offerings = []
        _affected_offerings = d.pop("affected_offerings")
        for affected_offerings_item_data in _affected_offerings:
            affected_offerings_item = MaintenanceAnnouncementOffering.from_dict(affected_offerings_item_data)

            affected_offerings.append(affected_offerings_item)

        service_provider_name = d.pop("service_provider_name")

        backend_id = d.pop("backend_id")

        message = d.pop("message", UNSET)

        internal_notes = d.pop("internal_notes", UNSET)

        _maintenance_type = d.pop("maintenance_type", UNSET)
        maintenance_type: Union[Unset, MaintenanceTypeEnum]
        if isinstance(_maintenance_type, Unset):
            maintenance_type = UNSET
        else:
            maintenance_type = MaintenanceTypeEnum(_maintenance_type)

        external_reference_url = d.pop("external_reference_url", UNSET)

        maintenance_announcement = cls(
            url=url,
            uuid=uuid,
            name=name,
            state=state,
            scheduled_start=scheduled_start,
            scheduled_end=scheduled_end,
            actual_start=actual_start,
            actual_end=actual_end,
            service_provider=service_provider,
            created_by=created_by,
            affected_offerings=affected_offerings,
            service_provider_name=service_provider_name,
            backend_id=backend_id,
            message=message,
            internal_notes=internal_notes,
            maintenance_type=maintenance_type,
            external_reference_url=external_reference_url,
        )

        maintenance_announcement.additional_properties = d
        return maintenance_announcement

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
