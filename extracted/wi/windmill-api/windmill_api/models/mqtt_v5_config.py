from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="MqttV5Config")


@_attrs_define
class MqttV5Config:
    """
    Attributes:
        clean_start (Union[Unset, bool]):
        topic_alias_maximum (Union[Unset, float]):
        session_expiry_interval (Union[Unset, float]):
    """

    clean_start: Union[Unset, bool] = UNSET
    topic_alias_maximum: Union[Unset, float] = UNSET
    session_expiry_interval: Union[Unset, float] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        clean_start = self.clean_start
        topic_alias_maximum = self.topic_alias_maximum
        session_expiry_interval = self.session_expiry_interval

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if clean_start is not UNSET:
            field_dict["clean_start"] = clean_start
        if topic_alias_maximum is not UNSET:
            field_dict["topic_alias_maximum"] = topic_alias_maximum
        if session_expiry_interval is not UNSET:
            field_dict["session_expiry_interval"] = session_expiry_interval

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        clean_start = d.pop("clean_start", UNSET)

        topic_alias_maximum = d.pop("topic_alias_maximum", UNSET)

        session_expiry_interval = d.pop("session_expiry_interval", UNSET)

        mqtt_v5_config = cls(
            clean_start=clean_start,
            topic_alias_maximum=topic_alias_maximum,
            session_expiry_interval=session_expiry_interval,
        )

        mqtt_v5_config.additional_properties = d
        return mqtt_v5_config

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
