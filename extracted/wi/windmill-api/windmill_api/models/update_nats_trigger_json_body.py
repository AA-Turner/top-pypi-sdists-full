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
        nats_resource_path (str): Path to the NATS resource containing connection configuration
        use_jetstream (bool): If true, uses NATS JetStream for durable message delivery
        subjects (List[str]): Array of NATS subjects to subscribe to
        path (str): The unique path identifier for this trigger
        script_path (str): Path to the script or flow to execute when a message is received
        is_flow (bool): True if script_path points to a flow, false if it points to a script
        stream_name (Union[Unset, None, str]): JetStream stream name (required when use_jetstream is true)
        consumer_name (Union[Unset, None, str]): JetStream consumer name (required when use_jetstream is true)
        error_handler_path (Union[Unset, str]): Path to a script or flow to run when the triggered job fails
        error_handler_args (Union[Unset, UpdateNatsTriggerJsonBodyErrorHandlerArgs]): The arguments to pass to the
            script or flow
        retry (Union[Unset, UpdateNatsTriggerJsonBodyRetry]): Retry configuration for failed module executions
        email (Union[Unset, str]): Email of the user who triggered jobs run as. Used during deployment to preserve the
            original trigger owner.
        preserve_email (Union[Unset, bool]): When true and the caller is a member of the 'wm_deployers' group, preserves
            the original email value instead of overwriting it.
    """

    nats_resource_path: str
    use_jetstream: bool
    subjects: List[str]
    path: str
    script_path: str
    is_flow: bool
    stream_name: Union[Unset, None, str] = UNSET
    consumer_name: Union[Unset, None, str] = UNSET
    error_handler_path: Union[Unset, str] = UNSET
    error_handler_args: Union[Unset, "UpdateNatsTriggerJsonBodyErrorHandlerArgs"] = UNSET
    retry: Union[Unset, "UpdateNatsTriggerJsonBodyRetry"] = UNSET
    email: Union[Unset, str] = UNSET
    preserve_email: Union[Unset, bool] = UNSET
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

        email = self.email
        preserve_email = self.preserve_email

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
        if email is not UNSET:
            field_dict["email"] = email
        if preserve_email is not UNSET:
            field_dict["preserve_email"] = preserve_email

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

        email = d.pop("email", UNSET)

        preserve_email = d.pop("preserve_email", UNSET)

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
            email=email,
            preserve_email=preserve_email,
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
