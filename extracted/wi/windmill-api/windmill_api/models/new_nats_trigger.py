from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.new_nats_trigger_error_handler_args import NewNatsTriggerErrorHandlerArgs
    from ..models.new_nats_trigger_retry import NewNatsTriggerRetry


T = TypeVar("T", bound="NewNatsTrigger")


@_attrs_define
class NewNatsTrigger:
    """
    Attributes:
        path (str):
        script_path (str):
        is_flow (bool):
        nats_resource_path (str):
        use_jetstream (bool):
        subjects (List[str]):
        stream_name (Union[Unset, str]):
        consumer_name (Union[Unset, str]):
        enabled (Union[Unset, bool]):
        error_handler_path (Union[Unset, str]):
        error_handler_args (Union[Unset, NewNatsTriggerErrorHandlerArgs]): The arguments to pass to the script or flow
        retry (Union[Unset, NewNatsTriggerRetry]):
    """

    path: str
    script_path: str
    is_flow: bool
    nats_resource_path: str
    use_jetstream: bool
    subjects: List[str]
    stream_name: Union[Unset, str] = UNSET
    consumer_name: Union[Unset, str] = UNSET
    enabled: Union[Unset, bool] = UNSET
    error_handler_path: Union[Unset, str] = UNSET
    error_handler_args: Union[Unset, "NewNatsTriggerErrorHandlerArgs"] = UNSET
    retry: Union[Unset, "NewNatsTriggerRetry"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        path = self.path
        script_path = self.script_path
        is_flow = self.is_flow
        nats_resource_path = self.nats_resource_path
        use_jetstream = self.use_jetstream
        subjects = self.subjects

        stream_name = self.stream_name
        consumer_name = self.consumer_name
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
                "nats_resource_path": nats_resource_path,
                "use_jetstream": use_jetstream,
                "subjects": subjects,
            }
        )
        if stream_name is not UNSET:
            field_dict["stream_name"] = stream_name
        if consumer_name is not UNSET:
            field_dict["consumer_name"] = consumer_name
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
        from ..models.new_nats_trigger_error_handler_args import NewNatsTriggerErrorHandlerArgs
        from ..models.new_nats_trigger_retry import NewNatsTriggerRetry

        d = src_dict.copy()
        path = d.pop("path")

        script_path = d.pop("script_path")

        is_flow = d.pop("is_flow")

        nats_resource_path = d.pop("nats_resource_path")

        use_jetstream = d.pop("use_jetstream")

        subjects = cast(List[str], d.pop("subjects"))

        stream_name = d.pop("stream_name", UNSET)

        consumer_name = d.pop("consumer_name", UNSET)

        enabled = d.pop("enabled", UNSET)

        error_handler_path = d.pop("error_handler_path", UNSET)

        _error_handler_args = d.pop("error_handler_args", UNSET)
        error_handler_args: Union[Unset, NewNatsTriggerErrorHandlerArgs]
        if isinstance(_error_handler_args, Unset):
            error_handler_args = UNSET
        else:
            error_handler_args = NewNatsTriggerErrorHandlerArgs.from_dict(_error_handler_args)

        _retry = d.pop("retry", UNSET)
        retry: Union[Unset, NewNatsTriggerRetry]
        if isinstance(_retry, Unset):
            retry = UNSET
        else:
            retry = NewNatsTriggerRetry.from_dict(_retry)

        new_nats_trigger = cls(
            path=path,
            script_path=script_path,
            is_flow=is_flow,
            nats_resource_path=nats_resource_path,
            use_jetstream=use_jetstream,
            subjects=subjects,
            stream_name=stream_name,
            consumer_name=consumer_name,
            enabled=enabled,
            error_handler_path=error_handler_path,
            error_handler_args=error_handler_args,
            retry=retry,
        )

        new_nats_trigger.additional_properties = d
        return new_nats_trigger

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
