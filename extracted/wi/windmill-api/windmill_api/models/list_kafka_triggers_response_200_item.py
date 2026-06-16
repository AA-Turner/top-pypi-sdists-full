import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.list_kafka_triggers_response_200_item_auto_offset_reset import (
    ListKafkaTriggersResponse200ItemAutoOffsetReset,
)
from ..models.list_kafka_triggers_response_200_item_filter_logic import ListKafkaTriggersResponse200ItemFilterLogic
from ..models.list_kafka_triggers_response_200_item_mode import ListKafkaTriggersResponse200ItemMode
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.list_kafka_triggers_response_200_item_error_handler_args import (
        ListKafkaTriggersResponse200ItemErrorHandlerArgs,
    )
    from ..models.list_kafka_triggers_response_200_item_extra_perms import ListKafkaTriggersResponse200ItemExtraPerms
    from ..models.list_kafka_triggers_response_200_item_filters_item import ListKafkaTriggersResponse200ItemFiltersItem
    from ..models.list_kafka_triggers_response_200_item_retry import ListKafkaTriggersResponse200ItemRetry


T = TypeVar("T", bound="ListKafkaTriggersResponse200Item")


@_attrs_define
class ListKafkaTriggersResponse200Item:
    """
    Attributes:
        kafka_resource_path (str): Path to the Kafka resource containing connection configuration
        group_id (str): Kafka consumer group ID for this trigger
        topics (List[str]): Array of Kafka topic names to subscribe to
        filters (List['ListKafkaTriggersResponse200ItemFiltersItem']):
        path (str): The unique Windmill path for this trigger. Must be of the form `u/<user>/<path>` or
            `f/<folder>/<path>`. This is the trigger object path, not the HTTP route path.
        script_path (str): Path to the script or flow to execute when triggered
        permissioned_as (str): The user or group this trigger runs as (permissioned_as)
        extra_perms (ListKafkaTriggersResponse200ItemExtraPerms): Additional permissions for this trigger
        workspace_id (str): The workspace this trigger belongs to
        edited_by (str): Username of the last person who edited this trigger
        edited_at (datetime.datetime): Timestamp of the last edit
        is_flow (bool): True if script_path points to a flow, false if it points to a script
        mode (ListKafkaTriggersResponse200ItemMode): job trigger mode
        filter_logic (Union[Unset, ListKafkaTriggersResponse200ItemFilterLogic]): Logic to apply when evaluating
            filters. 'and' requires all filters to match, 'or' requires any filter to match. Default:
            ListKafkaTriggersResponse200ItemFilterLogic.AND.
        auto_offset_reset (Union[Unset, ListKafkaTriggersResponse200ItemAutoOffsetReset]): Initial offset behavior when
            consumer group has no committed offset. 'latest' starts from new messages only, 'earliest' starts from the
            beginning. Default: ListKafkaTriggersResponse200ItemAutoOffsetReset.LATEST.
        auto_commit (Union[Unset, bool]): When true (default), offsets are committed automatically after receiving each
            message. When false, you must manually commit offsets using the commit_offsets endpoint. Default: True.
        server_id (Union[Unset, str]): ID of the server currently handling this trigger (internal)
        last_server_ping (Union[Unset, datetime.datetime]): Timestamp of last server heartbeat (internal)
        error (Union[Unset, str]): Last error message if the trigger failed
        error_handler_path (Union[Unset, str]): Path to a script or flow to run when the triggered job fails
        error_handler_args (Union[Unset, ListKafkaTriggersResponse200ItemErrorHandlerArgs]): The arguments to pass to
            the script or flow
        retry (Union[Unset, ListKafkaTriggersResponse200ItemRetry]): Retry configuration for failed module executions
        labels (Union[Unset, List[str]]):
        draft_only (Union[Unset, bool]): True when this row is a per-user draft with no deployed
            trigger at the same path. Set by list endpoints when
            `include_draft_only=true` synthesizes the row from the
            draft. Frontend renders a "Draft" badge.
        is_draft (Union[Unset, bool]): True when the authed user has a per-user draft at this path
            (over a deployed row or a synthesized draft-only row).
            Frontend appends a `*` to the displayed name.
    """

    kafka_resource_path: str
    group_id: str
    topics: List[str]
    filters: List["ListKafkaTriggersResponse200ItemFiltersItem"]
    path: str
    script_path: str
    permissioned_as: str
    extra_perms: "ListKafkaTriggersResponse200ItemExtraPerms"
    workspace_id: str
    edited_by: str
    edited_at: datetime.datetime
    is_flow: bool
    mode: ListKafkaTriggersResponse200ItemMode
    filter_logic: Union[
        Unset, ListKafkaTriggersResponse200ItemFilterLogic
    ] = ListKafkaTriggersResponse200ItemFilterLogic.AND
    auto_offset_reset: Union[
        Unset, ListKafkaTriggersResponse200ItemAutoOffsetReset
    ] = ListKafkaTriggersResponse200ItemAutoOffsetReset.LATEST
    auto_commit: Union[Unset, bool] = True
    server_id: Union[Unset, str] = UNSET
    last_server_ping: Union[Unset, datetime.datetime] = UNSET
    error: Union[Unset, str] = UNSET
    error_handler_path: Union[Unset, str] = UNSET
    error_handler_args: Union[Unset, "ListKafkaTriggersResponse200ItemErrorHandlerArgs"] = UNSET
    retry: Union[Unset, "ListKafkaTriggersResponse200ItemRetry"] = UNSET
    labels: Union[Unset, List[str]] = UNSET
    draft_only: Union[Unset, bool] = UNSET
    is_draft: Union[Unset, bool] = UNSET
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

        labels: Union[Unset, List[str]] = UNSET
        if not isinstance(self.labels, Unset):
            labels = self.labels

        draft_only = self.draft_only
        is_draft = self.is_draft

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
        if labels is not UNSET:
            field_dict["labels"] = labels
        if draft_only is not UNSET:
            field_dict["draft_only"] = draft_only
        if is_draft is not UNSET:
            field_dict["is_draft"] = is_draft

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.list_kafka_triggers_response_200_item_error_handler_args import (
            ListKafkaTriggersResponse200ItemErrorHandlerArgs,
        )
        from ..models.list_kafka_triggers_response_200_item_extra_perms import (
            ListKafkaTriggersResponse200ItemExtraPerms,
        )
        from ..models.list_kafka_triggers_response_200_item_filters_item import (
            ListKafkaTriggersResponse200ItemFiltersItem,
        )
        from ..models.list_kafka_triggers_response_200_item_retry import ListKafkaTriggersResponse200ItemRetry

        d = src_dict.copy()
        kafka_resource_path = d.pop("kafka_resource_path")

        group_id = d.pop("group_id")

        topics = cast(List[str], d.pop("topics"))

        filters = []
        _filters = d.pop("filters")
        for filters_item_data in _filters:
            filters_item = ListKafkaTriggersResponse200ItemFiltersItem.from_dict(filters_item_data)

            filters.append(filters_item)

        path = d.pop("path")

        script_path = d.pop("script_path")

        permissioned_as = d.pop("permissioned_as")

        extra_perms = ListKafkaTriggersResponse200ItemExtraPerms.from_dict(d.pop("extra_perms"))

        workspace_id = d.pop("workspace_id")

        edited_by = d.pop("edited_by")

        edited_at = isoparse(d.pop("edited_at"))

        is_flow = d.pop("is_flow")

        mode = ListKafkaTriggersResponse200ItemMode(d.pop("mode"))

        _filter_logic = d.pop("filter_logic", UNSET)
        filter_logic: Union[Unset, ListKafkaTriggersResponse200ItemFilterLogic]
        if isinstance(_filter_logic, Unset):
            filter_logic = UNSET
        else:
            filter_logic = ListKafkaTriggersResponse200ItemFilterLogic(_filter_logic)

        _auto_offset_reset = d.pop("auto_offset_reset", UNSET)
        auto_offset_reset: Union[Unset, ListKafkaTriggersResponse200ItemAutoOffsetReset]
        if isinstance(_auto_offset_reset, Unset):
            auto_offset_reset = UNSET
        else:
            auto_offset_reset = ListKafkaTriggersResponse200ItemAutoOffsetReset(_auto_offset_reset)

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
        error_handler_args: Union[Unset, ListKafkaTriggersResponse200ItemErrorHandlerArgs]
        if isinstance(_error_handler_args, Unset):
            error_handler_args = UNSET
        else:
            error_handler_args = ListKafkaTriggersResponse200ItemErrorHandlerArgs.from_dict(_error_handler_args)

        _retry = d.pop("retry", UNSET)
        retry: Union[Unset, ListKafkaTriggersResponse200ItemRetry]
        if isinstance(_retry, Unset):
            retry = UNSET
        else:
            retry = ListKafkaTriggersResponse200ItemRetry.from_dict(_retry)

        labels = cast(List[str], d.pop("labels", UNSET))

        draft_only = d.pop("draft_only", UNSET)

        is_draft = d.pop("is_draft", UNSET)

        list_kafka_triggers_response_200_item = cls(
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
            labels=labels,
            draft_only=draft_only,
            is_draft=is_draft,
        )

        list_kafka_triggers_response_200_item.additional_properties = d
        return list_kafka_triggers_response_200_item

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
