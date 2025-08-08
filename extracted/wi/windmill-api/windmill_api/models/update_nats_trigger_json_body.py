from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.update_nats_trigger_json_body_error_handler_args import UpdateNatsTriggerJsonBodyErrorHandlerArgs
    from ..models.update_nats_trigger_json_body_retry import UpdateNatsTriggerJsonBodyRetry


T = TypeVar("T", bound="UpdateNatsTriggerJsonBody")


@_attrs_define
class UpdateNatsTriggerJsonBody:
    """
    Attributes:
        nats_resource_path (str):
        use_jetstream (bool):
        subjects (List[str]):
        path (str):
        script_path (str):
        is_flow (bool):
        stream_name (Union[Unset, str]):
        consumer_name (Union[Unset, str]):
        error_handler_path (Union[Unset, str]):
        error_handler_args (Union[Unset, UpdateNatsTriggerJsonBodyErrorHandlerArgs]): The arguments to pass to the
            script or flow
        retry (Union[Unset, UpdateNatsTriggerJsonBodyRetry]):
    """

    nats_resource_path: str
    use_jetstream: bool
    subjects: List[str]
    path: str
    script_path: str
    is_flow: bool
    stream_name: Union[Unset, str] = UNSET
    consumer_name: Union[Unset, str] = UNSET
    error_handler_path: Union[Unset, str] = UNSET
    error_handler_args: Union[Unset, "UpdateNatsTriggerJsonBodyErrorHandlerArgs"] = UNSET
    retry: Union[Unset, "UpdateNatsTriggerJsonBodyRetry"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        nats_resource_path = self.nats_resource_path
        use_jetstream = self.use_jetstream
        subjects = self.subjects

        path = self.path
        script_path = self.script_path
        is_flow = self.is_flow
        stream_name = self.stream_name
        consumer_name = self.consumer_name
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
                "nats_resource_path": nats_resource_path,
                "use_jetstream": use_jetstream,
                "subjects": subjects,
                "path": path,
                "script_path": script_path,
                "is_flow": is_flow,
            }
        )
        if stream_name is not UNSET:
            field_dict["stream_name"] = stream_name
        if consumer_name is not UNSET:
            field_dict["consumer_name"] = consumer_name
        if error_handler_path is not UNSET:
            field_dict["error_handler_path"] = error_handler_path
        if error_handler_args is not UNSET:
            field_dict["error_handler_args"] = error_handler_args
        if retry is not UNSET:
            field_dict["retry"] = retry

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.update_nats_trigger_json_body_error_handler_args import UpdateNatsTriggerJsonBodyErrorHandlerArgs
        from ..models.update_nats_trigger_json_body_retry import UpdateNatsTriggerJsonBodyRetry

        d = src_dict.copy()
        nats_resource_path = d.pop("nats_resource_path")

        use_jetstream = d.pop("use_jetstream")

        subjects = cast(List[str], d.pop("subjects"))

        path = d.pop("path")

        script_path = d.pop("script_path")

        is_flow = d.pop("is_flow")

        stream_name = d.pop("stream_name", UNSET)

        consumer_name = d.pop("consumer_name", UNSET)

        error_handler_path = d.pop("error_handler_path", UNSET)

        _error_handler_args = d.pop("error_handler_args", UNSET)
        error_handler_args: Union[Unset, UpdateNatsTriggerJsonBodyErrorHandlerArgs]
        if isinstance(_error_handler_args, Unset):
            error_handler_args = UNSET
        else:
            error_handler_args = UpdateNatsTriggerJsonBodyErrorHandlerArgs.from_dict(_error_handler_args)

        _retry = d.pop("retry", UNSET)
        retry: Union[Unset, UpdateNatsTriggerJsonBodyRetry]
        if isinstance(_retry, Unset):
            retry = UNSET
        else:
            retry = UpdateNatsTriggerJsonBodyRetry.from_dict(_retry)

        update_nats_trigger_json_body = cls(
            nats_resource_path=nats_resource_path,
            use_jetstream=use_jetstream,
            subjects=subjects,
            path=path,
            script_path=script_path,
            is_flow=is_flow,
            stream_name=stream_name,
            consumer_name=consumer_name,
            error_handler_path=error_handler_path,
            error_handler_args=error_handler_args,
            retry=retry,
        )

        update_nats_trigger_json_body.additional_properties = d
        return update_nats_trigger_json_body

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
