import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.sqs_trigger_aws_auth_resource_type import SqsTriggerAwsAuthResourceType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.sqs_trigger_extra_perms import SqsTriggerExtraPerms


T = TypeVar("T", bound="SqsTrigger")


@_attrs_define
class SqsTrigger:
    """
    Attributes:
        queue_url (str):
        aws_auth_resource_type (SqsTriggerAwsAuthResourceType):
        aws_resource_path (str):
        enabled (bool):
        path (str):
        script_path (str):
        email (str):
        extra_perms (SqsTriggerExtraPerms):
        workspace_id (str):
        edited_by (str):
        edited_at (datetime.datetime):
        is_flow (bool):
        message_attributes (Union[Unset, List[str]]):
        server_id (Union[Unset, str]):
        last_server_ping (Union[Unset, datetime.datetime]):
        error (Union[Unset, str]):
    """

    queue_url: str
    aws_auth_resource_type: SqsTriggerAwsAuthResourceType
    aws_resource_path: str
    enabled: bool
    path: str
    script_path: str
    email: str
    extra_perms: "SqsTriggerExtraPerms"
    workspace_id: str
    edited_by: str
    edited_at: datetime.datetime
    is_flow: bool
    message_attributes: Union[Unset, List[str]] = UNSET
    server_id: Union[Unset, str] = UNSET
    last_server_ping: Union[Unset, datetime.datetime] = UNSET
    error: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        queue_url = self.queue_url
        aws_auth_resource_type = self.aws_auth_resource_type.value

        aws_resource_path = self.aws_resource_path
        enabled = self.enabled
        path = self.path
        script_path = self.script_path
        email = self.email
        extra_perms = self.extra_perms.to_dict()

        workspace_id = self.workspace_id
        edited_by = self.edited_by
        edited_at = self.edited_at.isoformat()

        is_flow = self.is_flow
        message_attributes: Union[Unset, List[str]] = UNSET
        if not isinstance(self.message_attributes, Unset):
            message_attributes = self.message_attributes

        server_id = self.server_id
        last_server_ping: Union[Unset, str] = UNSET
        if not isinstance(self.last_server_ping, Unset):
            last_server_ping = self.last_server_ping.isoformat()

        error = self.error

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "queue_url": queue_url,
                "aws_auth_resource_type": aws_auth_resource_type,
                "aws_resource_path": aws_resource_path,
                "enabled": enabled,
                "path": path,
                "script_path": script_path,
                "email": email,
                "extra_perms": extra_perms,
                "workspace_id": workspace_id,
                "edited_by": edited_by,
                "edited_at": edited_at,
                "is_flow": is_flow,
            }
        )
        if message_attributes is not UNSET:
            field_dict["message_attributes"] = message_attributes
        if server_id is not UNSET:
            field_dict["server_id"] = server_id
        if last_server_ping is not UNSET:
            field_dict["last_server_ping"] = last_server_ping
        if error is not UNSET:
            field_dict["error"] = error

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.sqs_trigger_extra_perms import SqsTriggerExtraPerms

        d = src_dict.copy()
        queue_url = d.pop("queue_url")

        aws_auth_resource_type = SqsTriggerAwsAuthResourceType(d.pop("aws_auth_resource_type"))

        aws_resource_path = d.pop("aws_resource_path")

        enabled = d.pop("enabled")

        path = d.pop("path")

        script_path = d.pop("script_path")

        email = d.pop("email")

        extra_perms = SqsTriggerExtraPerms.from_dict(d.pop("extra_perms"))

        workspace_id = d.pop("workspace_id")

        edited_by = d.pop("edited_by")

        edited_at = isoparse(d.pop("edited_at"))

        is_flow = d.pop("is_flow")

        message_attributes = cast(List[str], d.pop("message_attributes", UNSET))

        server_id = d.pop("server_id", UNSET)

        _last_server_ping = d.pop("last_server_ping", UNSET)
        last_server_ping: Union[Unset, datetime.datetime]
        if isinstance(_last_server_ping, Unset):
            last_server_ping = UNSET
        else:
            last_server_ping = isoparse(_last_server_ping)

        error = d.pop("error", UNSET)

        sqs_trigger = cls(
            queue_url=queue_url,
            aws_auth_resource_type=aws_auth_resource_type,
            aws_resource_path=aws_resource_path,
            enabled=enabled,
            path=path,
            script_path=script_path,
            email=email,
            extra_perms=extra_perms,
            workspace_id=workspace_id,
            edited_by=edited_by,
            edited_at=edited_at,
            is_flow=is_flow,
            message_attributes=message_attributes,
            server_id=server_id,
            last_server_ping=last_server_ping,
            error=error,
        )

        sqs_trigger.additional_properties = d
        return sqs_trigger

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
