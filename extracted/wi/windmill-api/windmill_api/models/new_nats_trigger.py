from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.new_nats_trigger_mode import NewNatsTriggerMode
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.new_nats_trigger_error_handler_args import NewNatsTriggerErrorHandlerArgs
    from ..models.new_nats_trigger_retry import NewNatsTriggerRetry


T = TypeVar("T", bound="NewNatsTrigger")


@_attrs_define
class NewNatsTrigger:
    """
    Attributes:
        path (str): The unique Windmill path for this trigger. Must be of the form `u/<user>/<path>` or
            `f/<folder>/<path>`. This is the trigger object path, not the HTTP route path.
        script_path (str): Path to the script or flow to execute when a message is received
        is_flow (bool): True if script_path points to a flow, false if it points to a script
        nats_resource_path (str): Path to the NATS resource containing connection configuration
        use_jetstream (bool): If true, uses NATS JetStream for durable message delivery
        subjects (List[str]): Array of NATS subjects to subscribe to
        stream_name (Union[Unset, None, str]): JetStream stream name (required when use_jetstream is true)
        consumer_name (Union[Unset, None, str]): JetStream consumer name (required when use_jetstream is true)
        mode (Union[Unset, NewNatsTriggerMode]): job trigger mode
        error_handler_path (Union[Unset, str]): Path to a script to run when the triggered job fails. A bare path,
            without the script/ or flow/ prefix a schedule error handler takes; it cannot be a flow.
        error_handler_args (Union[Unset, NewNatsTriggerErrorHandlerArgs]): The arguments to pass to the script or flow
        retry (Union[Unset, NewNatsTriggerRetry]): Retry configuration for failed module executions
        permissioned_as (Union[Unset, str]): The user or group this trigger runs as. Used during deployment to preserve
            the original trigger owner.
        preserve_permissioned_as (Union[Unset, bool]): When true and the caller is a member of the 'wm_deployers' group,
            preserves the original permissioned_as value instead of overwriting it.
        labels (Union[Unset, List[str]]):
    """

    path: str
    script_path: str
    is_flow: bool
    nats_resource_path: str
    use_jetstream: bool
    subjects: List[str]
    stream_name: Union[Unset, None, str] = UNSET
    consumer_name: Union[Unset, None, str] = UNSET
    mode: Union[Unset, NewNatsTriggerMode] = UNSET
    error_handler_path: Union[Unset, str] = UNSET
    error_handler_args: Union[Unset, "NewNatsTriggerErrorHandlerArgs"] = UNSET
    retry: Union[Unset, "NewNatsTriggerRetry"] = UNSET
    permissioned_as: Union[Unset, str] = UNSET
    preserve_permissioned_as: Union[Unset, bool] = UNSET
    labels: Union[Unset, List[str]] = UNSET
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

        permissioned_as = self.permissioned_as
        preserve_permissioned_as = self.preserve_permissioned_as
        labels: Union[Unset, List[str]] = UNSET
        if not isinstance(self.labels, Unset):
            labels = self.labels

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
        if mode is not UNSET:
            field_dict["mode"] = mode
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

        _mode = d.pop("mode", UNSET)
        mode: Union[Unset, NewNatsTriggerMode]
        if isinstance(_mode, Unset):
            mode = UNSET
        else:
            mode = NewNatsTriggerMode(_mode)

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

        permissioned_as = d.pop("permissioned_as", UNSET)

        preserve_permissioned_as = d.pop("preserve_permissioned_as", UNSET)

        labels = cast(List[str], d.pop("labels", UNSET))

        new_nats_trigger = cls(
            path=path,
            script_path=script_path,
            is_flow=is_flow,
            nats_resource_path=nats_resource_path,
            use_jetstream=use_jetstream,
            subjects=subjects,
            stream_name=stream_name,
            consumer_name=consumer_name,
            mode=mode,
            error_handler_path=error_handler_path,
            error_handler_args=error_handler_args,
            retry=retry,
            permissioned_as=permissioned_as,
            preserve_permissioned_as=preserve_permissioned_as,
            labels=labels,
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
