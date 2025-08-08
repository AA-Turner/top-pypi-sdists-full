from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.create_kafka_trigger_json_body_error_handler_args import CreateKafkaTriggerJsonBodyErrorHandlerArgs
    from ..models.create_kafka_trigger_json_body_retry import CreateKafkaTriggerJsonBodyRetry


T = TypeVar("T", bound="CreateKafkaTriggerJsonBody")


@_attrs_define
class CreateKafkaTriggerJsonBody:
    """
    Attributes:
        path (str):
        script_path (str):
        is_flow (bool):
        kafka_resource_path (str):
        group_id (str):
        topics (List[str]):
        enabled (Union[Unset, bool]):
        error_handler_path (Union[Unset, str]):
        error_handler_args (Union[Unset, CreateKafkaTriggerJsonBodyErrorHandlerArgs]): The arguments to pass to the
            script or flow
        retry (Union[Unset, CreateKafkaTriggerJsonBodyRetry]):
    """

    path: str
    script_path: str
    is_flow: bool
    kafka_resource_path: str
    group_id: str
    topics: List[str]
    enabled: Union[Unset, bool] = UNSET
    error_handler_path: Union[Unset, str] = UNSET
    error_handler_args: Union[Unset, "CreateKafkaTriggerJsonBodyErrorHandlerArgs"] = UNSET
    retry: Union[Unset, "CreateKafkaTriggerJsonBodyRetry"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        path = self.path
        script_path = self.script_path
        is_flow = self.is_flow
        kafka_resource_path = self.kafka_resource_path
        group_id = self.group_id
        topics = self.topics

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
                "path": path,
                "script_path": script_path,
                "is_flow": is_flow,
                "kafka_resource_path": kafka_resource_path,
                "group_id": group_id,
                "topics": topics,
            }
        )
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
        from ..models.create_kafka_trigger_json_body_error_handler_args import (
            CreateKafkaTriggerJsonBodyErrorHandlerArgs,
        )
        from ..models.create_kafka_trigger_json_body_retry import CreateKafkaTriggerJsonBodyRetry

        d = src_dict.copy()
        path = d.pop("path")

        script_path = d.pop("script_path")

        is_flow = d.pop("is_flow")

        kafka_resource_path = d.pop("kafka_resource_path")

        group_id = d.pop("group_id")

        topics = cast(List[str], d.pop("topics"))

        enabled = d.pop("enabled", UNSET)

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

        create_kafka_trigger_json_body = cls(
            path=path,
            script_path=script_path,
            is_flow=is_flow,
            kafka_resource_path=kafka_resource_path,
            group_id=group_id,
            topics=topics,
            enabled=enabled,
            error_handler_path=error_handler_path,
            error_handler_args=error_handler_args,
            retry=retry,
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
