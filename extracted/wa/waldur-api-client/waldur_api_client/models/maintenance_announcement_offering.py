from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.impact_level_display_enum import ImpactLevelDisplayEnum
from ..models.impact_level_enum import ImpactLevelEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="MaintenanceAnnouncementOffering")


@_attrs_define
class MaintenanceAnnouncementOffering:
    """
    Attributes:
        url (str):
        uuid (UUID):
        maintenance (str):
        offering (str):
        impact_level_display (ImpactLevelDisplayEnum):
        offering_name (str):
        impact_level (Union[Unset, ImpactLevelEnum]):
        impact_description (Union[Unset, str]): Specific description of how this offering will be affected
    """

    url: str
    uuid: UUID
    maintenance: str
    offering: str
    impact_level_display: ImpactLevelDisplayEnum
    offering_name: str
    impact_level: Union[Unset, ImpactLevelEnum] = UNSET
    impact_description: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        uuid = str(self.uuid)

        maintenance = self.maintenance

        offering = self.offering

        impact_level_display = self.impact_level_display.value

        offering_name = self.offering_name

        impact_level: Union[Unset, int] = UNSET
        if not isinstance(self.impact_level, Unset):
            impact_level = self.impact_level.value

        impact_description = self.impact_description

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "url": url,
                "uuid": uuid,
                "maintenance": maintenance,
                "offering": offering,
                "impact_level_display": impact_level_display,
                "offering_name": offering_name,
            }
        )
        if impact_level is not UNSET:
            field_dict["impact_level"] = impact_level
        if impact_description is not UNSET:
            field_dict["impact_description"] = impact_description

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        url = d.pop("url")

        uuid = UUID(d.pop("uuid"))

        maintenance = d.pop("maintenance")

        offering = d.pop("offering")

        impact_level_display = ImpactLevelDisplayEnum(d.pop("impact_level_display"))

        offering_name = d.pop("offering_name")

        _impact_level = d.pop("impact_level", UNSET)
        impact_level: Union[Unset, ImpactLevelEnum]
        if isinstance(_impact_level, Unset):
            impact_level = UNSET
        else:
            impact_level = ImpactLevelEnum(_impact_level)

        impact_description = d.pop("impact_description", UNSET)

        maintenance_announcement_offering = cls(
            url=url,
            uuid=uuid,
            maintenance=maintenance,
            offering=offering,
            impact_level_display=impact_level_display,
            offering_name=offering_name,
            impact_level=impact_level,
            impact_description=impact_description,
        )

        maintenance_announcement_offering.additional_properties = d
        return maintenance_announcement_offering

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
