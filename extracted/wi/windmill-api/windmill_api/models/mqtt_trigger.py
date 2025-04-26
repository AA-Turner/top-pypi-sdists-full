import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.mqtt_trigger_client_version import MqttTriggerClientVersion
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.mqtt_trigger_extra_perms import MqttTriggerExtraPerms
    from ..models.mqtt_trigger_subscribe_topics_item import MqttTriggerSubscribeTopicsItem
    from ..models.mqtt_trigger_v3_config import MqttTriggerV3Config
    from ..models.mqtt_trigger_v5_config import MqttTriggerV5Config


T = TypeVar("T", bound="MqttTrigger")


@_attrs_define
class MqttTrigger:
    """
    Attributes:
        mqtt_resource_path (str):
        subscribe_topics (List['MqttTriggerSubscribeTopicsItem']):
        enabled (bool):
        path (str):
        script_path (str):
        email (str):
        extra_perms (MqttTriggerExtraPerms):
        workspace_id (str):
        edited_by (str):
        edited_at (datetime.datetime):
        is_flow (bool):
        v3_config (Union[Unset, MqttTriggerV3Config]):
        v5_config (Union[Unset, MqttTriggerV5Config]):
        client_id (Union[Unset, str]):
        client_version (Union[Unset, MqttTriggerClientVersion]):
        server_id (Union[Unset, str]):
        last_server_ping (Union[Unset, datetime.datetime]):
        error (Union[Unset, str]):
    """

    mqtt_resource_path: str
    subscribe_topics: List["MqttTriggerSubscribeTopicsItem"]
    enabled: bool
    path: str
    script_path: str
    email: str
    extra_perms: "MqttTriggerExtraPerms"
    workspace_id: str
    edited_by: str
    edited_at: datetime.datetime
    is_flow: bool
    v3_config: Union[Unset, "MqttTriggerV3Config"] = UNSET
    v5_config: Union[Unset, "MqttTriggerV5Config"] = UNSET
    client_id: Union[Unset, str] = UNSET
    client_version: Union[Unset, MqttTriggerClientVersion] = UNSET
    server_id: Union[Unset, str] = UNSET
    last_server_ping: Union[Unset, datetime.datetime] = UNSET
    error: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        mqtt_resource_path = self.mqtt_resource_path
        subscribe_topics = []
        for subscribe_topics_item_data in self.subscribe_topics:
            subscribe_topics_item = subscribe_topics_item_data.to_dict()

            subscribe_topics.append(subscribe_topics_item)

        enabled = self.enabled
        path = self.path
        script_path = self.script_path
        email = self.email
        extra_perms = self.extra_perms.to_dict()

        workspace_id = self.workspace_id
        edited_by = self.edited_by
        edited_at = self.edited_at.isoformat()

        is_flow = self.is_flow
        v3_config: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.v3_config, Unset):
            v3_config = self.v3_config.to_dict()

        v5_config: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.v5_config, Unset):
            v5_config = self.v5_config.to_dict()

        client_id = self.client_id
        client_version: Union[Unset, str] = UNSET
        if not isinstance(self.client_version, Unset):
            client_version = self.client_version.value

        server_id = self.server_id
        last_server_ping: Union[Unset, str] = UNSET
        if not isinstance(self.last_server_ping, Unset):
            last_server_ping = self.last_server_ping.isoformat()

        error = self.error

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "mqtt_resource_path": mqtt_resource_path,
                "subscribe_topics": subscribe_topics,
                "enabled": enabled,
                "path": path,
                "script_path": script_path,
                "email": email,
                "extra_perms": extra_perms,
                "workspace_id": workspace_id,
                "edited_by": edited_by,
                "edited_at": edited_at,
                "is_flow": is_flow,
            }
        )
        if v3_config is not UNSET:
            field_dict["v3_config"] = v3_config
        if v5_config is not UNSET:
            field_dict["v5_config"] = v5_config
        if client_id is not UNSET:
            field_dict["client_id"] = client_id
        if client_version is not UNSET:
            field_dict["client_version"] = client_version
        if server_id is not UNSET:
            field_dict["server_id"] = server_id
        if last_server_ping is not UNSET:
            field_dict["last_server_ping"] = last_server_ping
        if error is not UNSET:
            field_dict["error"] = error

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.mqtt_trigger_extra_perms import MqttTriggerExtraPerms
        from ..models.mqtt_trigger_subscribe_topics_item import MqttTriggerSubscribeTopicsItem
        from ..models.mqtt_trigger_v3_config import MqttTriggerV3Config
        from ..models.mqtt_trigger_v5_config import MqttTriggerV5Config

        d = src_dict.copy()
        mqtt_resource_path = d.pop("mqtt_resource_path")

        subscribe_topics = []
        _subscribe_topics = d.pop("subscribe_topics")
        for subscribe_topics_item_data in _subscribe_topics:
            subscribe_topics_item = MqttTriggerSubscribeTopicsItem.from_dict(subscribe_topics_item_data)

            subscribe_topics.append(subscribe_topics_item)

        enabled = d.pop("enabled")

        path = d.pop("path")

        script_path = d.pop("script_path")

        email = d.pop("email")

        extra_perms = MqttTriggerExtraPerms.from_dict(d.pop("extra_perms"))

        workspace_id = d.pop("workspace_id")

        edited_by = d.pop("edited_by")

        edited_at = isoparse(d.pop("edited_at"))

        is_flow = d.pop("is_flow")

        _v3_config = d.pop("v3_config", UNSET)
        v3_config: Union[Unset, MqttTriggerV3Config]
        if isinstance(_v3_config, Unset):
            v3_config = UNSET
        else:
            v3_config = MqttTriggerV3Config.from_dict(_v3_config)

        _v5_config = d.pop("v5_config", UNSET)
        v5_config: Union[Unset, MqttTriggerV5Config]
        if isinstance(_v5_config, Unset):
            v5_config = UNSET
        else:
            v5_config = MqttTriggerV5Config.from_dict(_v5_config)

        client_id = d.pop("client_id", UNSET)

        _client_version = d.pop("client_version", UNSET)
        client_version: Union[Unset, MqttTriggerClientVersion]
        if isinstance(_client_version, Unset):
            client_version = UNSET
        else:
            client_version = MqttTriggerClientVersion(_client_version)

        server_id = d.pop("server_id", UNSET)

        _last_server_ping = d.pop("last_server_ping", UNSET)
        last_server_ping: Union[Unset, datetime.datetime]
        if isinstance(_last_server_ping, Unset):
            last_server_ping = UNSET
        else:
            last_server_ping = isoparse(_last_server_ping)

        error = d.pop("error", UNSET)

        mqtt_trigger = cls(
            mqtt_resource_path=mqtt_resource_path,
            subscribe_topics=subscribe_topics,
            enabled=enabled,
            path=path,
            script_path=script_path,
            email=email,
            extra_perms=extra_perms,
            workspace_id=workspace_id,
            edited_by=edited_by,
            edited_at=edited_at,
            is_flow=is_flow,
            v3_config=v3_config,
            v5_config=v5_config,
            client_id=client_id,
            client_version=client_version,
            server_id=server_id,
            last_server_ping=last_server_ping,
            error=error,
        )

        mqtt_trigger.additional_properties = d
        return mqtt_trigger

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
