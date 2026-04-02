from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="AdminAnnouncementMaintenanceAffectedOfferingsItem")


@_attrs_define
class AdminAnnouncementMaintenanceAffectedOfferingsItem:
    """
    Attributes:
        uuid (Union[Unset, UUID]):
        name (Union[Unset, str]):
        impact_level (Union[Unset, str]):
        impact_level_display (Union[Unset, str]):
        impact_description (Union[Unset, str]):
    """

    uuid: Union[Unset, UUID] = UNSET
    name: Union[Unset, str] = UNSET
    impact_level: Union[Unset, str] = UNSET
    impact_level_display: Union[Unset, str] = UNSET
    impact_description: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid: Union[Unset, str] = UNSET
        if not isinstance(self.uuid, Unset):
            uuid = str(self.uuid)

        name = self.name

        impact_level = self.impact_level

        impact_level_display = self.impact_level_display

        impact_description = self.impact_description

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if uuid is not UNSET:
            field_dict["uuid"] = uuid
        if name is not UNSET:
            field_dict["name"] = name
        if impact_level is not UNSET:
            field_dict["impact_level"] = impact_level
        if impact_level_display is not UNSET:
            field_dict["impact_level_display"] = impact_level_display
        if impact_description is not UNSET:
            field_dict["impact_description"] = impact_description

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _uuid = d.pop("uuid", UNSET)
        uuid: Union[Unset, UUID]
        if isinstance(_uuid, Unset):
            uuid = UNSET
        else:
            uuid = UUID(_uuid)

        name = d.pop("name", UNSET)

        impact_level = d.pop("impact_level", UNSET)

        impact_level_display = d.pop("impact_level_display", UNSET)

        impact_description = d.pop("impact_description", UNSET)

        admin_announcement_maintenance_affected_offerings_item = cls(
            uuid=uuid,
            name=name,
            impact_level=impact_level,
            impact_level_display=impact_level_display,
            impact_description=impact_description,
        )

        admin_announcement_maintenance_affected_offerings_item.additional_properties = d
        return admin_announcement_maintenance_affected_offerings_item

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
