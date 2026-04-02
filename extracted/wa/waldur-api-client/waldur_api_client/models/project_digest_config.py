import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.frequency_enum import FrequencyEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.project_digest_config_available_sections_item import ProjectDigestConfigAvailableSectionsItem


T = TypeVar("T", bound="ProjectDigestConfig")


@_attrs_define
class ProjectDigestConfig:
    """
    Attributes:
        uuid (UUID):
        last_sent_at (Union[None, datetime.datetime]):
        available_sections (list['ProjectDigestConfigAvailableSectionsItem']):
        is_enabled (Union[Unset, bool]):
        frequency (Union[Unset, FrequencyEnum]):
        enabled_sections (Union[Unset, list[str]]):
        day_of_week (Union[Unset, int]): For weekly/biweekly: 0=Sunday..6=Saturday
        day_of_month (Union[Unset, int]): For monthly: day of month (1-28)
    """

    uuid: UUID
    last_sent_at: Union[None, datetime.datetime]
    available_sections: list["ProjectDigestConfigAvailableSectionsItem"]
    is_enabled: Union[Unset, bool] = UNSET
    frequency: Union[Unset, FrequencyEnum] = UNSET
    enabled_sections: Union[Unset, list[str]] = UNSET
    day_of_week: Union[Unset, int] = UNSET
    day_of_month: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        last_sent_at: Union[None, str]
        if isinstance(self.last_sent_at, datetime.datetime):
            last_sent_at = self.last_sent_at.isoformat()
        else:
            last_sent_at = self.last_sent_at

        available_sections = []
        for available_sections_item_data in self.available_sections:
            available_sections_item = available_sections_item_data.to_dict()
            available_sections.append(available_sections_item)

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
        field_dict.update(
            {
                "uuid": uuid,
                "last_sent_at": last_sent_at,
                "available_sections": available_sections,
            }
        )
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
        from ..models.project_digest_config_available_sections_item import ProjectDigestConfigAvailableSectionsItem

        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        def _parse_last_sent_at(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_sent_at_type_0 = isoparse(data)

                return last_sent_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        last_sent_at = _parse_last_sent_at(d.pop("last_sent_at"))

        available_sections = []
        _available_sections = d.pop("available_sections")
        for available_sections_item_data in _available_sections:
            available_sections_item = ProjectDigestConfigAvailableSectionsItem.from_dict(available_sections_item_data)

            available_sections.append(available_sections_item)

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

        project_digest_config = cls(
            uuid=uuid,
            last_sent_at=last_sent_at,
            available_sections=available_sections,
            is_enabled=is_enabled,
            frequency=frequency,
            enabled_sections=enabled_sections,
            day_of_week=day_of_week,
            day_of_month=day_of_month,
        )

        project_digest_config.additional_properties = d
        return project_digest_config

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
