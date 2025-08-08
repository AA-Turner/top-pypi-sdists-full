from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.create_mqtt_trigger_json_body_client_version import CreateMqttTriggerJsonBodyClientVersion
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.create_mqtt_trigger_json_body_error_handler_args import CreateMqttTriggerJsonBodyErrorHandlerArgs
    from ..models.create_mqtt_trigger_json_body_retry import CreateMqttTriggerJsonBodyRetry
    from ..models.create_mqtt_trigger_json_body_subscribe_topics_item import (
        CreateMqttTriggerJsonBodySubscribeTopicsItem,
    )
    from ..models.create_mqtt_trigger_json_body_v3_config import CreateMqttTriggerJsonBodyV3Config
    from ..models.create_mqtt_trigger_json_body_v5_config import CreateMqttTriggerJsonBodyV5Config


T = TypeVar("T", bound="CreateMqttTriggerJsonBody")


@_attrs_define
class CreateMqttTriggerJsonBody:
    """
    Attributes:
        mqtt_resource_path (str):
        subscribe_topics (List['CreateMqttTriggerJsonBodySubscribeTopicsItem']):
        path (str):
        script_path (str):
        is_flow (bool):
        client_id (Union[Unset, str]):
        v3_config (Union[Unset, CreateMqttTriggerJsonBodyV3Config]):
        v5_config (Union[Unset, CreateMqttTriggerJsonBodyV5Config]):
        client_version (Union[Unset, CreateMqttTriggerJsonBodyClientVersion]):
        enabled (Union[Unset, bool]):
        error_handler_path (Union[Unset, str]):
        error_handler_args (Union[Unset, CreateMqttTriggerJsonBodyErrorHandlerArgs]): The arguments to pass to the
            script or flow
        retry (Union[Unset, CreateMqttTriggerJsonBodyRetry]):
    """

    mqtt_resource_path: str
    subscribe_topics: List["CreateMqttTriggerJsonBodySubscribeTopicsItem"]
    path: str
    script_path: str
    is_flow: bool
    client_id: Union[Unset, str] = UNSET
    v3_config: Union[Unset, "CreateMqttTriggerJsonBodyV3Config"] = UNSET
    v5_config: Union[Unset, "CreateMqttTriggerJsonBodyV5Config"] = UNSET
    client_version: Union[Unset, CreateMqttTriggerJsonBodyClientVersion] = UNSET
    enabled: Union[Unset, bool] = UNSET
    error_handler_path: Union[Unset, str] = UNSET
    error_handler_args: Union[Unset, "CreateMqttTriggerJsonBodyErrorHandlerArgs"] = UNSET
    retry: Union[Unset, "CreateMqttTriggerJsonBodyRetry"] = UNSET
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
        error_handler_path = self.error_handler_path
        error_handler_args: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.error_handler_args, Unset):
            error_handler_args = self.error_handler_args.to_dict()

        retry: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.retry, Unset):
            retry = self.retry.to_dict()

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
        if error_handler_path is not UNSET:
            field_dict["error_handler_path"] = error_handler_path
        if error_handler_args is not UNSET:
            field_dict["error_handler_args"] = error_handler_args
        if retry is not UNSET:
            field_dict["retry"] = retry

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.create_mqtt_trigger_json_body_error_handler_args import CreateMqttTriggerJsonBodyErrorHandlerArgs
        from ..models.create_mqtt_trigger_json_body_retry import CreateMqttTriggerJsonBodyRetry
        from ..models.create_mqtt_trigger_json_body_subscribe_topics_item import (
            CreateMqttTriggerJsonBodySubscribeTopicsItem,
        )
        from ..models.create_mqtt_trigger_json_body_v3_config import CreateMqttTriggerJsonBodyV3Config
        from ..models.create_mqtt_trigger_json_body_v5_config import CreateMqttTriggerJsonBodyV5Config

        d = src_dict.copy()
        mqtt_resource_path = d.pop("mqtt_resource_path")

        subscribe_topics = []
        _subscribe_topics = d.pop("subscribe_topics")
        for subscribe_topics_item_data in _subscribe_topics:
            subscribe_topics_item = CreateMqttTriggerJsonBodySubscribeTopicsItem.from_dict(subscribe_topics_item_data)

            subscribe_topics.append(subscribe_topics_item)

        path = d.pop("path")

        script_path = d.pop("script_path")

        is_flow = d.pop("is_flow")

        client_id = d.pop("client_id", UNSET)

        _v3_config = d.pop("v3_config", UNSET)
        v3_config: Union[Unset, CreateMqttTriggerJsonBodyV3Config]
        if isinstance(_v3_config, Unset):
            v3_config = UNSET
        else:
            v3_config = CreateMqttTriggerJsonBodyV3Config.from_dict(_v3_config)

        _v5_config = d.pop("v5_config", UNSET)
        v5_config: Union[Unset, CreateMqttTriggerJsonBodyV5Config]
        if isinstance(_v5_config, Unset):
            v5_config = UNSET
        else:
            v5_config = CreateMqttTriggerJsonBodyV5Config.from_dict(_v5_config)

        _client_version = d.pop("client_version", UNSET)
        client_version: Union[Unset, CreateMqttTriggerJsonBodyClientVersion]
        if isinstance(_client_version, Unset):
            client_version = UNSET
        else:
            client_version = CreateMqttTriggerJsonBodyClientVersion(_client_version)

        enabled = d.pop("enabled", UNSET)

        error_handler_path = d.pop("error_handler_path", UNSET)

        _error_handler_args = d.pop("error_handler_args", UNSET)
        error_handler_args: Union[Unset, CreateMqttTriggerJsonBodyErrorHandlerArgs]
        if isinstance(_error_handler_args, Unset):
            error_handler_args = UNSET
        else:
            error_handler_args = CreateMqttTriggerJsonBodyErrorHandlerArgs.from_dict(_error_handler_args)

        _retry = d.pop("retry", UNSET)
        retry: Union[Unset, CreateMqttTriggerJsonBodyRetry]
        if isinstance(_retry, Unset):
            retry = UNSET
        else:
            retry = CreateMqttTriggerJsonBodyRetry.from_dict(_retry)

        create_mqtt_trigger_json_body = cls(
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
            error_handler_path=error_handler_path,
            error_handler_args=error_handler_args,
            retry=retry,
        )

        create_mqtt_trigger_json_body.additional_properties = d
        return create_mqtt_trigger_json_body

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
