import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_nats_trigger_response_200_draft import GetNatsTriggerResponse200Draft
    from ..models.get_nats_trigger_response_200_error_handler_args import GetNatsTriggerResponse200ErrorHandlerArgs
    from ..models.get_nats_trigger_response_200_other_drafts_users_item import (
        GetNatsTriggerResponse200OtherDraftsUsersItem,
    )
    from ..models.get_nats_trigger_response_200_retry import GetNatsTriggerResponse200Retry


T = TypeVar("T", bound="GetNatsTriggerResponse200")


@_attrs_define
class GetNatsTriggerResponse200:
    """
    Attributes:
        nats_resource_path (str): Path to the NATS resource containing connection configuration
        use_jetstream (bool): If true, uses NATS JetStream for durable message delivery
        subjects (List[str]): Array of NATS subjects to subscribe to
        is_draft (bool):
        stream_name (Union[Unset, None, str]): JetStream stream name (required when use_jetstream is true)
        consumer_name (Union[Unset, None, str]): JetStream consumer name (required when use_jetstream is true)
        server_id (Union[Unset, str]): ID of the server currently handling this trigger (internal)
        last_server_ping (Union[Unset, datetime.datetime]): Timestamp of last server heartbeat (internal)
        error (Union[Unset, str]): Last error message if the trigger failed
        error_handler_path (Union[Unset, str]): Path to a script to run when the triggered job fails. A bare path,
            without the script/ or flow/ prefix a schedule error handler takes; it cannot be a flow.
        error_handler_args (Union[Unset, GetNatsTriggerResponse200ErrorHandlerArgs]): The arguments to pass to the
            script or flow
        retry (Union[Unset, GetNatsTriggerResponse200Retry]): Retry configuration for failed module executions
        draft_saved_at (Union[Unset, datetime.datetime]):
        no_deployed (Union[Unset, bool]):
        draft (Union[Unset, GetNatsTriggerResponse200Draft]):
        other_drafts_users (Union[Unset, List['GetNatsTriggerResponse200OtherDraftsUsersItem']]): Other workspace users
            (and the legacy NULL-email row, if any)
            with a saved draft at the same path. Populated only on the
            authed user's "get by path" responses for kinds the editor
            surfaces a fork banner for (script, flow, app, raw_app).
            Empty / omitted for kinds without that UI.
    """

    nats_resource_path: str
    use_jetstream: bool
    subjects: List[str]
    is_draft: bool
    stream_name: Union[Unset, None, str] = UNSET
    consumer_name: Union[Unset, None, str] = UNSET
    server_id: Union[Unset, str] = UNSET
    last_server_ping: Union[Unset, datetime.datetime] = UNSET
    error: Union[Unset, str] = UNSET
    error_handler_path: Union[Unset, str] = UNSET
    error_handler_args: Union[Unset, "GetNatsTriggerResponse200ErrorHandlerArgs"] = UNSET
    retry: Union[Unset, "GetNatsTriggerResponse200Retry"] = UNSET
    draft_saved_at: Union[Unset, datetime.datetime] = UNSET
    no_deployed: Union[Unset, bool] = UNSET
    draft: Union[Unset, "GetNatsTriggerResponse200Draft"] = UNSET
    other_drafts_users: Union[Unset, List["GetNatsTriggerResponse200OtherDraftsUsersItem"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        nats_resource_path = self.nats_resource_path
        use_jetstream = self.use_jetstream
        subjects = self.subjects

        is_draft = self.is_draft
        stream_name = self.stream_name
        consumer_name = self.consumer_name
        server_id = self.server_id
        last_server_ping: Union[Unset, str] = UNSET
        if not isinstance(self.last_server_ping, Unset):
            last_server_ping = self.last_server_ping.isoformat()

        error = self.error
        error_handler_path = self.error_handler_path
        error_handler_args: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.error_handler_args, Unset):
            error_handler_args = self.error_handler_args.to_dict()

        retry: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.retry, Unset):
            retry = self.retry.to_dict()

        draft_saved_at: Union[Unset, str] = UNSET
        if not isinstance(self.draft_saved_at, Unset):
            draft_saved_at = self.draft_saved_at.isoformat()

        no_deployed = self.no_deployed
        draft: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.draft, Unset):
            draft = self.draft.to_dict()

        other_drafts_users: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.other_drafts_users, Unset):
            other_drafts_users = []
            for other_drafts_users_item_data in self.other_drafts_users:
                other_drafts_users_item = other_drafts_users_item_data.to_dict()

                other_drafts_users.append(other_drafts_users_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "nats_resource_path": nats_resource_path,
                "use_jetstream": use_jetstream,
                "subjects": subjects,
                "is_draft": is_draft,
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
        if error_handler_path is not UNSET:
            field_dict["error_handler_path"] = error_handler_path
        if error_handler_args is not UNSET:
            field_dict["error_handler_args"] = error_handler_args
        if retry is not UNSET:
            field_dict["retry"] = retry
        if draft_saved_at is not UNSET:
            field_dict["draft_saved_at"] = draft_saved_at
        if no_deployed is not UNSET:
            field_dict["no_deployed"] = no_deployed
        if draft is not UNSET:
            field_dict["draft"] = draft
        if other_drafts_users is not UNSET:
            field_dict["other_drafts_users"] = other_drafts_users

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.get_nats_trigger_response_200_draft import GetNatsTriggerResponse200Draft
        from ..models.get_nats_trigger_response_200_error_handler_args import GetNatsTriggerResponse200ErrorHandlerArgs
        from ..models.get_nats_trigger_response_200_other_drafts_users_item import (
            GetNatsTriggerResponse200OtherDraftsUsersItem,
        )
        from ..models.get_nats_trigger_response_200_retry import GetNatsTriggerResponse200Retry

        d = src_dict.copy()
        nats_resource_path = d.pop("nats_resource_path")

        use_jetstream = d.pop("use_jetstream")

        subjects = cast(List[str], d.pop("subjects"))

        is_draft = d.pop("is_draft")

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

        error_handler_path = d.pop("error_handler_path", UNSET)

        _error_handler_args = d.pop("error_handler_args", UNSET)
        error_handler_args: Union[Unset, GetNatsTriggerResponse200ErrorHandlerArgs]
        if isinstance(_error_handler_args, Unset):
            error_handler_args = UNSET
        else:
            error_handler_args = GetNatsTriggerResponse200ErrorHandlerArgs.from_dict(_error_handler_args)

        _retry = d.pop("retry", UNSET)
        retry: Union[Unset, GetNatsTriggerResponse200Retry]
        if isinstance(_retry, Unset):
            retry = UNSET
        else:
            retry = GetNatsTriggerResponse200Retry.from_dict(_retry)

        _draft_saved_at = d.pop("draft_saved_at", UNSET)
        draft_saved_at: Union[Unset, datetime.datetime]
        if isinstance(_draft_saved_at, Unset):
            draft_saved_at = UNSET
        else:
            draft_saved_at = isoparse(_draft_saved_at)

        no_deployed = d.pop("no_deployed", UNSET)

        _draft = d.pop("draft", UNSET)
        draft: Union[Unset, GetNatsTriggerResponse200Draft]
        if isinstance(_draft, Unset):
            draft = UNSET
        else:
            draft = GetNatsTriggerResponse200Draft.from_dict(_draft)

        other_drafts_users = []
        _other_drafts_users = d.pop("other_drafts_users", UNSET)
        for other_drafts_users_item_data in _other_drafts_users or []:
            other_drafts_users_item = GetNatsTriggerResponse200OtherDraftsUsersItem.from_dict(
                other_drafts_users_item_data
            )

            other_drafts_users.append(other_drafts_users_item)

        get_nats_trigger_response_200 = cls(
            nats_resource_path=nats_resource_path,
            use_jetstream=use_jetstream,
            subjects=subjects,
            is_draft=is_draft,
            stream_name=stream_name,
            consumer_name=consumer_name,
            server_id=server_id,
            last_server_ping=last_server_ping,
            error=error,
            error_handler_path=error_handler_path,
            error_handler_args=error_handler_args,
            retry=retry,
            draft_saved_at=draft_saved_at,
            no_deployed=no_deployed,
            draft=draft,
            other_drafts_users=other_drafts_users,
        )

        get_nats_trigger_response_200.additional_properties = d
        return get_nats_trigger_response_200

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
