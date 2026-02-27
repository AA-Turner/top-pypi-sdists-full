from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.create_sqs_trigger_json_body_aws_auth_resource_type import CreateSqsTriggerJsonBodyAwsAuthResourceType
from ..models.create_sqs_trigger_json_body_mode import CreateSqsTriggerJsonBodyMode
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.create_sqs_trigger_json_body_error_handler_args import CreateSqsTriggerJsonBodyErrorHandlerArgs
    from ..models.create_sqs_trigger_json_body_retry import CreateSqsTriggerJsonBodyRetry


T = TypeVar("T", bound="CreateSqsTriggerJsonBody")


@_attrs_define
class CreateSqsTriggerJsonBody:
    """
    Attributes:
        queue_url (str): The full URL of the AWS SQS queue to poll for messages
        aws_auth_resource_type (CreateSqsTriggerJsonBodyAwsAuthResourceType): Authentication type - 'credentials' for
            access key/secret, 'oidc' for OpenID Connect
        aws_resource_path (str): Path to the AWS resource containing credentials or OIDC configuration
        path (str): The unique path identifier for this trigger
        script_path (str): Path to the script or flow to execute when a message is received
        is_flow (bool): True if script_path points to a flow, false if it points to a script
        message_attributes (Union[Unset, None, List[str]]): Array of SQS message attribute names to include with each
            message
        mode (Union[Unset, CreateSqsTriggerJsonBodyMode]): job trigger mode
        error_handler_path (Union[Unset, str]): Path to a script or flow to run when the triggered job fails
        error_handler_args (Union[Unset, CreateSqsTriggerJsonBodyErrorHandlerArgs]): The arguments to pass to the script
            or flow
        retry (Union[Unset, CreateSqsTriggerJsonBodyRetry]): Retry configuration for failed module executions
        email (Union[Unset, str]): Email of the user who triggered jobs run as. Used during deployment to preserve the
            original trigger owner.
        preserve_email (Union[Unset, bool]): When true and the caller is a member of the 'wm_deployers' group, preserves
            the original email value instead of overwriting it.
    """

    queue_url: str
    aws_auth_resource_type: CreateSqsTriggerJsonBodyAwsAuthResourceType
    aws_resource_path: str
    path: str
    script_path: str
    is_flow: bool
    message_attributes: Union[Unset, None, List[str]] = UNSET
    mode: Union[Unset, CreateSqsTriggerJsonBodyMode] = UNSET
    error_handler_path: Union[Unset, str] = UNSET
    error_handler_args: Union[Unset, "CreateSqsTriggerJsonBodyErrorHandlerArgs"] = UNSET
    retry: Union[Unset, "CreateSqsTriggerJsonBodyRetry"] = UNSET
    email: Union[Unset, str] = UNSET
    preserve_email: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        queue_url = self.queue_url
        aws_auth_resource_type = self.aws_auth_resource_type.value

        aws_resource_path = self.aws_resource_path
        path = self.path
        script_path = self.script_path
        is_flow = self.is_flow
        message_attributes: Union[Unset, None, List[str]] = UNSET
        if not isinstance(self.message_attributes, Unset):
            if self.message_attributes is None:
                message_attributes = None
            else:
                message_attributes = self.message_attributes

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
                "queue_url": queue_url,
                "aws_auth_resource_type": aws_auth_resource_type,
                "aws_resource_path": aws_resource_path,
                "path": path,
                "script_path": script_path,
                "is_flow": is_flow,
            }
        )
        if message_attributes is not UNSET:
            field_dict["message_attributes"] = message_attributes
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
        from ..models.create_sqs_trigger_json_body_error_handler_args import CreateSqsTriggerJsonBodyErrorHandlerArgs
        from ..models.create_sqs_trigger_json_body_retry import CreateSqsTriggerJsonBodyRetry

        d = src_dict.copy()
        queue_url = d.pop("queue_url")

        aws_auth_resource_type = CreateSqsTriggerJsonBodyAwsAuthResourceType(d.pop("aws_auth_resource_type"))

        aws_resource_path = d.pop("aws_resource_path")

        path = d.pop("path")

        script_path = d.pop("script_path")

        is_flow = d.pop("is_flow")

        message_attributes = cast(List[str], d.pop("message_attributes", UNSET))

        _mode = d.pop("mode", UNSET)
        mode: Union[Unset, CreateSqsTriggerJsonBodyMode]
        if isinstance(_mode, Unset):
            mode = UNSET
        else:
            mode = CreateSqsTriggerJsonBodyMode(_mode)

        error_handler_path = d.pop("error_handler_path", UNSET)

        _error_handler_args = d.pop("error_handler_args", UNSET)
        error_handler_args: Union[Unset, CreateSqsTriggerJsonBodyErrorHandlerArgs]
        if isinstance(_error_handler_args, Unset):
            error_handler_args = UNSET
        else:
            error_handler_args = CreateSqsTriggerJsonBodyErrorHandlerArgs.from_dict(_error_handler_args)

        _retry = d.pop("retry", UNSET)
        retry: Union[Unset, CreateSqsTriggerJsonBodyRetry]
        if isinstance(_retry, Unset):
            retry = UNSET
        else:
            retry = CreateSqsTriggerJsonBodyRetry.from_dict(_retry)

        email = d.pop("email", UNSET)

        preserve_email = d.pop("preserve_email", UNSET)

        create_sqs_trigger_json_body = cls(
            queue_url=queue_url,
            aws_auth_resource_type=aws_auth_resource_type,
            aws_resource_path=aws_resource_path,
            path=path,
            script_path=script_path,
            is_flow=is_flow,
            message_attributes=message_attributes,
            mode=mode,
            error_handler_path=error_handler_path,
            error_handler_args=error_handler_args,
            retry=retry,
            email=email,
            preserve_email=preserve_email,
        )

        create_sqs_trigger_json_body.additional_properties = d
        return create_sqs_trigger_json_body

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
