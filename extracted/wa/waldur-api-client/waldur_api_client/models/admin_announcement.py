import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.admin_announcement_type_enum import AdminAnnouncementTypeEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.admin_announcement_maintenance_affected_offerings_item import (
        AdminAnnouncementMaintenanceAffectedOfferingsItem,
    )


T = TypeVar("T", bound="AdminAnnouncement")


@_attrs_define
class AdminAnnouncement:
    """
    Attributes:
        uuid (Union[Unset, UUID]):
        description (Union[Unset, str]):
        active_from (Union[Unset, datetime.datetime]):
        active_to (Union[Unset, datetime.datetime]):
        is_active (Union[Unset, bool]):
        type_ (Union[Unset, AdminAnnouncementTypeEnum]):
        created (Union[Unset, datetime.datetime]):
        maintenance_uuid (Union[Unset, str]):
        maintenance_name (Union[Unset, str]):
        maintenance_type (Union[Unset, str]):
        maintenance_state (Union[Unset, str]):
        maintenance_scheduled_start (Union[Unset, datetime.datetime]):
        maintenance_scheduled_end (Union[Unset, datetime.datetime]):
        maintenance_service_provider (Union[Unset, str]):
        maintenance_affected_offerings (Union[Unset, list['AdminAnnouncementMaintenanceAffectedOfferingsItem']]):
        maintenance_external_reference_url (Union[Unset, str]):
    """

    uuid: Union[Unset, UUID] = UNSET
    description: Union[Unset, str] = UNSET
    active_from: Union[Unset, datetime.datetime] = UNSET
    active_to: Union[Unset, datetime.datetime] = UNSET
    is_active: Union[Unset, bool] = UNSET
    type_: Union[Unset, AdminAnnouncementTypeEnum] = UNSET
    created: Union[Unset, datetime.datetime] = UNSET
    maintenance_uuid: Union[Unset, str] = UNSET
    maintenance_name: Union[Unset, str] = UNSET
    maintenance_type: Union[Unset, str] = UNSET
    maintenance_state: Union[Unset, str] = UNSET
    maintenance_scheduled_start: Union[Unset, datetime.datetime] = UNSET
    maintenance_scheduled_end: Union[Unset, datetime.datetime] = UNSET
    maintenance_service_provider: Union[Unset, str] = UNSET
    maintenance_affected_offerings: Union[Unset, list["AdminAnnouncementMaintenanceAffectedOfferingsItem"]] = UNSET
    maintenance_external_reference_url: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid: Union[Unset, str] = UNSET
        if not isinstance(self.uuid, Unset):
            uuid = str(self.uuid)

        description = self.description

        active_from: Union[Unset, str] = UNSET
        if not isinstance(self.active_from, Unset):
            active_from = self.active_from.isoformat()

        active_to: Union[Unset, str] = UNSET
        if not isinstance(self.active_to, Unset):
            active_to = self.active_to.isoformat()

        is_active = self.is_active

        type_: Union[Unset, str] = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_.value

        created: Union[Unset, str] = UNSET
        if not isinstance(self.created, Unset):
            created = self.created.isoformat()

        maintenance_uuid = self.maintenance_uuid

        maintenance_name = self.maintenance_name

        maintenance_type = self.maintenance_type

        maintenance_state = self.maintenance_state

        maintenance_scheduled_start: Union[Unset, str] = UNSET
        if not isinstance(self.maintenance_scheduled_start, Unset):
            maintenance_scheduled_start = self.maintenance_scheduled_start.isoformat()

        maintenance_scheduled_end: Union[Unset, str] = UNSET
        if not isinstance(self.maintenance_scheduled_end, Unset):
            maintenance_scheduled_end = self.maintenance_scheduled_end.isoformat()

        maintenance_service_provider = self.maintenance_service_provider

        maintenance_affected_offerings: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.maintenance_affected_offerings, Unset):
            maintenance_affected_offerings = []
            for maintenance_affected_offerings_item_data in self.maintenance_affected_offerings:
                maintenance_affected_offerings_item = maintenance_affected_offerings_item_data.to_dict()
                maintenance_affected_offerings.append(maintenance_affected_offerings_item)

        maintenance_external_reference_url = self.maintenance_external_reference_url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if uuid is not UNSET:
            field_dict["uuid"] = uuid
        if description is not UNSET:
            field_dict["description"] = description
        if active_from is not UNSET:
            field_dict["active_from"] = active_from
        if active_to is not UNSET:
            field_dict["active_to"] = active_to
        if is_active is not UNSET:
            field_dict["is_active"] = is_active
        if type_ is not UNSET:
            field_dict["type"] = type_
        if created is not UNSET:
            field_dict["created"] = created
        if maintenance_uuid is not UNSET:
            field_dict["maintenance_uuid"] = maintenance_uuid
        if maintenance_name is not UNSET:
            field_dict["maintenance_name"] = maintenance_name
        if maintenance_type is not UNSET:
            field_dict["maintenance_type"] = maintenance_type
        if maintenance_state is not UNSET:
            field_dict["maintenance_state"] = maintenance_state
        if maintenance_scheduled_start is not UNSET:
            field_dict["maintenance_scheduled_start"] = maintenance_scheduled_start
        if maintenance_scheduled_end is not UNSET:
            field_dict["maintenance_scheduled_end"] = maintenance_scheduled_end
        if maintenance_service_provider is not UNSET:
            field_dict["maintenance_service_provider"] = maintenance_service_provider
        if maintenance_affected_offerings is not UNSET:
            field_dict["maintenance_affected_offerings"] = maintenance_affected_offerings
        if maintenance_external_reference_url is not UNSET:
            field_dict["maintenance_external_reference_url"] = maintenance_external_reference_url

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.admin_announcement_maintenance_affected_offerings_item import (
            AdminAnnouncementMaintenanceAffectedOfferingsItem,
        )

        d = dict(src_dict)
        _uuid = d.pop("uuid", UNSET)
        uuid: Union[Unset, UUID]
        if isinstance(_uuid, Unset):
            uuid = UNSET
        else:
            uuid = UUID(_uuid)

        description = d.pop("description", UNSET)

        _active_from = d.pop("active_from", UNSET)
        active_from: Union[Unset, datetime.datetime]
        if isinstance(_active_from, Unset):
            active_from = UNSET
        else:
            active_from = isoparse(_active_from)

        _active_to = d.pop("active_to", UNSET)
        active_to: Union[Unset, datetime.datetime]
        if isinstance(_active_to, Unset):
            active_to = UNSET
        else:
            active_to = isoparse(_active_to)

        is_active = d.pop("is_active", UNSET)

        _type_ = d.pop("type", UNSET)
        type_: Union[Unset, AdminAnnouncementTypeEnum]
        if isinstance(_type_, Unset):
            type_ = UNSET
        else:
            type_ = AdminAnnouncementTypeEnum(_type_)

        _created = d.pop("created", UNSET)
        created: Union[Unset, datetime.datetime]
        if isinstance(_created, Unset):
            created = UNSET
        else:
            created = isoparse(_created)

        maintenance_uuid = d.pop("maintenance_uuid", UNSET)

        maintenance_name = d.pop("maintenance_name", UNSET)

        maintenance_type = d.pop("maintenance_type", UNSET)

        maintenance_state = d.pop("maintenance_state", UNSET)

        _maintenance_scheduled_start = d.pop("maintenance_scheduled_start", UNSET)
        maintenance_scheduled_start: Union[Unset, datetime.datetime]
        if isinstance(_maintenance_scheduled_start, Unset):
            maintenance_scheduled_start = UNSET
        else:
            maintenance_scheduled_start = isoparse(_maintenance_scheduled_start)

        _maintenance_scheduled_end = d.pop("maintenance_scheduled_end", UNSET)
        maintenance_scheduled_end: Union[Unset, datetime.datetime]
        if isinstance(_maintenance_scheduled_end, Unset):
            maintenance_scheduled_end = UNSET
        else:
            maintenance_scheduled_end = isoparse(_maintenance_scheduled_end)

        maintenance_service_provider = d.pop("maintenance_service_provider", UNSET)

        maintenance_affected_offerings = []
        _maintenance_affected_offerings = d.pop("maintenance_affected_offerings", UNSET)
        for maintenance_affected_offerings_item_data in _maintenance_affected_offerings or []:
            maintenance_affected_offerings_item = AdminAnnouncementMaintenanceAffectedOfferingsItem.from_dict(
                maintenance_affected_offerings_item_data
            )

            maintenance_affected_offerings.append(maintenance_affected_offerings_item)

        maintenance_external_reference_url = d.pop("maintenance_external_reference_url", UNSET)

        admin_announcement = cls(
            uuid=uuid,
            description=description,
            active_from=active_from,
            active_to=active_to,
            is_active=is_active,
            type_=type_,
            created=created,
            maintenance_uuid=maintenance_uuid,
            maintenance_name=maintenance_name,
            maintenance_type=maintenance_type,
            maintenance_state=maintenance_state,
            maintenance_scheduled_start=maintenance_scheduled_start,
            maintenance_scheduled_end=maintenance_scheduled_end,
            maintenance_service_provider=maintenance_service_provider,
            maintenance_affected_offerings=maintenance_affected_offerings,
            maintenance_external_reference_url=maintenance_external_reference_url,
        )

        admin_announcement.additional_properties = d
        return admin_announcement

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
