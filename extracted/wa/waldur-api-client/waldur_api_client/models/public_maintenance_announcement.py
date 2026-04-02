import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.maintenance_type_enum import MaintenanceTypeEnum
from ..models.public_maintenance_announcement_state_enum import PublicMaintenanceAnnouncementStateEnum

if TYPE_CHECKING:
    from ..models.maintenance_announcement_offering import MaintenanceAnnouncementOffering


T = TypeVar("T", bound="PublicMaintenanceAnnouncement")


@_attrs_define
class PublicMaintenanceAnnouncement:
    """
    Attributes:
        url (str):
        uuid (UUID):
        name (str):
        message (str):
        maintenance_type (MaintenanceTypeEnum):
        maintenance_type_display (str):
        external_reference_url (str): Optional reference to an external maintenance tracker
        state (PublicMaintenanceAnnouncementStateEnum):
        scheduled_start (datetime.datetime): When the maintenance is scheduled to begin
        scheduled_end (datetime.datetime): When the maintenance is scheduled to complete
        actual_start (Union[None, datetime.datetime]): When the maintenance actually began
        actual_end (Union[None, datetime.datetime]): When the maintenance actually completed
        affected_offerings (list['MaintenanceAnnouncementOffering']):
        service_provider_name (str):
    """

    url: str
    uuid: UUID
    name: str
    message: str
    maintenance_type: MaintenanceTypeEnum
    maintenance_type_display: str
    external_reference_url: str
    state: PublicMaintenanceAnnouncementStateEnum
    scheduled_start: datetime.datetime
    scheduled_end: datetime.datetime
    actual_start: Union[None, datetime.datetime]
    actual_end: Union[None, datetime.datetime]
    affected_offerings: list["MaintenanceAnnouncementOffering"]
    service_provider_name: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        uuid = str(self.uuid)

        name = self.name

        message = self.message

        maintenance_type = self.maintenance_type.value

        maintenance_type_display = self.maintenance_type_display

        external_reference_url = self.external_reference_url

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

        affected_offerings = []
        for affected_offerings_item_data in self.affected_offerings:
            affected_offerings_item = affected_offerings_item_data.to_dict()
            affected_offerings.append(affected_offerings_item)

        service_provider_name = self.service_provider_name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "url": url,
                "uuid": uuid,
                "name": name,
                "message": message,
                "maintenance_type": maintenance_type,
                "maintenance_type_display": maintenance_type_display,
                "external_reference_url": external_reference_url,
                "state": state,
                "scheduled_start": scheduled_start,
                "scheduled_end": scheduled_end,
                "actual_start": actual_start,
                "actual_end": actual_end,
                "affected_offerings": affected_offerings,
                "service_provider_name": service_provider_name,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.maintenance_announcement_offering import MaintenanceAnnouncementOffering

        d = dict(src_dict)
        url = d.pop("url")

        uuid = UUID(d.pop("uuid"))

        name = d.pop("name")

        message = d.pop("message")

        maintenance_type = MaintenanceTypeEnum(d.pop("maintenance_type"))

        maintenance_type_display = d.pop("maintenance_type_display")

        external_reference_url = d.pop("external_reference_url")

        state = PublicMaintenanceAnnouncementStateEnum(d.pop("state"))

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

        affected_offerings = []
        _affected_offerings = d.pop("affected_offerings")
        for affected_offerings_item_data in _affected_offerings:
            affected_offerings_item = MaintenanceAnnouncementOffering.from_dict(affected_offerings_item_data)

            affected_offerings.append(affected_offerings_item)

        service_provider_name = d.pop("service_provider_name")

        public_maintenance_announcement = cls(
            url=url,
            uuid=uuid,
            name=name,
            message=message,
            maintenance_type=maintenance_type,
            maintenance_type_display=maintenance_type_display,
            external_reference_url=external_reference_url,
            state=state,
            scheduled_start=scheduled_start,
            scheduled_end=scheduled_end,
            actual_start=actual_start,
            actual_end=actual_end,
            affected_offerings=affected_offerings,
            service_provider_name=service_provider_name,
        )

        public_maintenance_announcement.additional_properties = d
        return public_maintenance_announcement

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
