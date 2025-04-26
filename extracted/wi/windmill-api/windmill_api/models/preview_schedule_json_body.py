from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PreviewScheduleJsonBody")


@_attrs_define
class PreviewScheduleJsonBody:
    """
    Attributes:
        schedule (str):
        timezone (str):
        cron_version (Union[Unset, str]):
    """

    schedule: str
    timezone: str
    cron_version: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        schedule = self.schedule
        timezone = self.timezone
        cron_version = self.cron_version

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "schedule": schedule,
                "timezone": timezone,
            }
        )
        if cron_version is not UNSET:
            field_dict["cron_version"] = cron_version

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        schedule = d.pop("schedule")

        timezone = d.pop("timezone")

        cron_version = d.pop("cron_version", UNSET)

        preview_schedule_json_body = cls(
            schedule=schedule,
            timezone=timezone,
            cron_version=cron_version,
        )

        preview_schedule_json_body.additional_properties = d
        return preview_schedule_json_body

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
