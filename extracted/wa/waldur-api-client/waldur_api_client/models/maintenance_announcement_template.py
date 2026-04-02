from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.maintenance_type_enum import MaintenanceTypeEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.maintenance_announcement_offering import MaintenanceAnnouncementOffering


T = TypeVar("T", bound="MaintenanceAnnouncementTemplate")


@_attrs_define
class MaintenanceAnnouncementTemplate:
    """
    Attributes:
        url (str):
        uuid (UUID):
        name (str):
        service_provider (str): Service provider announcing the maintenance
        affected_offerings (list['MaintenanceAnnouncementOffering']):
        message (Union[Unset, str]):
        maintenance_type (Union[Unset, MaintenanceTypeEnum]):
    """

    url: str
    uuid: UUID
    name: str
    service_provider: str
    affected_offerings: list["MaintenanceAnnouncementOffering"]
    message: Union[Unset, str] = UNSET
    maintenance_type: Union[Unset, MaintenanceTypeEnum] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        uuid = str(self.uuid)

        name = self.name

        service_provider = self.service_provider

        affected_offerings = []
        for affected_offerings_item_data in self.affected_offerings:
            affected_offerings_item = affected_offerings_item_data.to_dict()
            affected_offerings.append(affected_offerings_item)

        message = self.message

        maintenance_type: Union[Unset, int] = UNSET
        if not isinstance(self.maintenance_type, Unset):
            maintenance_type = self.maintenance_type.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "url": url,
                "uuid": uuid,
                "name": name,
                "service_provider": service_provider,
                "affected_offerings": affected_offerings,
            }
        )
        if message is not UNSET:
            field_dict["message"] = message
        if maintenance_type is not UNSET:
            field_dict["maintenance_type"] = maintenance_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.maintenance_announcement_offering import MaintenanceAnnouncementOffering

        d = dict(src_dict)
        url = d.pop("url")

        uuid = UUID(d.pop("uuid"))

        name = d.pop("name")

        service_provider = d.pop("service_provider")

        affected_offerings = []
        _affected_offerings = d.pop("affected_offerings")
        for affected_offerings_item_data in _affected_offerings:
            affected_offerings_item = MaintenanceAnnouncementOffering.from_dict(affected_offerings_item_data)

            affected_offerings.append(affected_offerings_item)

        message = d.pop("message", UNSET)

        _maintenance_type = d.pop("maintenance_type", UNSET)
        maintenance_type: Union[Unset, MaintenanceTypeEnum]
        if isinstance(_maintenance_type, Unset):
            maintenance_type = UNSET
        else:
            maintenance_type = MaintenanceTypeEnum(_maintenance_type)

        maintenance_announcement_template = cls(
            url=url,
            uuid=uuid,
            name=name,
            service_provider=service_provider,
            affected_offerings=affected_offerings,
            message=message,
            maintenance_type=maintenance_type,
        )

        maintenance_announcement_template.additional_properties = d
        return maintenance_announcement_template

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
