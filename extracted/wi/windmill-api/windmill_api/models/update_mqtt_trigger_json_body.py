from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.update_mqtt_trigger_json_body_client_version import UpdateMqttTriggerJsonBodyClientVersion
from ..models.update_mqtt_trigger_json_body_mode import UpdateMqttTriggerJsonBodyMode
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.update_mqtt_trigger_json_body_error_handler_args import UpdateMqttTriggerJsonBodyErrorHandlerArgs
    from ..models.update_mqtt_trigger_json_body_retry import UpdateMqttTriggerJsonBodyRetry
    from ..models.update_mqtt_trigger_json_body_subscribe_topics_item import (
        UpdateMqttTriggerJsonBodySubscribeTopicsItem,
    )
    from ..models.update_mqtt_trigger_json_body_v3_config import UpdateMqttTriggerJsonBodyV3Config
    from ..models.update_mqtt_trigger_json_body_v5_config import UpdateMqttTriggerJsonBodyV5Config


T = TypeVar("T", bound="UpdateMqttTriggerJsonBody")


@_attrs_define
class UpdateMqttTriggerJsonBody:
    """
    Attributes:
        mqtt_resource_path (str): Path to the MQTT resource containing broker connection configuration
        subscribe_topics (List['UpdateMqttTriggerJsonBodySubscribeTopicsItem']): Array of MQTT topics to subscribe to,
            each with topic name and QoS level
        path (str): The unique Windmill path for this trigger. Must be of the form `u/<user>/<path>` or
            `f/<folder>/<path>`. This is the trigger object path, not the HTTP route path.
        script_path (str): Path to the script or flow to execute when a message is received
        is_flow (bool): True if script_path points to a flow, false if it points to a script
        client_id (Union[Unset, None, str]): MQTT client ID for this connection
        v3_config (Union[Unset, None, UpdateMqttTriggerJsonBodyV3Config]): MQTT v3 specific configuration
            (clean_session)
        v5_config (Union[Unset, None, UpdateMqttTriggerJsonBodyV5Config]): MQTT v5 specific configuration (clean_start,
            topic_alias_maximum, session_expiry_interval)
        client_version (Union[Unset, None, UpdateMqttTriggerJsonBodyClientVersion]): MQTT protocol version ('v3' or
            'v5')
        mode (Union[Unset, UpdateMqttTriggerJsonBodyMode]): job trigger mode
        error_handler_path (Union[Unset, str]): Path to a script or flow to run when the triggered job fails
        error_handler_args (Union[Unset, UpdateMqttTriggerJsonBodyErrorHandlerArgs]): The arguments to pass to the
            script or flow
        retry (Union[Unset, UpdateMqttTriggerJsonBodyRetry]): Retry configuration for failed module executions
        permissioned_as (Union[Unset, str]): The user or group this trigger runs as. Used during deployment to preserve
            the original trigger owner.
        preserve_permissioned_as (Union[Unset, bool]): When true and the caller is a member of the 'wm_deployers' group,
            preserves the original permissioned_as value instead of overwriting it.
        labels (Union[Unset, List[str]]):
    """

    mqtt_resource_path: str
    subscribe_topics: List["UpdateMqttTriggerJsonBodySubscribeTopicsItem"]
    path: str
    script_path: str
    is_flow: bool
    client_id: Union[Unset, None, str] = UNSET
    v3_config: Union[Unset, None, "UpdateMqttTriggerJsonBodyV3Config"] = UNSET
    v5_config: Union[Unset, None, "UpdateMqttTriggerJsonBodyV5Config"] = UNSET
    client_version: Union[Unset, None, UpdateMqttTriggerJsonBodyClientVersion] = UNSET
    mode: Union[Unset, UpdateMqttTriggerJsonBodyMode] = UNSET
    error_handler_path: Union[Unset, str] = UNSET
    error_handler_args: Union[Unset, "UpdateMqttTriggerJsonBodyErrorHandlerArgs"] = UNSET
    retry: Union[Unset, "UpdateMqttTriggerJsonBodyRetry"] = UNSET
    permissioned_as: Union[Unset, str] = UNSET
    preserve_permissioned_as: Union[Unset, bool] = UNSET
    labels: Union[Unset, List[str]] = UNSET
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
        v3_config: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.v3_config, Unset):
            v3_config = self.v3_config.to_dict() if self.v3_config else None

        v5_config: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.v5_config, Unset):
            v5_config = self.v5_config.to_dict() if self.v5_config else None

        client_version: Union[Unset, None, str] = UNSET
        if not isinstance(self.client_version, Unset):
            client_version = self.client_version.value if self.client_version else None

        mode: Union[Unset, str] = UNSET
        if not isinstance(self.mode, Unset):
            mode = self.mode.value

        error_handler_path = self.error_handler_path
        error_handler_args: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.error_handler_args, Unset):
            error_handler_args = self.error_handler_args.to_dict()

        retry: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.retry, Unset):
            retry = self.retry.to_dict()

        permissioned_as = self.permissioned_as
        preserve_permissioned_as = self.preserve_permissioned_as
        labels: Union[Unset, List[str]] = UNSET
        if not isinstance(self.labels, Unset):
            labels = self.labels

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
        if mode is not UNSET:
            field_dict["mode"] = mode
        if error_handler_path is not UNSET:
            field_dict["error_handler_path"] = error_handler_path
        if error_handler_args is not UNSET:
            field_dict["error_handler_args"] = error_handler_args
        if retry is not UNSET:
            field_dict["retry"] = retry
        if permissioned_as is not UNSET:
            field_dict["permissioned_as"] = permissioned_as
        if preserve_permissioned_as is not UNSET:
            field_dict["preserve_permissioned_as"] = preserve_permissioned_as
        if labels is not UNSET:
            field_dict["labels"] = labels

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.update_mqtt_trigger_json_body_error_handler_args import UpdateMqttTriggerJsonBodyErrorHandlerArgs
        from ..models.update_mqtt_trigger_json_body_retry import UpdateMqttTriggerJsonBodyRetry
        from ..models.update_mqtt_trigger_json_body_subscribe_topics_item import (
            UpdateMqttTriggerJsonBodySubscribeTopicsItem,
        )
        from ..models.update_mqtt_trigger_json_body_v3_config import UpdateMqttTriggerJsonBodyV3Config
        from ..models.update_mqtt_trigger_json_body_v5_config import UpdateMqttTriggerJsonBodyV5Config

        d = src_dict.copy()
        mqtt_resource_path = d.pop("mqtt_resource_path")

        subscribe_topics = []
        _subscribe_topics = d.pop("subscribe_topics")
        for subscribe_topics_item_data in _subscribe_topics:
            subscribe_topics_item = UpdateMqttTriggerJsonBodySubscribeTopicsItem.from_dict(subscribe_topics_item_data)

            subscribe_topics.append(subscribe_topics_item)

        path = d.pop("path")

        script_path = d.pop("script_path")

        is_flow = d.pop("is_flow")

        client_id = d.pop("client_id", UNSET)

        _v3_config = d.pop("v3_config", UNSET)
        v3_config: Union[Unset, None, UpdateMqttTriggerJsonBodyV3Config]
        if _v3_config is None:
            v3_config = None
        elif isinstance(_v3_config, Unset):
            v3_config = UNSET
        else:
            v3_config = UpdateMqttTriggerJsonBodyV3Config.from_dict(_v3_config)

        _v5_config = d.pop("v5_config", UNSET)
        v5_config: Union[Unset, None, UpdateMqttTriggerJsonBodyV5Config]
        if _v5_config is None:
            v5_config = None
        elif isinstance(_v5_config, Unset):
            v5_config = UNSET
        else:
            v5_config = UpdateMqttTriggerJsonBodyV5Config.from_dict(_v5_config)

        _client_version = d.pop("client_version", UNSET)
        client_version: Union[Unset, None, UpdateMqttTriggerJsonBodyClientVersion]
        if _client_version is None:
            client_version = None
        elif isinstance(_client_version, Unset):
            client_version = UNSET
        else:
            client_version = UpdateMqttTriggerJsonBodyClientVersion(_client_version)

        _mode = d.pop("mode", UNSET)
        mode: Union[Unset, UpdateMqttTriggerJsonBodyMode]
        if isinstance(_mode, Unset):
            mode = UNSET
        else:
            mode = UpdateMqttTriggerJsonBodyMode(_mode)

        error_handler_path = d.pop("error_handler_path", UNSET)

        _error_handler_args = d.pop("error_handler_args", UNSET)
        error_handler_args: Union[Unset, UpdateMqttTriggerJsonBodyErrorHandlerArgs]
        if isinstance(_error_handler_args, Unset):
            error_handler_args = UNSET
        else:
            error_handler_args = UpdateMqttTriggerJsonBodyErrorHandlerArgs.from_dict(_error_handler_args)

        _retry = d.pop("retry", UNSET)
        retry: Union[Unset, UpdateMqttTriggerJsonBodyRetry]
        if isinstance(_retry, Unset):
            retry = UNSET
        else:
            retry = UpdateMqttTriggerJsonBodyRetry.from_dict(_retry)

        permissioned_as = d.pop("permissioned_as", UNSET)

        preserve_permissioned_as = d.pop("preserve_permissioned_as", UNSET)

        labels = cast(List[str], d.pop("labels", UNSET))

        update_mqtt_trigger_json_body = cls(
            mqtt_resource_path=mqtt_resource_path,
            subscribe_topics=subscribe_topics,
            path=path,
            script_path=script_path,
            is_flow=is_flow,
            client_id=client_id,
            v3_config=v3_config,
            v5_config=v5_config,
            client_version=client_version,
            mode=mode,
            error_handler_path=error_handler_path,
            error_handler_args=error_handler_args,
            retry=retry,
            permissioned_as=permissioned_as,
            preserve_permissioned_as=preserve_permissioned_as,
            labels=labels,
        )

        update_mqtt_trigger_json_body.additional_properties = d
        return update_mqtt_trigger_json_body

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
