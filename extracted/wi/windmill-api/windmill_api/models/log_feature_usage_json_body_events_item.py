from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="LogFeatureUsageJsonBodyEventsItem")


@_attrs_define
class LogFeatureUsageJsonBodyEventsItem:
    """
    Attributes:
        feature (str):
        kind (str):
        key (Union[Unset, str]):
        entity_id (Union[Unset, str]):
        value (Union[Unset, int]):
    """

    feature: str
    kind: str
    key: Union[Unset, str] = UNSET
    entity_id: Union[Unset, str] = UNSET
    value: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        feature = self.feature
        kind = self.kind
        key = self.key
        entity_id = self.entity_id
        value = self.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "feature": feature,
                "kind": kind,
            }
        )
        if key is not UNSET:
            field_dict["key"] = key
        if entity_id is not UNSET:
            field_dict["entity_id"] = entity_id
        if value is not UNSET:
            field_dict["value"] = value

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        feature = d.pop("feature")

        kind = d.pop("kind")

        key = d.pop("key", UNSET)

        entity_id = d.pop("entity_id", UNSET)

        value = d.pop("value", UNSET)

        log_feature_usage_json_body_events_item = cls(
            feature=feature,
            kind=kind,
            key=key,
            entity_id=entity_id,
            value=value,
        )

        log_feature_usage_json_body_events_item.additional_properties = d
        return log_feature_usage_json_body_events_item

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
