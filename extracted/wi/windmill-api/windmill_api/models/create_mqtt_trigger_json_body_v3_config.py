from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateMqttTriggerJsonBodyV3Config")


@_attrs_define
class CreateMqttTriggerJsonBodyV3Config:
    """
    Attributes:
        clean_session (Union[Unset, bool]):
    """

    clean_session: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        clean_session = self.clean_session

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if clean_session is not UNSET:
            field_dict["clean_session"] = clean_session

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        clean_session = d.pop("clean_session", UNSET)

        create_mqtt_trigger_json_body_v3_config = cls(
            clean_session=clean_session,
        )

        create_mqtt_trigger_json_body_v3_config.additional_properties = d
        return create_mqtt_trigger_json_body_v3_config

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
