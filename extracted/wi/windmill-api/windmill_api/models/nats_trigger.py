import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.nats_trigger_extra_perms import NatsTriggerExtraPerms


T = TypeVar("T", bound="NatsTrigger")


@_attrs_define
class NatsTrigger:
    """
    Attributes:
        nats_resource_path (str):
        use_jetstream (bool):
        subjects (List[str]):
        enabled (bool):
        path (str):
        script_path (str):
        email (str):
        extra_perms (NatsTriggerExtraPerms):
        workspace_id (str):
        edited_by (str):
        edited_at (datetime.datetime):
        is_flow (bool):
        stream_name (Union[Unset, str]):
        consumer_name (Union[Unset, str]):
        server_id (Union[Unset, str]):
        last_server_ping (Union[Unset, datetime.datetime]):
        error (Union[Unset, str]):
    """

    nats_resource_path: str
    use_jetstream: bool
    subjects: List[str]
    enabled: bool
    path: str
    script_path: str
    email: str
    extra_perms: "NatsTriggerExtraPerms"
    workspace_id: str
    edited_by: str
    edited_at: datetime.datetime
    is_flow: bool
    stream_name: Union[Unset, str] = UNSET
    consumer_name: Union[Unset, str] = UNSET
    server_id: Union[Unset, str] = UNSET
    last_server_ping: Union[Unset, datetime.datetime] = UNSET
    error: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        nats_resource_path = self.nats_resource_path
        use_jetstream = self.use_jetstream
        subjects = self.subjects

        enabled = self.enabled
        path = self.path
        script_path = self.script_path
        email = self.email
        extra_perms = self.extra_perms.to_dict()

        workspace_id = self.workspace_id
        edited_by = self.edited_by
        edited_at = self.edited_at.isoformat()

        is_flow = self.is_flow
        stream_name = self.stream_name
        consumer_name = self.consumer_name
        server_id = self.server_id
        last_server_ping: Union[Unset, str] = UNSET
        if not isinstance(self.last_server_ping, Unset):
            last_server_ping = self.last_server_ping.isoformat()

        error = self.error

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "nats_resource_path": nats_resource_path,
                "use_jetstream": use_jetstream,
                "subjects": subjects,
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
        if stream_name is not UNSET:
            field_dict["stream_name"] = stream_name
        if consumer_name is not UNSET:
            field_dict["consumer_name"] = consumer_name
        if server_id is not UNSET:
            field_dict["server_id"] = server_id
        if last_server_ping is not UNSET:
            field_dict["last_server_ping"] = last_server_ping
        if error is not UNSET:
            field_dict["error"] = error

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.nats_trigger_extra_perms import NatsTriggerExtraPerms

        d = src_dict.copy()
        nats_resource_path = d.pop("nats_resource_path")

        use_jetstream = d.pop("use_jetstream")

        subjects = cast(List[str], d.pop("subjects"))

        enabled = d.pop("enabled")

        path = d.pop("path")

        script_path = d.pop("script_path")

        email = d.pop("email")

        extra_perms = NatsTriggerExtraPerms.from_dict(d.pop("extra_perms"))

        workspace_id = d.pop("workspace_id")

        edited_by = d.pop("edited_by")

        edited_at = isoparse(d.pop("edited_at"))

        is_flow = d.pop("is_flow")

        stream_name = d.pop("stream_name", UNSET)

        consumer_name = d.pop("consumer_name", UNSET)

        server_id = d.pop("server_id", UNSET)

        _last_server_ping = d.pop("last_server_ping", UNSET)
        last_server_ping: Union[Unset, datetime.datetime]
        if isinstance(_last_server_ping, Unset):
            last_server_ping = UNSET
        else:
            last_server_ping = isoparse(_last_server_ping)

        error = d.pop("error", UNSET)

        nats_trigger = cls(
            nats_resource_path=nats_resource_path,
            use_jetstream=use_jetstream,
            subjects=subjects,
            enabled=enabled,
            path=path,
            script_path=script_path,
            email=email,
            extra_perms=extra_perms,
            workspace_id=workspace_id,
            edited_by=edited_by,
            edited_at=edited_at,
            is_flow=is_flow,
            stream_name=stream_name,
            consumer_name=consumer_name,
            server_id=server_id,
            last_server_ping=last_server_ping,
            error=error,
        )

        nats_trigger.additional_properties = d
        return nats_trigger

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
