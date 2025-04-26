from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.new_mqtt_trigger_client_version import NewMqttTriggerClientVersion
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.new_mqtt_trigger_subscribe_topics_item import NewMqttTriggerSubscribeTopicsItem
    from ..models.new_mqtt_trigger_v3_config import NewMqttTriggerV3Config
    from ..models.new_mqtt_trigger_v5_config import NewMqttTriggerV5Config


T = TypeVar("T", bound="NewMqttTrigger")


@_attrs_define
class NewMqttTrigger:
    """
    Attributes:
        mqtt_resource_path (str):
        subscribe_topics (List['NewMqttTriggerSubscribeTopicsItem']):
        path (str):
        script_path (str):
        is_flow (bool):
        client_id (Union[Unset, str]):
        v3_config (Union[Unset, NewMqttTriggerV3Config]):
        v5_config (Union[Unset, NewMqttTriggerV5Config]):
        client_version (Union[Unset, NewMqttTriggerClientVersion]):
        enabled (Union[Unset, bool]):
    """

    mqtt_resource_path: str
    subscribe_topics: List["NewMqttTriggerSubscribeTopicsItem"]
    path: str
    script_path: str
    is_flow: bool
    client_id: Union[Unset, str] = UNSET
    v3_config: Union[Unset, "NewMqttTriggerV3Config"] = UNSET
    v5_config: Union[Unset, "NewMqttTriggerV5Config"] = UNSET
    client_version: Union[Unset, NewMqttTriggerClientVersion] = UNSET
    enabled: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        mqtt_resource_path = self.mqtt_resource_path
        subscribe_topics = []
        for subscribe_topics_item_data in self.subscribe_topics:
            subscribe_topics_item = subscribe_topics_item_data.to_dict()

            subscribe_topics.append(subscribe_topics_item)

        path = self.path
        script_path = self.script_path
        is_flow = self.is_flow
        client_id = self.client_id
        v3_config: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.v3_config, Unset):
            v3_config = self.v3_config.to_dict()

        v5_config: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.v5_config, Unset):
            v5_config = self.v5_config.to_dict()

        client_version: Union[Unset, str] = UNSET
        if not isinstance(self.client_version, Unset):
            client_version = self.client_version.value

        enabled = self.enabled

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "mqtt_resource_path": mqtt_resource_path,
                "subscribe_topics": subscribe_topics,
                "path": path,
                "script_path": script_path,
                "is_flow": is_flow,
            }
        )
        if client_id is not UNSET:
            field_dict["client_id"] = client_id
        if v3_config is not UNSET:
            field_dict["v3_config"] = v3_config
        if v5_config is not UNSET:
            field_dict["v5_config"] = v5_config
        if client_version is not UNSET:
            field_dict["client_version"] = client_version
        if enabled is not UNSET:
            field_dict["enabled"] = enabled

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.new_mqtt_trigger_subscribe_topics_item import NewMqttTriggerSubscribeTopicsItem
        from ..models.new_mqtt_trigger_v3_config import NewMqttTriggerV3Config
        from ..models.new_mqtt_trigger_v5_config import NewMqttTriggerV5Config

        d = src_dict.copy()
        mqtt_resource_path = d.pop("mqtt_resource_path")

        subscribe_topics = []
        _subscribe_topics = d.pop("subscribe_topics")
        for subscribe_topics_item_data in _subscribe_topics:
            subscribe_topics_item = NewMqttTriggerSubscribeTopicsItem.from_dict(subscribe_topics_item_data)

            subscribe_topics.append(subscribe_topics_item)

        path = d.pop("path")

        script_path = d.pop("script_path")

        is_flow = d.pop("is_flow")

        client_id = d.pop("client_id", UNSET)

        _v3_config = d.pop("v3_config", UNSET)
        v3_config: Union[Unset, NewMqttTriggerV3Config]
        if isinstance(_v3_config, Unset):
            v3_config = UNSET
        else:
            v3_config = NewMqttTriggerV3Config.from_dict(_v3_config)

        _v5_config = d.pop("v5_config", UNSET)
        v5_config: Union[Unset, NewMqttTriggerV5Config]
        if isinstance(_v5_config, Unset):
            v5_config = UNSET
        else:
            v5_config = NewMqttTriggerV5Config.from_dict(_v5_config)

        _client_version = d.pop("client_version", UNSET)
        client_version: Union[Unset, NewMqttTriggerClientVersion]
        if isinstance(_client_version, Unset):
            client_version = UNSET
        else:
            client_version = NewMqttTriggerClientVersion(_client_version)

        enabled = d.pop("enabled", UNSET)

        new_mqtt_trigger = cls(
            mqtt_resource_path=mqtt_resource_path,
            subscribe_topics=subscribe_topics,
            path=path,
            script_path=script_path,
            is_flow=is_flow,
            client_id=client_id,
            v3_config=v3_config,
            v5_config=v5_config,
            client_version=client_version,
            enabled=enabled,
        )

        new_mqtt_trigger.additional_properties = d
        return new_mqtt_trigger

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
