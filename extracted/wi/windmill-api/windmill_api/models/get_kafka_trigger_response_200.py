import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.get_kafka_trigger_response_200_auto_offset_reset import GetKafkaTriggerResponse200AutoOffsetReset
from ..models.get_kafka_trigger_response_200_filter_logic import GetKafkaTriggerResponse200FilterLogic
from ..models.get_kafka_trigger_response_200_mode import GetKafkaTriggerResponse200Mode
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_kafka_trigger_response_200_error_handler_args import GetKafkaTriggerResponse200ErrorHandlerArgs
    from ..models.get_kafka_trigger_response_200_extra_perms import GetKafkaTriggerResponse200ExtraPerms
    from ..models.get_kafka_trigger_response_200_filters_item import GetKafkaTriggerResponse200FiltersItem
    from ..models.get_kafka_trigger_response_200_retry import GetKafkaTriggerResponse200Retry


T = TypeVar("T", bound="GetKafkaTriggerResponse200")


@_attrs_define
class GetKafkaTriggerResponse200:
    """
    Attributes:
        kafka_resource_path (str): Path to the Kafka resource containing connection configuration
        group_id (str): Kafka consumer group ID for this trigger
        topics (List[str]): Array of Kafka topic names to subscribe to
        filters (List['GetKafkaTriggerResponse200FiltersItem']):
        path (str): The unique path identifier for this trigger
        script_path (str): Path to the script or flow to execute when triggered
        permissioned_as (str): The user or group this trigger runs as (permissioned_as)
        extra_perms (GetKafkaTriggerResponse200ExtraPerms): Additional permissions for this trigger
        workspace_id (str): The workspace this trigger belongs to
        edited_by (str): Username of the last person who edited this trigger
        edited_at (datetime.datetime): Timestamp of the last edit
        is_flow (bool): True if script_path points to a flow, false if it points to a script
        mode (GetKafkaTriggerResponse200Mode): job trigger mode
        filter_logic (Union[Unset, GetKafkaTriggerResponse200FilterLogic]): Logic to apply when evaluating filters.
            'and' requires all filters to match, 'or' requires any filter to match. Default:
            GetKafkaTriggerResponse200FilterLogic.AND.
        auto_offset_reset (Union[Unset, GetKafkaTriggerResponse200AutoOffsetReset]): Initial offset behavior when
            consumer group has no committed offset. 'latest' starts from new messages only, 'earliest' starts from the
            beginning. Default: GetKafkaTriggerResponse200AutoOffsetReset.LATEST.
        auto_commit (Union[Unset, bool]): When true (default), offsets are committed automatically after receiving each
            message. When false, you must manually commit offsets using the commit_offsets endpoint. Default: True.
        server_id (Union[Unset, str]): ID of the server currently handling this trigger (internal)
        last_server_ping (Union[Unset, datetime.datetime]): Timestamp of last server heartbeat (internal)
        error (Union[Unset, str]): Last error message if the trigger failed
        error_handler_path (Union[Unset, str]): Path to a script or flow to run when the triggered job fails
        error_handler_args (Union[Unset, GetKafkaTriggerResponse200ErrorHandlerArgs]): The arguments to pass to the
            script or flow
        retry (Union[Unset, GetKafkaTriggerResponse200Retry]): Retry configuration for failed module executions
    """

    kafka_resource_path: str
    group_id: str
    topics: List[str]
    filters: List["GetKafkaTriggerResponse200FiltersItem"]
    path: str
    script_path: str
    permissioned_as: str
    extra_perms: "GetKafkaTriggerResponse200ExtraPerms"
    workspace_id: str
    edited_by: str
    edited_at: datetime.datetime
    is_flow: bool
    mode: GetKafkaTriggerResponse200Mode
    filter_logic: Union[Unset, GetKafkaTriggerResponse200FilterLogic] = GetKafkaTriggerResponse200FilterLogic.AND
    auto_offset_reset: Union[
        Unset, GetKafkaTriggerResponse200AutoOffsetReset
    ] = GetKafkaTriggerResponse200AutoOffsetReset.LATEST
    auto_commit: Union[Unset, bool] = True
    server_id: Union[Unset, str] = UNSET
    last_server_ping: Union[Unset, datetime.datetime] = UNSET
    error: Union[Unset, str] = UNSET
    error_handler_path: Union[Unset, str] = UNSET
    error_handler_args: Union[Unset, "GetKafkaTriggerResponse200ErrorHandlerArgs"] = UNSET
    retry: Union[Unset, "GetKafkaTriggerResponse200Retry"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        kafka_resource_path = self.kafka_resource_path
        group_id = self.group_id
        topics = self.topics

        filters = []
        for filters_item_data in self.filters:
            filters_item = filters_item_data.to_dict()

            filters.append(filters_item)

        path = self.path
        script_path = self.script_path
        permissioned_as = self.permissioned_as
        extra_perms = self.extra_perms.to_dict()

        workspace_id = self.workspace_id
        edited_by = self.edited_by
        edited_at = self.edited_at.isoformat()

        is_flow = self.is_flow
        mode = self.mode.value

        filter_logic: Union[Unset, str] = UNSET
        if not isinstance(self.filter_logic, Unset):
            filter_logic = self.filter_logic.value

        auto_offset_reset: Union[Unset, str] = UNSET
        if not isinstance(self.auto_offset_reset, Unset):
            auto_offset_reset = self.auto_offset_reset.value

        auto_commit = self.auto_commit
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

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "kafka_resource_path": kafka_resource_path,
                "group_id": group_id,
                "topics": topics,
                "filters": filters,
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
        if filter_logic is not UNSET:
            field_dict["filter_logic"] = filter_logic
        if auto_offset_reset is not UNSET:
            field_dict["auto_offset_reset"] = auto_offset_reset
        if auto_commit is not UNSET:
            field_dict["auto_commit"] = auto_commit
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

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.get_kafka_trigger_response_200_error_handler_args import (
            GetKafkaTriggerResponse200ErrorHandlerArgs,
        )
        from ..models.get_kafka_trigger_response_200_extra_perms import GetKafkaTriggerResponse200ExtraPerms
        from ..models.get_kafka_trigger_response_200_filters_item import GetKafkaTriggerResponse200FiltersItem
        from ..models.get_kafka_trigger_response_200_retry import GetKafkaTriggerResponse200Retry

        d = src_dict.copy()
        kafka_resource_path = d.pop("kafka_resource_path")

        group_id = d.pop("group_id")

        topics = cast(List[str], d.pop("topics"))

        filters = []
        _filters = d.pop("filters")
        for filters_item_data in _filters:
            filters_item = GetKafkaTriggerResponse200FiltersItem.from_dict(filters_item_data)

            filters.append(filters_item)

        path = d.pop("path")

        script_path = d.pop("script_path")

        permissioned_as = d.pop("permissioned_as")

        extra_perms = GetKafkaTriggerResponse200ExtraPerms.from_dict(d.pop("extra_perms"))

        workspace_id = d.pop("workspace_id")

        edited_by = d.pop("edited_by")

        edited_at = isoparse(d.pop("edited_at"))

        is_flow = d.pop("is_flow")

        mode = GetKafkaTriggerResponse200Mode(d.pop("mode"))

        _filter_logic = d.pop("filter_logic", UNSET)
        filter_logic: Union[Unset, GetKafkaTriggerResponse200FilterLogic]
        if isinstance(_filter_logic, Unset):
            filter_logic = UNSET
        else:
            filter_logic = GetKafkaTriggerResponse200FilterLogic(_filter_logic)

        _auto_offset_reset = d.pop("auto_offset_reset", UNSET)
        auto_offset_reset: Union[Unset, GetKafkaTriggerResponse200AutoOffsetReset]
        if isinstance(_auto_offset_reset, Unset):
            auto_offset_reset = UNSET
        else:
            auto_offset_reset = GetKafkaTriggerResponse200AutoOffsetReset(_auto_offset_reset)

        auto_commit = d.pop("auto_commit", UNSET)

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
        error_handler_args: Union[Unset, GetKafkaTriggerResponse200ErrorHandlerArgs]
        if isinstance(_error_handler_args, Unset):
            error_handler_args = UNSET
        else:
            error_handler_args = GetKafkaTriggerResponse200ErrorHandlerArgs.from_dict(_error_handler_args)

        _retry = d.pop("retry", UNSET)
        retry: Union[Unset, GetKafkaTriggerResponse200Retry]
        if isinstance(_retry, Unset):
            retry = UNSET
        else:
            retry = GetKafkaTriggerResponse200Retry.from_dict(_retry)

        get_kafka_trigger_response_200 = cls(
            kafka_resource_path=kafka_resource_path,
            group_id=group_id,
            topics=topics,
            filters=filters,
            path=path,
            script_path=script_path,
            permissioned_as=permissioned_as,
            extra_perms=extra_perms,
            workspace_id=workspace_id,
            edited_by=edited_by,
            edited_at=edited_at,
            is_flow=is_flow,
            mode=mode,
            filter_logic=filter_logic,
            auto_offset_reset=auto_offset_reset,
            auto_commit=auto_commit,
            server_id=server_id,
            last_server_ping=last_server_ping,
            error=error,
            error_handler_path=error_handler_path,
            error_handler_args=error_handler_args,
            retry=retry,
        )

        get_kafka_trigger_response_200.additional_properties = d
        return get_kafka_trigger_response_200

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
