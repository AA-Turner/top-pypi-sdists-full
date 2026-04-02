from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.impact_level_enum import ImpactLevelEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="MaintenanceAnnouncementOfferingRequest")


@_attrs_define
class MaintenanceAnnouncementOfferingRequest:
    """
    Attributes:
        maintenance (str):
        offering (str):
        impact_level (Union[Unset, ImpactLevelEnum]):
        impact_description (Union[Unset, str]): Specific description of how this offering will be affected
    """

    maintenance: str
    offering: str
    impact_level: Union[Unset, ImpactLevelEnum] = UNSET
    impact_description: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        maintenance = self.maintenance

        offering = self.offering

        impact_level: Union[Unset, int] = UNSET
        if not isinstance(self.impact_level, Unset):
            impact_level = self.impact_level.value

        impact_description = self.impact_description

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "maintenance": maintenance,
                "offering": offering,
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
        maintenance = d.pop("maintenance")

        offering = d.pop("offering")

        _impact_level = d.pop("impact_level", UNSET)
        impact_level: Union[Unset, ImpactLevelEnum]
        if isinstance(_impact_level, Unset):
            impact_level = UNSET
        else:
            impact_level = ImpactLevelEnum(_impact_level)

        impact_description = d.pop("impact_description", UNSET)

        maintenance_announcement_offering_request = cls(
            maintenance=maintenance,
            offering=offering,
            impact_level=impact_level,
            impact_description=impact_description,
        )

        maintenance_announcement_offering_request.additional_properties = d
        return maintenance_announcement_offering_request

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
