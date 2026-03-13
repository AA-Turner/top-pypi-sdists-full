from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.create_kafka_trigger_json_body_auto_offset_reset import CreateKafkaTriggerJsonBodyAutoOffsetReset
from ..models.create_kafka_trigger_json_body_mode import CreateKafkaTriggerJsonBodyMode
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.create_kafka_trigger_json_body_error_handler_args import CreateKafkaTriggerJsonBodyErrorHandlerArgs
    from ..models.create_kafka_trigger_json_body_filters_item import CreateKafkaTriggerJsonBodyFiltersItem
    from ..models.create_kafka_trigger_json_body_retry import CreateKafkaTriggerJsonBodyRetry


T = TypeVar("T", bound="CreateKafkaTriggerJsonBody")


@_attrs_define
class CreateKafkaTriggerJsonBody:
    """
    Attributes:
        path (str): The unique path identifier for this trigger
        script_path (str): Path to the script or flow to execute when a message is received
        is_flow (bool): True if script_path points to a flow, false if it points to a script
        kafka_resource_path (str): Path to the Kafka resource containing connection configuration
        group_id (str): Kafka consumer group ID for this trigger
        topics (List[str]): Array of Kafka topic names to subscribe to
        filters (List['CreateKafkaTriggerJsonBodyFiltersItem']):
        auto_offset_reset (Union[Unset, CreateKafkaTriggerJsonBodyAutoOffsetReset]): Initial offset behavior when
            consumer group has no committed offset. Default: CreateKafkaTriggerJsonBodyAutoOffsetReset.LATEST.
        auto_commit (Union[Unset, bool]): When true (default), offsets are committed automatically after receiving each
            message. When false, you must manually commit offsets using the commit_offsets endpoint. Default: True.
        mode (Union[Unset, CreateKafkaTriggerJsonBodyMode]): job trigger mode
        error_handler_path (Union[Unset, str]): Path to a script or flow to run when the triggered job fails
        error_handler_args (Union[Unset, CreateKafkaTriggerJsonBodyErrorHandlerArgs]): The arguments to pass to the
            script or flow
        retry (Union[Unset, CreateKafkaTriggerJsonBodyRetry]): Retry configuration for failed module executions
        email (Union[Unset, str]): Email of the user who triggered jobs run as. Used during deployment to preserve the
            original trigger owner.
        preserve_email (Union[Unset, bool]): When true and the caller is a member of the 'wm_deployers' group, preserves
            the original email value instead of overwriting it.
    """

    path: str
    script_path: str
    is_flow: bool
    kafka_resource_path: str
    group_id: str
    topics: List[str]
    filters: List["CreateKafkaTriggerJsonBodyFiltersItem"]
    auto_offset_reset: Union[
        Unset, CreateKafkaTriggerJsonBodyAutoOffsetReset
    ] = CreateKafkaTriggerJsonBodyAutoOffsetReset.LATEST
    auto_commit: Union[Unset, bool] = True
    mode: Union[Unset, CreateKafkaTriggerJsonBodyMode] = UNSET
    error_handler_path: Union[Unset, str] = UNSET
    error_handler_args: Union[Unset, "CreateKafkaTriggerJsonBodyErrorHandlerArgs"] = UNSET
    retry: Union[Unset, "CreateKafkaTriggerJsonBodyRetry"] = UNSET
    email: Union[Unset, str] = UNSET
    preserve_email: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        path = self.path
        script_path = self.script_path
        is_flow = self.is_flow
        kafka_resource_path = self.kafka_resource_path
        group_id = self.group_id
        topics = self.topics

        filters = []
        for filters_item_data in self.filters:
            filters_item = filters_item_data.to_dict()

            filters.append(filters_item)

        auto_offset_reset: Union[Unset, str] = UNSET
        if not isinstance(self.auto_offset_reset, Unset):
            auto_offset_reset = self.auto_offset_reset.value

        auto_commit = self.auto_commit
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

        email = self.email
        preserve_email = self.preserve_email

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "path": path,
                "script_path": script_path,
                "is_flow": is_flow,
                "kafka_resource_path": kafka_resource_path,
                "group_id": group_id,
                "topics": topics,
                "filters": filters,
            }
        )
        if auto_offset_reset is not UNSET:
            field_dict["auto_offset_reset"] = auto_offset_reset
        if auto_commit is not UNSET:
            field_dict["auto_commit"] = auto_commit
        if mode is not UNSET:
            field_dict["mode"] = mode
        if error_handler_path is not UNSET:
            field_dict["error_handler_path"] = error_handler_path
        if error_handler_args is not UNSET:
            field_dict["error_handler_args"] = error_handler_args
        if retry is not UNSET:
            field_dict["retry"] = retry
        if email is not UNSET:
            field_dict["email"] = email
        if preserve_email is not UNSET:
            field_dict["preserve_email"] = preserve_email

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.create_kafka_trigger_json_body_error_handler_args import (
            CreateKafkaTriggerJsonBodyErrorHandlerArgs,
        )
        from ..models.create_kafka_trigger_json_body_filters_item import CreateKafkaTriggerJsonBodyFiltersItem
        from ..models.create_kafka_trigger_json_body_retry import CreateKafkaTriggerJsonBodyRetry

        d = src_dict.copy()
        path = d.pop("path")

        script_path = d.pop("script_path")

        is_flow = d.pop("is_flow")

        kafka_resource_path = d.pop("kafka_resource_path")

        group_id = d.pop("group_id")

        topics = cast(List[str], d.pop("topics"))

        filters = []
        _filters = d.pop("filters")
        for filters_item_data in _filters:
            filters_item = CreateKafkaTriggerJsonBodyFiltersItem.from_dict(filters_item_data)

            filters.append(filters_item)

        _auto_offset_reset = d.pop("auto_offset_reset", UNSET)
        auto_offset_reset: Union[Unset, CreateKafkaTriggerJsonBodyAutoOffsetReset]
        if isinstance(_auto_offset_reset, Unset):
            auto_offset_reset = UNSET
        else:
            auto_offset_reset = CreateKafkaTriggerJsonBodyAutoOffsetReset(_auto_offset_reset)

        auto_commit = d.pop("auto_commit", UNSET)

        _mode = d.pop("mode", UNSET)
        mode: Union[Unset, CreateKafkaTriggerJsonBodyMode]
        if isinstance(_mode, Unset):
            mode = UNSET
        else:
            mode = CreateKafkaTriggerJsonBodyMode(_mode)

        error_handler_path = d.pop("error_handler_path", UNSET)

        _error_handler_args = d.pop("error_handler_args", UNSET)
        error_handler_args: Union[Unset, CreateKafkaTriggerJsonBodyErrorHandlerArgs]
        if isinstance(_error_handler_args, Unset):
            error_handler_args = UNSET
        else:
            error_handler_args = CreateKafkaTriggerJsonBodyErrorHandlerArgs.from_dict(_error_handler_args)

        _retry = d.pop("retry", UNSET)
        retry: Union[Unset, CreateKafkaTriggerJsonBodyRetry]
        if isinstance(_retry, Unset):
            retry = UNSET
        else:
            retry = CreateKafkaTriggerJsonBodyRetry.from_dict(_retry)

        email = d.pop("email", UNSET)

        preserve_email = d.pop("preserve_email", UNSET)

        create_kafka_trigger_json_body = cls(
            path=path,
            script_path=script_path,
            is_flow=is_flow,
            kafka_resource_path=kafka_resource_path,
            group_id=group_id,
            topics=topics,
            filters=filters,
            auto_offset_reset=auto_offset_reset,
            auto_commit=auto_commit,
            mode=mode,
            error_handler_path=error_handler_path,
            error_handler_args=error_handler_args,
            retry=retry,
            email=email,
            preserve_email=preserve_email,
        )

        create_kafka_trigger_json_body.additional_properties = d
        return create_kafka_trigger_json_body

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
