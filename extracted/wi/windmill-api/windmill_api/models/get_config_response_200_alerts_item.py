from typing import Any, Dict, List, Type, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="GetConfigResponse200AlertsItem")


@_attrs_define
class GetConfigResponse200AlertsItem:
    """
    Attributes:
        name (str):
        tags_to_monitor (List[str]):
        jobs_num_threshold (int):
        alert_cooldown_seconds (int):
        alert_time_threshold_seconds (int):
    """

    name: str
    tags_to_monitor: List[str]
    jobs_num_threshold: int
    alert_cooldown_seconds: int
    alert_time_threshold_seconds: int
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        tags_to_monitor = self.tags_to_monitor

        jobs_num_threshold = self.jobs_num_threshold
        alert_cooldown_seconds = self.alert_cooldown_seconds
        alert_time_threshold_seconds = self.alert_time_threshold_seconds

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "tags_to_monitor": tags_to_monitor,
                "jobs_num_threshold": jobs_num_threshold,
                "alert_cooldown_seconds": alert_cooldown_seconds,
                "alert_time_threshold_seconds": alert_time_threshold_seconds,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        tags_to_monitor = cast(List[str], d.pop("tags_to_monitor"))

        jobs_num_threshold = d.pop("jobs_num_threshold")

        alert_cooldown_seconds = d.pop("alert_cooldown_seconds")

        alert_time_threshold_seconds = d.pop("alert_time_threshold_seconds")

        get_config_response_200_alerts_item = cls(
            name=name,
            tags_to_monitor=tags_to_monitor,
            jobs_num_threshold=jobs_num_threshold,
            alert_cooldown_seconds=alert_cooldown_seconds,
            alert_time_threshold_seconds=alert_time_threshold_seconds,
        )

        get_config_response_200_alerts_item.additional_properties = d
        return get_config_response_200_alerts_item

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
