import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.get_azure_trigger_response_200_azure_mode import GetAzureTriggerResponse200AzureMode
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_azure_trigger_response_200_draft import GetAzureTriggerResponse200Draft
    from ..models.get_azure_trigger_response_200_error_handler_args import GetAzureTriggerResponse200ErrorHandlerArgs
    from ..models.get_azure_trigger_response_200_other_drafts_users_item import (
        GetAzureTriggerResponse200OtherDraftsUsersItem,
    )
    from ..models.get_azure_trigger_response_200_retry import GetAzureTriggerResponse200Retry


T = TypeVar("T", bound="GetAzureTriggerResponse200")


@_attrs_define
class GetAzureTriggerResponse200:
    """
    Attributes:
        azure_resource_path (str):
        azure_mode (GetAzureTriggerResponse200AzureMode): Azure Event Grid trigger mode.
        scope_resource_id (str): ARM resource ID of the topic (basic) or namespace (namespace modes).
        subscription_name (str):
        is_draft (bool):
        topic_name (Union[Unset, None, str]): Topic name within the namespace (namespace modes only).
        event_type_filters (Union[Unset, None, List[str]]):
        server_id (Union[Unset, str]):
        last_server_ping (Union[Unset, datetime.datetime]):
        error (Union[Unset, str]):
        error_handler_path (Union[Unset, str]):
        error_handler_args (Union[Unset, GetAzureTriggerResponse200ErrorHandlerArgs]): The arguments to pass to the
            script or flow
        retry (Union[Unset, GetAzureTriggerResponse200Retry]): Retry configuration for failed module executions
        draft_saved_at (Union[Unset, datetime.datetime]):
        no_deployed (Union[Unset, bool]):
        draft (Union[Unset, GetAzureTriggerResponse200Draft]):
        other_drafts_users (Union[Unset, List['GetAzureTriggerResponse200OtherDraftsUsersItem']]): Other workspace users
            (and the legacy NULL-email row, if any)
            with a saved draft at the same path. Populated only on the
            authed user's "get by path" responses for kinds the editor
            surfaces a fork banner for (script, flow, app, raw_app).
            Empty / omitted for kinds without that UI.
    """

    azure_resource_path: str
    azure_mode: GetAzureTriggerResponse200AzureMode
    scope_resource_id: str
    subscription_name: str
    is_draft: bool
    topic_name: Union[Unset, None, str] = UNSET
    event_type_filters: Union[Unset, None, List[str]] = UNSET
    server_id: Union[Unset, str] = UNSET
    last_server_ping: Union[Unset, datetime.datetime] = UNSET
    error: Union[Unset, str] = UNSET
    error_handler_path: Union[Unset, str] = UNSET
    error_handler_args: Union[Unset, "GetAzureTriggerResponse200ErrorHandlerArgs"] = UNSET
    retry: Union[Unset, "GetAzureTriggerResponse200Retry"] = UNSET
    draft_saved_at: Union[Unset, datetime.datetime] = UNSET
    no_deployed: Union[Unset, bool] = UNSET
    draft: Union[Unset, "GetAzureTriggerResponse200Draft"] = UNSET
    other_drafts_users: Union[Unset, List["GetAzureTriggerResponse200OtherDraftsUsersItem"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        azure_resource_path = self.azure_resource_path
        azure_mode = self.azure_mode.value

        scope_resource_id = self.scope_resource_id
        subscription_name = self.subscription_name
        is_draft = self.is_draft
        topic_name = self.topic_name
        event_type_filters: Union[Unset, None, List[str]] = UNSET
        if not isinstance(self.event_type_filters, Unset):
            if self.event_type_filters is None:
                event_type_filters = None
            else:
                event_type_filters = self.event_type_filters

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
                "azure_resource_path": azure_resource_path,
                "azure_mode": azure_mode,
                "scope_resource_id": scope_resource_id,
                "subscription_name": subscription_name,
                "is_draft": is_draft,
            }
        )
        if topic_name is not UNSET:
            field_dict["topic_name"] = topic_name
        if event_type_filters is not UNSET:
            field_dict["event_type_filters"] = event_type_filters
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
        from ..models.get_azure_trigger_response_200_draft import GetAzureTriggerResponse200Draft
        from ..models.get_azure_trigger_response_200_error_handler_args import (
            GetAzureTriggerResponse200ErrorHandlerArgs,
        )
        from ..models.get_azure_trigger_response_200_other_drafts_users_item import (
            GetAzureTriggerResponse200OtherDraftsUsersItem,
        )
        from ..models.get_azure_trigger_response_200_retry import GetAzureTriggerResponse200Retry

        d = src_dict.copy()
        azure_resource_path = d.pop("azure_resource_path")

        azure_mode = GetAzureTriggerResponse200AzureMode(d.pop("azure_mode"))

        scope_resource_id = d.pop("scope_resource_id")

        subscription_name = d.pop("subscription_name")

        is_draft = d.pop("is_draft")

        topic_name = d.pop("topic_name", UNSET)

        event_type_filters = cast(List[str], d.pop("event_type_filters", UNSET))

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
        error_handler_args: Union[Unset, GetAzureTriggerResponse200ErrorHandlerArgs]
        if isinstance(_error_handler_args, Unset):
            error_handler_args = UNSET
        else:
            error_handler_args = GetAzureTriggerResponse200ErrorHandlerArgs.from_dict(_error_handler_args)

        _retry = d.pop("retry", UNSET)
        retry: Union[Unset, GetAzureTriggerResponse200Retry]
        if isinstance(_retry, Unset):
            retry = UNSET
        else:
            retry = GetAzureTriggerResponse200Retry.from_dict(_retry)

        _draft_saved_at = d.pop("draft_saved_at", UNSET)
        draft_saved_at: Union[Unset, datetime.datetime]
        if isinstance(_draft_saved_at, Unset):
            draft_saved_at = UNSET
        else:
            draft_saved_at = isoparse(_draft_saved_at)

        no_deployed = d.pop("no_deployed", UNSET)

        _draft = d.pop("draft", UNSET)
        draft: Union[Unset, GetAzureTriggerResponse200Draft]
        if isinstance(_draft, Unset):
            draft = UNSET
        else:
            draft = GetAzureTriggerResponse200Draft.from_dict(_draft)

        other_drafts_users = []
        _other_drafts_users = d.pop("other_drafts_users", UNSET)
        for other_drafts_users_item_data in _other_drafts_users or []:
            other_drafts_users_item = GetAzureTriggerResponse200OtherDraftsUsersItem.from_dict(
                other_drafts_users_item_data
            )

            other_drafts_users.append(other_drafts_users_item)

        get_azure_trigger_response_200 = cls(
            azure_resource_path=azure_resource_path,
            azure_mode=azure_mode,
            scope_resource_id=scope_resource_id,
            subscription_name=subscription_name,
            is_draft=is_draft,
            topic_name=topic_name,
            event_type_filters=event_type_filters,
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

        get_azure_trigger_response_200.additional_properties = d
        return get_azure_trigger_response_200

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
