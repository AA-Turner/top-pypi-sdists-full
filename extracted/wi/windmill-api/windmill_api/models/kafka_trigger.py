import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.kafka_trigger_auto_offset_reset import KafkaTriggerAutoOffsetReset
from ..models.kafka_trigger_mode import KafkaTriggerMode
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.kafka_trigger_error_handler_args import KafkaTriggerErrorHandlerArgs
    from ..models.kafka_trigger_extra_perms import KafkaTriggerExtraPerms
    from ..models.kafka_trigger_filters_item import KafkaTriggerFiltersItem
    from ..models.kafka_trigger_retry import KafkaTriggerRetry


T = TypeVar("T", bound="KafkaTrigger")


@_attrs_define
class KafkaTrigger:
    """
    Attributes:
        kafka_resource_path (str): Path to the Kafka resource containing connection configuration
        group_id (str): Kafka consumer group ID for this trigger
        topics (List[str]): Array of Kafka topic names to subscribe to
        filters (List['KafkaTriggerFiltersItem']):
        path (str): The unique path identifier for this trigger
        script_path (str): Path to the script or flow to execute when triggered
        email (str): Email of the user who owns this trigger, used for permissioned_as
        extra_perms (KafkaTriggerExtraPerms): Additional permissions for this trigger
        workspace_id (str): The workspace this trigger belongs to
        edited_by (str): Username of the last person who edited this trigger
        edited_at (datetime.datetime): Timestamp of the last edit
        is_flow (bool): True if script_path points to a flow, false if it points to a script
        mode (KafkaTriggerMode): job trigger mode
        auto_offset_reset (Union[Unset, KafkaTriggerAutoOffsetReset]): Initial offset behavior when consumer group has
            no committed offset. 'latest' starts from new messages only, 'earliest' starts from the beginning. Default:
            KafkaTriggerAutoOffsetReset.LATEST.
        auto_commit (Union[Unset, bool]): When true (default), offsets are committed automatically after receiving each
            message. When false, you must manually commit offsets using the commit_offsets endpoint. Default: True.
        server_id (Union[Unset, str]): ID of the server currently handling this trigger (internal)
        last_server_ping (Union[Unset, datetime.datetime]): Timestamp of last server heartbeat (internal)
        error (Union[Unset, str]): Last error message if the trigger failed
        error_handler_path (Union[Unset, str]): Path to a script or flow to run when the triggered job fails
        error_handler_args (Union[Unset, KafkaTriggerErrorHandlerArgs]): The arguments to pass to the script or flow
        retry (Union[Unset, KafkaTriggerRetry]): Retry configuration for failed module executions
    """

    kafka_resource_path: str
    group_id: str
    topics: List[str]
    filters: List["KafkaTriggerFiltersItem"]
    path: str
    script_path: str
    email: str
    extra_perms: "KafkaTriggerExtraPerms"
    workspace_id: str
    edited_by: str
    edited_at: datetime.datetime
    is_flow: bool
    mode: KafkaTriggerMode
    auto_offset_reset: Union[Unset, KafkaTriggerAutoOffsetReset] = KafkaTriggerAutoOffsetReset.LATEST
    auto_commit: Union[Unset, bool] = True
    server_id: Union[Unset, str] = UNSET
    last_server_ping: Union[Unset, datetime.datetime] = UNSET
    error: Union[Unset, str] = UNSET
    error_handler_path: Union[Unset, str] = UNSET
    error_handler_args: Union[Unset, "KafkaTriggerErrorHandlerArgs"] = UNSET
    retry: Union[Unset, "KafkaTriggerRetry"] = UNSET
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
        email = self.email
        extra_perms = self.extra_perms.to_dict()

        workspace_id = self.workspace_id
        edited_by = self.edited_by
        edited_at = self.edited_at.isoformat()

        is_flow = self.is_flow
        mode = self.mode.value

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
                "email": email,
                "extra_perms": extra_perms,
                "workspace_id": workspace_id,
                "edited_by": edited_by,
                "edited_at": edited_at,
                "is_flow": is_flow,
                "mode": mode,
            }
        )
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
        from ..models.kafka_trigger_error_handler_args import KafkaTriggerErrorHandlerArgs
        from ..models.kafka_trigger_extra_perms import KafkaTriggerExtraPerms
        from ..models.kafka_trigger_filters_item import KafkaTriggerFiltersItem
        from ..models.kafka_trigger_retry import KafkaTriggerRetry

        d = src_dict.copy()
        kafka_resource_path = d.pop("kafka_resource_path")

        group_id = d.pop("group_id")

        topics = cast(List[str], d.pop("topics"))

        filters = []
        _filters = d.pop("filters")
        for filters_item_data in _filters:
            filters_item = KafkaTriggerFiltersItem.from_dict(filters_item_data)

            filters.append(filters_item)

        path = d.pop("path")

        script_path = d.pop("script_path")

        email = d.pop("email")

        extra_perms = KafkaTriggerExtraPerms.from_dict(d.pop("extra_perms"))

        workspace_id = d.pop("workspace_id")

        edited_by = d.pop("edited_by")

        edited_at = isoparse(d.pop("edited_at"))

        is_flow = d.pop("is_flow")

        mode = KafkaTriggerMode(d.pop("mode"))

        _auto_offset_reset = d.pop("auto_offset_reset", UNSET)
        auto_offset_reset: Union[Unset, KafkaTriggerAutoOffsetReset]
        if isinstance(_auto_offset_reset, Unset):
            auto_offset_reset = UNSET
        else:
            auto_offset_reset = KafkaTriggerAutoOffsetReset(_auto_offset_reset)

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
        error_handler_args: Union[Unset, KafkaTriggerErrorHandlerArgs]
        if isinstance(_error_handler_args, Unset):
            error_handler_args = UNSET
        else:
            error_handler_args = KafkaTriggerErrorHandlerArgs.from_dict(_error_handler_args)

        _retry = d.pop("retry", UNSET)
        retry: Union[Unset, KafkaTriggerRetry]
        if isinstance(_retry, Unset):
            retry = UNSET
        else:
            retry = KafkaTriggerRetry.from_dict(_retry)

        kafka_trigger = cls(
            kafka_resource_path=kafka_resource_path,
            group_id=group_id,
            topics=topics,
            filters=filters,
            path=path,
            script_path=script_path,
            email=email,
            extra_perms=extra_perms,
            workspace_id=workspace_id,
            edited_by=edited_by,
            edited_at=edited_at,
            is_flow=is_flow,
            mode=mode,
            auto_offset_reset=auto_offset_reset,
            auto_commit=auto_commit,
            server_id=server_id,
            last_server_ping=last_server_ping,
            error=error,
            error_handler_path=error_handler_path,
            error_handler_args=error_handler_args,
            retry=retry,
        )

        kafka_trigger.additional_properties = d
        return kafka_trigger

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
