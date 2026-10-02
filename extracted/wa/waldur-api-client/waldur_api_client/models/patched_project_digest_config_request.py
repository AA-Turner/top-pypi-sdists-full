from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.frequency_enum import FrequencyEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="PatchedProjectDigestConfigRequest")


@_attrs_define
class PatchedProjectDigestConfigRequest:
    """
    Attributes:
        is_enabled (Union[Unset, bool]):
        frequency (Union[Unset, FrequencyEnum]):
        enabled_sections (Union[Unset, list[str]]):
        day_of_week (Union[Unset, int]): For weekly/biweekly: 0=Sunday..6=Saturday
        day_of_month (Union[Unset, int]): For monthly: day of month (1-28)
    """

    is_enabled: Union[Unset, bool] = UNSET
    frequency: Union[Unset, FrequencyEnum] = UNSET
    enabled_sections: Union[Unset, list[str]] = UNSET
    day_of_week: Union[Unset, int] = UNSET
    day_of_month: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        is_enabled = self.is_enabled

        frequency: Union[Unset, str] = UNSET
        if not isinstance(self.frequency, Unset):
            frequency = self.frequency.value

        enabled_sections: Union[Unset, list[str]] = UNSET
        if not isinstance(self.enabled_sections, Unset):
            enabled_sections = self.enabled_sections

        day_of_week = self.day_of_week

        day_of_month = self.day_of_month

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if is_enabled is not UNSET:
            field_dict["is_enabled"] = is_enabled
        if frequency is not UNSET:
            field_dict["frequency"] = frequency
        if enabled_sections is not UNSET:
            field_dict["enabled_sections"] = enabled_sections
        if day_of_week is not UNSET:
            field_dict["day_of_week"] = day_of_week
        if day_of_month is not UNSET:
            field_dict["day_of_month"] = day_of_month

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        is_enabled = d.pop("is_enabled", UNSET)

        _frequency = d.pop("frequency", UNSET)
        frequency: Union[Unset, FrequencyEnum]
        if isinstance(_frequency, Unset):
            frequency = UNSET
        else:
            frequency = FrequencyEnum(_frequency)

        enabled_sections = cast(list[str], d.pop("enabled_sections", UNSET))

        day_of_week = d.pop("day_of_week", UNSET)

        day_of_month = d.pop("day_of_month", UNSET)

        patched_project_digest_config_request = cls(
            is_enabled=is_enabled,
            frequency=frequency,
            enabled_sections=enabled_sections,
            day_of_week=day_of_week,
            day_of_month=day_of_month,
        )

        patched_project_digest_config_request.additional_properties = d
        return patched_project_digest_config_request

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
