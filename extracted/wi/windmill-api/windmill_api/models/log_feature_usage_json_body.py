from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.log_feature_usage_json_body_events_item import LogFeatureUsageJsonBodyEventsItem


T = TypeVar("T", bound="LogFeatureUsageJsonBody")


@_attrs_define
class LogFeatureUsageJsonBody:
    """
    Attributes:
        events (List['LogFeatureUsageJsonBodyEventsItem']):
    """

    events: List["LogFeatureUsageJsonBodyEventsItem"]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        events = []
        for events_item_data in self.events:
            events_item = events_item_data.to_dict()

            events.append(events_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "events": events,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.log_feature_usage_json_body_events_item import LogFeatureUsageJsonBodyEventsItem

        d = src_dict.copy()
        events = []
        _events = d.pop("events")
        for events_item_data in _events:
            events_item = LogFeatureUsageJsonBodyEventsItem.from_dict(events_item_data)

            events.append(events_item)

        log_feature_usage_json_body = cls(
            events=events,
        )

        log_feature_usage_json_body.additional_properties = d
        return log_feature_usage_json_body

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
