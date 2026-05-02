from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.update_kafka_trigger_json_body_auto_offset_reset import UpdateKafkaTriggerJsonBodyAutoOffsetReset
from ..models.update_kafka_trigger_json_body_filter_logic import UpdateKafkaTriggerJsonBodyFilterLogic
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.update_kafka_trigger_json_body_error_handler_args import UpdateKafkaTriggerJsonBodyErrorHandlerArgs
    from ..models.update_kafka_trigger_json_body_filters_item import UpdateKafkaTriggerJsonBodyFiltersItem
    from ..models.update_kafka_trigger_json_body_retry import UpdateKafkaTriggerJsonBodyRetry


T = TypeVar("T", bound="UpdateKafkaTriggerJsonBody")


@_attrs_define
class UpdateKafkaTriggerJsonBody:
    """
    Attributes:
        kafka_resource_path (str): Path to the Kafka resource containing connection configuration
        group_id (str): Kafka consumer group ID for this trigger
        topics (List[str]): Array of Kafka topic names to subscribe to
        filters (List['UpdateKafkaTriggerJsonBodyFiltersItem']):
        path (str): The unique Windmill path for this trigger. Must be of the form `u/<user>/<path>` or
            `f/<folder>/<path>`. This is the trigger object path, not the HTTP route path.
        script_path (str): Path to the script or flow to execute when a message is received
        is_flow (bool): True if script_path points to a flow, false if it points to a script
        filter_logic (Union[Unset, UpdateKafkaTriggerJsonBodyFilterLogic]): Logic to apply when evaluating filters.
            'and' requires all filters to match, 'or' requires any filter to match. Default:
            UpdateKafkaTriggerJsonBodyFilterLogic.AND.
        auto_offset_reset (Union[Unset, UpdateKafkaTriggerJsonBodyAutoOffsetReset]): Initial offset behavior when
            consumer group has no committed offset. Default: UpdateKafkaTriggerJsonBodyAutoOffsetReset.LATEST.
        auto_commit (Union[Unset, bool]): When true (default), offsets are committed automatically after receiving each
            message. When false, you must manually commit offsets using the commit_offsets endpoint. Default: True.
        error_handler_path (Union[Unset, str]): Path to a script or flow to run when the triggered job fails
        error_handler_args (Union[Unset, UpdateKafkaTriggerJsonBodyErrorHandlerArgs]): The arguments to pass to the
            script or flow
        retry (Union[Unset, UpdateKafkaTriggerJsonBodyRetry]): Retry configuration for failed module executions
        permissioned_as (Union[Unset, str]): The user or group this trigger runs as. Used during deployment to preserve
            the original trigger owner.
        preserve_permissioned_as (Union[Unset, bool]): When true and the caller is a member of the 'wm_deployers' group,
            preserves the original permissioned_as value instead of overwriting it.
        labels (Union[Unset, List[str]]):
    """

    kafka_resource_path: str
    group_id: str
    topics: List[str]
    filters: List["UpdateKafkaTriggerJsonBodyFiltersItem"]
    path: str
    script_path: str
    is_flow: bool
    filter_logic: Union[Unset, UpdateKafkaTriggerJsonBodyFilterLogic] = UpdateKafkaTriggerJsonBodyFilterLogic.AND
    auto_offset_reset: Union[
        Unset, UpdateKafkaTriggerJsonBodyAutoOffsetReset
    ] = UpdateKafkaTriggerJsonBodyAutoOffsetReset.LATEST
    auto_commit: Union[Unset, bool] = True
    error_handler_path: Union[Unset, str] = UNSET
    error_handler_args: Union[Unset, "UpdateKafkaTriggerJsonBodyErrorHandlerArgs"] = UNSET
    retry: Union[Unset, "UpdateKafkaTriggerJsonBodyRetry"] = UNSET
    permissioned_as: Union[Unset, str] = UNSET
    preserve_permissioned_as: Union[Unset, bool] = UNSET
    labels: Union[Unset, List[str]] = UNSET
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
        is_flow = self.is_flow
        filter_logic: Union[Unset, str] = UNSET
        if not isinstance(self.filter_logic, Unset):
            filter_logic = self.filter_logic.value

        auto_offset_reset: Union[Unset, str] = UNSET
        if not isinstance(self.auto_offset_reset, Unset):
            auto_offset_reset = self.auto_offset_reset.value

        auto_commit = self.auto_commit
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
                "kafka_resource_path": kafka_resource_path,
                "group_id": group_id,
                "topics": topics,
                "filters": filters,
                "path": path,
                "script_path": script_path,
                "is_flow": is_flow,
            }
        )
        if filter_logic is not UNSET:
            field_dict["filter_logic"] = filter_logic
        if auto_offset_reset is not UNSET:
            field_dict["auto_offset_reset"] = auto_offset_reset
        if auto_commit is not UNSET:
            field_dict["auto_commit"] = auto_commit
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
        from ..models.update_kafka_trigger_json_body_error_handler_args import (
            UpdateKafkaTriggerJsonBodyErrorHandlerArgs,
        )
        from ..models.update_kafka_trigger_json_body_filters_item import UpdateKafkaTriggerJsonBodyFiltersItem
        from ..models.update_kafka_trigger_json_body_retry import UpdateKafkaTriggerJsonBodyRetry

        d = src_dict.copy()
        kafka_resource_path = d.pop("kafka_resource_path")

        group_id = d.pop("group_id")

        topics = cast(List[str], d.pop("topics"))

        filters = []
        _filters = d.pop("filters")
        for filters_item_data in _filters:
            filters_item = UpdateKafkaTriggerJsonBodyFiltersItem.from_dict(filters_item_data)

            filters.append(filters_item)

        path = d.pop("path")

        script_path = d.pop("script_path")

        is_flow = d.pop("is_flow")

        _filter_logic = d.pop("filter_logic", UNSET)
        filter_logic: Union[Unset, UpdateKafkaTriggerJsonBodyFilterLogic]
        if isinstance(_filter_logic, Unset):
            filter_logic = UNSET
        else:
            filter_logic = UpdateKafkaTriggerJsonBodyFilterLogic(_filter_logic)

        _auto_offset_reset = d.pop("auto_offset_reset", UNSET)
        auto_offset_reset: Union[Unset, UpdateKafkaTriggerJsonBodyAutoOffsetReset]
        if isinstance(_auto_offset_reset, Unset):
            auto_offset_reset = UNSET
        else:
            auto_offset_reset = UpdateKafkaTriggerJsonBodyAutoOffsetReset(_auto_offset_reset)

        auto_commit = d.pop("auto_commit", UNSET)

        error_handler_path = d.pop("error_handler_path", UNSET)

        _error_handler_args = d.pop("error_handler_args", UNSET)
        error_handler_args: Union[Unset, UpdateKafkaTriggerJsonBodyErrorHandlerArgs]
        if isinstance(_error_handler_args, Unset):
            error_handler_args = UNSET
        else:
            error_handler_args = UpdateKafkaTriggerJsonBodyErrorHandlerArgs.from_dict(_error_handler_args)

        _retry = d.pop("retry", UNSET)
        retry: Union[Unset, UpdateKafkaTriggerJsonBodyRetry]
        if isinstance(_retry, Unset):
            retry = UNSET
        else:
            retry = UpdateKafkaTriggerJsonBodyRetry.from_dict(_retry)

        permissioned_as = d.pop("permissioned_as", UNSET)

        preserve_permissioned_as = d.pop("preserve_permissioned_as", UNSET)

        labels = cast(List[str], d.pop("labels", UNSET))

        update_kafka_trigger_json_body = cls(
            kafka_resource_path=kafka_resource_path,
            group_id=group_id,
            topics=topics,
            filters=filters,
            path=path,
            script_path=script_path,
            is_flow=is_flow,
            filter_logic=filter_logic,
            auto_offset_reset=auto_offset_reset,
            auto_commit=auto_commit,
            error_handler_path=error_handler_path,
            error_handler_args=error_handler_args,
            retry=retry,
            permissioned_as=permissioned_as,
            preserve_permissioned_as=preserve_permissioned_as,
            labels=labels,
        )

        update_kafka_trigger_json_body.additional_properties = d
        return update_kafka_trigger_json_body

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
