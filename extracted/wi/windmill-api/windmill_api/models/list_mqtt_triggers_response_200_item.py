import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.list_mqtt_triggers_response_200_item_client_version import ListMqttTriggersResponse200ItemClientVersion
from ..models.list_mqtt_triggers_response_200_item_mode import ListMqttTriggersResponse200ItemMode
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.list_mqtt_triggers_response_200_item_error_handler_args import (
        ListMqttTriggersResponse200ItemErrorHandlerArgs,
    )
    from ..models.list_mqtt_triggers_response_200_item_extra_perms import ListMqttTriggersResponse200ItemExtraPerms
    from ..models.list_mqtt_triggers_response_200_item_retry import ListMqttTriggersResponse200ItemRetry
    from ..models.list_mqtt_triggers_response_200_item_subscribe_topics_item import (
        ListMqttTriggersResponse200ItemSubscribeTopicsItem,
    )
    from ..models.list_mqtt_triggers_response_200_item_v3_config import ListMqttTriggersResponse200ItemV3Config
    from ..models.list_mqtt_triggers_response_200_item_v5_config import ListMqttTriggersResponse200ItemV5Config


T = TypeVar("T", bound="ListMqttTriggersResponse200Item")


@_attrs_define
class ListMqttTriggersResponse200Item:
    """
    Attributes:
        mqtt_resource_path (str): Path to the MQTT resource containing broker connection configuration
        subscribe_topics (List['ListMqttTriggersResponse200ItemSubscribeTopicsItem']): Array of MQTT topics to subscribe
            to, each with topic name and QoS level
        path (str): The unique Windmill path for this trigger. Must be of the form `u/<user>/<path>` or
            `f/<folder>/<path>`. This is the trigger object path, not the HTTP route path.
        script_path (str): Path to the script or flow to execute when triggered
        permissioned_as (str): The user or group this trigger runs as (permissioned_as)
        extra_perms (ListMqttTriggersResponse200ItemExtraPerms): Additional permissions for this trigger
        workspace_id (str): The workspace this trigger belongs to
        edited_by (str): Username of the last person who edited this trigger
        edited_at (datetime.datetime): Timestamp of the last edit
        is_flow (bool): True if script_path points to a flow, false if it points to a script
        mode (ListMqttTriggersResponse200ItemMode): job trigger mode
        v3_config (Union[Unset, None, ListMqttTriggersResponse200ItemV3Config]): MQTT v3 specific configuration
            (clean_session)
        v5_config (Union[Unset, None, ListMqttTriggersResponse200ItemV5Config]): MQTT v5 specific configuration
            (clean_start, topic_alias_maximum, session_expiry_interval)
        client_id (Union[Unset, None, str]): MQTT client ID for this connection
        client_version (Union[Unset, None, ListMqttTriggersResponse200ItemClientVersion]): MQTT protocol version ('v3'
            or 'v5')
        server_id (Union[Unset, str]): ID of the server currently handling this trigger (internal)
        last_server_ping (Union[Unset, datetime.datetime]): Timestamp of last server heartbeat (internal)
        error (Union[Unset, str]): Last error message if the trigger failed
        error_handler_path (Union[Unset, str]): Path to a script or flow to run when the triggered job fails
        error_handler_args (Union[Unset, ListMqttTriggersResponse200ItemErrorHandlerArgs]): The arguments to pass to the
            script or flow
        retry (Union[Unset, ListMqttTriggersResponse200ItemRetry]): Retry configuration for failed module executions
        labels (Union[Unset, List[str]]):
        draft_only (Union[Unset, bool]): True when this row is a per-user draft with no deployed
            trigger at the same path. Set by list endpoints when
            `include_draft_only=true` synthesizes the row from the
            draft. Frontend renders a "Draft" badge.
        is_draft (Union[Unset, bool]): True when the authed user has a per-user draft at this path
            (over a deployed row or a synthesized draft-only row).
            Frontend appends a `*` to the displayed name.
    """

    mqtt_resource_path: str
    subscribe_topics: List["ListMqttTriggersResponse200ItemSubscribeTopicsItem"]
    path: str
    script_path: str
    permissioned_as: str
    extra_perms: "ListMqttTriggersResponse200ItemExtraPerms"
    workspace_id: str
    edited_by: str
    edited_at: datetime.datetime
    is_flow: bool
    mode: ListMqttTriggersResponse200ItemMode
    v3_config: Union[Unset, None, "ListMqttTriggersResponse200ItemV3Config"] = UNSET
    v5_config: Union[Unset, None, "ListMqttTriggersResponse200ItemV5Config"] = UNSET
    client_id: Union[Unset, None, str] = UNSET
    client_version: Union[Unset, None, ListMqttTriggersResponse200ItemClientVersion] = UNSET
    server_id: Union[Unset, str] = UNSET
    last_server_ping: Union[Unset, datetime.datetime] = UNSET
    error: Union[Unset, str] = UNSET
    error_handler_path: Union[Unset, str] = UNSET
    error_handler_args: Union[Unset, "ListMqttTriggersResponse200ItemErrorHandlerArgs"] = UNSET
    retry: Union[Unset, "ListMqttTriggersResponse200ItemRetry"] = UNSET
    labels: Union[Unset, List[str]] = UNSET
    draft_only: Union[Unset, bool] = UNSET
    is_draft: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        mqtt_resource_path = self.mqtt_resource_path
        subscribe_topics = []
        for subscribe_topics_item_data in self.subscribe_topics:
            subscribe_topics_item = subscribe_topics_item_data.to_dict()

            subscribe_topics.append(subscribe_topics_item)

        path = self.path
        script_path = self.script_path
        permissioned_as = self.permissioned_as
        extra_perms = self.extra_perms.to_dict()

        workspace_id = self.workspace_id
        edited_by = self.edited_by
        edited_at = self.edited_at.isoformat()

        is_flow = self.is_flow
        mode = self.mode.value

        v3_config: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.v3_config, Unset):
            v3_config = self.v3_config.to_dict() if self.v3_config else None

        v5_config: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.v5_config, Unset):
            v5_config = self.v5_config.to_dict() if self.v5_config else None

        client_id = self.client_id
        client_version: Union[Unset, None, str] = UNSET
        if not isinstance(self.client_version, Unset):
            client_version = self.client_version.value if self.client_version else None

        server_id = self.server_id
        last_server_ping: Union[Unset, str] = UNSET
        if not isinstance(self.last_server_ping, Unset):
            last_server_ping = self.last_server_ping.isoformat()

        error = self.error
        error_handler_path = self.error_handler_path
        error_handler_args: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.error_handler_args, Unset):
            error_handler_args = self.error_handler_args.to_dict()

        retry: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.retry, Unset):
            retry = self.retry.to_dict()

        labels: Union[Unset, List[str]] = UNSET
        if not isinstance(self.labels, Unset):
            labels = self.labels

        draft_only = self.draft_only
        is_draft = self.is_draft

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "mqtt_resource_path": mqtt_resource_path,
                "subscribe_topics": subscribe_topics,
                "path": path,
                "script_path": script_path,
                "permissioned_as": permissioned_as,
                "extra_perms": extra_perms,
                "workspace_id": workspace_id,
                "edited_by": edited_by,
                "edited_at": edited_at,
                "is_flow": is_flow,
                "mode": mode,
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
        if error_handler_path is not UNSET:
            field_dict["error_handler_path"] = error_handler_path
        if error_handler_args is not UNSET:
            field_dict["error_handler_args"] = error_handler_args
        if retry is not UNSET:
            field_dict["retry"] = retry
        if labels is not UNSET:
            field_dict["labels"] = labels
        if draft_only is not UNSET:
            field_dict["draft_only"] = draft_only
        if is_draft is not UNSET:
            field_dict["is_draft"] = is_draft

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.list_mqtt_triggers_response_200_item_error_handler_args import (
            ListMqttTriggersResponse200ItemErrorHandlerArgs,
        )
        from ..models.list_mqtt_triggers_response_200_item_extra_perms import ListMqttTriggersResponse200ItemExtraPerms
        from ..models.list_mqtt_triggers_response_200_item_retry import ListMqttTriggersResponse200ItemRetry
        from ..models.list_mqtt_triggers_response_200_item_subscribe_topics_item import (
            ListMqttTriggersResponse200ItemSubscribeTopicsItem,
        )
        from ..models.list_mqtt_triggers_response_200_item_v3_config import ListMqttTriggersResponse200ItemV3Config
        from ..models.list_mqtt_triggers_response_200_item_v5_config import ListMqttTriggersResponse200ItemV5Config

        d = src_dict.copy()
        mqtt_resource_path = d.pop("mqtt_resource_path")

        subscribe_topics = []
        _subscribe_topics = d.pop("subscribe_topics")
        for subscribe_topics_item_data in _subscribe_topics:
            subscribe_topics_item = ListMqttTriggersResponse200ItemSubscribeTopicsItem.from_dict(
                subscribe_topics_item_data
            )

            subscribe_topics.append(subscribe_topics_item)

        path = d.pop("path")

        script_path = d.pop("script_path")

        permissioned_as = d.pop("permissioned_as")

        extra_perms = ListMqttTriggersResponse200ItemExtraPerms.from_dict(d.pop("extra_perms"))

        workspace_id = d.pop("workspace_id")

        edited_by = d.pop("edited_by")

        edited_at = isoparse(d.pop("edited_at"))

        is_flow = d.pop("is_flow")

        mode = ListMqttTriggersResponse200ItemMode(d.pop("mode"))

        _v3_config = d.pop("v3_config", UNSET)
        v3_config: Union[Unset, None, ListMqttTriggersResponse200ItemV3Config]
        if _v3_config is None:
            v3_config = None
        elif isinstance(_v3_config, Unset):
            v3_config = UNSET
        else:
            v3_config = ListMqttTriggersResponse200ItemV3Config.from_dict(_v3_config)

        _v5_config = d.pop("v5_config", UNSET)
        v5_config: Union[Unset, None, ListMqttTriggersResponse200ItemV5Config]
        if _v5_config is None:
            v5_config = None
        elif isinstance(_v5_config, Unset):
            v5_config = UNSET
        else:
            v5_config = ListMqttTriggersResponse200ItemV5Config.from_dict(_v5_config)

        client_id = d.pop("client_id", UNSET)

        _client_version = d.pop("client_version", UNSET)
        client_version: Union[Unset, None, ListMqttTriggersResponse200ItemClientVersion]
        if _client_version is None:
            client_version = None
        elif isinstance(_client_version, Unset):
            client_version = UNSET
        else:
            client_version = ListMqttTriggersResponse200ItemClientVersion(_client_version)

        server_id = d.pop("server_id", UNSET)

        _last_server_ping = d.pop("last_server_ping", UNSET)
        last_server_ping: Union[Unset, datetime.datetime]
        if isinstance(_last_server_ping, Unset):
            last_server_ping = UNSET
        else:
            last_server_ping = isoparse(_last_server_ping)

        error = d.pop("error", UNSET)

        error_handler_path = d.pop("error_handler_path", UNSET)

        _error_handler_args = d.pop("error_handler_args", UNSET)
        error_handler_args: Union[Unset, ListMqttTriggersResponse200ItemErrorHandlerArgs]
        if isinstance(_error_handler_args, Unset):
            error_handler_args = UNSET
        else:
            error_handler_args = ListMqttTriggersResponse200ItemErrorHandlerArgs.from_dict(_error_handler_args)

        _retry = d.pop("retry", UNSET)
        retry: Union[Unset, ListMqttTriggersResponse200ItemRetry]
        if isinstance(_retry, Unset):
            retry = UNSET
        else:
            retry = ListMqttTriggersResponse200ItemRetry.from_dict(_retry)

        labels = cast(List[str], d.pop("labels", UNSET))

        draft_only = d.pop("draft_only", UNSET)

        is_draft = d.pop("is_draft", UNSET)

        list_mqtt_triggers_response_200_item = cls(
            mqtt_resource_path=mqtt_resource_path,
            subscribe_topics=subscribe_topics,
            path=path,
            script_path=script_path,
            permissioned_as=permissioned_as,
            extra_perms=extra_perms,
            workspace_id=workspace_id,
            edited_by=edited_by,
            edited_at=edited_at,
            is_flow=is_flow,
            mode=mode,
            v3_config=v3_config,
            v5_config=v5_config,
            client_id=client_id,
            client_version=client_version,
            server_id=server_id,
            last_server_ping=last_server_ping,
            error=error,
            error_handler_path=error_handler_path,
            error_handler_args=error_handler_args,
            retry=retry,
            labels=labels,
            draft_only=draft_only,
            is_draft=is_draft,
        )

        list_mqtt_triggers_response_200_item.additional_properties = d
        return list_mqtt_triggers_response_200_item

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
