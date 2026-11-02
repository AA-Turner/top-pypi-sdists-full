from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="DucklakeSettingsDucklakesAdditionalPropertyMaintenance")


@_attrs_define
class DucklakeSettingsDucklakesAdditionalPropertyMaintenance:
    """Scheduled maintenance (enterprise) - snapshot expiry, adjacent-file compaction and orphaned-file cleanup, run as a
    managed per-lake schedule

        Attributes:
            enabled (bool):
            schedule (Union[Unset, str]): cron cadence (v2, UTC); defaults to daily at 03h with a per-lake minute offset
            retention_days (Union[Unset, int]): snapshot retention window in days (default 7); time-travel older than this
                stops working
            compaction (Union[Unset, bool]): merge adjacent small parquet files (default true)
            orphan_cleanup (Union[Unset, bool]): delete orphaned files older than max(retention, 1 day) (default true)
    """

    enabled: bool
    schedule: Union[Unset, str] = UNSET
    retention_days: Union[Unset, int] = UNSET
    compaction: Union[Unset, bool] = UNSET
    orphan_cleanup: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        enabled = self.enabled
        schedule = self.schedule
        retention_days = self.retention_days
        compaction = self.compaction
        orphan_cleanup = self.orphan_cleanup

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "enabled": enabled,
            }
        )
        if schedule is not UNSET:
            field_dict["schedule"] = schedule
        if retention_days is not UNSET:
            field_dict["retention_days"] = retention_days
        if compaction is not UNSET:
            field_dict["compaction"] = compaction
        if orphan_cleanup is not UNSET:
            field_dict["orphan_cleanup"] = orphan_cleanup

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        enabled = d.pop("enabled")

        schedule = d.pop("schedule", UNSET)

        retention_days = d.pop("retention_days", UNSET)

        compaction = d.pop("compaction", UNSET)

        orphan_cleanup = d.pop("orphan_cleanup", UNSET)

        ducklake_settings_ducklakes_additional_property_maintenance = cls(
            enabled=enabled,
            schedule=schedule,
            retention_days=retention_days,
            compaction=compaction,
            orphan_cleanup=orphan_cleanup,
        )

        ducklake_settings_ducklakes_additional_property_maintenance.additional_properties = d
        return ducklake_settings_ducklakes_additional_property_maintenance

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
